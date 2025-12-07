# app.py - التطبيق المركزي الكامل
from flask import Flask, jsonify, request, render_template
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

# تأكد من وجود مجلد data
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

# ========== المسار 1: جلب منتج معين ==========
@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    """جلب بيانات منتج معين."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return jsonify({
                'success': False, 
                'error': 'الكتالوج غير موجود',
                'suggestion': 'قم بتحديث الكتالوج أولاً من /admin/update-catalog'
            }), 404
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        # البحث عن المنتج
        products = catalog.get('products', [])
        for product in products:
            if str(product.get('id')) == str(product_id):
                return jsonify({
                    'success': True,
                    'product': product
                })
        
        # إذا لم يوجد، حاول البحث بالـ retailer_id
        for product in products:
            if str(product.get('retailer_id')) == str(product_id):
                return jsonify({
                    'success': True,
                    'product': product
                })
        
        return jsonify({
            'success': False, 
            'error': f'المنتج غير موجود (ID: {product_id})',
            'total_products': len(products),
            'available_ids': [p.get('id') for p in products[:10]]
        }), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
      # ========== المسار 2: استقبال طلب جديد ==========
@app.route('/api/order', methods=['POST'])
def create_order():
    """استقبال طلب جديد من صفحة الهبوط."""
    try:
        # جلب بيانات الطلب
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
        sender_info = get_sender_info(order_data.get('merchant_id', ''))
        order_data['sender_name'] = sender_info['name']
        order_data['sender_phone'] = sender_info['phone']
        order_data['sender_address'] = sender_info['address']
        order_data['sender_city'] = sender_info['city']
        order_data['sender_area'] = sender_info['area']
        
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
        
        # إرجاع الاستجابة
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'تم استلام طلبك بنجاح'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== المسار 3: لوحة التحكم ==========
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    """عرض لوحة التحكم."""
    try:
        # جلب الطلبات
        orders = []
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        
        # جلب آخر تحديث للكتالوج
        catalog_updated = None
        if os.path.exists(CATALOG_FILE):
            catalog_updated = datetime.fromtimestamp(os.path.getmtime(CATALOG_FILE)).strftime('%Y-%m-%d %H:%M')
        
        return render_template('admin.html', 
                             orders=orders, 
                             total_orders=len(orders),
                             catalog_updated=catalog_updated)
        
    except Exception as e:
        return f"خطأ في تحميل اللوحة: {str(e)}", 500
# ========== المسارات الجديدة للوحة التحكم ==========

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """جلب إحصائيات اللوحة."""
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
                total_products = catalog.get('metadata', {}).get('total_products', 0)
        
        return jsonify({
            'success': True,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'confirmed_orders': confirmed_orders,
            'total_products': total_products,
            'exportable_orders': pending_orders + confirmed_orders
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

@app.route('/api/order/<order_id>')
def get_order(order_id):
    """جلب طلب محدد."""
    try:
        if not os.path.exists(ORDERS_FILE):
            return jsonify({'success': False, 'error': 'لا توجد طلبات'}), 404
        
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        for order in orders:
            if order.get('order_id') == order_id:
                return jsonify({'success': True, 'order': order})
        
        return jsonify({'success': False, 'error': 'الطلب غير موجود'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/api/sync-status')
def sync_status():
    """حالة مزامنة الكتالوج."""
    try:
        from utils.facebook_sync import check_sync_status
        status = check_sync_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'synced': False, 'message': str(e)})

@app.route('/api/order/<order_id>/status', methods=['POST'])
def update_order_status(order_id):
    """تحديث حالة الطلب."""
    try:
        if not os.path.exists(ORDERS_FILE):
            return jsonify({'success': False, 'error': 'لا توجد طلبات'}), 404
        
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        updated = False
        for order in orders:
            if order.get('order_id') == order_id:
                order['status'] = request.json.get('status', 'pending')
                order['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(orders, f, ensure_ascii=False, indent=2)
            
            return jsonify({'success': True, 'message': 'تم تحديث الحالة'})
        else:
            return jsonify({'success': False, 'error': 'الطلب غير موجود'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== المسار 4: تصدير Speedaf ==========
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

# ========== المسار 5: جلب قوائم المدن والمناطق ==========
@app.route('/api/cities-areas', methods=['GET'])
def get_cities_areas():
    """جلب قوائم المدن والمناطق."""
    try:
        from config import (
            CITY_TRANSLATIONS_AR_TO_EN,
            OFFICIAL_CITIES_AREAS
        )
        
        return jsonify({
            'success': True,
            'cities': CITY_TRANSLATIONS_AR_TO_EN,
            'city_areas': OFFICIAL_CITIES_AREAS
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== المسار 6: تحديث الكتالوج ==========
@app.route('/admin/update-catalog', methods=['GET', 'POST'])
def update_catalog():
    """تحديث الكتالوج من فيسبوك."""
    try:
        from utils.facebook_sync import sync_facebook_catalogs
        
        result = sync_facebook_catalogs()
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': 'تم تحديث الكتالوج بنجاح',
                'products_count': result.get('total_products', 0),
                'updated_at': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'خطأ غير معروف'),
                'message': result.get('message', 'فشل تحديث الكتالوج')
            }), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
      # ========== المسار 7: إنشاء روابط صفحات الهبوط ==========
@app.route('/admin/generate-landing-links', methods=['GET'])
def generate_landing_links():
    """إنشاء روابط صفحات الهبوط لجميع المنتجات."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return render_template('landing_links.html', 
                                 error='الكتالوج غير موجود',
                                 total_products=0,
                                 products=[])
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        products = catalog.get('products', [])
        
        if not products:
            return render_template('landing_links.html',
                                 error='لا توجد منتجات في الكتالوج',
                                 total_products=0,
                                 products=[])
        
        # حساب عدد التجار
        merchants = set()
        for product in products:
            merchants.add(product.get('merchant_id', ''))
        
        return render_template('landing_links.html',
                             products=products,
                             total_products=len(products),
                             total_merchants=len(merchants),
                             last_updated=catalog.get('metadata', {}).get('last_updated', ''),
                             error=None)
        
    except Exception as e:
        return render_template('landing_links.html',
                             error=f'خطأ: {str(e)}',
                             total_products=0,
                             products=[])

