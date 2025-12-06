# ملف models/merchant.py المعدل
# تعريف نموذج التاجر مع أنظمة العمولات المختلفة والمرتجعات

class Merchant:
    """نموذج يمثل تاجراً في النظام مع نظام عمولاته الخاص."""
    
    # ثوابت أنواع العمولات
    COMMISSION_FIXED_VARIABLE = 'fixed_variable'      # مبلغ ثابت يختلف حسب المنتج (يدخل يدوي)
    COMMISSION_PERCENTAGE_VARIABLE = 'percentage_variable'  # نسبة تختلف حسب المنتج (يدخل يدوي)
    COMMISSION_PERCENTAGE_FIXED = 'percentage_fixed'  # نسبة ثابتة (كاستيل فارما)
    COMMISSION_COMPLEX_EXTERNAL = 'complex_external'  # نظام معقد من ملف خارجي (يونيليفر)
    
    def __init__(self, merchant_id, data=None):
        """
        تهيئة تاجر جديد.
        
        Args:
            merchant_id (str): المعرف الفريد للتاجر (مطابق للسيكرتس)
            data (dict): بيانات إضافية للتاجر
        """
        self.id = merchant_id
        self.data = data or {}
        
        # تعيين البيانات الأساسية حسب التاجر
        self._setup_merchant_info(merchant_id)
        
        # سياسة المرتجعات
        self.return_policy = self.data.get('return_policy', {})
    
    def _setup_merchant_info(self, merchant_id):
        """تعيين المعلومات الأساسية لكل تاجر بناءً على معرفه."""
        
        # قاعدة بيانات التجار الثابتة - مرتبطة بالسيكرتس التي ذكرتها
        MERCHANTS_DB = {
            # كاستيل فارما - نسبتين عمولة (5% على العرض + 5% على السعر)
            'CASTELPHARMA': {
                'name': 'كاستيل فارما',
                'catalog_id_env': 'CASTELPHARMA',
                'address': 'الزقازيق الشرقية، حي الزهور',
                'phone': '+20 10 64147284',
                'contact_name': 'شركة كاستيل فارما',
                'commission_type': self.COMMISSION_PERCENTAGE_FIXED,
                'commission_structure': {
                    'offer_commission': 0.05,      # 5% على العروض المقدمة من كاستيل
                    'product_commission': 0.05,    # 5% على سعر المنتج
                    'speedaf_discount': True,      # خصم سبيداف مخصوم منه سعر الشحن
                    'variable_range': (0.15, 0.30) # 15% إلى 30% للمنتجات الأخرى (يدوي)
                },
                'return_policy': {
                    'responsible': 'merchant',     # المرتجعات على التاجر
                    'shipping_refund': 0.50,       # 50% من مصاريف الشحن
                    'notes': 'المرتجعات على التاجر، استرداد 50% من مصاريف الشحن'
                },
                'notes': '5% على العروض + 5% على السعر + خصم سبيداف. المرتجعات على التاجر'
            },
            
            # Azúcar - عمولة ثابتة تختلف حسب المنتج (يدخل يدوي)
            'SUDIID': {
                'name': 'Azúcar',
                'catalog_id_env': 'SUDIID',
                'address': 'الزقازيق الشرقية، حي الزهور',
                'phone': '+20 10 17549330',
                'contact_name': 'Azúcar',
                'commission_type': self.COMMISSION_FIXED_VARIABLE,
                'commission_structure': {
                    'default_commission': 10,      # 10 جنيه افتراضي
                    'per_product_manual': True,    # يدخل لكل منتج يدويًا
                    'min_commission': 5,
                    'max_commission': 50
                },
                'return_policy': {
                    'responsible': 'merchant',     # المرتجعات على التاجر
                    'shipping_refund': 0.50,       # 50% من مصاريف الشحن
                    'notes': 'المرتجعات على التاجر، استرداد 50% من مصاريف الشحن'
                },
                'notes': 'عمولة ثابتة تختلف حسب المنتج (تدخل يدويًا). المرتجعات على التاجر'
            },
            
            # Unilever - نظام معقد من ملف PDF خارجي
            'UNILEVERID': {
                'name': 'يونيليفر',
                'catalog_id_env': 'UNILEVERID',
                'address': 'الزقازيق الشرقية، حي الزهور',
                'phone': '01055688136',
                'contact_name': 'يونيليفر',
                'commission_type': self.COMMISSION_COMPLEX_EXTERNAL,
                'commission_structure': {
                    'source': 'pdf_file',          # المصدر: ملف PDF
                    'contains': [
                        'prices',
                        'my_discount',
                        'customer_discount',
                        'retail_prices',
                        'return_policy_me'         # المرتجعات على حسابي
                    ],
                    'file_required': True
                },
                'return_policy': {
                    'responsible': 'me',           # المرتجعات على حسابي
                    'shipping_refund': 0.50,       # 50% من مصاريف الشحن
                    'notes': 'المرتجعات على حسابي، استرداد 50% من مصاريف الشحن'
                },
                'notes': 'نظام معقد من ملف PDF. المرتجعات على حسابي'
            },
            
            # Fofo - عمولة ثابتة تختلف حسب المنتج (يدخل يدوي)
            'FOFO': {
                'name': 'Fofo',
                'catalog_id_env': 'FOFO',
                'address': 'الزقازيق الشرقية، حي الزهور',
                'phone': '+20 12 12137256',
                'contact_name': 'Fofo',
                'commission_type': self.COMMISSION_FIXED_VARIABLE,
                'commission_structure': {
                    'default_commission': 5,       # 5 جنيه افتراضي
                    'per_product_manual': True,    # يدخل لكل منتج يدويًا
                    'min_commission': 3,
                    'max_commission': 20
                },
                'return_policy': {
                    'responsible': 'merchant',     # المرتجعات على التاجر
                    'shipping_refund': 0.50,       # 50% من مصاريف الشحن
                    'notes': 'المرتجعات على التاجر، استرداد 50% من مصاريف الشحن'
                },
                'notes': 'عمولة ثابتة تختلف حسب المنتج (تدخل يدويًا). المرتجعات على التاجر'
            },
            
            # Bussnis - الخاص بك
            'BUSSNISID': {
                'name': 'متجر Argento',
                'catalog_id_env': 'BUSSNISID',
                'address': 'الزقازيق الشرقية، حي الزهور',
                'phone': '01055688136',
                'contact_name': 'مدير المتجر',
                'commission_type': 'none',
                'commission_structure': {},
                'return_policy': {
                    'responsible': 'me',
                    'shipping_refund': 1.00,       # 100% من مصاريف الشحن
                    'notes': 'منتجات المتجر الرئيسي'
                },
                'notes': 'الكتالوج الرئيسي للمتجر'
            }
        }
        
        # إذا كان التاجر معروفاً في قاعدة البيانات
        if merchant_id in MERCHANTS_DB:
            merchant_info = MERCHANTS_DB[merchant_id]
            for key, value in merchant_info.items():
                setattr(self, key, value)
        else:
            # إذا كان تاجراً جديداً غير معرف
            self.name = self.data.get('name', 'تاجر جديد')
            self.catalog_id_env = merchant_id
            self.address = self.data.get('address', '')
            self.phone = self.data.get('phone', '')
            self.contact_name = self.data.get('contact_name', '')
            self.commission_type = self.data.get('commission_type', 'unknown')
            self.commission_structure = self.data.get('commission_structure', {})
            self.return_policy = self.data.get('return_policy', {})
            self.notes = self.data.get('notes', '')
    
    def get_catalog_id(self):
        """الحصول على معرف الكتالوج الفعلي."""
        return self.catalog_id_env
    
    def calculate_commission(self, product_data, order_data=None):
        """
        حساب العمولة بناءً على نوع التاجر والبيانات.
        
        Args:
            product_data (dict): بيانات المنتج (يجب أن يحتوي على commission_value إذا كان يدوي)
            order_data (dict): بيانات الطلب (للشحن والعروض)
            
        Returns:
            dict: تفاصيل العمولة والمرتجعات
        """
        product_price = float(product_data.get('price', 0))
        quantity = int(product_data.get('quantity', 1))
        manual_commission = product_data.get('commission_value')  # القيمة اليدوية
        
        result = {
            'product_id': product_data.get('id'),
            'product_name': product_data.get('title'),
            'quantity': quantity,
            'unit_price': product_price,
            'total_price': product_price * quantity,
            'commission_type': self.commission_type,
            'merchant_id': self.id,
            'merchant_name': self.name
        }
        
        # حساب العمولة حسب نوع التاجر
        if self.commission_type == self.COMMISSION_FIXED_VARIABLE:
            # عمولة ثابتة تختلف حسب المنتج (يدخل يدوي)
            if manual_commission is not None:
                commission = float(manual_commission) * quantity
                result.update({
                    'commission': commission,
                    'commission_per_unit': float(manual_commission),
                    'details': f'عمولة يدوية: {manual_commission} ج × {quantity} قطعة',
                    'calculation': 'manual_per_product'
                })
            else:
                # استخدام القيمة الافتراضية
                default_commission = self.commission_structure.get('default_commission', 0)
                commission = default_commission * quantity
                result.update({
                    'commission': commission,
                    'commission_per_unit': default_commission,
                    'details': f'عمولة افتراضية: {default_commission} ج × {quantity} قطعة',
                    'calculation': 'default'
                })
        
        elif self.commission_type == self.COMMISSION_PERCENTAGE_FIXED and self.id == 'CASTELPHARMA':
            # كاستيل فارما: 5% على العروض + 5% على السعر
            base_commission = product_price * 0.05 * quantity
            
            # حساب عمولة العروض إذا كان هناك عرض
            offer_commission = 0
            if order_data and 'has_castel_offer' in order_data:
                offer_total = order_data.get('castel_offer_total', 0)
                offer_commission = offer_total * 0.05
            
            total_commission = base_commission + offer_commission
            
            result.update({
                'commission': total_commission,
                'base_commission': base_commission,
                'offer_commission': offer_commission,
                'details': (
                    f'كاستيل فارما (5% على السعر + 5% على العروض):\n'
                    f'• 5% من سعر المنتج: {base_commission:.2f} ج\n'
                    f'• 5% من العروض: {offer_commission:.2f} ج'
                ),
                'calculation': 'castel_dual_percentage'
            })
        
        elif self.commission_type == self.COMMISSION_PERCENTAGE_VARIABLE:
            # نسبة تختلف حسب المنتج (يدخل يدوي)
            if manual_commission is not None:
                commission_rate = float(manual_commission) / 100.0
                commission = product_price * commission_rate * quantity
                result.update({
                    'commission': commission,
                    'commission_rate': commission_rate,
                    'details': f'نسبة يدوية: {manual_commission}% من {product_price * quantity:.2f} ج',
                    'calculation': 'manual_percentage'
                })
            else:
                # استخدام النطاق المتاح
                min_rate, max_rate = self.commission_structure.get('variable_range', (0.15, 0.30))
                avg_rate = (min_rate + max_rate) / 2
                commission = product_price * avg_rate * quantity
                result.update({
                    'commission': commission,
                    'commission_rate': avg_rate,
                    'details': f'نسبة متوسطة: {avg_rate*100:.1f}% من {product_price * quantity:.2f} ج',
                    'calculation': 'average_range'
                })
        
        elif self.commission_type == self.COMMISSION_COMPLEX_EXTERNAL and self.id == 'UNILEVERID':
            # يونيليفر: نظام معقد من ملف PDF
            result.update({
                'commission': 0,  # سيتم حسابها يدويًا من الملف
                'details': 'يتم حساب العمولة يدويًا من ملف PDF (أسعار، خصومات، مرتجعات)',
                'calculation': 'external_pdf',
                'requires_manual_calculation': True,
                'pdf_instructions': 'ارجع إلى ملف PDF للأسعار والخصومات'
            })
        
        else:
            # نظام افتراضي
            result.update({
                'commission': 0,
                'details': 'لا توجد عمولة محددة',
                'calculation': 'none'
            })
        
        # إضافة سياسة المرتجعات
        result['return_policy'] = {
            'responsible': self.return_policy.get('responsible', 'unknown'),
            'shipping_refund_rate': self.return_policy.get('shipping_refund', 0.50),
            'notes': self.return_policy.get('notes', '')
        }
        
        # حساب استرداد الشحن في حالة المرتجعات
        shipping_cost = order_data.get('shipping_cost', 0) if order_data else 0
        result['return_policy']['shipping_refund_amount'] = (
            shipping_cost * result['return_policy']['shipping_refund_rate']
        )
        
        return result
    
    def needs_manual_commission_entry(self):
        """هل يحتاج التاجر لإدخال عمولة يدوية لكل منتج؟"""
        if self.commission_type in [self.COMMISSION_FIXED_VARIABLE, self.COMMISSION_PERCENTAGE_VARIABLE]:
            return self.commission_structure.get('per_product_manual', False)
        return False
    
    def can_order_partial(self):
        """هل يسمح التاجر بالطلبات الجزئية؟"""
        if self.commission_type == self.COMMISSION_COMPLEX_EXTERNAL and self.id == 'UNILEVERID':
            return False  # يونيليفر يحتاج كرتونة كاملة
        return True
    
    def get_min_order_quantity(self):
        """الحصول على أقل كمية للطلب."""
        if self.commission_type == self.COMMISSION_COMPLEX_EXTERNAL and self.id == 'UNILEVERID':
            return 24  # كرتونة يونيليفر
        return 1
    
    def to_dict(self):
        """تحويل بيانات التاجر إلى قاموس."""
        return {
            'id': self.id,
            'name': self.name,
            'catalog_id_env': self.catalog_id_env,
            'address': self.address,
            'phone': self.phone,
            'contact_name': self.contact_name,
            'commission_type': self.commission_type,
            'commission_structure': self.commission_structure,
            'return_policy': self.return_policy,
            'notes': self.notes,
            'needs_manual_entry': self.needs_manual_commission_entry(),
            'can_order_partial': self.can_order_partial(),
            'min_order_quantity': self.get_min_order_quantity()
        }
    
    def __str__(self):
        """تمثيل نصي للتاجر."""
        return f"{self.name} ({self.id}) - {self.commission_type}"# نموذج التاجر
