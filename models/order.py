# ملف models/order.py
# تعريف نموذج الطلب مع العروض والشحن والمدفوعات

from datetime import datetime
import uuid

class Order:
    """نموذج يمثل طلباً كاملاً في النظام."""
    
    # حالات الطلب
    STATUS_PENDING = 'pending'           # منتظر الدفع
    STATUS_CONFIRMED = 'confirmed'       # تم التأكيد
    STATUS_PROCESSING = 'processing'     # قيد التجهيز
    STATUS_SHIPPED = 'shipped'          # تم الشحن
    STATUS_DELIVERED = 'delivered'      # تم التسليم
    STATUS_CANCELLED = 'cancelled'      # ملغي
    STATUS_RETURNED = 'returned'        # مرتجع
    
    # وسائل الدفع
    PAYMENT_CASH = 'cash_on_delivery'    # الدفع عند الاستلام
    PAYMENT_BANK = 'bank_transfer'       # تحويل بنكي
    PAYMENT_VODAFONE = 'vodafone_cash'   # فودافون كاش
    PAYMENT_FWRY = 'fawry'              # فوري
    
    # مصادر الطلب
    SOURCE_WHATSAPP = 'whatsapp'         # واتساب
    SOURCE_WEBSITE = 'website'           # الموقع
    SOURCE_PHONE = 'phone'              # اتصال هاتفي
    SOURCE_FACEBOOK = 'facebook'         # فيسبوك
    SOURCE_INSTAGRAM = 'instagram'       # إنستجرام
    
    def __init__(self, order_data=None):
        """
        تهيئة طلب جديد.
        
        Args:
            order_data (dict): بيانات الطلب الأساسية
        """
        # معرفات فريدة
        self.order_id = order_data.get('order_id') or f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        self.reference_id = order_data.get('reference_id') or ''
        
        # معلومات العميل
        self.customer = {
            'name': order_data.get('customer_name', ''),
            'phone': order_data.get('customer_phone', ''),
            'whatsapp': order_data.get('customer_whatsapp', ''),
            'email': order_data.get('customer_email', ''),
            'notes': order_data.get('customer_notes', '')
        }
        
        # معلومات الشحن
        self.shipping = {
            'address': order_data.get('shipping_address', ''),
            'city': order_data.get('shipping_city', ''),
            'area': order_data.get('shipping_area', ''),
            'building': order_data.get('shipping_building', ''),
            'floor': order_data.get('shipping_floor', ''),
            'apartment': order_data.get('shipping_apartment', ''),
            'landmark': order_data.get('shipping_landmark', ''),
            'notes': order_data.get('shipping_notes', '')
        }
        
        # المنتجات
        self.products = order_data.get('products', [])  # قائمة منتجات
        self.merchants = {}  # تجميع المنتجات حسب التاجر
        
        # الحسابات المالية
        self.subtotal = float(order_data.get('subtotal', 0))  # إجمالي المنتجات
        self.shipping_cost = float(order_data.get('shipping_cost', 0))  # تكلفة الشحن
        self.discount = float(order_data.get('discount', 0))  # الخصومات
        self.total = float(order_data.get('total', 0))  # الإجمالي النهائي
        self.paid_amount = float(order_data.get('paid_amount', 0))  # المبلغ المدفوع
        self.due_amount = float(order_data.get('due_amount', 0))  # المبلغ المستحق
        
        # العمولات والأرباح
        self.commissions = order_data.get('commissions', {})  # العمولات حسب التاجر
        self.total_commission = float(order_data.get('total_commission', 0))  # إجمالي العمولات
        self.net_profit = float(order_data.get('net_profit', 0))  # صافي الربح
        
        # معلومات الشحن من Speedaf
        self.speedaf_data = order_data.get('speedaf_data', {})
        self.tracking_number = order_data.get('tracking_number', '')
        self.shipment_status = order_data.get('shipment_status', 'pending')
        
        # الحالة والمعلومات
        self.status = order_data.get('status', self.STATUS_PENDING)
        self.payment_method = order_data.get('payment_method', self.PAYMENT_CASH)
        self.payment_status = order_data.get('payment_status', 'pending')
        self.source = order_data.get('source', self.SOURCE_WHATSAPP)
        
        # التواريخ
        self.created_at = order_data.get('created_at') or datetime.now().isoformat()
        self.updated_at = order_data.get('updated_at') or datetime.now().isoformat()
        self.estimated_delivery = order_data.get('estimated_delivery', '')
        
        # العروض والتخفيضات
        self.offers_applied = order_data.get('offers_applied', [])
        self.free_shipping = order_data.get('free_shipping', False)
        self.free_shipping_reason = order_data.get('free_shipping_reason', '')
        
        # ملاحظات داخلية
        self.internal_notes = order_data.get('internal_notes', '')
        self.admin_notes = order_data.get('admin_notes', '')
        
        # التحقق من صحة الطلب
        self.valid = self._validate_order()
        
        # تجميع المنتجات حسب التاجر
        self._group_products_by_merchant()
    
    def _validate_order(self):
        """التحقق من صحة بيانات الطلب."""
        if not self.customer.get('name') or not self.customer.get('phone'):
            return False
        
        if not self.shipping.get('address') or not self.shipping.get('city'):
            return False
        
        if len(self.products) == 0:
            return False
        
        if self.total <= 0:
            return False
        
        return True
    
    def _group_products_by_merchant(self):
        """تجميع المنتجات حسب التاجر للتسهيل."""
        self.merchants = {}
        
        for product in self.products:
            merchant_id = product.get('merchant_id')
            if not merchant_id:
                continue
            
            if merchant_id not in self.merchants:
                self.merchants[merchant_id] = {
                    'merchant_name': product.get('merchant_name', ''),
                    'products': [],
                    'subtotal': 0,
                    'commission': 0
                }
            
            self.merchants[merchant_id]['products'].append(product)
            
            # حساب الإجمالي للتاجر
            product_total = float(product.get('price', 0)) * int(product.get('quantity', 1))
            self.merchants[merchant_id]['subtotal'] += product_total
            
            # حساب العمولة للتاجر (إذا كانت محسوبة مسبقاً)
            product_commission = float(product.get('commission', 0))
            self.merchants[merchant_id]['commission'] += product_commission
    
    def add_product(self, product_data):
        """
        إضافة منتج إلى الطلب.
        
        Args:
            product_data (dict): بيانات المنتج
        """
        product_data['order_item_id'] = f"ITEM-{len(self.products)+1:03d}"
        self.products.append(product_data)
        
        # تحديث الإجماليات
        self._update_totals()
        self._group_products_by_merchant()
    
    def remove_product(self, product_id):
        """
        إزالة منتج من الطلب.
        
        Args:
            product_id (str): معرف المنتج
            
        Returns:
            bool: True إذا تمت الإزالة بنجاح
        """
        for i, product in enumerate(self.products):
            if product.get('id') == product_id or product.get('retailer_id') == product_id:
                self.products.pop(i)
                self._update_totals()
                self._group_products_by_merchant()
                return True
        return False
    
    def update_quantity(self, product_id, new_quantity):
        """
        تحديث كمية منتج.
        
        Args:
            product_id (str): معرف المنتج
            new_quantity (int): الكمية الجديدة
            
        Returns:
            bool: True إذا تم التحديث بنجاح
        """
        for product in self.products:
            if product.get('id') == product_id or product.get('retailer_id') == product_id:
                product['quantity'] = new_quantity
                product['total'] = float(product.get('price', 0)) * new_quantity
                self._update_totals()
                self._group_products_by_merchant()
                return True
        return False
    
    def _update_totals(self):
        """تحديث جميع الإجماليات المالية."""
        # حساب إجمالي المنتجات
        self.subtotal = sum(float(p.get('price', 0)) * int(p.get('quantity', 1)) for p in self.products)
        
        # حساب إجمالي العمولات
        self.total_commission = sum(float(p.get('commission', 0)) for p in self.products)
        
        # حساب الإجمالي النهائي
        self.total = self.subtotal + self.shipping_cost - self.discount
        
        # حساب المبلغ المستحق
        self.due_amount = self.total - self.paid_amount
        
        # حساب صافي الربح
        self.net_profit = self.total_commission - self.shipping_cost
    
    def apply_free_shipping(self, threshold=100, min_profit=15):
        """
        تطبيق الشحن المجاني إذا استوفى الشروط.
        
        Args:
            threshold (float): حد صافي الربح للشحن المجاني
            min_profit (float): أقل ربح مطلوب
            
        Returns:
            bool: True إذا تم تطبيق الشحن المجاني
        """
        # حساب صافي الربح قبل الشحن
        profit_before_shipping = self.total_commission
        
        # التحقق من الشروط
        if profit_before_shipping >= threshold and self.shipping_cost > 0:
            # تطبيق الشحن المجاني
            self.free_shipping = True
            self.free_shipping_reason = f"صافي الربح ({profit_before_shipping:.2f} ج) تجاوز الحد ({threshold} ج)"
            
            # تخزين تكلفة الشحن الأصلية ثم إلغائها
            self.original_shipping_cost = self.shipping_cost
            self.shipping_cost = 0
            
            # تحديث الإجماليات
            self._update_totals()
            return True
        
        return False
    
    def apply_offer(self, offer_type, offer_value):
        """
        تطبيق عرض ترويجي.
        
        Args:
            offer_type (str): نوع العرض ('percentage', 'fixed', 'bundle')
            offer_value: قيمة العرض (نسبة مئوية أو مبلغ ثابت)
            
        Returns:
            dict: تفاصيل العرض المطبق
        """
        offer_details = {
            'type': offer_type,
            'value': offer_value,
            'applied_at': datetime.now().isoformat()
        }
        
        if offer_type == 'percentage' and 0 < offer_value < 100:
            # خصم نسبة مئوية
            discount_amount = self.subtotal * (offer_value / 100)
            self.discount += discount_amount
            offer_details['discount_amount'] = discount_amount
            offer_details['description'] = f"خصم {offer_value}% على المنتجات"
            
        elif offer_type == 'fixed' and offer_value > 0:
            # خصم مبلغ ثابت
            self.discount += offer_value
            offer_details['discount_amount'] = offer_value
            offer_details['description'] = f"خصم {offer_value:.2f} ج"
            
        elif offer_type == 'bundle':
            # عرض حزمة (مثل اشترِ 2 واحصل على 1 مجاناً)
            offer_details['description'] = "عرض حزمة"
            # سيتم تطبيقه يدوياً على المنتجات المحددة
        
        self.offers_applied.append(offer_details)
        self._update_totals()
        
        return offer_details
    
    def set_shipping_cost(self, region, base_rates, handling_fee=5):
        """
        حساب وتحديد تكلفة الشحن.
        
        Args:
            region (str): المنطقة (Cairo, Giza, Alexandria, etc.)
            base_rates (dict): أسعار الشحن الأساسية
            handling_fee (float): رسوم المناولة
        """
        # الحصول على سعر المنطقة أو السعر الافتراضي
        region_rate = base_rates.get(region, base_rates.get('default', 80))
        
        # حساب تكلفة الشحن
        self.shipping_cost = region_rate + handling_fee
        self._update_totals()
        
        # التحقق من أهلية الشحن المجاني
        self.apply_free_shipping()
    
    def set_speedaf_data(self, speedaf_data):
        """
        تعيين بيانات Speedaf للشحنة.
        
        Args:
            speedaf_data (dict): بيانات Speedaf
        """
        self.speedaf_data = speedaf_data
        
        if 'tracking_number' in speedaf_data:
            self.tracking_number = speedaf_data['tracking_number']
        
        if 'status' in speedaf_data:
            self.shipment_status = speedaf_data['status']
    
    def update_status(self, new_status, notes=''):
        """
        تحديث حالة الطلب.
        
        Args:
            new_status (str): الحالة الجديدة
            notes (str): ملاحظات عن التغيير
        """
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
        
        # إضافة إلى الملاحظات الإدارية
        status_change_note = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: تغيير الحالة من {old_status} إلى {new_status}"
        if notes:
            status_change_note += f" - {notes}"
        
        self.admin_notes = f"{status_change_note}\n{self.admin_notes}"
    
    def calculate_for_unilever(self, product_data, wholesale_price, pack_size=24):
        """
        حساب خاص لطلبات Unilever (الكرتونات).
        
        Args:
            product_data (dict): بيانات المنتج
            wholesale_price (float): سعر الجملة
            pack_size (int): حجم الكرتونة
            
        Returns:
            dict: تفاصيل الحساب
        """
        quantity_needed = product_data.get('quantity', 1)
        
        # حساب عدد الكرتونات المطلوبة (تقريب لأعلى)
        cartons_needed = (quantity_needed + pack_size - 1) // pack_size
        
        # الكمية الفعلية التي سيتم شراؤها (كرتونات كاملة)
        actual_quantity = cartons_needed * pack_size
        
        # تكلفة الشراء
        purchase_cost = wholesale_price * actual_quantity
        
        # حساب الربح
        sales_revenue = float(product_data.get('price', 0)) * quantity_needed
        profit = sales_revenue - purchase_cost
        
        return {
            'cartons_needed': cartons_needed,
            'actual_quantity': actual_quantity,
            'purchase_cost': purchase_cost,
            'sales_revenue': sales_revenue,
            'profit': profit,
            'excess_quantity': actual_quantity - quantity_needed,
            'unit_cost': purchase_cost / actual_quantity if actual_quantity > 0 else 0
        }
    
    def to_dict(self, include_products=True):
        """
        تحويل الطلب إلى قاموس.
        
        Args:
            include_products (bool): تضمين قائمة المنتجات
            
        Returns:
            dict: بيانات الطلب
        """
        order_dict = {
            'order_id': self.order_id,
            'reference_id': self.reference_id,
            'customer': self.customer,
            'shipping': self.shipping,
            'financial': {
                'subtotal': self.subtotal,
                'shipping_cost': self.shipping_cost,
                'discount': self.discount,
                'total': self.total,
                'paid_amount': self.paid_amount,
                'due_amount': self.due_amount,
                'total_commission': self.total_commission,
                'net_profit': self.net_profit
            },
            'merchants_summary': self.merchants,
            'speedaf_data': self.speedaf_data,
            'tracking_number': self.tracking_number,
            'shipment_status': self.shipment_status,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'source': self.source,
            'timestamps': {
                'created_at': self.created_at,
                'updated_at': self.updated_at,
                'estimated_delivery': self.estimated_delivery
            },
            'offers': {
                'offers_applied': self.offers_applied,
                'free_shipping': self.free_shipping,
                'free_shipping_reason': self.free_shipping_reason
            },
            'notes': {
                'internal_notes': self.internal_notes,
                'admin_notes': self.admin_notes
            },
            'valid': self.valid
        }
        
        if include_products:
            order_dict['products'] = self.products
        
        return order_dict
    
    def __str__(self):
        """تمثيل نصي للطلب."""
        return f"Order {self.order_id}: {self.customer['name']} - {self.total:.2f} {self.status}"# نموذج الطلب
    def extract_speedaf_data(self):
    """
    استخراج بيانات الطلب لتنسيق Speedaf الـ 22 عمود.
    
    Returns:
        dict: بيانات البرومبت
    """
    # تحديد الراسل بناءً على التاجر الرئيسي
    sender_name = self._get_sender_name()
    sender_phone = self._get_sender_phone()
    
    # استخراج بيانات المستلم
    receiver_name = self.customer.get('name', '').strip()
    receiver_phone = self._format_phone(self.customer.get('phone', ''))
    
    # استخراج المدينة والمنطقة (ستحتاج لقائمة رسمية)
    sender_city, sender_area = self._extract_city_area(self.shipping.get('city', ''), 
                                                      self.shipping.get('area', ''))
    receiver_city, receiver_area = self._extract_city_area(self.shipping.get('city', ''), 
                                                          self.shipping.get('area', ''))
    
    # اسم المنتج (من أول منتج أو وصف عام)
    goods_name = self._get_goods_name()
    
    # حساب COD (سعر المنتج + الشحن)
    cod_value = self.total if self.total > 0 else 0
    
    return {
        'sender': {
            'name': sender_name,
            'phone': sender_phone,
            'city': sender_city,
            'area': sender_area,
            'address': self.shipping.get('address', '')
        },
        'receiver': {
            'name': receiver_name,
            'phone': receiver_phone,
            'city': receiver_city,
            'area': receiver_area,
            'address': self._format_receiver_address()
        },
        'goods': {
            'type': 'Normal',
            'name': goods_name,
            'quantity': 1,
            'weight': 1,
            'cod': cod_value,
            'allow_open': 'No',  # افتراضي
            'delivery_type': 'Deliver'
        },
        'order_id': self.order_id
    }

