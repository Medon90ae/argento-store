// landing/script.js - النسخة المعدلة
const API_BASE_URL = 'https://speedafargento.com';
let currentProduct = null;
let currentShippingCost = 0;

// خريطة مصاريف الشحن حسب المدينة
const SHIPPING_RATES = {
    'Sharqia': 75, 'Cairo': 65, 'Giza': 65, 'Alexandria': 75,
    'Dakahlia': 75, 'Gharbia': 75, 'Monufia': 75, 'Qalyubia': 75,
    'Behira': 75, 'Ismailia': 85, 'Port Said': 85, 'Suez': 85,
    'Damietta': 75, 'Aswan': 130, 'Asyut': 95, 'BeniSuef': 95,
    'Faiyum': 95, 'Minya': 95, 'Qena': 130, 'Red Sea': 130,
    'New Valley': 130, 'Matrouh': 130, 'North Sinai': 130,
    'South Sinai': 130, 'Luxor': 130, 'Sohag': 95,
    'default': 80
};

// عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product_id');
    
    if (!productId) {
        showError('خطأ: لم يتم تحديد منتج. الرجاء استخدام رابط صحيح.');
        return;
    }
    
    // 1. جلب بيانات المنتج من API
    loadProductData(productId);
    
    // 2. تحميل قوائم المدن والمناطق من البيانات المحلية
    loadCitiesAndAreas();
    
    // 3. إعداد نموذج الطلب
    setupOrderForm();
    
    // 4. تحديث عند تغيير المدينة
    document.getElementById('city').addEventListener('change', updateAreasAndShipping);
});

// ==================== الوظائف الأساسية ====================

