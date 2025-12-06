# ملف models/product.py
# تعريف نموذج المنتج

class Product:
    """نموذج يمثل منتجاً في النظام."""
    
    def __init__(self, data=None):
        """
        تهيئة منتج جديد.
        
        Args:
            data (dict): بيانات المنتج من Facebook Catalog أو مصدر آخر
        """
        # البيانات الأساسية
        self.id = data.get('id') or ''  # معرف المنتج الفريد
        self.retailer_id = data.get('retailer_id') or ''  # معرف التاجر للمنتج
        self.title = data.get('title') or data.get('name') or 'منتج بدون اسم'
        self.description = data.get('description') or ''
        
        # السعر والعملة
        self.price = float(data.get('price', 0))
        self.currency = data.get('currency', 'EGP')
        self.original_price = float(data.get('original_price', self.price))
        
        # معلومات التاجر
        self.merchant_id = data.get('merchant_id') or ''
        self.merchant_name = data.get('merchant_name') or ''
        self.catalog_id = data.get('catalog_id') or ''  # معرف الكتالوج الأصلي
        
        # الصور والمتعلقات
        self.image_url = data.get('image') or data.get('image_url') or ''
        self.images = data.get('images') or []
        
        # الحالة والمخزون
        self.availability = data.get('availability', 'in stock')
        self.status = data.get('status', 'active')
        self.stock_quantity = int(data.get('stock_quantity', 0))
        
        # معلومات إضافية للتجار المعقدين (مثل Unilever)
        self.wholesale_price = float(data.get('wholesale_price', 0))  # سعر الجملة
        self.pack_size = int(data.get('pack_size', 1))  # حجم الكرتونة (مثلاً 24)
        self.min_order_qty = int(data.get('min_order_qty', 1))  # أقل كمية للطلب
        
        # بيانات أولية من المصدر
        self.raw_data = data or {}
        
        # معلومات التتبع الداخلية
        self.created_at = data.get('created_at') or ''
        self.updated_at = data.get('updated_at') or ''
    
    def to_dict(self):
        """تحويل المنتج إلى قاموس (للتخزين أو إرساله كـ JSON)."""
        return {
            'id': self.id,
            'retailer_id': self.retailer_id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'currency': self.currency,
            'original_price': self.original_price,
            'merchant_id': self.merchant_id,
            'merchant_name': self.merchant_name,
            'catalog_id': self.catalog_id,
            'image_url': self.image_url,
            'images': self.images,
            'availability': self.availability,
            'status': self.status,
            'stock_quantity': self.stock_quantity,
            'wholesale_price': self.wholesale_price,
            'pack_size': self.pack_size,
            'min_order_qty': self.min_order_qty,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def calculate_commission(self, merchant_type, quantity=1):
        """
        حساب العمولة على هذا المنتج (سيتم تفصيله أكثر في services/commission_calculator.py)
        
        Args:
            merchant_type (str): نوع التاجر ('fixed', 'percentage', 'complex')
            quantity (int): الكمية المطلوبة
            
        Returns:
            float: قيمة العمولة
        """
        # هذه دالة أساسية، التفاصيل في commission_calculator.py
        if merchant_type == 'fixed':
            return 5 * quantity  # مثال: 5 جنيه لكل قطعة
        elif merchant_type == 'percentage':
            return self.price * 0.15 * quantity  # مثال: 15%
        else:
            return 0
    
    def is_available(self):
        """التحقق من توفر المنتج للطلب."""
        return self.availability.lower() in ['in stock', 'available'] and self.status == 'active'
    
    def get_display_price(self):
        """الحصول على السعر مع العملة للعرض."""
        return f"{self.price:.2f} {self.currency}"# نموذج المنتج
