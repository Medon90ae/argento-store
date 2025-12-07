
# utils/speedaf_exporter.py
# توليد ملف CSV بتنسيق Speedaf الدقيق (22 عمود)

import json
import os
from datetime import datetime
import re

def generate_speedaf_csv():
    """
    توليد محتوى CSV بتنسيق Speedaf المطلوب (22 عمود).
    
    Returns:
        str: محتوى CSV كامل بدون عناوين أعمدة
    """
    try:
        # جلب الطلبات المؤهلة للتصدير
        orders = get_exportable_orders()
        
        if not orders:
            return ""
        
        # توليد صف لكل طلب
        csv_rows = []
        for order in orders:
            csv_row = convert_order_to_speedaf_row(order)
            if csv_row:
                csv_rows.append(csv_row)
        
        # دمج الصفوف بفواصل أسطر
        return "\n".join(csv_rows)
        
    except Exception as e:
        print(f"خطأ في توليد ملف Speedaf: {e}")
        return ""

def get_exportable_orders():
    """
    جلب الطلبات المؤهلة للتصدير إلى Speedaf.
    
    Returns:
        list: قائمة الطلبات المؤهلة
    """
    orders_file = 'data/orders.json'
    
    if not os.path.exists(orders_file):
        return []
    
    try:
        with open(orders_file, 'r', encoding='utf-8') as f:
            orders = json.load(f)
        
        # تصفية الطلبات: معلق أو مؤكد ولم يتم شحنه بعد
        export_orders = []
        for order in orders:
            status = order.get('status', '').lower()
            # استبعاد الطلبات الملغاة أو المسلمة بالفعل
            if status in ['pending', 'confirmed', 'processing']:
                export_orders.append(order)
        
        return export_orders
        
    except Exception as e:
        print(f"خطأ في قراءة الطلبات: {e}")
        return []

def convert_order_to_speedaf_row(order):
    """
    تحويل طلب إلى صف Speedaf (22 عمود).
    
    Args:
        order (dict): بيانات الطلب
        
    Returns:
        str: صف CSV واحد (22 عمود مفصولة بتبويبات)
    """
    try:
        # ===== العمود 1: S.O. =====
        so_number = ""  # فارغ دائماً
        
        # ===== العمود 2: Goods type =====
        goods_type = "Normal"  # ثابتة
        
        # ===== العمود 3: Goods name =====
        goods_name = order.get('product_title', 'منتج')
        # اختصار إذا كان طويلاً
        if len(goods_name) > 100:
            goods_name = goods_name[:97] + "..."
        
        # ===== العمود 4: Quantity =====
        quantity = "1"  # قيمة افتراضية
        
        # ===== العمود 5: Weight =====
        weight = "1"  # قيمة افتراضية
        
        # ===== العمود 6: COD =====
        # سعر المنتج + الشحن
        product_price = float(order.get('product_price', 0))
        shipping_cost = float(order.get('shipping_cost', 0))
        cod_value = product_price + shipping_cost
        cod = str(cod_value)
        
        # ===== العمود 7: Insure price =====
        insure_price = ""  # فارغ
        
        # ===== العمود 8: Whether to allow the package to be opened =====
        allow_open = "No"  # افتراضي No
        
        # ===== العمود 9: Remark =====
        remark = ""  # فارغ
        
        # ===== العمود 10: Name (Sender) =====
        sender_name = get_sender_name(order)
        
        # ===== العمود 11: Telephone (Sender) =====
        sender_phone = format_phone_for_speedaf(order.get('sender_phone', '01055688136'))
        
        # ===== العمود 12: City (Sender) =====
        sender_city = get_city_from_config("الزقازيق")  # مدينة الراسل ثابتة
        
        # ===== العمود 13: Area (Sender) =====
        sender_area = get_area_from_config("الزقازيق", "حي الزهور")  # منطقة الراسل ثابتة
        
        # ===== العمود 14: Senders address =====
        sender_address = order.get('sender_address', 'الزقازيق الشرقية، حي الزهور')
        
        # ===== العمود 15: Sender Email =====
        sender_email = ""  # فارغ
        
        # ===== العمود 16: Name (Receiver) =====
        receiver_name = order.get('customer_name', '').strip()
        
        # ===== العمود 17: Telephone (Receiver) =====
        receiver_phone = format_phone_for_speedaf(order.get('customer_phone', ''))
        
        # ===== العمود 18: City (Receiver) =====
        receiver_city = get_city_from_config(order.get('shipping_city', 'الزقازيق'))
        
        # ===== العمود 19: Area (Receiver) =====
        receiver_area = get_area_from_config(
            order.get('shipping_city', 'الزقازيق'),
            order.get('shipping_area', 'حي الزهور')
        )
        
        # ===== العمود 20: Receivers address =====
        receiver_address = build_receiver_address(order)
        
        # ===== العمود 21: Receiver Email =====
        receiver_email = ""  # فارغ
        
        # ===== العمود 22: Delivery Type =====
        delivery_type = "Deliver"  # ثابتة
        
        # تجميع الحقول في قائمة
        fields = [
            so_number,                    # 1. S.O.
            goods_type,                   # 2. Goods type
            goods_name,                   # 3. Goods name
            quantity,                     # 4. Quantity
            weight,                       # 5. Weight
            cod,                          # 6. COD
            insure_price,                 # 7. Insure price
            allow_open,                   # 8. Whether to allow the package to be opened
            remark,                       # 9. Remark
            sender_name,                  # 10. Name (Sender)
            sender_phone,                 # 11. Telephone (Sender)
            sender_city,                  # 12. City (Sender)
            sender_area,                  # 13. Area (Sender)
            sender_address,               # 14. Senders address
            sender_email,                 # 15. Sender Email
            receiver_name,                # 16. Name (Receiver)
            receiver_phone,               # 17. Telephone (Receiver)
            receiver_city,                # 18. City (Receiver)
            receiver_area,                # 19. Area (Receiver)
            receiver_address,             # 20. Receivers address
            receiver_email,               # 21. Receiver Email
            delivery_type                 # 22. Delivery Type
        ]
        
        # التحقق من عدم وجود قيم فارغة أساسية
        if not receiver_name or not receiver_phone or not receiver_city:
            print(f"تحذير: طلب {order.get('order_id')} ناقص بيانات أساسية")
            return None
        
        # الانضمام بعلامات التبويب
        return "\t".join(fields)
        
    except Exception as e:
        print(f"خطأ في تحويل الطلب {order.get('order_id')}: {e}")
        return None