// 1. جلب بيانات المنتج
async function loadProductData(productId) {
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/api/product/${productId}`);
        
        if (!response.ok) {
            throw new Error('المنتج غير موجود أو حدث خطأ في الخادم');
        }
        
        const data = await response.json();
        if (data.success && data.product) {
            currentProduct = data.product;
            updateProductDisplay();
            calculateShipping('Sharqia', 'Zagazig');
            updateOrderSummary();
        } else {
            throw new Error('بيانات المنتج غير صحيحة');
        }
        
        showLoading(false);
        
    } catch (error) {
        showError(`خطأ في تحميل المنتج: ${error.message}`);
        showLoading(false);
    }
}

// 2. تحديث عرض المنتج
function updateProductDisplay() {
    if (!currentProduct) return;
    
    document.getElementById('product-title').textContent = currentProduct.name || currentProduct.title || 'منتج بدون اسم';
    document.getElementById('product-price').textContent = (currentProduct.price || 0).toLocaleString();
    
    // التاجر
    const merchantName = currentProduct.merchant_name || 
                        currentProduct.merchant_id || 
                        'Argento Store';
    document.getElementById('product-merchant').textContent = `التاجر: ${merchantName}`;
    
    // الوصف
    document.getElementById('product-description').textContent = 
        currentProduct.description || 'لا يوجد وصف مفصل للمنتج.';
    
    // الصورة
    const productImage = document.getElementById('product-image');
    if (currentProduct.image_url) {
        productImage.src = currentProduct.image_url;
        productImage.alt = currentProduct.name;
    }
}

// 3. تحميل قوائم المدن والمناطق
function loadCitiesAndAreas() {
    // استخدام البيانات المحلية مباشرة (المجلوبة من Excel)
    citiesData = EGYPT_CITIES_EN_TO_AR;
    areasData = EGYPT_CITY_AREAS;
    
    // تعبئة قائمة المدن
    populateCities();
}

// 4. تعبئة قائمة المدن
function populateCities() {
    const citySelect = document.getElementById('city');
    citySelect.innerHTML = '<option value="">اختر المحافظة</option>';
    
    // ترتيب المدن أبجدياً حسب العربية
    const sortedCities = Object.entries(citiesData)
        .sort((a, b) => a[1].localeCompare(b[1]));
    
    sortedCities.forEach(([enName, arName]) => {
        const option = document.createElement('option');
        option.value = enName;        // الإنجليزية (للسرعة والشحن)
        option.textContent = arName;  // العربية (للعرض)
        option.setAttribute('data-arabic', arName);
        citySelect.appendChild(option);
    });
}

// 5. تحديث قائمة المناطق
function updateAreasAndShipping() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    const selectedCity = citySelect.value;
    
    areaSelect.innerHTML = '<option value="">اختر المنطقة</option>';
    
    if (selectedCity && areasData[selectedCity]) {
        // ترتيب المناطق أبجدياً
        const sortedAreas = areasData[selectedCity].sort();
        
        sortedAreas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;  // الإنجليزية
            
            // ترجمة المنطقة للعربية إذا كانت متوفرة
            const arabicArea = AREA_TRANSLATIONS[area] || area;
            option.textContent = arabicArea;
            option.setAttribute('data-arabic', arabicArea);
            
            areaSelect.appendChild(option);
        });
        
        areaSelect.disabled = false;
    } else {
        areaSelect.disabled = true;
    }
    
    // تحديث الشحن
    updateShippingCost();
}

// 6. حساب تكلفة الشحن
function calculateShipping(city, area) {
    let baseCost = SHIPPING_RATES[city] || SHIPPING_RATES['default'];
    currentShippingCost = baseCost + 5; // رسوم المناولة
    
    const shippingElement = document.getElementById('shipping-cost');
    shippingElement.textContent = `${currentShippingCost.toLocaleString()} جنيه`;
    shippingElement.style.fontWeight = 'bold';
    
    return currentShippingCost;
}

// 7. تحديث تكلفة الشحن
function updateShippingCost() {
    const city = document.getElementById('city').value;
    const area = document.getElementById('area').value;
    
    if (city) {
        calculateShipping(city, area);
        updateOrderSummary();
    }
}

// 8. تحديث ملخص الطلب
function updateOrderSummary() {
    if (!currentProduct) return;
    
    const productPrice = currentProduct.price || 0;
    const total = productPrice + currentShippingCost;
    
    document.getElementById('summary-price').textContent = `${productPrice.toLocaleString()} ج`;
    document.getElementById('summary-shipping').textContent = `${currentShippingCost.toLocaleString()} ج`;
    document.getElementById('summary-total').textContent = `${total.toLocaleString()} ج`;
}

// 9. إعداد نموذج الطلب
function setupOrderForm() {
    const orderForm = document.getElementById('order-form');
    
    // نسخ الهاتف للواتساب
    document.getElementById('customer-phone').addEventListener('change', function() {
        const whatsapp = document.getElementById('customer-whatsapp');
        if (!whatsapp.value) {
            whatsapp.value = this.value;
        }
    });
    
    // إرسال النموذج
    orderForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        if (!validateForm()) return;
        
        const orderData = collectOrderData();
        await submitOrder(orderData);
    });
}

// 10. التحقق من صحة النموذج
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
    
    // التحقق من رقم الهاتف
    const phone = document.getElementById('customer-phone').value.trim();
    if (!/^01[0-9]{9}$/.test(phone)) {
        showError('يرجى إدخال رقم هاتف صحيح (11 رقم تبدأ بـ 01)');
        return false;
    }
    
    return isValid;
}

// 11. جمع بيانات الطلب
function collectOrderData() {
    const productPrice = currentProduct.price || 0;
    const totalAmount = productPrice + currentShippingCost;
    
    // الحصول على الاسم العربي للمدينة والمنطقة
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    
    const selectedCityOption = citySelect.options[citySelect.selectedIndex];
    const selectedAreaOption = areaSelect.options[areaSelect.selectedIndex];
    
    return {
        // بيانات المنتج
        product_id: currentProduct.id,
        product_name: currentProduct.name || currentProduct.title,
        product_price: productPrice,
        product_image: currentProduct.image_url,
        merchant_id: currentProduct.merchant_id || 'DEFAULT',
        
        // بيانات العميل
        customer_name: document.getElementById('customer-name').value.trim(),
        customer_phone: document.getElementById('customer-phone').value.trim(),
        customer_whatsapp: document.getElementById('customer-whatsapp').value.trim() || 
                          document.getElementById('customer-phone').value.trim(),
        
        // بيانات العنوان (عربي)
        customer_city: selectedCityOption.getAttribute('data-arabic') || selectedCityOption.textContent,
        customer_area: selectedAreaOption.getAttribute('data-arabic') || selectedAreaOption.textContent,
        customer_address: document.getElementById('address').value.trim(),
        customer_building: document.getElementById('building').value.trim(),
        customer_apartment: document.getElementById('apartment').value.trim(),
        customer_landmark: document.getElementById('landmark').value.trim(),
        
        // بيانات الشحن (إنجليزي)
        shipping_city: citySelect.value,
        shipping_area: areaSelect.value,
        
        // الحسابات المالية
        subtotal: productPrice,
        shipping_cost: currentShippingCost,
        total_amount: totalAmount,
        payment_method: 'cash_on_delivery',
        
        // معلومات إضافية
        source: 'landing_page',
        page_url: window.location.href,
        order_date: new Date().toISOString()
    };
}

// 12. إرسال الطلب إلى API
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
            showSuccessModal(result.order_id);
            // إرسال إشعار واتساب
            sendWhatsAppNotification(orderData, result.order_id);
        } else {
            throw new Error(result.error || result.message || 'حدث خطأ في الخادم');
        }
        
    } catch (error) {
        showError(`خطأ في إرسال الطلب: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// 13. إرسال إشعار واتساب
function sendWhatsAppNotification(orderData, orderId) {
    const message = `🎉 طلب جديد #${orderId}

👤 العميل: ${orderData.customer_name}
📞 الهاتف: ${orderData.customer_phone}
📍 العنوان: ${orderData.customer_city} - ${orderData.customer_area}
${orderData.customer_address}

🛒 المنتج: ${orderData.product_name}
💰 السعر: ${orderData.product_price} ج
🚚 الشحن: ${orderData.shipping_cost} ج
💰 الإجمالي: ${orderData.total_amount} ج

📝 الرابط: ${orderData.page_url}`;
    
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/201055688136?text=${encodedMessage}`;
    
    // يمكن فتح الرابط تلقائياً (اختياري)
    // setTimeout(() => window.open(whatsappUrl, '_blank'), 1000);
    
    console.log('رسالة واتساب جاهزة:', whatsappUrl);
}

// ==================== وظائف مساعدة للواجهة ====================

function showLoading(show, message = 'جاري التحميل...') {
    const submitBtn = document.getElementById('submit-btn');
    
    if (show) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> تأكيد الطلب والدفع عند الاستلام';
    }
}

function showError(message) {
    const existingError = document.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    const form = document.getElementById('order-form');
    form.parentNode.insertBefore(errorDiv, form);
    
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccessModal(orderId) {
    document.getElementById('order-id').textContent = orderId;
    document.getElementById('success-modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('success-modal').style.display = 'none';
}

// ==================== أحداث الصفحة ====================

window.addEventListener('click', function(event) {
    const modal = document.getElementById('success-modal');
    if (event.target === modal) closeModal();
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') closeModal();
});

// تنسيق أرقام الهواتف
['customer-phone', 'customer-whatsapp'].forEach(id => {
    document.getElementById(id).addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 11) value = value.substring(0, 11);
        e.target.value = value;
    });
});

console.log('صفحة الهبوط جاهزة للتشغيل!');
