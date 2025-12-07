# نقطة دخول التطبيق
# app.py - التطبيق المركزي المبسط
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # للسماح لصفحات الهبوط بالاتصال

# مسارات الملفات
CATALOG_FILE = 'data/catalog_cache.json'
ORDERS_FILE = 'data/orders.json'

# تأكد من وجود مجلد data
os.makedirs('data', exist_ok=True)

# ========== المسار 1: جلب منتج معين ==========
@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    """جلب بيانات منتج معين."""
    try:
        # تحميل الكتالوج المخبأ
        if os.path.exists(CATALOG_FILE):
            with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
        else:
            return jsonify({'error': 'الكتالوج غير متوفر'}), 404
        
        # البحث عن المنتج
        for product in catalog:
            if str(product.get('id')) == product_id or str(product.get('retailer_id')) == product_id:
                # تحديد التاجر بناءً على معرف الكتالوج
                merchant_info = get_merchant_info(product.get('catalog_id', ''))
                
                # إضافة معلومات التاجر
                product['merchant_name'] = merchant_info['name']
                product['merchant_id'] = merchant_info['id']
                product['merchant_phone'] = merchant_info['phone']
                
                return jsonify({'product': product})
        
        return jsonify({'error': 'المنتج غير موجود'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== المسار 2: استقبال طلب جديد ==========
@app.route('/api/order', methods=['POST'])
def create_order():
    """استقبال طلب جديد من صفحة الهبوط."""
    try:
        # جلب بيانات الطلب
        order_data = request.json
        
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
        
        # تحميل الطلبات الحالية
        orders = []
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        
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
            AREA_TRANSLATIONS_AR_TO_EN,
            OFFICIAL_CITIES_AREAS
        )
        
        return jsonify({
            'cities': CITY_TRANSLATIONS_AR_TO_EN,
            'areas': AREA_TRANSLATIONS_AR_TO_EN,
            'city_areas': OFFICIAL_CITIES_AREAS
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== المسار 6: تحديث الكتالوج ==========
@app.route('/admin/update-catalog', methods=['POST'])
def update_catalog():
    """تحديث الكتالوج من فيسبوك."""
    try:
        from utils.facebook_sync import sync_facebook_catalogs
        
        result = sync_facebook_catalogs()
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث الكتالوج بنجاح',
            'products_count': result.get('total_products', 0),
            'updated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========== وظائف مساعدة ==========
def get_merchant_info(catalog_id):
    """الحصول على معلومات التاجر بناءً على معرف الكتالوج."""
    merchants = {
        'SUDIID': {
            'id': 'SUDIID',
            'name': 'Azúcar',
            'phone': '01017549330',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'CASTELPHARMA': {
            'id': 'CASTELPHARMA',
            'name': 'كاستيل فارما',
            'phone': '01064147284',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'FOFO': {
            'id': 'FOFO',
            'name': 'Fofo',
            'phone': '01212137256',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'UNILEVERID': {
            'id': 'UNILEVERID',
            'name': 'يونيليفر',
            'phone': '01055688136',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        }
    }
    
    # البحث عن التاجر المناسب
    for merchant_id, info in merchants.items():
        if merchant_id in catalog_id:
            return info
    
    # افتراضي
    return {
        'id': 'DEFAULT',
        'name': 'Argento Store',
        'phone': '01055688136',
        'city':'sharqia',
        'area':'zagszig',
        'address': 'الزقازيق الشرقية، حي الزهور'
    }

def get_sender_info(merchant_id):
    """الحصول على بيانات الراسل لـ Speedaf."""
    senders = {
        'SUDIID': {
            'name': 'Azúcar',
            'phone': '01017549330',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'CASTELPHARMA': {
            'name': 'كاستيل فارما',
            'phone': '01064147284',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'FOFO': {
            'name': 'Fofo',
            'phone': '01212137256',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'UNILEVERID': {
            'name': 'يونيليفر',
            'phone': '01055688136',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'الزقازيق الشرقية، حي الزهور'
        },
        'DEFAULT': {
            'name': 'Argento Store',
            'phone': '01055688136',
            'city':'sharqia',
            'area':'zagszig',
            'address': 'حي الزهور، الزقازيق'
        }
    }
    
    return senders.get(merchant_id, senders['DEFAULT'])

# ========== نقطة الدخول ==========
@app.route('/')
def home():
    """الصفحة الرئيسية."""
    return jsonify({
        'app': 'Argento Store Central API',
        'version': '1.0',
        'endpoints': {
            'GET /api/product/<id>': 'جلب بيانات منتج',
            'POST /api/order': 'إنشاء طلب جديد',
            'GET /admin': 'لوحة التحكم',
            'GET /api/cities-areas': 'قوائم المدن والمناطق'
        }
    })

@app.route('/admin/update-catalog', methods=['POST'])
def update_catalog():
    from utils.facebook_sync import sync_facebook_catalogs
    result = sync_facebook_catalogs()
    return jsonify(result)

# ========== تشغيل التطبيق ==========
if __name__ == '__main__':
    # في Railway، استمع على المنفذ المحدد في متغير البيئة
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