def get_sender_name(order):
    """
    تحديد اسم الراسل بناءً على التاجر.
    
    Args:
        order (dict): بيانات الطلب
        
    Returns:
        str: اسم الراسل
    """
    merchant_id = order.get('merchant_id', '')
    
    sender_names = {
        'SUDIID': 'Azúcar',
        'CASTELPHARMA': 'كاستيل فارما',
        'FOFO': 'Fofo',
        'UNILEVERID': 'يونيليفر'
    }
    
    return sender_names.get(merchant_id, 'Argento Store')

def format_phone_for_speedaf(phone):
    """
    تنسيق رقم الهاتف لـ Speedaf (11 رقم).
    
    Args:
        phone (str): رقم الهاتف
        
    Returns:
        str: رقم مهيأ بـ 11 رقم
    """
    if not phone:
        return "0" * 11
    
    # إزالة كل ما ليس رقم
    digits = ''.join(filter(str.isdigit, str(phone)))
    
    if len(digits) == 10 and digits.startswith('1'):
        return '0' + digits
    elif len(digits) == 11:
        return digits
    elif len(digits) == 12 and digits.startswith('20'):
        return '0' + digits[2:]
    elif len(digits) == 9:
        return '01' + digits
    elif len(digits) == 8:
        return '010' + digits
    
    # إذا لم يتطابق مع أي شكل، أعد 11 صفر
    return "0" * 11

def get_city_from_config(city_input):
    """
    استخراج اسم المدينة بالإنجليزية من القائمة الرسمية.
    
    Args:
        city_input (str): اسم المدينة (عربي أو إنجليزي)
        
    Returns:
        str: اسم المدينة بالإنجليزية
    """
    try:
        # محاولة استيراد خرائط الترجمة من config
        from config import CITY_TRANSLATIONS_AR_TO_EN
        
        # البحث في الترجمة من العربية إلى الإنجليزية
        if city_input in CITY_TRANSLATIONS_AR_TO_EN:
            return CITY_TRANSLATIONS_AR_TO_EN[city_input]
        
        # البحث العكسي (إذا كان الإدخال إنجليزي)
        for ar_name, en_name in CITY_TRANSLATIONS_AR_TO_EN.items():
            if en_name == city_input:
                return en_name
        
        # إذا لم يتم العثور، استخدم الافتراضي
        return "Sharqia"
        
    except ImportError:
        # إذا لم يتوفر config، استخدم القائمة المدمجة
        city_mapping = {
            'الزقازيق': 'Sharqia',
            'القاهرة': 'Cairo',
            'الجيزة': 'Giza',
            'الإسكندرية': 'Alexandria',
            'الشرقية': 'Sharqia',
            'المنصورة': 'Dakahlia',
            'طنطا': 'Gharbia',
            'المنيا': 'Minya'
        }
        
        return city_mapping.get(city_input, 'Sharqia')

