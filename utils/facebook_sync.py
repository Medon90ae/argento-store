# utils/facebook_sync.py - الإصدار المصحح
import os
import json
import requests
from datetime import datetime
import time

# مسار الملفات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, 'data', 'catalog_cache.json')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# تأكد من وجود مجلد data
os.makedirs(DATA_DIR, exist_ok=True)

def sync_facebook_catalogs():
    """مزامنة جميع كتالوجات فيسبوك."""
    try:
        print("🔄 بدء مزامنة كتالوجات فيسبوك...")
        
        catalog_ids = ['SUDIID', 'CASTELPHARMA', 'FOFO', 'UNILEVERID']
        all_products = []
        catalog_stats = {}
        
        for catalog_id in catalog_ids:
            try:
                print(f"📦 جلب منتجات كتالوج: {catalog_id}")
                
                # استخدم الوظائف الحالية
                products = get_facebook_catalog_products_simple(catalog_id)
                
                if products:
                    for product in products:
                        product['merchant_id'] = catalog_id
                        product['merchant_name'] = get_merchant_name(catalog_id)
                    
                    all_products.extend(products)
                    catalog_stats[catalog_id] = {
                        'product_count': len(products),
                        'status': 'success',
                        'last_sync': datetime.now().isoformat()
                    }
                    
                    print(f"✅ تم جلب {len(products)} منتج من {catalog_id}")
                else:
                    catalog_stats[catalog_id] = {
                        'product_count': 0,
                        'status': 'empty',
                        'last_sync': datetime.now().isoformat()
                    }
                    print(f"⚠️  لا توجد منتجات في كتالوج {catalog_id}")
                    
            except Exception as e:
                print(f"❌ خطأ في كتالوج {catalog_id}: {e}")
                catalog_stats[catalog_id] = {
                    'product_count': 0,
                    'status': 'error',
                    'error': str(e),
                    'last_sync': datetime.now().isoformat()
                }
        
        # حفظ جميع المنتجات
        save_data = {
            'metadata': {
                'total_products': len(all_products),
                'last_updated': datetime.now().isoformat(),
                'catalogs': list(catalog_stats.keys()),
                'catalog_stats': catalog_stats
            },
            'products': all_products
        }
        
        with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 تم حفظ {len(all_products)} منتج في {CATALOG_FILE}")
        
        return {
            'success': True,
            'total_products': len(all_products),
            'message': f'تم تحديث الكتالوج بـ {len(all_products)} منتج'
        }
        
    except Exception as e:
        print(f"❌ خطأ في المزامنة: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': 'فشل تحديث الكتالوج'
        }

