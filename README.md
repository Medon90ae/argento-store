# Argento Store

مشروع ويب متجر بسيط بـ Python + Flask يحتوي على صفحات هبوط للمنتجات ولوحة إدارة بسيطة.

## الميزات

- عرض منتجات من كتالوجات Facebook
- صفحات هبوط مخصصة لكل منتج
- معالجة طلبات العملاء مع حفظ في Excel والـ JSON
- تحويل المدن والمناطق باستخدام `addresses.xlsx`
- لوحة إدارة admins للمنتجات والطلبات
- GitHub Actions لتحديث الروابط
- نشر على Railway

## التشغيل المحلي

1. استنسخ المشروع:
   ```bash
   git clone https://github.com/Medon90ae/argento-store.git
   cd argento-store
   ```

2. قم بتثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```

3. أضف المتغيرات البيئية في ملف `.env` (أو env vars):
   ```
   FBACCSESSTOKEN=your_facebook_access_token
   ADMIN_TOKEN=your_admin_token
   ```

4. شغل التطبيق:
   ```bash
   python app.py
   ```

5. افتح المتصفح على `http://localhost:5000`

## الـ APIs

- `GET /` - عرض المنتجات
- `GET /api/products` - JSON المنتجات
- `GET /landing/<slug>` - صفحة هبوط المنتج
- `POST /api/landing_order` - إرسال طلب
- `GET /admin?token=<ADMIN_TOKEN>` - لوحة الإدارة
- `POST /api/update_catalog` - تحديث المنتجات من Facebook (Admin فقط)
- `POST /api/archive_orders` - أرشفة وإعادة ضبط الطلبات (Admin فقط)

## اختبار الـ APIs

### الحصول على المنتجات:
```bash
curl http://localhost:5000/api/products
```

### إرسال طلب:
```bash
curl -X POST http://localhost:5000/api/landing_order \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "123",
    "quantity": 2,
    "customer": {
      "name": "أحمد",
      "phone": "01234567890",
      "city": "الزقازيق",
      "area": "حي الزهور",
      "address": "شارع الجامعة"
    }
  }'
```

## الأرشفة

- تستخدم `archive_and_reset_orders()` لنسخ `addresses.xlsx` إلى `data/archives/` مع طابع زمني، وإعادة ضبط الورقة "0".
- يمكن تشغيلها من لوحة الإدارة أو workflow آخر.

## النشر على Railway

1. اربط المشروع إلى GitHub على Railway.
2. أضف env vars في Settings:
   - `FBACCSESSTOKEN`
   - `ADMIN_TOKEN`
3. اضغط Deploy.

## ملاحظات مهمة

- لا تستخدم بيانات وهمية - فقط بيانات حقيقية من Facebook catalogs.
- إذا لم يكن الكتالوج يحتوي منتجات، يتم تخطيه.
- زر "تحديث المنتجات" لإضافة الجديدة دون تكرار.
- تحويل المدن/المناطق يتم آلياً باستخدام القاموس في `addresses.xlsx`.
- الأمان: استخدم Admin Token لحماية endpoints.

---

**إذ كان هناك مشاكل، تحقق من logs في app.py وaddresses.xlsx وجودها.**
