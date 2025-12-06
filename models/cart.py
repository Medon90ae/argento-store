# نموذج عربة التسوق
# ملف models/cart.py
# عربة التسوق التي تدعم منتجات من كتالوجات متعددة

class ShoppingCart:
    """عربة تسوق تدعم منتجات من تجار مختلفين."""
    
    def __init__(self, cart_id=None):
        """
        تهيئة عربة تسوق.
        
        Args:
            cart_id (str): معرف العربة (للجلسة أو المستخدم)
        """
        self.cart_id = cart_id or f"CART-{str(uuid.uuid4())[:8]}"
        self.items = []  # قائمة العناصر
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        
        # إحصائيات
        self.item_count = 0
        self.total_price = 0.0
        self.merchants = set()  # مجموعة التجار في العربة
    
    def add_item(self, product, quantity=1, merchant_id=None):
        """
        إضافة منتج إلى العربة.
        
        Args:
            product (dict/Product): بيانات المنتج
            quantity (int): الكمية
            merchant_id (str): معرف التاجر
            
        Returns:
            bool: True إذا تمت الإضافة بنجاح
        """
        # تحويل إلى قاموس إذا كان كائن Product
        if hasattr(product, 'to_dict'):
            product_data = product.to_dict()
        else:
            product_data = product
        
        product_id = product_data.get('id') or product_data.get('retailer_id')
        
        # التحقق من وجود المنتج مسبقاً
        for item in self.items:
            if item.get('product_id') == product_id and item.get('merchant_id') == merchant_id:
                # زيادة الكمية إذا كان نفس المنتج والتاجر
                item['quantity'] += quantity
                item['total'] = item['price'] * item['quantity']
                self._update_totals()
                return True
        
        # إضافة منتج جديد
        new_item = {
            'cart_item_id': f"CART-ITEM-{len(self.items)+1:03d}",
            'product_id': product_id,
            'retailer_id': product_data.get('retailer_id'),
            'title': product_data.get('title', 'منتج بدون اسم'),
            'price': float(product_data.get('price', 0)),
            'quantity': quantity,
            'total': float(product_data.get('price', 0)) * quantity,
            'image': product_data.get('image_url') or product_data.get('image', ''),
            'merchant_id': merchant_id or product_data.get('merchant_id', ''),
            'merchant_name': product_data.get('merchant_name', ''),
            'added_at': datetime.now().isoformat()
        }
        
        self.items.append(new_item)
        self._update_totals()
        return True
    
    def remove_item(self, cart_item_id):
        """
        إزالة عنصر من العربة.
        
        Args:
            cart_item_id (str): معرف عنصر العربة
            
        Returns:
            bool: True إذا تمت الإزالة
        """
        for i, item in enumerate(self.items):
            if item.get('cart_item_id') == cart_item_id:
                self.items.pop(i)
                self._update_totals()
                return True
        return False
    
    def update_quantity(self, cart_item_id, new_quantity):
        """
        تحديث كمية عنصر.
        
        Args:
            cart_item_id (str): معرف العنصر
            new_quantity (int): الكمية الجديدة
            
        Returns:
            bool: True إذا تم التحديث
        """
        for item in self.items:
            if item.get('cart_item_id') == cart_item_id:
                if new_quantity <= 0:
                    return self.remove_item(cart_item_id)
                
                item['quantity'] = new_quantity
                item['total'] = item['price'] * new_quantity
                self._update_totals()
                return True
        return False
    
    def clear(self):
        """تفريغ العربة بالكامل."""
        self.items = []
        self._update_totals()
    
    def _update_totals(self):
        """تحديث الإجماليات."""
        self.item_count = sum(item['quantity'] for item in self.items)
        self.total_price = sum(item['total'] for item in self.items)
        
        # تحديث مجموعة التجار
        self.merchants = set(item['merchant_id'] for item in self.items if item.get('merchant_id'))
        
        self.updated_at = datetime.now().isoformat()
    
    def get_items_by_merchant(self):
        """
        تجميع العناصر حسب التاجر.
        
        Returns:
            dict: عناصر مجمعة حسب معرف التاجر
        """
        merchant_items = {}
        
        for item in self.items:
            merchant_id = item.get('merchant_id', 'unknown')
            
            if merchant_id not in merchant_items:
                merchant_items[merchant_id] = {
                    'merchant_name': item.get('merchant_name', ''),
                    'items': [],
                    'subtotal': 0
                }
            
            merchant_items[merchant_id]['items'].append(item)
            merchant_items[merchant_id]['subtotal'] += item['total']
        
        return merchant_items
    
    def get_suggestions_for_free_shipping(self, free_shipping_threshold=100):
        """
        اقتراح منتجات للوصول للشحن المجاني.
        
        Args:
            free_shipping_threshold (float): حد الشحن المجاني
            
        Returns:
            dict: معلومات الاقتراحات
        """
        current_total = self.total_price
        remaining = max(0, free_shipping_threshold - current_total)
        
        return {
            'current_total': current_total,
            'free_shipping_threshold': free_shipping_threshold,
            'remaining': remaining,
            'needs_more': remaining > 0,
            'message': f"أنت تحتاج {remaining:.2f} ج أخرى للوصول للشحن المجاني!" if remaining > 0 else "🎉 مؤهل للشحن المجاني!"
        }
    
    def calculate_potential_commission(self, merchants_config):
        """
        حساب العمولة المحتملة للطلبات في العربة.
        
        Args:
            merchants_config (dict): إعدادات التجار من config
            
        Returns:
            dict: تفاصيل العمولات
        """
        commissions_by_merchant = {}
        total_commission = 0
        
        for item in self.items:
            merchant_id = item.get('merchant_id')
            if not merchant_id:
                continue
            
            # الحصول على إعدادات التاجر
            merchant_config = merchants_config.get(merchant_id, {})
            commission_type = merchant_config.get('commission_type', '')
            
            # حساب العمولة (نموذج مبسط، التفاصيل في commission_calculator.py)
            item_commission = 0
            
            if commission_type == 'fixed_per_item':
                commission_value = merchant_config.get('commission_value', 0)
                item_commission = commission_value * item['quantity']
            elif commission_type == 'percentage':
                commission_rate = merchant_config.get('commission_value', 0)
                item_commission = item['total'] * commission_rate
            
            # التجميع
            if merchant_id not in commissions_by_merchant:
                commissions_by_merchant[merchant_id] = {
                    'merchant_name': item.get('merchant_name', ''),
                    'items_count': 0,
                    'subtotal': 0,
                    'commission': 0
                }
            
            commissions_by_merchant[merchant_id]['items_count'] += item['quantity']
            commissions_by_merchant[merchant_id]['subtotal'] += item['total']
            commissions_by_merchant[merchant_id]['commission'] += item_commission
            
            total_commission += item_commission
        
        return {
            'by_merchant': commissions_by_merchant,
            'total_commission': total_commission,
            'estimated_profit': total_commission  # قبل خصم الشحن
        }
    
    def to_order_data(self, customer_info=None, shipping_info=None):
        """
        تحويل العربة إلى بيانات طلب.
        
        Args:
            customer_info (dict): معلومات العميل
            shipping_info (dict): معلومات الشحن
            
        Returns:
            dict: بيانات الطلب الجاهزة
        """
        order_data = {
            'products': self.items.copy(),
            'subtotal': self.total_price,
            'item_count': self.item_count,
            'merchants_count': len(self.merchants),
            'cart_id': self.cart_id
        }
        
        if customer_info:
            order_data.update({
                'customer_name': customer_info.get('name', ''),
                'customer_phone': customer_info.get('phone', ''),
                'customer_whatsapp': customer_info.get('whatsapp', ''),
                'customer_email': customer_info.get('email', ''),
                'customer_notes': customer_info.get('notes', '')
            })
        
        if shipping_info:
            order_data.update({
                'shipping_address': shipping_info.get('address', ''),
                'shipping_city': shipping_info.get('city', ''),
                'shipping_area': shipping_info.get('area', ''),
                'shipping_building': shipping_info.get('building', ''),
                'shipping_floor': shipping_info.get('floor', ''),
                'shipping_apartment': shipping_info.get('apartment', ''),
                'shipping_landmark': shipping_info.get('landmark', ''),
                'shipping_notes': shipping_info.get('notes', '')
            })
        
        return order_data
    
    def to_dict(self, include_items=True):
        """
        تحويل العربة إلى قاموس.
        
        Args:
            include_items (bool): تضمين قائمة العناصر
            
        Returns:
            dict: بيانات العربة
        """
        cart_dict = {
            'cart_id': self.cart_id,
            'item_count': self.item_count,
            'total_price': self.total_price,
            'merchants_count': len(self.merchants),
            'merchants': list(self.merchants),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if include_items:
            cart_dict['items'] = self.items
            cart_dict['by_merchant'] = self.get_items_by_merchant()
        
        return cart_dict
    
    def __str__(self):
        """تمثيل نصي للعربة."""
        return f"عربة التسوق {self.cart_id}: {self.item_count} منتج، {self.total_price:.2f} ج"