def get_facebook_catalog_products_simple(catalog_id):
    """جلب منتجات الكتالوج بطريقة مبسطة (نموذجية)."""
    # بيانات نموذجية للمنتجات (للتجربة)
    products = []
    
    # أنشئ بعض المنتجات النموذجية بناءً على التاجر
    if catalog_id == 'SUDIID':  # Azúcar
        products = [
            {
                'id': 'SUDIID_001',
                'name': 'سكر أبيض ناعم 1 كجم',
                'title': 'سكر أبيض ناعم 1 كجم',
                'price': 25.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/FF6B6B/fff?text=Sugar',
                'description': 'سكر أبيض ناعم عالي الجودة، مناسب للاستخدام المنزلي والصناعي',
                'availability': 'in stock',
                'retailer_id': 'SUGAR001'
            },
            {
                'id': 'SUDIID_002',
                'name': 'سكر بني عضوي 500 جم',
                'title': 'سكر بني عضوي 500 جم',
                'price': 35.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/4ECDC4/fff?text=Brown+Sugar',
                'description': 'سكر بني عضوي طبيعي، غني بالمعادن',
                'availability': 'in stock',
                'retailer_id': 'SUGAR002'
            }
        ]
    elif catalog_id == 'CASTELPHARMA':  # كاستيل فارما
        products = [
            {
                'id': 'CASTEL_001',
                'name': 'باراسيتامول 500 ملجم',
                'title': 'باراسيتامول 500 ملجم',
                'price': 15.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/45B7D1/fff?text=Paracetamol',
                'description': 'مسكن للألم وخافض للحرارة',
                'availability': 'in stock',
                'retailer_id': 'MED001'
            },
            {
                'id': 'CASTEL_002',
                'name': 'فيتامين سي 1000 ملجم',
                'title': 'فيتامين سي 1000 ملجم',
                'price': 45.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/96CEB4/fff?text=Vitamin+C',
                'description': 'مكمل غذائي لفيتامين سي لتعزيز المناعة',
                'availability': 'in stock',
                'retailer_id': 'MED002'
            }
        ]
    elif catalog_id == 'FOFO':  # Fofo
        products = [
            {
                'id': 'FOFO_001',
                'name': 'تيشيرت قطني رجالي',
                'title': 'تيشيرت قطني رجالي',
                'price': 120.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/FECA57/fff?text=T-Shirt',
                'description': 'تيشيرت قطني ناعم، مناسب للاستخدام اليومي',
                'availability': 'in stock',
                'retailer_id': 'TSHIRT001'
            }
        ]
    elif catalog_id == 'UNILEVERID':  # يونيليفر
        products = [
            {
                'id': 'UNILEVER_001',
                'name': 'صابون دوف 100 جم',
                'title': 'صابون دوف 100 جم',
                'price': 20.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/FF9FF3/fff?text=Dove',
                'description': 'صابون ترطيب للبشرة الحساسة',
                'availability': 'in stock',
                'retailer_id': 'SOAP001'
            },
            {
                'id': 'UNILEVER_002',
                'name': 'شامبو كلير 400 مل',
                'title': 'شامبو كلير 400 مل',
                'price': 65.0,
                'currency': 'EGP',
                'image_url': 'https://via.placeholder.com/300x300/54A0FF/fff?text=Shampoo',
                'description': 'شامبو للعناية بالشعر الدهني',
                'availability': 'in stock',
                'retailer_id': 'SHAMPOO001'
            }
        ]
    
    return products

def get_merchant_name(catalog_id):
    """الحصول على اسم التاجر."""
    merchants = {
        'SUDIID': 'Azúcar',
        'CASTELPHARMA': 'كاستيل فارما',
        'FOFO': 'Fofo',
        'UNILEVERID': 'يونيليفر'
    }
    return merchants.get(catalog_id, 'تاجر غير معروف')

def check_sync_status():
    """التحقق من حالة آخر مزامنة."""
    if not os.path.exists(CATALOG_FILE):
        return {
            'synced': False,
            'message': 'لم تتم المزامنة بعد',
            'total_products': 0
        }
    
    try:
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
        
        metadata = catalog_data.get('metadata', {})
        last_updated = metadata.get('last_updated', '')
        total_products = metadata.get('total_products', 0)
        
        if last_updated:
            sync_time = datetime.fromisoformat(last_updated)
            now = datetime.now()
            hours_diff = (now - sync_time).total_seconds() / 3600
            
            return {
                'synced': True,
                'last_sync': last_updated,
                'hours_ago': round(hours_diff, 1),
                'total_products': total_products,
                'message': f'آخر مزامنة منذ {round(hours_diff, 1)} ساعة'
            }
        
    except Exception as e:
        return {
            'synced': False,
            'message': f'خطأ في قراءة حالة المزامنة: {e}',
            'total_products': 0
        }
    
    return {
        'synced': False,
        'message': 'حالة غير معروفة',
        'total_products': 0
    }

def get_cached_products():
    """جلب المنتجات المخزنة مؤقتاً."""
    try:
        if not os.path.exists(CATALOG_FILE):
            return []
        
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog_data = json.load(f)
        
        return catalog_data.get('products', [])
        
    except Exception as e:
        print(f"❌ خطأ في جلب المنتجات: {e}")
        return []

# للاختبار
if __name__ == "__main__":
    result = sync_facebook_catalogs()
    print(f"النتيجة: {result}")
