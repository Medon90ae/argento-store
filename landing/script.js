// landing/script.js
// الجوهر: جلب المنتج + حساب الشحن + إرسال الطلب

// إعدادات API الأساسية
const API_BASE_URL = 'https://speedafargento.com'; // سيتم تغييره لرابط Railway الفعلي
let currentProduct = null;
let currentShippingCost = 0;

// خريطة مصاريف الشحن حسب المدينة (افتراضية - ستأتي من config.py)
const SHIPPING_RATES = {
    'Sharqia': 75,
    'Cairo': 65,
    'Giza': 65,
    'Alexandria': 75,
    'Dakahlia': 75,
    'Gharbia': 75,
    'Monufia': 75,
    'Qalyubia': 75,
    'Behira': 75,
    'Ismailia': 85,
    'Port Said': 85,
    'Suez': 85,
    'Damietta': 75,
    'Aswan': 130,
    'Asyut': 95,
    'BeniSuef': 95,
    'Faiyum': 95,
    'Minya': 95,
    'Qena': 130,
    'Red Sea': 130,
    'New Valley': 130,
    'Matrouh': 130,
    'North Sinai': 130,
    'South Sinai': 130,
    'Luxor': 130,
    'Sohag': 95,
    'default': 80
};

// البيانات الأولية للمدن والمناطق (سيتم جلبها من API)
let citiesData = {};
let areasData = {};

// عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // 1. استخراج معرف المنتج من الرابط
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product_id');
    
    if (!productId) {
        showError('خطأ: لم يتم تحديد منتج. الرجاء استخدام رابط صحيح.');
        return;
    }
    
    // 2. جلب بيانات المنتج من API
    loadProductData(productId);
    
    // 3. تحميل قوائم المدن والمناطق
    loadCitiesAndAreas();
    
    // 4. إعداد نموذج الطلب
    setupOrderForm();
    
    // 5. تحديث ملخص الطلب عند تغيير المدينة
    document.getElementById('city').addEventListener('change', updateShippingAndSummary);
    document.getElementById('area').addEventListener('change', updateShippingAndSummary);
});

// ==================== الوظائف الأساسية ====================

// 1. جلب بيانات المنتج من API
async function loadProductData(productId) {
    try {
        showLoading(true);
        
        // جلب بيانات المنتج من API التطبيق المركزي
        const response = await fetch(`${API_BASE_URL}/api/product/${productId}`);
        
        if (!response.ok) {
            throw new Error('المنتج غير موجود أو حدث خطأ في الخادم');
        }
        
        const data = await response.json();
        currentProduct = data.product;
        
        // تحديث واجهة المنتج
        updateProductDisplay();
        
        // حساب الشحن الافتراضي (محافظة الشرقية)
        calculateShipping('Sharqia', 'Zagazig');
        
        // تحديث ملخص الطلب
        updateOrderSummary();
        
        showLoading(false);
        
    } catch (error) {
        showError(`خطأ في تحميل المنتج: ${error.message}`);
        showLoading(false);
    }
}

// 2. تحديث عرض المنتج
function updateProductDisplay() {
    if (!currentProduct) return;
    
    // تحديث العناصر
    document.getElementById('product-title').textContent = currentProduct.title || 'منتج بدون اسم';
    document.getElementById('product-price').textContent = currentProduct.price?.toLocaleString() || '0';
    document.getElementById('product-merchant').textContent = `التاجر: ${currentProduct.merchant_name || 'غير معروف'}`;
    document.getElementById('product-description').textContent = currentProduct.description || 'لا يوجد وصف';
    
    // تحديث الصورة
    const productImage = document.getElementById('product-image');
    if (currentProduct.image_url) {
        productImage.src = currentProduct.image_url;
        productImage.alt = currentProduct.title;
    } else {
        productImage.src = 'https://via.placeholder.com/400x400/2c3e50/ecf0f1?text=Argento+Store';
    }
    
    // تحديث الـ Badge بناءً على التوفر
    const badge = document.getElementById('product-badge');
    if (currentProduct.availability === 'out of stock') {
        badge.textContent = 'غير متوفر';
        badge.style.backgroundColor = '#e74c3c';
        document.getElementById('submit-btn').disabled = true;
        document.getElementById('submit-btn').style.opacity = '0.6';
    } else if (currentProduct.status === 'on_sale') {
        badge.textContent = 'عرض خاص';
        badge.style.backgroundColor = '#f39c12';
    }
}

