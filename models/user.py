# ملف models/user.py
# نموذج المستخدم/العميل (للمراحل المتقدمة)

class User:
    """نموذج مستخدم/عميل للنظام."""
    
    def __init__(self, user_data=None):
        self.user_id = user_data.get('user_id', '')
        self.name = user_data.get('name', '')
        self.phone = user_data.get('phone', '')
        self.whatsapp = user_data.get('whatsapp', '')
        self.email = user_data.get('email', '')
        self.address = user_data.get('address', {})
        self.preferences = user_data.get('preferences', {})
        self.order_history = user_data.get('order_history', [])
        self.created_at = user_data.get('created_at', '')
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'phone': self.phone,
            'whatsapp': self.whatsapp,
            'email': self.email,
            'address': self.address,
            'preferences': self.preferences,
            'order_count': len(self.order_history),
            'created_at': self.created_at
        }
