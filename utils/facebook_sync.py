# utils/facebook_sync.py
# مزامنة المنتجات من كتالوجات فيسبوك والتجار المختلفة

import os
import json
import requests
from datetime import datetime
import time

def sync_facebook_catalogs():
    """
    المزامنة الرئيسية: جلب جميع الكتالوجات من فيسبوك.
    
    Returns:
        dict: نتائج المزامنة
    """
    print("🔍 بدء مزامنة كتالوجات فيسبوك...")
    
    try:
        # الحصول على مفاتيح API من متغيرات البيئة
        access_token = os.environ.get('FBACCSESSTOKEN')
        
        if not access_token:
            return {
                'success': False,
                'error': 'مفتاح فيسبوك غير موجود في متغيرات البيئة'
            }
        
        # قائمة معرفات الكتالوجات من متغيرات البيئة
        catalog_ids = get_catalog_ids_from_env()
        
        if not catalog_ids:
            return {
                'success': False,
                'error': 'لا توجد معرفات كتالوجات في متغيرات البيئة'
            }
        
        # جلب المنتجات من كل كتالوج
        all_products = []
        catalog_stats = {}
        
        for catalog_name, catalog_id in catalog_ids.items():
            print(f"📦 جلب كتالوج: {catalog_name} ({catalog_id})")
            
            products = fetch_catalog_products(catalog_id, access_token, catalog_name)
            
            if products:
                all_products.extend(products)
                catalog_stats[catalog_name] = {
                    
def get_catalog_ids_from_env():
    """
    الحصول على معرفات الكتالوجات من متغيرات البيئة.
    
    Returns:
        dict: {catalog_name: catalog_id}
    """
    catalog_mapping = {
        'SUDIID': os.environ.get('SUDIID'),
        'UNILEVERID': os.environ.get('UNILEVERID'),
        'BUSSNISID': os.environ.get('BUSSNISID'),
        'FOFO': os.environ.get('FOFO'),
        'CASTELPHARMA': os.environ.get('CASTELPHARMA')
    }
    
    # تصفية القيم الفارغة
    return {k: v for k, v in catalog_mapping.items() if v}

def fetch_catalog_products(catalog_id, access_token, catalog_name):
    """
    جلب المنتجات من كتالوج فيسبوك معين.
    
    Args:
        catalog_id (str): معرف الكتالوج
        access_token (str): توكن فيسبوك
        catalog_name (str): اسم الكتالوج (لتحديد التاجر)
        
    Returns:
        list: قائمة المنتجات
    """
    try:
        # أولاً: جلب معلومات الكتالوج
        catalog_info = get_catalog_info(catalog_id, access_token)
        
        if not catalog_info:
            print(f"⚠️  تعذر جلب معلومات الكتالوج {catalog_id}")
            return []
        
        # تحديد edge المناسب للمنتجات
        product_edge = determine_product_edge(catalog_info)
        
        if not product_edge:
            print(f"⚠️  لا يوجد edge للمنتجات في الكتالوج {catalog_id}")
            return []
        
        # جلب المنتجات
        products = []
        api_version = 'v18.0'  # أو 'v19.0' حسب الصلاحية
        
        url = f"https://graph.facebook.com/{api_version}/{catalog_id}/{product_edge}"
        params = {
            'access_token': access_token,
            'fields': 'id,name,description,price,currency,image_url,availability,retailer_id,condition',
            'limit': 100  # الحد الأقصى المسموح به
        }
        
        print(f"🌐 جلب المنتجات من: {catalog_name}")
        
        while url:
            try:
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code != 200:
                    print(f"⚠️  خطأ API: {response.status_code}")
                    break
                
                data = response.json()
                
                if 'data' in data:
                    for product in data['data']:
                        # إضافة معلومات التاجر
                        product['catalog_id'] = catalog_id
                        product['catalog_name'] = catalog_name
                        product['merchant_id'] = catalog_name
                        product['merchant_name'] = get_merchant_name(catalog_name)
                        product['merchant_phone'] = get_merchant_phone(catalog_name)
                        
                        # تنظيف البيانات
                        cleaned_product = clean_product_data(product)
                        products.append(cleaned_product)
                
                # التالي للصفحة التالية
                if 'paging' in data and 'next' in data['paging']:
                    url = data['paging']['next']
                    params = {}  # إعادة تعيين الـ params لأن الرابط التالي يحتوي كل شيء
                else:
                    url = None
                
                # انتظر قليلاً لتجنب Rate Limit
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"⚠️  خطأ في الاتصال: {e}")
                break
        
        print(f"✅ تم جلب {len(products)} منتج من {catalog_name}")
        return products
        
    except Exception as e:
        print(f"❌ خطأ في جلب منتجات {catalog_name}: {e}")
        return []