// 3. تحميل قوائم المدن والمناطق من API
async function loadCitiesAndAreas() {
    try {
        // جلب القوائم من API التطبيق المركزي
        const response = await fetch(`${API_BASE_URL}/api/cities-areas`);
        
        if (response.ok) {
            const data = await response.json();
            citiesData = data.cities || {};
            areasData = data.areas || {};
        } else {
            // إذا فشل API، استخدام البيانات الافتراضية
            useDefaultCitiesAreas();
        }
        
        // تعبئة قائمة المدن
        populateCities();
        
    } catch (error) {
        console.error('Error loading cities/areas:', error);
        useDefaultCitiesAreas();
        populateCities();
    }
}

// 4. استخدام البيانات الافتراضية للمدن والمناطق (من config.py)
function useDefaultCitiesAreas() {
    citiesData = {
        'Sharqia': 'الشرقية',
        'Cairo': 'القاهرة',
        'Giza': 'الجيزة',
        'Alexandria': 'الإسكندرية',
        'Dakahlia': 'الدقهلية',
        'Gharbia': 'الغربية',
        'Monufia': 'المنوفية',
        'Qalyubia': 'القليوبية',
        'Behira': 'البحيرة',
        'Ismailia': 'الإسماعيلية',
        'Port Said': 'بورسعيد',
        'Suez': 'السويس',
        'Damietta': 'دمياط',
        'Aswan': 'أسوان',
        'Asyut': 'أسيوط',
        'BeniSuef': 'بني سويف',
        'Faiyum': 'الفيوم',
        'Minya': 'المنيا',
        'Qena': 'قنا',
        'Red Sea': 'البحر الأحمر',
        'New Valley': 'الوادي الجديد',
        'Matrouh': 'مطروح',
        'North Sinai': 'شمال سيناء',
        'South Sinai': 'جنوب سيناء',
        'Luxor': 'الأقصر',
        'Sohag': 'سوهاج'
    };
    
    areasData = {
        'Sharqia': ['Zagazig', 'Minya El Qamh', 'Mashtol Al Souq', 'Hihya', 'Abu Hammad', 'Bilbeis'],
        'Cairo': ['Downtown', 'Nasr City', 'Maadi', 'Helwan', 'Shorouk', 'Ain Shams', 'El Marg'],
        'Giza': ['Faisal', 'Haram', 'Dokki', 'Mohandisen', 'Imbaba', 'Bolak Al Dakrour'],
        'Alexandria': ['Al-agamy', 'Sidi Gaber', 'El-Raml', 'Montaza', 'Al Mamurah', 'Abu Qir']
    };
}

// 5. تعبئة قائمة المدن
function populateCities() {
    const citySelect = document.getElementById('city');
    citySelect.innerHTML = '<option value="">اختر المحافظة</option>';
    
    // إضافة المدن مع ترجمتها العربية
    Object.entries(citiesData).forEach(([enName, arName]) => {
        const option = document.createElement('option');
        option.value = enName;  // القيمة: الإنجليزية (لـ Speedaf)
        option.textContent = arName;  // النص: العربية (للعرض)
        citySelect.appendChild(option);
    });
}

// 6. تحديث قائمة المناطق عند تغيير المدينة
function updateAreas() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    const selectedCity = citySelect.value;
    
    areaSelect.innerHTML = '<option value="">اختر المنطقة</option>';
    
    if (selectedCity && areasData[selectedCity]) {
        areasData[selectedCity].forEach(area => {
            const option = document.createElement('option');
            option.value = area;  // الإنجليزية
            // محاولة ترجمة المنطقة للعربية إذا كانت متوفرة
            option.textContent = area;  // يمكن إضافة ترجمة هنا لاحقاً
            areaSelect.appendChild(option);
        });
    }
    
    // تحديث الشحن والملخص
    updateShippingAndSummary();
}

