import os
import json
import datetime
import uuid
from collections import defaultdict
import requests
from slugify import slugify

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
import tempfile

app = Flask(__name__)

# Load env vars
FB_ACCESS_TOKEN = os.getenv('FBACCSESSTOKEN', 'your_access_token_here')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'admin123')

BUSINESS_CATALOGS = {
    'CASTELPHARMA': 'CASTELPHARMA',  # replace with actual IDs
    'FOFO': 'FOFO',
    'SUDIID': 'SUDIID',
    'UNILEVERID': 'UNILEVERID',
}

# Global city_area dict
CITY_AREA_DICT = {}

def load_city_area_dict():
    """Load city to areas mapping from addresses.xlsx"""
    global CITY_AREA_DICT
    if os.path.exists('addresses.xlsx'):
        wb = load_workbook('addresses.xlsx')
        if 'Speedaf standard address data' in wb.sheetnames:
            sheet = wb['Speedaf standard address data']
            CITY_AREA_DICT = defaultdict(list)
            header = [cell.value for cell in sheet[1] if cell.value]
            if 'City' in header and 'Area' in header:
                city_idx = header.index('City')
                area_idx = header.index('Area')
                for row in sheet.iter_rows(min_row=2):
                    city = row[city_idx].value
                    area = row[area_idx].value
                    if city and area:
                        CITY_AREA_DICT[city.strip()].append(area.strip())
    print(f"Loaded {len(CITY_AREA_DICT)} cities with areas")

def load_catalog():
    """Load products from first valid catalog file"""
    paths = ['data/catalog_cache.json', 'catalog.json', 'data/catalogs/latest.json']
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data, path
                    elif isinstance(data, dict) and 'products' in data:
                        return data['products'], path
            except Exception as e:
                print(f"Error loading {path}: {e}")
    return [], None