def get_catalog_info(catalog_id, access_token):
    """
    جلب معلومات أساسية عن الكتالوج.
    
    Args:
        catalog_id (str): معرف الكتالوج
        access_token (str): توكن فيسبوك
        
    Returns:
        dict: معلومات الكتالوج
    """
    try:
        url = f"https://graph.facebook.com/v18.0/{catalog_id}"
        params = {
            'access_token': access_token,
            'fields': 'id,name,product_count,vertical'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        
        return None
        
    except Exception:
        return None

def determine_product_edge(catalog_info):
    """
    تحديد edge المناسب لجلب المنتجات.
    
    Args:
        catalog_info (dict): معلومات الكتالوج
        
    Returns:
        str: اسم الـ edge ('products' أو 'items' أو 'product_items')
    """
    # محاولة جلب metadata
    try:
        if 'metadata' in catalog_info and 'connections' in catalog_info['metadata']:
            connections = catalog_info['metadata']['connections']
            
            if 'products' in connections:
                return 'products'
            elif 'items' in connections:
                return 'items'
            elif 'product_items' in connections:
                return 'product_items'
    except Exception:
        pass
    
    # إذا فشل، جرب الافتراضيات
    edges_to_try = ['products', 'items', 'product_items']
    
    return edges_to_try[0]  # افترض 'products'

def get_merchant_name(catalog_name):
    """
    الحصول على اسم التاجر بناءً على معرف الكتالوج.
    
    Args:
        catalog_name (str): اسم الكتالوج
        
    Returns:
        str: اسم التاجر
    """
    merchant_names = {
        'SUDIID': 'Azúcar',
        'CASTELPHARMA': 'كاستيل فارما',
        'FOFO': 'Fofo',
        'UNILEVERID': 'يونيليفر',
        'BUSSNISID': 'متجر Argento'
    }
    
    return merchant_names.get(catalog_name, 'تاجر غير معروف')

def get_merchant_phone(catalog_name):
    """
    الحصول على هاتف التاجر.
    
    Args:
        catalog_name (str): اسم الكتالوج
        
    Returns:
        str: رقم الهاتف
    """
    merchant_phones = {
        'SUDIID': '01017549330',
        'CASTELPHARMA': '01064147284',
        'FOFO': '01212137256',
        'UNILEVERID': '01055688136',
        'BUSSNISID': '01055688136'
    }
    
    return merchant_phones.get(catalog_name, '01055688136')

def clean_product_data(product):
    """
    تنظيف وتنسيق بيانات المنتج.
    
    Args:
        product (dict): بيانات المنتج الأولية
        
    Returns:
        dict: بيانات المنتج المنظفة
    """
    cleaned = product.copy()
    
    # تأكد من وجود الحقول الأساسية
    cleaned['id'] = cleaned.get('id', '')
    cleaned['retailer_id'] = cleaned.get('retailer_id', cleaned.get('id', ''))
    
    # تنظيف الاسم
    if 'name' in cleaned and cleaned['name']:
        cleaned['title'] = cleaned['name']
    elif 'title' in cleaned and cleaned['title']:
        cleaned['name'] = cleaned['title']
    else:
        cleaned['title'] = 'منتج بدون اسم'
        cleaned['name'] = 'منتج بدون اسم'
    
    # تنظيف الوصف
    if 'description' not in cleaned or not cleaned['description']:
        cleaned['description'] = 'لا يوجد وصف'
    
    # تنظيف السعر
    if 'price' in cleaned and cleaned['price']:
        if isinstance(cleaned['price'], str):
            # تحويل من "100 EGP" إلى رقم
            try:
                price_parts = cleaned['price'].split()
                if price_parts:
                    cleaned['price'] = float(price_parts[0])
            except:
                cleaned['price'] = 0.0
    else:
        cleaned['price'] = 0.0
    
    # العملة
    if 'currency' not in cleaned or not cleaned['currency']:
        cleaned['currency'] = 'EGP'
    
    # الصورة
    if 'image_url' not in cleaned or not cleaned['image_url']:
        cleaned['image_url'] = 'https://via.placeholder.com/300x300/2c3e50/ecf0f1?text=Argento+Store'
    
    # التوفر
    if 'availability' not in cleaned:
        cleaned['availability'] = 'in stock'
    
    # التاريخ
    cleaned['last_updated'] = datetime.now().isoformat()
    
    return cleaned

def save_products_to_file(products, catalog_stats):
    """
    حفظ المنتجات في ملف JSON محلي.
    
    Args:
        products (list): قائمة المنتجات
        catalog_stats (dict): إحصائيات الكتالوجات
    """
    try:
        # إنشاء مجلد data إذا لم يكن موجوداً
        os.makedirs('data', exist_ok=True)
        
        # إضافة metadata
        catalog_data = {
            'metadata': {
                'last_sync': datetime.now().isoformat(),
                'total_products': len(products),
                'catalogs': catalog_stats
            },
            'products': products
        }
        
        # حفظ في ملف
        file_path = 'data/catalog_cache.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(catalog_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ {len(products)} منتج في {file_path}")
        
        # حفظ نسخة احتياطية
        backup_path = f"data/catalog_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(catalog_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"❌ خطأ في حفظ الملف: {e}")

def update_merchants_file(catalog_stats):
    """
    تحديث ملف التجار بأحدث المعلومات.
    
    Args:
        catalog_stats (dict): إحصائيات الكتالوجات
    """
    try:
        merchants_file = 'data/merchants.json'
        merchants = {}
        
        # إذا كان الملف موجوداً، حمله
        if os.path.exists(merchants_file):
            with open(merchants_file, 'r', encoding='utf-8') as f:
                merchants = json.load(f)
        
        # تحديث بيانات كل تاجر
        for catalog_name, stats in catalog_stats.items():
            if catalog_name not in merchants:
                merchants[catalog_name] = {
                    'name': get_merchant_name(catalog_name),
                    'phone': get_merchant_phone(catalog_name),
                    'catalog_id': stats['id'],
                    'address': 'الزقازيق الشرقية، حي الزهور'
                }
            
            # تحديث الإحصائيات
            merchants[catalog_name]['product_count'] = stats.get('product_count', 0)
            merchants[catalog_name]['last_sync'] = stats.get('last_sync', '')
            merchants[catalog_name]['last_updated'] = datetime.now().isoformat()
        
        # حفظ الملف
        with open(merchants_file, 'w', encoding='utf-8') as f:
            json.dump(merchants, f, ensure_ascii=False, indent=2)
        
        print("📊 تم تحديث ملف التجار")
        
    except Exception as e:
        print(f"⚠️  خطأ في تحديث ملف التجار: {e}")

def get_single_product(product_id):
    """
    جلب منتج معين من الكتالوج المخبأ.
    
    Args:
        product_id (str): معرف المنتج
        
    Returns:
        dict: بيانات المنتج أو None إذا لم يوجد
    """
    try:
        file_path = 'data/catalog_cache.json'
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
        
        # البحث في المنتجات
        for product in catalog_data.get('products', []):
            if product.get('id') == product_id or product.get('retailer_id') == product_id:
                return product
        
        return None
        
    except Exception as e:
        print(f"❌ خطأ في جلب المنتج: {e}")
        return None

def force_resync():
    """
    إعادة مزامنة قسرية (تجاهل الكاش).
    """
    print("🔄 بدء إعادة مزامنة قسرية...")
    
    # حذف الملف المخبأ لفرض إعادة المزامنة
    cache_file = 'data/catalog_cache.json'
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("🗑️  تم حذف الملف المخبأ")
    
    # إعادة المزامنة
    return sync_facebook_catalogs()

def check_sync_status():
    """
    التحقق من حالة آخر مزامنة.
    
    Returns:
        dict: حالة المزامنة
    """
    cache_file = 'data/catalog_cache.json'
    
    if not os.path.exists(cache_file):
        return {
            'synced': False,
            'message': 'لم تتم المزامنة بعد'
        }
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
        
        last_sync = catalog_data.get('metadata', {}).get('last_sync', '')
        total_products = catalog_data.get('metadata', {}).get('total_products', 0)
        
        if last_sync:
            sync_time = datetime.fromisoformat(last_sync)
            now = datetime.now()
            hours_diff = (now - sync_time).total_seconds() / 3600
            
            return {
                'synced': True,
                'last_sync': last_sync,
                'hours_ago': round(hours_diff, 1),
                'total_products': total_products,
                'message': f'آخر مزامنة منذ {round(hours_diff, 1)} ساعة'
            }
        
    except Exception as e:
        return {
            'synced': False,
            'message': f'خطأ في قراءة حالة المزامنة: {e}'
        }
    
    return {
        'synced': False,
        'message': 'حالة غير معروفة'
    }

# وظيفة للاستخدام في السكربتات
if __name__ == "__main__":
    # اختبار المزامنة
    print("🧪 اختبار مزامنة فيسبوك...")
    
    result = sync_facebook_catalogs()
    
    if result['success']:
        print(f"✅ نجحت المزامنة!")
        print(f"📊 المنتجات: {result['total_products']}")
        print(f"📦 الكتالوجات: {len(result['catalogs'])}")
        
        for catalog_name, stats in result['catalogs'].items():
            print(f"   - {catalog_name}: {stats['product_count']} منتج")
    else:
        print(f"❌ فشلت المزامنة: {result.get('error', 'خطأ غير معروف')}")