// 7. حساب تكلفة الشحن
function calculateShipping(city, area) {
    // احصل على سعر الشحن الأساسي للمدينة
    let baseCost = SHIPPING_RATES[city] || SHIPPING_RATES['default'];
    
    // إضافة رسوم المناولة (5 جنيه)
    currentShippingCost = baseCost + 5;
    
    // عرض تكلفة الشحن
    const shippingElement = document.getElementById('shipping-cost');
    shippingElement.textContent = `${currentShippingCost.toLocaleString()} جنيه`;
    shippingElement.style.fontWeight = 'bold';
    shippingElement.style.color = '#e74c3c';
    
    return currentShippingCost;
}

// 8. تحديث الشحن والملخص
function updateShippingAndSummary() {
    const city = document.getElementById('city').value;
    const area = document.getElementById('area').value;
    
    if (city) {
        calculateShipping(city, area);
        updateOrderSummary();
    }
}

// 9. تحديث ملخص الطلب
function updateOrderSummary() {
    if (!currentProduct) return;
    
    const productPrice = currentProduct.price || 0;
    const total = productPrice + currentShippingCost;
    
    // تحديث العناصر
    document.getElementById('summary-price').textContent = `${productPrice.toLocaleString()} ج`;
    document.getElementById('summary-shipping').textContent = `${currentShippingCost.toLocaleString()} ج`;
    document.getElementById('summary-total').textContent = `${total.toLocaleString()} ج`;
}

// 10. إعداد نموذج الطلب
function setupOrderForm() {
    const orderForm = document.getElementById('order-form');
    
    orderForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        // التحقق من صحة البيانات
        if (!validateForm()) {
            return;
        }
        
        // جمع بيانات الطلب
        const orderData = collectOrderData();
        
        // إرسال الطلب
        await submitOrder(orderData);
    });
}

// 11. التحقق من صحة النموذج
function validateForm() {
    const requiredFields = ['customer-name', 'customer-phone', 'city', 'area', 'address'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '#3498db';
        }
    });
    
    // التحقق من صحة رقم الهاتف
    const phone = document.getElementById('customer-phone').value.trim();
    const phoneRegex = /^01[0-9]{9}$/;
    if (!phoneRegex.test(phone)) {
        showError('يرجى إدخال رقم هاتف صحيح (11 رقم تبدأ بـ 01)');
        return false;
    }
    
    return isValid;
}

// 12. جمع بيانات الطلب
function collectOrderData() {
    const productPrice = currentProduct.price || 0;
    const totalAmount = productPrice + currentShippingCost;
    
    return {
        // بيانات المنتج
        product_id: currentProduct.id,
        product_retailer_id: currentProduct.retailer_id,
        product_title: currentProduct.title,
        product_price: productPrice,
        product_image: currentProduct.image_url,
        merchant_id: currentProduct.merchant_id,
        merchant_name: currentProduct.merchant_name,
        
        // بيانات العميل
        customer_name: document.getElementById('customer-name').value.trim(),
        customer_phone: document.getElementById('customer-phone').value.trim(),
        customer_whatsapp: document.getElementById('customer-whatsapp').value.trim() || 
                          document.getElementById('customer-phone').value.trim(),
        
        // بيانات العنوان
        shipping_city: document.getElementById('city').value,
        shipping_area: document.getElementById('area').value,
        shipping_address: document.getElementById('address').value.trim(),
        shipping_building: document.getElementById('building').value.trim(),
        shipping_apartment: document.getElementById('apartment').value.trim(),
        shipping_landmark: document.getElementById('landmark').value.trim(),
        
        // الحسابات المالية
        subtotal: productPrice,
        shipping_cost: currentShippingCost,
        total_amount: totalAmount,
        payment_method: 'cash_on_delivery',
        
        // معلومات إضافية
        source: 'landing_page',
        page_url: window.location.href,
        timestamp: new Date().toISOString()
    };
}