def _get_sender_name(self):
    """الحصول على اسم الراسل بناءً على التاجر."""
    if self.merchants:
        # أخذ اسم التاجر الأول
        for merchant_id, merchant_data in self.merchants.items():
            if merchant_id == 'SUDIID':
                return 'Azúcar'
            elif merchant_id == 'CASTELPHARMA':
                return 'كاستيل فارما'
            elif merchant_id == 'FOFO':
                return 'Fofo'
            elif merchant_id == 'UNILEVERID':
                return 'يونيليفر'
    
    # اسم افتراضي
    return 'Argento Store'

def _get_sender_phone(self):
    """الحصول على هاتف الراسل بناءً على التاجر."""
    if self.merchants:
        for merchant_id, merchant_data in self.merchants.items():
            if merchant_id == 'SUDIID':
                return '01017549330'
            elif merchant_id == 'CASTELPHARMA':
                return '01064147284'
            elif merchant_id == 'FOFO':
                return '01212137256'
            elif merchant_id == 'UNILEVERID':
                return '01055688136'
    
    return '01055688136'  # رقمك

def _format_phone(self, phone):
    """تنسيق الهاتف كـ 11 رقم."""
    # إزالة أي مسافات أو رموز
    cleaned = ''.join(filter(str.isdigit, str(phone)))
    
    if cleaned.startswith('20'):
        # إذا بدأ بـ 20 (مصر)، أزل 20 وأضف 0
        if len(cleaned) >= 12:
            return '0' + cleaned[2:11] if len(cleaned) > 11 else '0' + cleaned[2:]
    elif cleaned.startswith('01') and len(cleaned) == 10:
        # إذا كان 10 أرقام وبدأ بـ 01
        return '0' + cleaned
    elif len(cleaned) == 10:
        return '0' + cleaned
    elif len(cleaned) == 11:
        return cleaned
    
    # إذا لم يتطابق مع أي شكل، أعد كـ 11 صفر
    return '0' * 11