def get_area_from_config(city_input, area_input):
    """
    استخراج اسم المنطقة بالإنجليزية من القائمة الرسمية.
    
    Args:
        city_input (str): اسم المدينة
        area_input (str): اسم المنطقة
        
    Returns:
        str: اسم المنطقة بالإنجليزية
    """
    try:
        # محاولة استيراد خرائط الترجمة من config
        from config import AREA_TRANSLATIONS_AR_TO_EN
        
        # البحث في الترجمة من العربية إلى الإنجليزية
        if area_input in AREA_TRANSLATIONS_AR_TO_EN:
            return AREA_TRANSLATIONS_AR_TO_EN[area_input]
        
        # البحث العكسي (إذا كان الإدخال إنجليزي)
        for ar_name, en_name in AREA_TRANSLATIONS_AR_TO_EN.items():
            if en_name == area_input:
                return en_name
        
        # إذا لم يتم العثور، استخدم منطق استبدال بسيط
        area_mapping = {
            'حي الزهور': 'Zagazig',
            'الزقازيق': 'Zagazig',
            'المعادي': 'Maadi',
            'المهندسين': 'Mohandisen',
            'وسط البلد': 'Downtown',
            'مدينة نصر': 'Nasr City',
            'الشيخ زايد': 'Sheikh Zayed'
        }
        
        return area_mapping.get(area_input, 'Zagazig')
        
    except ImportError:
        # إذا لم يتوفر config، استخدم القائمة المدمجة
        area_mapping = {
            'حي الزهور': 'Zagazig',
            'الزقازيق': 'Zagazig',
            'المعادي': 'Maadi',
            'المهندسين': 'Mohandisen'
        }
        
        return area_mapping.get(area_input, 'Zagazig')

def build_receiver_address(order):
    """
    بناء عنوان المستلم.
    
    Args:
        order (dict): بيانات الطلب
        
    Returns:
        str: العنوان الكامل
    """
    address_parts = []
    
    # العنوان الأساسي
    if order.get('shipping_address'):
        address_parts.append(order['shipping_address'])
    
    # المبنى
    if order.get('shipping_building'):
        address_parts.append(f"مبنى {order['shipping_building']}")
    
    # الشقة
    if order.get('shipping_apartment'):
        address_parts.append(f"شقة {order['shipping_apartment']}")
    
    # علامة مميزة
    if order.get('shipping_landmark'):
        address_parts.append(f"بجوار {order['shipping_landmark']}")
    
    # المنطقة
    if order.get('shipping_area'):
        address_parts.append(order['shipping_area'])
    
    # المدينة
    if order.get('shipping_city'):
        address_parts.append(order['shipping_city'])
    
    # إذا لم يكن هناك عنوان، استخدم قيمة افتراضية
    if not address_parts:
        return "عنوان غير محدد"
    
    return "، ".join(address_parts)

def export_to_file():
    """
    تصدير ملف Speedaf إلى ملف CSV.
    
    Returns:
        dict: معلومات عن الملف المُصدر
    """
    try:
        csv_content = generate_speedaf_csv()
        
        if not csv_content:
            return {
                'success': False,
                'message': 'لا توجد طلبات مؤهلة للتصدير'
            }
        
        # إنشاء اسم للملف
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"speedaf_export_{timestamp}.csv"
        filepath = os.path.join('data', 'exports', filename)
        
        # تأكد من وجود مجلد exports
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # حفظ الملف
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        # حساب عدد الصفوف
        row_count = len(csv_content.strip().split('\n'))
        
        return {
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'row_count': row_count,
            'download_url': f"/data/exports/{filename}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f"خطأ في التصدير: {str(e)}"
        }

def get_speedaf_headers():
    """
    الحصول على عناوين أعمدة Speedaf (للعرض فقط).
    
    Returns:
        list: عناوين الأعمدة الـ 22
    """
    return [
        'S.O.',
        'Goods type',
        'Goods name',
        'Quantity',
        'Weight',
        'COD',
        'Insure price',
        'Whether to allow the package to be opened',
        'Remark',
        'Name',
        'Telephone',
        'City',
        'Area',
        'Senders address',
        'Sender Email',
        'Name',
        'Telephone',
        'City',
        'Area',
        'Receivers address',
        'Receiver Email',
        'Delivery Type'
    ]

# وظيفة مساعدة للاختبار
def test_speedaf_export():
    """اختبار وظيفة التصدير."""
    # إنشاء طلب تجريبي
    test_order = {
        'order_id': 'TEST-001',
        'product_title': 'شامبو يونيليفر 250 مل',
        'product_price': 45.0,
        'shipping_cost': 65.0,
        'merchant_id': 'UNILEVERID',
        'sender_phone': '01055688136',
        'sender_address': 'الزقازيق الشرقية، حي الزهور',
        'customer_name': 'أحمد محمد',
        'customer_phone': '01012345678',
        'shipping_city': 'الزقازيق',
        'shipping_area': 'حي الزهور',
        'shipping_address': 'شارع النور، بجوار مسجد الفتح',
        'shipping_building': '12',
        'shipping_apartment': '5',
        'shipping_landmark': 'مدرسة النور الابتدائية',
        'status': 'pending'
    }
    
    # توليد الصف
    csv_row = convert_order_to_speedaf_row(test_order)
    
    print("=" * 50)
    print("اختبار تصدير Speedaf")
    print("=" * 50)
    print(f"عدد الحقول: {len(csv_row.split('\\t'))}")
    print(f"الصف الناتج: {csv_row}")
    print("=" * 50)
    
    return csv_row

if __name__ == "__main__":
    # اختبار الوظيفة
    test_result = test_speedaf_export()
    print("✅ اختبار تصدير Speedaf مكتمل")
