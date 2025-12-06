# نموذج الشحنة
# ملف models/shipment.py (معدل تمامًا)
# متخصص في توليد صفوف Speedaf بتنسيق الـ 22 عمود

class SpeedafShipmentGenerator:
    """مولد صفوف Speedaf بتنسيق الـ 22 عمود."""
    
    def __init__(self):
        # قوائم المدن والمناطق الرسمية (يجب ملؤها من config أو ملف خارجي)
        self.official_cities = self._load_official_cities()
        self.official_areas = self._load_official_areas()
        
        # بيانات الراسلين الثابتة لكل تاجر
        self.sender_profiles = {
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
    
    def _load_official_cities(self):
        """تحميل قائمة المدن الرسمية."""
        # TODO: سيتم تحميلها من config أو قاعدة بيانات
        return {
            'الزقازيق': 'Sharqia',
            'القاهرة': 'Cairo',
            'الجيزة': 'Giza',
            'الإسكندرية': 'Alexandria',
            'المنصورة': 'Dakahlia',
            'طنطا': 'Gharbia',
            'المنيا': 'Minya',
            'أسيوط': 'Assiut',
            'سوهاج': 'Sohag',
            'قنا': 'Qena',
            'الأقصر': 'Luxor',
            'أسوان': 'Aswan',
            'بورسعيد': 'Port Said',
            'الإسماعيلية': 'Ismailia',
            'السويس': 'Suez',
            'شرم الشيخ': 'South Sinai',
            'العريش': 'North Sinai'
        }
    
    def _load_official_areas(self):
        """تحميل قائمة المناطق الرسمية."""
        # TODO: سيتم تحميلها من config أو قاعدة بيانات
        return {
            # مناطق الشرقية
            'حي الزهور': 'Zagazig',
            'الزقازيق': 'Zagazig',
            'أبو كبير': 'Abu Kabir',
            'ههيا': 'Hehya',
            'فاقوس': 'Faqous',
            'الصالحية': 'El Salheya',
            'ديرب نجم': 'Deirb Negm',
            
            # مناطق القاهرة
            'المعادي': 'Maadi',
            'المهندسين': 'Mohandessin',
            'وسط البلد': 'Downtown',
            'مدينة نصر': 'Nasr City',
            'الشيخ زايد': 'Sheikh Zayed',
            '6 أكتوبر': '6th of October',
            
            # مناطق الإسكندرية
            'سموحة': 'Smouha',
            'المنتزة': 'Montaza',
            'اللبان': 'Labban',
            'العصافرة': 'Asafra'
        }
    
    def generate_shipment_row(self, order, merchant_id=None):
        """
        توليد صف Speedaf واحد من طلب.
        
        Args:
            order (Order): كائن الطلب
            merchant_id (str): معرف التاجر (إذا كان الطلب من تاجر محدد)
            
        Returns:
            str: صف Speedaf (22 عمود مفصولة بتبويبات)
        """
        # الحصول على بيانات الراسل
        sender = self._get_sender_data(merchant_id)
        
        # الحصول على بيانات المستلم من الطلب
        receiver = self._extract_receiver_data(order)
        
        # الحصول على بيانات المنتج
        goods = self._extract_goods_data(order)
        
        # توليد الصف
        return self._build_speedaf_row(sender, receiver, goods, order.order_id)
    
    def _get_sender_data(self, merchant_id):
        """الحصول على بيانات الراسل."""
        if merchant_id and merchant_id in self.sender_profiles:
            return self.sender_profiles[merchant_id]
        
        return self.sender_profiles['DEFAULT']
    
    def _extract_receiver_data(self, order):
        """استخراج بيانات المستلم من الطلب."""
        # تنسيق الهاتف
        phone = self._format_phone(order.customer.get('phone', ''))
        
        # استخراج المدينة والمنطقة
        city_input = order.shipping.get('city', 'الزقازيق')
        area_input = order.shipping.get('area', 'حي الزهور')
        
        city = self.official_cities.get(city_input, 'Sharqia')
        area = self.official_areas.get(area_input, 'Zagazig')
        
        # تنسيق العنوان
        address = self._format_address(order.shipping)
        
        return {
            'name': order.customer.get('name', '').strip(),
            'phone': phone,
            'city': city,
            'area': area,
            'address': address
        }
    
    def _extract_goods_data(self, order):
        """استخراج بيانات المنتج."""
        goods_name = 'منتجات تسوق'
        if order.products:
            first_product = order.products[0]
            goods_name = first_product.get('title', 'منتجات تسوق')
            
            # اختصار الاسم إذا كان طويلاً
            if len(goods_name) > 30:
                goods_name = goods_name[:27] + '...'
        
        # تحديد COD
        cod_value = order.total
        
        return {
            'type': 'Normal',
            'name': goods_name,
            'quantity': 1,
            'weight': 1,
            'cod': cod_value,
            'allow_open': 'No',
            'delivery_type': 'Deliver'
        }
    
    def _format_phone(self, phone):
        """تنسيق الهاتف إلى 11 رقم."""
        # إزالة المسافات والرموز
        digits = ''.join(filter(str.isdigit, str(phone)))
        
        if len(digits) == 10 and digits.startswith('1'):
            return '0' + digits
        elif len(digits) == 11:
            return digits
        elif len(digits) == 12 and digits.startswith('20'):
            return '0' + digits[2:]
        
        return '0' * 11  # قيمة افتراضية
    
    def _format_address(self, shipping_info):
        """تنسيق العنوان."""
        parts = []
        
        if shipping_info.get('address'):
            parts.append(shipping_info['address'])
        
        if shipping_info.get('building'):
            parts.append(f"مبنى {shipping_info['building']}")
        
        if shipping_info.get('floor'):
            parts.append(f"دور {shipping_info['floor']}")
        
        if shipping_info.get('apartment'):
            parts.append(f"شقة {shipping_info['apartment']}")
        
        if shipping_info.get('landmark'):
            parts.append(f"بجوار {shipping_info['landmark']}")
        
        return '، '.join(parts) if parts else 'عنوان غير محدد'
    
    def _build_speedaf_row(self, sender, receiver, goods, order_id):
        """بناء صف Speedaf بتنسيق الـ 22 عمود."""
        fields = [
            '',  # 1. S.O.
            goods['type'],  # 2. Goods type
            goods['name'],  # 3. Goods name
            str(goods['quantity']),  # 4. Quantity
            str(goods['weight']),  # 5. Weight
            str(goods['cod']),  # 6. COD
            '',  # 7. Insure price
            goods['allow_open'],  # 8. Allow open
            '',  # 9. Remark
            sender['name'],  # 10. Sender Name
            sender['phone'],  # 11. Sender Telephone
            sender['city'],  # 12. Sender City
            sender['area'],  # 13. Sender Area
            sender['address'],  # 14. Sender Address
            '',  # 15. Sender Email
            receiver['name'],  # 16. Receiver Name
            receiver['phone'],  # 17. Receiver Telephone
            receiver['city'],  # 18. Receiver City
            receiver['area'],  # 19. Receiver Area
            receiver['address'],  # 20. Receiver Address
            '',  # 21. Receiver Email
            goods['delivery_type']  # 22. Delivery Type
        ]
        
        return '\t'.join(fields)
    
    def generate_csv_content(self, orders, merchant_id=None):
        """
        توليد محتوى CSV كامل لعدة طلبات.
        
        Args:
            orders (list): قائمة كائنات Order
            merchant_id (str): معرف التاجر
            
        Returns:
            str: محتوى CSV كامل (بدون عناوين أعمدة)
        """
        rows = []
        for order in orders:
            row = self.generate_shipment_row(order, merchant_id)
            rows.append(row)
        
        return '\n'.join(rows)
    
    def get_headers(self):
        """الحصول على عناوين الأعمدة (للعرض فقط، لا تضاف للملف)."""
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
