// script_simplified.js - نسخة مبسطة مع دعم الترجمة
const API_BASE_URL = window.location.origin;
let currentProduct = null;
let currentShippingCost = 50; // تكلفة شحن افتراضية

// بيانات المدن والمناطق
let citiesData = {};      // الإنجليزية ← العربية
let areasData = {};       // المدينة ← قائمة المناطق
let areaTranslations = {}; // الإنجليزية ← العربية للمناطق

// ====================
// الترجمة الذكية باستخدام AI (محلياً)
// ====================

// قاموس ترجمة المدن
const cityTranslations = {
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
    'Menya': 'المنيا',
    'Qena': 'قنا',
    'Red Sea': 'البحر الأحمر',
    'New Valley': 'الوادي الجديد',
    'Matrouh': 'مطروح',
    'North Sinai': 'شمال سيناء',
    'South Sinai': 'جنوب سيناء',
    'Luxor': 'الأقصر',
    'Sohag': 'سوهاج',
    'Banha': 'بنها',
    'Mansoura': 'المنصورة',
    'Kafr El-Sheikh': 'كفر الشيخ',
    '6th of October': 'السادس من أكتوبر',
    '10th of Ramadan City': 'العاشر من رمضان',
    'New Administrative Capital': 'العاصمة الإدارية',
    'El Sheikh Zayed': 'الشيخ زايد',
    'Badr City': 'مدينة بدر',
    'El Obour': 'العبور',
    'North Coast': 'الساحل الشمالي',
    'Ain Sokhna': 'العين السخنة',
    'El Gouna': 'الجونة'
};

// قاموس ترجمة المناطق الشائعة
const areaTranslationsDict = {
    'Zagazig': 'الزقازيق',
    'Maadi': 'المعادي',
    'Nasr City': 'مدينة نصر',
    'New Cairo': 'القاهرة الجديدة',
    'Dokki': 'الدقي',
    'Mohandisen': 'المهندسين',
    'Sidi Gaber': 'سيدي جابر',
    'El-Raml': 'الرمل',
    'Heliopolis': 'مصر الجديدة',
    'Downtown': 'وسط البلد',
    'Zamalek': 'الزمالك',
    'Helwan': 'حلوان',
    'Shorouk': 'الشروق',
    'Haram': 'الهرم',
    'Faisal': 'فيصل',
    'Imbaba': 'إمبابة',
    'Smouha': 'سموحة',
    'Miami': 'ميامي',
    'Stanley': 'ستانلي',
    'Montaza': 'المنتزة'
};

// دالة ترجمة ذكية بسيطة
function translateToArabic(text) {
    if (!text) return text;
    
    // إذا كان النص عربي أصلاً، أرجعه كما هو
    if (/[\u0600-\u06FF]/.test(text)) {
        return text;
    }
    
    // ابحث في قواميس الترجمة
    if (cityTranslations[text]) {
        return cityTranslations[text];
    }
    
    if (areaTranslationsDict[text]) {
        return areaTranslationsDict[text];
    }
    
    // إذا لم يوجد، أرجع النص الأصلي
    return text;
}

// ====================
// عند تحميل الصفحة
// ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 صفحة الهبوط المبسطة جاهزة');
    
    // جلب ID المنتج من URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('product_id') || getProductIdFromPath();
    
    if (!productId) {
        showError('خطأ: لم يتم تحديد منتج. الرجاء استخدام رابط صحيح.');
        return;
    }
    
    console.log('📦 معرف المنتج:', productId);
    
    // تحميل البيانات
    loadProductData(productId);
    loadCitiesFromExcel();
    setupOrderForm();
});

// استخراج ID المنتج من المسار
function getProductIdFromPath() {
    const path = window.location.pathname;
    const match = path.match(/\/product\/([^\/]+)/);
    return match ? match[1] : null;
}

// ====================
// تحميل بيانات المنتج
// ====================

