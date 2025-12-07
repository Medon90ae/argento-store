# app_simplified.py - نظام مبسط لإدارة الطلبات وصفحات الهبوط
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# مسارات الملفات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_FILE = os.path.join(BASE_DIR, 'data', 'catalog_cache.json')
ORDERS_FILE = os.path.join(BASE_DIR, 'data', 'orders.json')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# تأكد من وجود مجلد data
os.makedirs(DATA_DIR, exist_ok=True)

# ========== صفحة الهبوط - نسخة مبسطة ==========
@app.route('/product/<product_id>')
def landing_page(product_id):
    """صفحة هبوط للمنتج."""
    return send_from_directory('landing', 'index.html')

@app.route('/landing/<path:filename>')
def landing_files(filename):
    """ملفات صفحة الهبوط (CSS, JS, إلخ)."""
    return send_from_directory('landing', filename)

# ========== جلب بيانات منتج معين ==========
@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    """جلب بيانات منتج معين من الكتالوج."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return jsonify({
                'success': False, 
                'error': 'الكتالوج غير موجود. قم بتحديثه من لوحة التحكم أولاً'
            }), 404
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        products = catalog.get('products', [])
        
        # البحث بالـ ID أو retailer_id
        for product in products:
            if str(product.get('id')) == str(product_id) or \
               str(product.get('retailer_id')) == str(product_id):
                # إضافة رابط صفحة الهبوط
                product['landing_url'] = f"/product/{product.get('id')}"
                return jsonify({
                    'success': True,
                    'product': product
                })
        
        return jsonify({
            'success': False, 
            'error': f'المنتج غير موجود (ID: {product_id})'
        }), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== استقبال طلب جديد ==========
@app.route('/api/order', methods=['POST'])
def create_order():
    """استقبال طلب جديد من صفحة الهبوط."""
    try:
        order_data = request.json
        
        if not order_data:
            return jsonify({'success': False, 'error': 'بيانات الطلب فارغة'}), 400
        
        # إنشاء معرف فريد للطلب
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # إضافة بيانات إضافية
        order_data['order_id'] = order_id
        order_data['created_at'] = datetime.now().isoformat()
        order_data['status'] = 'pending'
        order_data['payment_status'] = 'pending'
        
        # تحديد بيانات الراسل بناءً على التاجر
        merchant_id = order_data.get('merchant_id', '')
        sender_info = get_sender_info(merchant_id)
        order_data.update({
            'sender_name': sender_info['name'],
            'sender_phone': sender_info['phone'],
            'sender_address': sender_info['address'],
            'sender_city': sender_info['city'],
            'sender_area': sender_info['area']
        })
        
        # تحميل الطلبات الحالية
        orders = []
        if os.path.exists(ORDERS_FILE):
            try:
                with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                    orders = json.load(f)
            except:
                orders = []
        
        # إضافة الطلب الجديد
        orders.append(order_data)
        
        # حفظ الطلبات
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'تم استلام طلبك بنجاح'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== لوحة التحكم - النسخة المبسطة ==========
@app.route('/admin')
def admin_dashboard():
    """لوحة تحكم مبسطة."""
    return render_template('admin/dashboard.html')

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """إحصائيات لوحة التحكم."""
    try:
        # عد الطلبات
        total_orders = 0
        pending_orders = 0
        confirmed_orders = 0
        
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                orders = json.load(f)
                total_orders = len(orders)
                pending_orders = len([o for o in orders if o.get('status') == 'pending'])
                confirmed_orders = len([o for o in orders if o.get('status') == 'confirmed'])
        
        # عد المنتجات
        total_products = 0
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
                total_products = len(catalog.get('products', []))
        
        return jsonify({
            'success': True,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'confirmed_orders': confirmed_orders,
            'total_products': total_products
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders')
def get_orders():
    """جلب جميع الطلبات."""
    try:
        orders = []
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        
        # ترتيب من الأحدث للأقدم
        orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== إدارة المنتجات ==========
@app.route('/api/products')
def get_all_products():
    """جلب جميع المنتجات."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return jsonify({
                'success': False,
                'error': 'الكتالوج غير موجود',
                'products': []
            }), 404
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        products = catalog.get('products', [])
        
        # إضافة روابط صفحات الهبوط
        for product in products:
            product_id = product.get('id') or product.get('retailer_id')
            product['landing_url'] = f"/product/{product_id}"
            product['website'] = f"https://speedafargento.com/product/{product_id}"
        
        return jsonify({
            'success': True,
            'products': products,
            'count': len(products),
            'last_updated': catalog.get('metadata', {}).get('last_updated', '')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'products': []
        }), 500

