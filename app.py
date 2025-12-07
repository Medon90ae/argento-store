# app.py - مُعدّل لدعم صفحات هبوط لكل منتج وتوليد روابطها
# استبدِل هذا الملف في جذر المشروع argento-store-main/app.py

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid
from slugify import slugify  # pip install python-slugify

app = Flask(__name__)
CORS(app)

# -------------------------
# Paths & defaults
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')
# candidate catalog paths (priority order)
CATALOG_PATHS = [
    os.path.join(DATA_DIR, 'catalog_cache.json'),
    os.path.join(BASE_DIR, 'catalog.json'),
    os.path.join(DATA_DIR, 'catalogs', 'latest.json'),
    os.path.join(BASE_DIR, 'catalog.json'),  # redundant but safe
]

# ensure data dir exists
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------
# Optional imports from repo services (non-fatal)
# -------------------------
try:
    # modules may exist; attempt to import to avoid breaking app if they reference things
    import services.order_processor as order_processor  # type: ignore
    import services.speedaf_integration as speedaf_integration  # type: ignore
except Exception:
    order_processor = None
    speedaf_integration = None

# -------------------------
# Catalog loading / saving / helpers
# -------------------------
def load_catalog():
    """
    Return (products_list, source_path) or ([], None).
    Accepts multiple catalog structures:
      - plain list JSON
      - dict with 'products' key
      - dict with first list-valued key
    """
    for p in CATALOG_PATHS:
        try:
            if os.path.exists(p) and os.path.getsize(p) > 0:
                with open(p, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # if dict with 'products'
                if isinstance(data, dict):
                    if isinstance(data.get('products'), list):
                        return data['products'], p
                    # find any list value
                    for v in data.values():
                        if isinstance(v, list):
                            return v, p
                if isinstance(data, list):
                    return data, p
        except Exception as e:
            app.logger.warning(f'Failed to load catalog from {p}: {e}')
    return [], None

def save_catalog_products(products, out_path=None):
    """
    Save the products list to data/catalog_cache.json by default.
    Returns written path or None.
    """
    out = out_path or os.path.join(DATA_DIR, 'catalog_cache.json')
    try:
        # write products as a JSON array (simple cache)
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        return out
    except Exception as e:
        app.logger.error(f'Failed to write catalog cache to {out}: {e}')
        return None

def generate_landing_links(write_back=True):
    """
    Ensure each product has product['website'] = "/landing/<slug_or_id>"
    Returns (changed_count, out_path)
    """
    products, src = load_catalog()
    if not products:
        return 0, None
    changed = 0
    for p in products:
        name = p.get('name') or p.get('title') or p.get('product_name') or ''
        pid = str(p.get('id') or p.get('sku') or '').strip()
        slug = pid if pid else slugify(name)
        link = f"/landing/{slug}"
        if p.get('website') != link:
            p['website'] = link
            changed += 1
    out = save_catalog_products(products) if write_back else None
    return changed, out

def find_product_by_slug(slug):
    """
    Try to locate product by:
      - website field ending with slug
      - id or sku equals slug
      - slugified name equals slug
    """
    products, _ = load_catalog()
    if not products:
        return None
    s = slug.lower()
    for p in products:
        # website match
        w = (p.get('website') or '').strip().lower()
        if w.endswith('/' + s) or (w and w.strip('/').split('/')[-1] == s):
            return p
        # id/sku match
        pid = str(p.get('id') or p.get('sku') or '').lower()
        if pid == s:
            return p
        # name slug match
        name = p.get('name') or p.get('title') or ''
        if slugify(name).lower() == s:
            return p
    return None

# -------------------------
# Routes: index / api / landing
# -------------------------
@app.route('/')
def index():
    # Attempt to display an index that uses the existing templates/index.html
    # Templates expect 'products' variable in many stores; provide that.
    products, _ = load_catalog()
    # If template expects dict structure, adapt as needed
    return render_template('index.html', products=products)

@app.route('/api/products', methods=['GET'])
def api_products():
    products, src = load_catalog()
    return jsonify({"ok": True, "count": len(products), "products": products})

@app.route('/landing/<slug>', methods=['GET'])
def product_landing(slug):
    product = find_product_by_slug(slug)
    if not product:
        return render_template('404.html'), 404
    # Render product landing template - the repo may not have this file.
    # If missing, try to render templates/index.html with a single product context.
    tpl = 'product_landing.html'
    if os.path.exists(os.path.join(BASE_DIR, 'templates', tpl)):
        return render_template(tpl, product=product)
    # fallback: render a minimal inline page using index.html layout if available
    return render_template('index.html', products=[product])

@app.route('/api/landing_order', methods=['POST'])
def landing_order():
    # Accept form-encoded or JSON
    data = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})
    # expected keys: product_id or product_slug or product, name, phone, city, area, address
    ref = data.get('product_id') or data.get('product_slug') or data.get('product')
    product = None
    if ref:
        product = find_product_by_slug(str(ref))
    order = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "product": product or {"id": ref, "name": data.get('product_name') or data.get('name')},
        "customer": {
            "name": data.get('name'),
            "phone": data.get('phone'),
            "city": data.get('city'),
            "area": data.get('area'),
            "address": data.get('address'),
        },
        "status": "new",
        "raw": data
    }
    # persist order
    try:
        if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
            with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        with open(ORDERS_FILE, 'r+', encoding='utf-8') as f:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = []
            existing.insert(0, order)
            f.seek(0)
            json.dump(existing, f, ensure_ascii=False, indent=2)
            f.truncate()
    except Exception as e:
        app.logger.error(f'Failed to write order: {e}')
        return jsonify({"ok": False, "error": str(e)}), 500

    # optional: call order processor hook if available
    try:
        if order_processor and hasattr(order_processor, 'on_new_order'):
            try:
                order_processor.on_new_order(order)
            except Exception as e:
                app.logger.warning(f'order_processor.on_new_order failed: {e}')
    except Exception:
        pass

    return jsonify({"ok": True, "order_id": order['id']})

# Admin utility route (unsafe if public) - disabled by default.
# If you want a quick trigger from browser, uncomment and protect it.
# @app.route('/admin/generate_links', methods=['POST'])
# def admin_generate_links():
#     # protect this route in production
#     changed, out = generate_landing_links(write_back=True)
#     return jsonify({"ok": True, "updated": changed, "wrote": out})

# -------------------------
# CLI helpers so you can call from python -c "from app import generate_landing_links; print(generate_landing_links())"
# -------------------------
if __name__ == '__main__':
    # If run directly, ensure landing links exist
    try:
        changed, out = generate_landing_links(write_back=True)
        if changed:
            app.logger.info(f'generate_landing_links: updated {changed} products -> {out}')
    except Exception as e:
        app.logger.warning(f'generate_landing_links on startup failed: {e}')

    port = int(os.environ.get('PORT', 10000))
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