# ========== المسار 8: جلب المنتجات للروابط ==========
@app.route('/api/products-for-links')
def get_products_for_links():
    """جلب المنتجات لعرض الروابط."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return jsonify({
                'success': False, 
                'error': 'الكتالوج غير موجود',
                'products': [],
                'count': 0
            }), 404
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        products = catalog.get('products', [])
        
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
            'products': [],
            'count': 0
        }), 500

# ========== الصفحة الرئيسية ==========
@app.route('/')
def home():
    """الصفحة الرئيسية."""
    return jsonify({
        'success': True,
        'app': 'Argento Store Central API',
        'version': '1.0',
        'endpoints': {
            'GET /': 'الصفحة الرئيسية',
            'GET /api/product/<id>': 'جلب بيانات منتج',
            'POST /api/order': 'إنشاء طلب جديد',
            'GET /admin': 'لوحة التحكم',
            'GET /api/dashboard-stats': 'إحصائيات اللوحة',
            'GET /api/orders': 'جلب جميع الطلبات',
            'GET /api/sync-status': 'حالة المزامنة',
            'POST /api/order/<id>/status': 'تحديث حالة الطلب',
            'GET /api/cities-areas': 'قوائم المدن والمناطق',
            'GET /admin/export-speedaf': 'تصدير Speedaf',
            'GET /admin/update-catalog': 'تحديث الكتالوج',
            'GET /admin/generate-landing-links': 'إنشاء روابط صفحات الهبوط',
            'GET /api/products-for-links': 'جلب المنتجات للروابط'
        }
    })

# ========== وظائف مساعدة ==========
def get_sender_info(merchant_id):
    """الحصول على بيانات الراسل لـ Speedaf."""
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

def get_merchant_name(merchant_id):
    """الحصول على اسم التاجر."""
    merchants = {
        'SUDIID': 'Azúcar',
        'CASTELPHARMA': 'كاستيل فارما',
        'FOFO': 'Fofo',
        'UNILEVERID': 'يونيليفر'
    }
    return merchants.get(merchant_id, merchant_id)

# ========== تشغيل التطبيق ==========
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
  