def _extract_city_area(self, city_input, area_input):
    """
    استخراج المدينة والمنطقة من القائمة الرسمية.
    TODO: ستحتاج لقاعدة بيانات المدن والمناطق
    """
    # قائمة المدن الرسمية (مثال)
    official_cities = {
        'الزقازيق': 'Sharqia',
        'القاهرة': 'Cairo',
        'الجيزة': 'Giza',
        'الإسكندرية': 'Alexandria',
        'المنصورة': 'Dakahlia',
        'طنطا': 'Gharbia',
        'المنيا': 'Minya'
    }
    
    # قائمة المناطق الرسمية (مثال)
    official_areas = {
        'الزقازيق': 'Zagazig',
        'حي الزهور': 'Zagazig',
        'الشرقية': 'Sharqia',
        'وسط البلد': 'Downtown',
        'المعادي': 'Maadi',
        'المهندسين': 'Mohandessin',
        'سموحة': 'Smouha'
    }
    
    # البحث عن المدينة
    city = official_cities.get(city_input, 'Sharqia')
    
    # البحث عن المنطقة
    area = official_areas.get(area_input, 'Zagazig')
    
    return city, area

def _get_goods_name(self):
    """الحصول على اسم المنتج للبوليصة."""
    if self.products:
        # أخذ اسم أول منتج
        first_product = self.products[0]
        product_name = first_product.get('title', '')
        
        # اختصار إذا كان طويلاً
        if len(product_name) > 30:
            product_name = product_name[:27] + '...'
        
        return product_name
    
    return 'منتجات تسوق'