// 13. إرسال الطلب إلى API
async function submitOrder(orderData) {
    try {
        showLoading(true, 'جاري إرسال طلبك...');
        
        const response = await fetch(`${API_BASE_URL}/api/order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            // نجاح: عرض نافذة التأكيد
            showSuccessModal(result.order_id);
            
            // إرسال إشعار واتساب (اختياري)
            sendWhatsAppNotification(orderData, result.order_id);
            
            // إعادة تعيين النموذج (اختياري)
            // document.getElementById('order-form').reset();
            
        } else {
            throw new Error(result.message || 'حدث خطأ في الخادم');
        }
        
    } catch (error) {
        showError(`خطأ في إرسال الطلب: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// 14. إرسال إشعار واتساب (وظيفة مساعدة)
function sendWhatsAppNotification(orderData, orderId) {
    // بناء رسالة الواتساب
    const message = `🎉 طلب جديد #${orderId}
    
👤 العميل: ${orderData.customer_name}
📞 الهاتف: ${orderData.customer_phone}
📍 العنوان: ${orderData.shipping_city} - ${orderData.shipping_area}
${orderData.shipping_address}
    
🛒 المنتج: ${orderData.product_title}
💰 السعر: ${orderData.product_price} ج
🚚 الشحن: ${orderData.shipping_cost} ج
💰 الإجمالي: ${orderData.total_amount} ج
    
📝 الرابط: ${orderData.page_url}`;
    
    // ترميز الرسالة لرابط واتساب
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/201055688136?text=${encodedMessage}`;
    
    // يمكن فتح الرابط في نافذة جديدة (اختياري)
    // window.open(whatsappUrl, '_blank');
    
    console.log('رسالة واتساب جاهزة:', whatsappUrl);
}

// ==================== وظائف مساعدة للواجهة ====================

// عرض حالة التحميل
function showLoading(show, message = 'جاري التحميل...') {
    const submitBtn = document.getElementById('submit-btn');
    
    if (show) {
        submitBtn.classList.add('loading');
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
        submitBtn.disabled = true;
    } else {
        submitBtn.classList.remove('loading');
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> تأكيد الطلب والدفع عند الاستلام';
        submitBtn.disabled = false;
    }
}

// عرض رسالة خطأ
function showError(message) {
    // إزالة أي رسائل خطأ سابقة
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // إنشاء رسالة الخطأ الجديدة
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    // إضافة الرسالة أعلى النموذج
    const form = document.getElementById('order-form');
    form.parentNode.insertBefore(errorDiv, form);
    
    // إزالة الرسالة بعد 5 ثواني
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

// عرض نافذة النجاح
function showSuccessModal(orderId) {
    document.getElementById('order-id').textContent = orderId;
    
    const message = `شكراً لك! تم استلام طلبك رقم ${orderId} وسنتواصل معك خلال 24 ساعة لتأكيد الطلب وتفاصيل الشحن.`;
    document.getElementById('success-message').innerHTML = message;
    
    const modal = document.getElementById('success-modal');
    modal.style.display = 'flex';
}

// إغلاق نافذة النجاح
function closeModal() {
    const modal = document.getElementById('success-modal');
    modal.style.display = 'none';
}

// ==================== إعدادات متقدمة ====================

// إغلاق النافذة عند النقر خارجها
window.addEventListener('click', function(event) {
    const modal = document.getElementById('success-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// إغلاق النافذة بالزر Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// تنسيق رقم الهاتف أثناء الكتابة
document.getElementById('customer-phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.substring(0, 11);
    e.target.value = value;
});

// نفس الشيء للواتساب
document.getElementById('customer-whatsapp').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.substring(0, 11);
    e.target.value = value;
});

// تسليط الضوء على الحقول المطلوبة
const requiredFields = document.querySelectorAll('[required]');
requiredFields.forEach(field => {
    field.addEventListener('blur', function() {
        if (!this.value.trim()) {
            this.style.borderColor = '#e74c3c';
            this.style.boxShadow = '0 0 0 2px rgba(231, 76, 60, 0.2)';
        } else {
            this.style.borderColor = '#3498db';
            this.style.boxShadow = 'none';
        }
    });
});

// ==================== تهيئة الصفحة ====================

// إضافة تحميل البيانات الأولية
console.log('صفحة الهبوط لـ Argento Store جاهزة للتشغيل!');
console.log('API Base URL:', API_BASE_URL);

// إشعار للمطور
if (API_BASE_URL === 'https://speedafargento.com') {
    console.warn('⚠️  تذكر تغيير API_BASE_URL لرابط Railway الفعلي بعد النشر!');
      }