async function loadProductData(productId) {
    try {
        console.log(`📦 جاري تحميل المنتج ${productId}...`);
        
        const response = await fetch(`${API_BASE_URL}/api/product/${productId}`);
        
        if (!response.ok) {
            throw new Error(`خطأ HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success && data.product) {
            currentProduct = data.product;
            console.log('✅ تم تحميل المنتج:', currentProduct);
            updateProductDisplay();
        } else {
            throw new Error(data.error || 'بيانات المنتج غير صحيحة');
        }
        
    } catch (error) {
        console.error('❌ خطأ في تحميل المنتج:', error);
        showError('تعذر تحميل بيانات المنتج. الرجاء المحاولة لاحقاً.');
    }
}

// ====================
// تحديث عرض المنتج
// ====================

function updateProductDisplay() {
    if (!currentProduct) return;
    
    console.log('🎨 جاري تحديث عرض المنتج...');
    
    // العنوان
    const title = currentProduct.title || currentProduct.name || 'منتج';
    document.getElementById('product-title').textContent = title;
    document.getElementById('page-title').textContent = title + ' - Argento Store';
    
    // الصورة
    const image = currentProduct.image || currentProduct.image_url || 
                  (currentProduct.raw && currentProduct.raw.image_url) ||
                  'https://via.placeholder.com/400x400?text=No+Image';
    document.getElementById('product-image').src = image;
    document.getElementById('product-image').alt = title;
    
    // السعر
    const price = currentProduct.price || 0;
    document.getElementById('product-price').textContent = price.toLocaleString('ar-EG');
    document.getElementById('summary-price').textContent = price.toLocaleString('ar-EG') + ' ج';
    
    // التاجر
    const merchantName = currentProduct.merchant_name || 'Argento Store';
    document.getElementById('product-merchant').textContent = 'التاجر: ' + merchantName;
    
    // الوصف
    const description = currentProduct.description || 
                       'منتج عالي الجودة من ' + merchantName;
    document.getElementById('product-description').textContent = description;
    
    // تحديث الملخص
    updateOrderSummary();
    
    console.log(`✅ تم عرض المنتج: ${title} - ${price} ج`);
}

// ====================
// تحميل المدن من Excel
// ====================

async function loadCitiesFromExcel() {
    try {
        console.log('📂 جاري تحميل بيانات المدن من Excel...');
        
        const excelUrl = 'https://raw.githubusercontent.com/Medon90ae/argento-store/main/data/addresses.xlsx';
        
        const response = await fetch(excelUrl);
        
        if (!response.ok) {
            throw new Error(`خطأ في التحميل: ${response.status}`);
        }
        
        const arrayBuffer = await response.arrayBuffer();
        console.log('✅ تم تحميل ملف Excel:', arrayBuffer.byteLength, 'بايت');
        
        // قراءة Excel
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        
        console.log(`✅ تم قراءة ${jsonData.length} صف`);
        
        // معالجة البيانات
        processExcelData(jsonData);
        populateCities();
        
    } catch (error) {
        console.error('❌ خطأ في تحميل Excel:', error);
        // استخدم بيانات احتياطية
        useBackupCities();
    }
}

// ====================
// معالجة بيانات Excel
// ====================

function processExcelData(jsonData) {
    citiesData = {};
    areasData = {};
    areaTranslations = {};
    
    const uniqueCities = new Set();
    
    jsonData.forEach((row, index) => {
        try {
            const values = Object.values(row).filter(v => v !== null && v !== undefined && String(v).trim());
            
            if (values.length < 2) return;
            
            let city = String(values[0]).trim();
            let area = String(values[1]).trim();
            
            if (!city || !area) return;
            
            // حفظ المدينة
            uniqueCities.add(city);
            citiesData[city] = translateToArabic(city);
            
            // حفظ المنطقة
            if (!areasData[city]) {
                areasData[city] = [];
            }
            
            if (!areasData[city].includes(area)) {
                areasData[city].push(area);
            }
            
            // حفظ ترجمة المنطقة
            areaTranslations[area] = translateToArabic(area);
            
        } catch (e) {
            console.warn(`⚠️ تخطي الصف ${index}:`, e);
        }
    });
    
    // ترتيب المناطق
    for (const city in areasData) {
        areasData[city].sort();
    }
    
    console.log(`✅ تم معالجة ${uniqueCities.size} مدينة`);
}

// ====================
// بيانات احتياطية
// ====================

function useBackupCities() {
    console.log('⚠️ استخدام بيانات احتياطية للمدن');
    
    citiesData = {
        'Sharqia': 'الشرقية',
        'Cairo': 'القاهرة',
        'Giza': 'الجيزة',
        'Alexandria': 'الإسكندرية',
        'Dakahlia': 'الدقهلية'
    };
    
    areasData = {
        'Sharqia': ['Zagazig', 'Abu Hammad', 'Bilbeis'],
        'Cairo': ['Nasr City', 'Maadi', 'New Cairo', 'Downtown'],
        'Giza': ['Dokki', 'Mohandisen', 'Haram', 'Faisal'],
        'Alexandria': ['Sidi Gaber', 'Smouha', 'Miami'],
        'Dakahlia': ['El Mansoura', 'Mit Ghamr', 'Talkha']
    };
    
    areaTranslations = Object.assign({}, areaTranslationsDict);
    
    populateCities();
}

// ====================
// ملء قائمة المدن
// ====================

function populateCities() {
    const citySelect = document.getElementById('city');
    
    if (!citySelect) return;
    
    citySelect.innerHTML = '<option value="">اختر المحافظة</option>';
    
    // ترتيب المدن أبجدياً حسب العربية
    const sortedCities = Object.entries(citiesData)
        .sort((a, b) => a[1].localeCompare(b[1], 'ar'));
    
    sortedCities.forEach(([enName, arName]) => {
        const option = document.createElement('option');
        option.value = enName;
        option.textContent = arName;
        citySelect.appendChild(option);
    });
    
    console.log(`✅ تم تعبئة ${sortedCities.length} مدينة`);
    
    // حدث التغيير
    citySelect.addEventListener('change', updateAreas);
}

// ====================
// تحديث المناطق
// ====================

function updateAreas() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    
    if (!citySelect || !areaSelect) return;
    
    const selectedCity = citySelect.value;
    
    areaSelect.innerHTML = '<option value="">اختر المنطقة</option>';
    
    if (selectedCity && areasData[selectedCity]) {
        const areas = areasData[selectedCity].sort();
        
        areas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            option.textContent = areaTranslations[area] || area;
            areaSelect.appendChild(option);
        });
        
        areaSelect.disabled = false;
        console.log(`✅ تم تعبئة ${areas.length} منطقة لـ ${selectedCity}`);
    } else {
        areaSelect.disabled = true;
    }
    
    // تحديث الشحن
    updateShippingCost();
}

// ====================
// تحديث تكلفة الشحن
// ====================

function updateShippingCost() {
    const city = document.getElementById('city')?.value;
    
    if (city) {
        // تكلفة شحن بسيطة
        currentShippingCost = 50;
        
        document.getElementById('shipping-cost').textContent = currentShippingCost + ' جنيه';
        document.getElementById('summary-shipping').textContent = currentShippingCost + ' ج';
        
        updateOrderSummary();
    }
}

// ====================
// تحديث ملخص الطلب
// ====================

function updateOrderSummary() {
    const productPrice = currentProduct ? (currentProduct.price || 0) : 0;
    const shippingCost = currentShippingCost || 0;
    const total = productPrice + shippingCost;
    
    document.getElementById('summary-price').textContent = productPrice.toLocaleString('ar-EG') + ' ج';
    document.getElementById('summary-shipping').textContent = shippingCost.toLocaleString('ar-EG') + ' ج';
    document.getElementById('summary-total').textContent = total.toLocaleString('ar-EG') + ' ج';
}

// ====================
// إعداد نموذج الطلب
// ====================

function setupOrderForm() {
    const orderForm = document.getElementById('order-form');
    
    if (!orderForm) return;
    
    orderForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        if (!currentProduct) {
            showError('لم يتم تحميل بيانات المنتج بعد');
            return;
        }
        
        // جمع البيانات
        const formData = {
            // بيانات المنتج
            product_id: currentProduct.id || currentProduct.retailer_id,
            product_title: currentProduct.title || currentProduct.name,
            product_price: currentProduct.price || 0,
            merchant_id: currentProduct.merchant_id || 'DEFAULT',
            merchant_name: currentProduct.merchant_name || 'Argento Store',
            
            // بيانات العميل
            customer_name: document.getElementById('customer-name').value.trim(),
            customer_phone: document.getElementById('customer-phone').value.trim(),
            customer_whatsapp: document.getElementById('customer-whatsapp').value.trim() || 
                              document.getElementById('customer-phone').value.trim(),
            
            // عنوان الشحن
            shipping_city: document.getElementById('city').value,
            shipping_area: document.getElementById('area').value,
            shipping_address: document.getElementById('address').value.trim(),
            shipping_building: document.getElementById('building').value.trim(),
            shipping_apartment: document.getElementById('apartment').value.trim(),
            shipping_landmark: document.getElementById('landmark').value.trim(),
            
            // التكاليف
            shipping_cost: currentShippingCost,
            total_amount: (currentProduct.price || 0) + currentShippingCost
        };
        
        // إرسال الطلب
        await submitOrder(formData);
    });
    
    console.log('✅ تم إعداد نموذج الطلب');
}

// ====================
// إرسال الطلب
// ====================

async function submitOrder(orderData) {
    try {
        showLoader(true);
        
        console.log('📤 إرسال الطلب:', orderData);
        
        const response = await fetch(`${API_BASE_URL}/api/order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('✅ تم إرسال الطلب بنجاح:', result.order_id);
            showSuccessModal(result.order_id);
        } else {
            throw new Error(result.error || 'فشل إرسال الطلب');
        }
        
    } catch (error) {
        console.error('❌ خطأ في إرسال الطلب:', error);
        showError('حدث خطأ أثناء إرسال طلبك. الرجاء المحاولة مرة أخرى.');
    } finally {
        showLoader(false);
    }
}

// ====================
// واجهة المستخدم
// ====================

function showSuccessModal(orderId) {
    document.getElementById('order-id').textContent = orderId;
    document.getElementById('success-modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('success-modal').style.display = 'none';
    // إعادة تعيين النموذج
    document.getElementById('order-form').reset();
    document.getElementById('area').disabled = true;
}

function showLoader(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = show ? 'flex' : 'none';
    }
}

function showError(message) {
    alert('⚠️ ' + message);
}

console.log('✅ تم تحميل السكريبت المبسط بنجاح');