def _format_receiver_address(self):
    """تنسيق عنوان المستلم."""
    address_parts = []
    
    if self.shipping.get('address'):
        address_parts.append(self.shipping['address'])
    
    if self.shipping.get('building'):
        address_parts.append(f"مبني {self.shipping['building']}")
    
    if self.shipping.get('apartment'):
        address_parts.append(f"شقة {self.shipping['apartment']}")
    
    if self.shipping.get('landmark'):
        address_parts.append(f"بجوار {self.shipping['landmark']}")
    
    return '، '.join(address_parts) if address_parts else 'عنوان غير محدد'

def generate_speedaf_row(self):
    """
    توليد صف Speedaf واحد (22 عمود).
    
    Returns:
        str: صف بتنسيق الـ 22 عمود مفصولة بتبويبات
    """
    data = self.extract_speedaf_data()
    
    # بناء الصف حسب التنسيق المطلوب
    row_fields = [
        '',  # 1. S.O. - فارغ
        data['goods']['type'],  # 2. Goods type
        data['goods']['name'],  # 3. Goods name
        str(data['goods']['quantity']),  # 4. Quantity
        str(data['goods']['weight']),  # 5. Weight
        str(data['goods']['cod']),  # 6. COD
        '',  # 7. Insure price - فارغ
        data['goods']['allow_open'],  # 8. Whether to allow the package to be opened
        '',  # 9. Remark - فارغ
        data['sender']['name'],  # 10. Name (Sender)
        data['sender']['phone'],  # 11. Telephone (Sender)
        data['sender']['city'],  # 12. City (Sender)
        data['sender']['area'],  # 13. Area (Sender)
        data['sender']['address'],  # 14. Senders address
        '',  # 15. Sender Email - فارغ
        data['receiver']['name'],  # 16. Name (Receiver)
        data['receiver']['phone'],  # 17. Telephone (Receiver)
        data['receiver']['city'],  # 18. City (Receiver)
        data['receiver']['area'],  # 19. Area (Receiver)
        data['receiver']['address'],  # 20. Receivers address
        '',  # 21. Receiver Email - فارغ
        data['goods']['delivery_type']  # 22. Delivery Type
    ]
    
    return '\t'.join(row_fields)