# ========== تحديث روابط المنتجات في الكتالوج ==========
@app.route('/admin/update-product-links', methods=['POST'])
def update_product_links():
    """تحديث روابط صفحات الهبوط في الكتالوج."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return jsonify({
                'success': False,
                'error': 'الكتالوج غير موجود'
            }), 404
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        products = catalog.get('products', [])
        updated_count = 0
        
        # تحديث كل منتج
        for product in products:
            product_id = product.get('id') or product.get('retailer_id')
            if product_id:
                # إضافة رابط صفحة الهبوط
                product['website'] = f"https://speedafargento.com/product/{product_id}"
                product['landing_url'] = f"/product/{product_id}"
                updated_count += 1
        
        # حفظ التعديلات
        catalog['metadata']['links_updated_at'] = datetime.now().isoformat()
        
        with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'تم تحديث روابط {updated_count} منتج',
            'updated_count': updated_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== تحديث الكتالوج ==========
@app.route('/admin/update-catalog', methods=['GET', 'POST'])
def update_catalog():
    """تحديث الكتالوج من فيسبوك."""
    try:
        from utils.facebook_sync import sync_facebook_catalogs
        
        result = sync_facebook_catalogs()
        
        if result.get('success'):
            # تحديث الروابط تلقائياً بعد المزامنة
            update_product_links()
            
            return jsonify({
                'success': True,
                'message': 'تم تحديث الكتالوج وروابط المنتجات بنجاح',
                'products_count': result.get('total_products', 0),
                'updated_at': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'خطأ غير معروف')
            }), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== جلب قوائم المدن والمناطق ==========
@app.route('/api/cities-areas', methods=['GET'])
def get_cities_areas():
    """جلب قوائم المدن والمناطق من ملف Excel."""
    try:
        # سنقرأها من ملف Excel مباشرة في الواجهة
        # هنا نرجع فقط مسار الملف
        return jsonify({
            'success': True,
            'excel_file_url': 'https://raw.githubusercontent.com/Medon90ae/argento-store/main/data/addresses.xlsx'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== تصدير Speedaf ==========
@app.route('/admin/export-speedaf', methods=['GET'])
def export_speedaf():
    """تصدير الطلبات بصيغة Speedaf."""
    try:
        from utils.speedaf_exporter import generate_speedaf_csv
        
        csv_content = generate_speedaf_csv()
        
        return jsonify({
            'success': True,
            'csv_content': csv_content,
            'filename': f'speedaf_export_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== الصفحة الرئيسية ==========
@app.route('/')
def home():
    """الصفحة الرئيسية - توجيه إلى الداشبورد."""
    return jsonify({
        'success': True,
        'app': 'Argento Store - Simplified',
        'version': '2.0',
        'message': 'استخدم /admin للوصول إلى لوحة التحكم',
        'endpoints': {
            'GET /admin': 'لوحة التحكم',
            'GET /product/<id>': 'صفحة هبوط المنتج',
            'GET /api/products': 'جلب جميع المنتجات',
            'GET /api/product/<id>': 'جلب منتج محدد',
            'POST /api/order': 'إنشاء طلب جديد',
            'GET /api/orders': 'جلب جميع الطلبات',
            'GET /api/dashboard-stats': 'إحصائيات اللوحة',
            'POST /admin/update-catalog': 'تحديث الكتالوج',
            'POST /admin/update-product-links': 'تحديث روابط المنتجات',
            'GET /admin/export-speedaf': 'تصدير Speedaf'
        }
    })

# ========== وظائف مساعدة ==========
def get_sender_info(merchant_id):
    """الحصول على بيانات الراسل."""
    senders = {
        'SUDIID': {
            'name': 'Azúcar',
            'phone': '01017549330',
            'city': 'Sharqia',
            'area': 'Zagazig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'CASTELPHARMA': {
            'name': 'كاستيل فارما',
            'phone': '01064147284',
            'city': 'Sharqia',
            'area': 'Zagazig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'FOFO': {
            'name': 'Fofo',
            'phone': '01212137256',
            'city': 'Sharqia',
            'area': 'Zagazig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'UNILEVERID': {
            'name': 'يونيليفر',
            'phone': '01055688136',
            'city': 'Sharqia',
            'area': 'Zagazig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'DEFAULT': {
            'name': 'Argento Store',
            'phone': '01055688136',
            'city': 'Sharqia',
            'area': 'Zagazig',
            'address': 'حي الزهور، الزقازيق'
        }
    }
    
    return senders.get(merchant_id, senders['DEFAULT'])

# ========== تشغيل التطبيق ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