def save_catalog_products(products, out_path=None):
    """Save products to JSON safely"""
    if out_path is None:
        out_path = 'data/catalog_cache.json'
    dir_path = os.path.dirname(out_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    temp_path = out_path + '.tmp'
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        os.replace(temp_path, out_path)
        print(f"Saved {len(products)} products to {out_path}")
    except Exception as e:
        print(f"Error saving {out_path}: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def fetch_facebook_products(catalog_id, access_token):
    """Fetch products from Facebook catalog"""
    url = f"https://graph.facebook.com/v18.0/{catalog_id}/products"
    params = {
        'fields': 'id,name,description,price,currency,availability,brand,image_url',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return [p for p in data.get('data', []) if p.get('availability') in ['available', None]]
    else:
        print(f"Failed to fetch {catalog_id}: {response.status_code}")
        return []

def update_catalogs():
    """Fetch and merge products without duplicates"""
    all_products = []
    seen_ids = set()
    for name, cid in BUSINESS_CATALOGS.items():
        prods = fetch_facebook_products(cid, FB_ACCESS_TOKEN)
        print(f"Fetched {len(prods)} from {name}")
        for p in prods:
            pid = p.get('id')
            if pid not in seen_ids:
                seen_ids.add(pid)
                all_products.append({
                    'id': pid,
                    'sku': f"{name}-{pid}",
                    'title': p.get('name', ''),
                    'description': p.get('description', ''),
                    'price': float(p.get('price', {}).get('amount', '0')),
                    'currency': p.get('price', {}).get('currency', 'EGP'),
                    'brand': p.get('brand', ''),
                    'image_url': p.get('image_url', ''),
                    'shipping_price': 50.0,  # default
                    'free_shipping': False,
                    'offers': []
                })
    return all_products

def generate_landing_links(products, write_back=True):
    """Add website slug to products if missing"""
    changed = 0
    for p in products:
        if 'website' not in p or not p['website']:
            slug = p.get('id') or p.get('sku') or slugify(p.get('title', ''))
            p['website'] = f"/landing/{slug}"
            changed += 1
    if write_back and changed > 0:
        save_catalog_products(products)
    return changed, 'data/catalog_cache.json'

def find_product_by_slug(slug):
    """Find product by slug in website, id, sku, or title"""
    products, _ = load_catalog()
    for p in products:
        if p.get('website', '').endswith(f"/{slug}"):
            return p
        if str(p.get('id', '')) == slug or str(p.get('sku', '')) == slug:
            return p
        if slugify(p.get('title', '')) == slug:
            return p
    return None

def calculate_order(product, quantity, offer=None):
    """Calculate prices with offers and shipping"""
    price_per = product['price']
    subtotal = price_per * quantity
    shipping_applied = 0 if product.get('free_shipping') else product['shipping_price']
    discount = 0
    offer = product.get('offers', [])[-1] if not offer else offer  # latest if none specified
    if offer:
        if offer['type'] == 'percentage':
            discount = subtotal * (offer['value'] / 100)
        elif offer['type'] == 'fixed':
            discount = min(offer['value'], subtotal)
    total = subtotal - discount + shipping_applied
    return subtotal, discount, shipping_applied, total

def add_order_to_excel(order):
    """Append order to addresses.xlsx sheet '0'"""
    if not os.path.exists('addresses.xlsx'):
        wb = Workbook()
        wb['Sheet'].title = '0'
        wb.save('addresses.xlsx')

    def atomic_write(data):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        try:
            orig_wb = load_workbook('addresses.xlsx')
            if '0' not in orig_wb.sheetnames:
                orig_wb.create_sheet('0')
            sheet = orig_wb['0']
            row = len(sheet['A']) + 1
            for i, val in enumerate(data, 1):
                sheet.cell(row=row, column=i, value=val)
            orig_wb.save(temp_path)
            os.replace(temp_path, 'addresses.xlsx')
        except Exception as e:
            print(f"Error adding to Excel: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Map order to Excel columns
    # Assuming columns as in read_file: S.O., Goods type, ..., Receiver Email, Delivery Type
    goods = {'name': order['product']['title'], 'quantity': order['quantity'], 'price': order['price']}
    sender = order.get('customer', {}).get('sender', {})
    receiver = order['customer']
    data = [
        '',  # S.O.
        'product',  # Goods type
        order['product']['title'],  # Goods name
        order['quantity'],  # Quantity
        0.5,  # Weight
        order['total'],  # COD
        0,  # Insure price
        'No',  # Whether to allow the package to be opened
        order.get('notes', ''),  # Remark
        sender.get('name', ''), sender.get('phone', ''), sender.get('city', ''), sender.get('area', ''), sender.get('address', ''), sender.get('email', ''),
        receiver.get('name', ''), receiver.get('phone', ''), receiver.get('city', ''), receiver.get('area', ''), receiver.get('address', ''), receiver.get('email', ''),
        'standard'  # Delivery Type
    ]
    atomic_write(data)

def archive_and_reset_orders(archive_dir='data/archives'):
    """Archive current addresses.xlsx to data/archives with timestamp and reset sheet '0'"""
    if not os.path.exists('addresses.xlsx'):
        return False
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(archive_dir, exist_ok=True)
    archive_path = os.path.join(archive_dir, f'orders_{timestamp}.xlsx')
    try:
        import shutil
        shutil.copy('addresses.xlsx', archive_path)
        # Reset sheet '0'
        wb = load_workbook('addresses.xlsx')
        if '0' in wb.sheetnames:
            wb['0'].delete_rows(2, wb['0'].max_row)  # keeps header
            wb.save('addresses.xlsx')
        return True, archive_path
    except Exception as e:
        print(f"Archive error: {e}")
        return False, None

# Routes
@app.route('/')
def index():
    products, _ = load_catalog()
    if not products:
        # Fallback to first product if list
        return render_template('index.html', products=[])
    return render_template('index.html', products=products)

@app.route('/api/products')
def api_products():
    products, _ = load_catalog()
    return jsonify({'ok': True, 'count': len(products), 'products': products})

@app.route('/landing/<slug>')
def product_landing(slug):
    product = find_product_by_slug(slug)
    if product:
        return render_template('product_landing.html', product=product, city_areas=CITY_AREA_DICT)
    # Fallback
    products, _ = load_catalog()
    if products:
        return render_template('product_landing.html', product=products[0], city_areas=CITY_AREA_DICT)
    return render_template('index.html', products=[])

@app.route('/api/landing_order', methods=['POST'])
def landing_order():
    data = request.get_json() or request.form.to_dict()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    customer = data.get('customer', {})

    products, _ = load_catalog()
    product = next((p for p in products if str(p.get('id', '')) == str(product_id)), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 400

    subtotal, discount, shipping_applied, total = calculate_order(product, quantity)

    order = {
        'id': str(uuid.uuid4()),
        'created_at': datetime.datetime.utcnow().isoformat(),
        'product': {k: v for k, v in product.items() if k in ['id', 'title', 'price']},
        'quantity': quantity,
        'subtotal': subtotal,
        'discount': discount,
        'shipping': shipping_applied,
        'total': total,
        'status': 'new',
        'customer': customer,
        'raw': data
    }

    # Load existing orders
    if os.path.exists('data/orders.json'):
        try:
            with open('data/orders.json', 'r', encoding='utf-8') as f:
                orders = json.load(f)
            if not isinstance(orders, list):
                orders = []
        except:
            orders = []
    else:
        orders = []

    # Insert at top
    orders.insert(0, order)

    # Save orders
    try:
        with open('data/orders.json', 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving orders: {e}")

    # Add to Excel
    add_order_to_excel(order)

    return jsonify({'ok': True, 'order_id': order['id']})

@app.route('/admin')
def admin():
    token = request.args.get('token') or request.cookies.get('admin_token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'Admin access denied'}), 403

    products, _ = load_catalog()
    if os.path.exists('data/orders.json'):
        try:
            with open('data/orders.json', 'r', encoding='utf-8') as f:
                orders = json.load(f)
        except:
            orders = []
    else:
        orders = []

    today = datetime.datetime.utcnow().date().isoformat()
    today_orders = [o for o in orders if o.get('created_at', '').startswith(today)]
    today_sales = sum(float(o.get('total', 0)) for o in today_orders)

    stats = {
        'total_orders': len(orders),
        'today_orders': len(today_orders),
        'today_sales': today_sales,
        'total_products': len(products),
        'free_shipping_products': len([p for p in products if p.get('free_shipping')])
    }

    return render_template('admin.html', stats=stats, products=products, orders=orders[:50])  # last 50

@app.route('/api/update_catalog', methods=['POST'])
def api_update_catalog():
    if request.headers.get('Authorization') != f"Bearer {ADMIN_TOKEN}":
        return jsonify({'error': 'Unauthorized'}), 401

    new_products = update_catalogs()
    if new_products:
        # Merge with existing without duplicates based on id
        old_products, _ = load_catalog()
        seen_ids = {p.get('id'): i for i, p in enumerate(old_products)}
        for np in new_products:
            pid = np['id']
            if pid in seen_ids:
                # Update existing
                old_products[seen_ids[pid]] = np
            else:
                old_products.append(np)
        generate_landing_links(old_products, write_back=True)
        return jsonify({'ok': True, 'total': len(old_products)})
    return jsonify({'ok': False, 'message': 'No new products'})

@app.route('/api/update_product', methods=['POST'])
def api_update_product():
    if request.headers.get('Authorization') != f"Bearer {ADMIN_TOKEN}":
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    pid = data.get('id')
    if not pid:
        return jsonify({'error': 'Product ID required'}), 400

    products, path = load_catalog()
    for p in products:
        if str(p.get('id')) == str(pid):
            for k in ['title', 'price', 'shipping_price', 'free_shipping']:
                if k in data:
                    p[k] = data[k]
            save_catalog_products(products)
            return jsonify({'ok': True})
    return jsonify({'error': 'Product not found'})

@app.route('/api/archive_orders', methods=['POST'])
def api_archive_orders():
    if request.headers.get('Authorization') != f"Bearer {ADMIN_TOKEN}":
        return jsonify({'error': 'Unauthorized'}), 401

    success, archive_path = archive_and_reset_orders()
    if success:
        # Reset orders.json too? or just Excel sheet
        with open('data/orders.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        return jsonify({'ok': True, 'archive_path': archive_path})
    return jsonify({'error': 'Archive failed'})

if __name__ == '__main__':
    load_city_area_dict()
    products, _ = load_catalog()
    if not products:
        print("No products found, you may need to update catalog via /api/update_catalog")
    app.run(host='0.0.0.0', port=5000, debug=True)
