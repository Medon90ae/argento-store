// landing/script.js - النسخة النهائية
// يقرأ بيانات المدن والمناطق من ملف Excel مباشرة

const API_BASE_URL = 'https://speedafargento.com';
let currentProduct = null;
let currentShippingCost = 0;

// متغيرات تخزين بيانات المدن والمناطق
let citiesData = {};      // الإنجليزية ← العربية
let areasData = {};       // المدينة ← قائمة المناطق
let areaTranslations = {}; // الإنجليزية ← العربية للمناطق

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
    
    // 2. تحميل بيانات المدن والمناطق من ملف Excel
    loadCitiesFromExcel();
    
    // 3. إعداد نموذج الطلب
    setupOrderForm();
    
    // 4. تحديث عند تغيير المدينة
    document.getElementById('city').addEventListener('change', updateAreasAndShipping);
    
    // 5. نسخ رقم الهاتف للواتساب تلقائياً
    document.getElementById('customer-phone').addEventListener('change', function() {
        const whatsapp = document.getElementById('customer-whatsapp');
        if (!whatsapp.value) {
            whatsapp.value = this.value;
        }
    });
});

// ==================== قراءة ملف Excel ====================

async function loadCitiesFromExcel() {
    try {
        console.log('📂 جاري تحميل بيانات المدن من ملف Excel...');
        showLoading(true, 'جاري تحميل قوائم المدن...');
        
        // مسار ملف Excel على GitHub
        const excelUrl = 'https://raw.githubusercontent.com/Medon90ae/argento-store/main/data/addresses.xlsx';
        
        // تحميل ملف Excel
        const response = await fetch(excelUrl);
        if (!response.ok) throw new Error(`خطأ HTTP: ${response.status}`);
        
        const arrayBuffer = await response.arrayBuffer();
        
        // قراءة ملف Excel باستخدام SheetJS
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        
        // البحث عن الورقة الصحيحة
        let sheetName = workbook.SheetNames.find(name => 
            name.toLowerCase().includes('speedaf') || 
            name.toLowerCase().includes('address')
        );
        
        // إذا لم نجد، نستخدم الورقة الثانية أو الأولى
        if (!sheetName) {
            sheetName = workbook.SheetNames.length > 1 ? workbook.SheetNames[1] : workbook.SheetNames[0];
        }
        
        const worksheet = workbook.Sheets[sheetName];
        
        // تحويل إلى JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        
        console.log(`✅ تم تحميل ${jsonData.length} صف من البيانات من ورقة: ${sheetName}`);
        
        // معالجة البيانات
        processExcelData(jsonData);
        
        // تعبئة قائمة المدن
        populateCities();
        
        showLoading(false);
        
    } catch (error) {
        console.error('❌ خطأ في تحميل ملف Excel:', error);
        showError('تعذر تحميل قوائم المدن. جاري استخدام البيانات المحلية...');
        
        // استخدام بيانات افتراضية إذا فشل التحميل
        useFallbackData();
        populateCities();
        showLoading(false);
    }
}

function processExcelData(jsonData) {
    // مسح المتغيرات
    citiesData = {};
    areasData = {};
    areaTranslations = {};
    
    // تخزين المدن الفريدة
    const uniqueCities = new Set();
    
    jsonData.forEach((row, index) => {
        try {
            let city = null;
            let area = null;
            
            // البحث عن أعمدة المدينة والمنطقة
            for (const [key, value] of Object.entries(row)) {
                const val = String(value).trim();
                if (!val || val === 'undefined' || val === 'null') continue;
                
                const keyLower = key.toLowerCase();
                
                // التعرف على عمود المدينة
                if (keyLower.includes('city') || keyLower.includes('المدينة') || 
                    keyLower.includes('المحافظة') || keyLower.includes('governorate')) {
                    city = val;
                }
                // التعرف على عمود المنطقة
                else if (keyLower.includes('area') || keyLower.includes('المنطقة') || 
                         keyLower.includes('location') || keyLower.includes('المكان')) {
                    area = val;
                }
            }
            
            // إذا لم نتعرف، نستخدم أول عمودين غير فارغين
            if (!city || !area) {
                const values = Object.values(row).filter(v => 
                    v && String(v).trim() && 
                    String(v).trim() !== 'undefined' && 
                    String(v).trim() !== 'null'
                );
                
                if (values.length >= 2) {
                    city = String(values[0]).trim();
                    area = String(values[1]).trim();
                } else {
                    return; // تخطي هذا الصف
                }
            }
            
            // تنظيف البيانات
            city = cleanText(city);
            area = cleanText(area);
            
            // حفظ المدينة الفريدة
            uniqueCities.add(city);
            
            // إضافة المدينة إلى القائمة
            citiesData[city] = city; // مؤقتاً
            
            // إضافة المنطقة إلى المدينة
            if (!areasData[city]) {
                areasData[city] = [];
            }
            
            if (!areasData[city].includes(area)) {
                areasData[city].push(area);
            }
            
            // حفظ ترجمة المنطقة
            areaTranslations[area] = area; // مؤقتاً
            
        } catch (e) {
            console.warn(`⚠️ خطأ في معالجة الصف ${index}:`, e);
        }
    });
    
    console.log(`🏙️  تم معالجة ${uniqueCities.size} مدينة`);
    
    // ترتيب المناطق أبجدياً
    for (const city in areasData) {
        areasData[city].sort();
    }
    
    // ترجمة أسماء المدن المعروفة
    translateCityNames();
    
    // ترجمة المناطق المعروفة
    translateAreaNames();
}

function cleanText(text) {
    if (!text || typeof text !== 'string') return '';
    
    // إزالة المسافات الزائدة والأحرف الغريبة
    return text
        .replace(/\s+/g, ' ')
        .replace(/[^\w\s\-()\/.,&]/g, '')
        .trim();
}

function translateCityNames() {
    // قاموس ترجمة المدن المشهورة
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
        'Qena': 'قنا',
        'Red Sea': 'البحر الأحمر',
        'New Valley': 'الوادي الجديد',
        'Matrouh': 'مطروح',
        'North Sinai': 'شمال سيناء',
        'South Sinai': 'جنوب سيناء',
        'Luxor': 'الأقصر',
        'Sohag': 'سوهاج',
        'Zagazig': 'الزقازيق',
        'El Mansoura': 'المنصورة',
        'Tanta': 'طنطا',
        'El Mahalla El Kubra': 'المحلة الكبرى',
        'Damanhour': 'دمنهور',
        'Benha': 'بنها',
        'Kafr El Sheikh': 'كفر الشيخ',
        'Hurghada': 'الغردقة',
        'Sharm El Sheikh': 'شرم الشيخ',
        'Marsa Matruh': 'مرسى مطروح',
        'El Arish': 'العريش'
    };
    
    // تحديث ترجمات المدن
    const newCitiesData = {};
    for (const [enCity, arCity] of Object.entries(cityTranslations)) {
        // البحث بأحرف كبيرة وصغيرة
        const foundKey = Object.keys(citiesData).find(key => 
            key.toLowerCase() === enCity.toLowerCase()
        );
        
        if (foundKey) {
            newCitiesData[foundKey] = arCity;
        }
    }
    
    // إضافة المدن التي لم يتم ترجمتها
    for (const city in citiesData) {
        if (!newCitiesData[city]) {
            newCitiesData[city] = city;
        }
    }
    
    citiesData = newCitiesData;
    console.log('✅ تمت ترجمة أسماء المدن');
}

function translateAreaNames() {
    // قاموس ترجمة المناطق المشهورة
    const translations = {
        'Zagazig': 'الزقازيق',
        'Maadi': 'المعادي',
        'Nasr City': 'مدينة نصر',
        'New Cairo': 'القاهرة الجديدة',
        'Helwan': 'حلوان',
        'Shorouk': 'الشروق',
        'Ain Shams': 'عين شمس',
        'El Marg': 'المرج',
        'Heliopolis': 'هليوبوليس',
        'Zamalek': 'الزمالك',
        'Dokki': 'الدقي',
        'Mohandisen': 'المهندسين',
        'Manial': 'المنيل',
        'Faisal': 'فيصل',
        'Haram': 'الهرم',
        'Hadayk Ahram': 'حدائق الأهرام',
        'Imbaba': 'إمبابة',
        'Bolak Al Dakrour': 'بولاق الدكرور',
        'Al Agouzah': 'العجوزة',
        'Sidi Gaber': 'سيدي جابر',
        'El-Raml': 'الرمل',
        'Montaza': 'المنتزة',
        'Al Mamurah': 'المعمورة',
        'Abu Qir': 'أبو قير',
        'El-Agamy': 'العجمي',
        'Dekhela': 'الدخيلة',
        'Borg al arab': 'برج العرب',
        'Smouha': 'سموحة',
        'Sidi Bishr': 'سيدي بشر',
        'Miami': 'ميامي',
        'Stanley': 'ستانلي',
        'El Mansoura': 'المنصورة',
        'Mit Ghamr': 'ميت غمر',
        'Talkha': 'طلخا',
        'Tanta': 'طنطا',
        'El Mahalla El Kubra': 'المحلة الكبرى',
        'Zefta': 'زفتى',
        'Shibin el Kom': 'شبين الكوم',
        'Menouf': 'منوف',
        'Tala': 'تلا',
        'Banha': 'بنها',
        'Damanhour': 'دمنهور',
        'Kafr El Dawwar': 'كفر الدوار',
        'Rasheed': 'رشيد',
        'Ismailia': 'الإسماعيلية',
        'Fayed': 'فايد',
        'Port Said': 'بورسعيد',
        'Suez': 'السويس',
        'Damietta': 'دمياط',
        'Hurghada': 'الغردقة',
        'Sharm El Sheikh': 'شرم الشيخ',
        'Marsa Matruh': 'مرسى مطروح',
        'El Arish': 'العريش',
        'Luxor City': 'الأقصر',
        'Aswan city': 'أسوان',
        'Asyut city': 'أسيوط',
        'Beni Suef city': 'بني سويف',
        'Faiyum center': 'الفيوم',
        'Minya City': 'المنيا',
        'Sohag': 'سوهاج'
    };
    
    // تحديث ترجمات المناطق
    for (const [enArea, arArea] of Object.entries(translations)) {
        areaTranslations[enArea] = arArea;
    }
}

function useFallbackData() {
    console.log('🔄 استخدام البيانات الافتراضية...');
    
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
        'Cairo': ['Maadi', 'Nasr City', 'New Cairo', 'Helwan', 'Shorouk', 'Ain Shams', 'El Marg'],
        'Giza': ['Faisal', 'Haram', 'Dokki', 'Mohandisen', 'Imbaba', 'Bolak Al Dakrour'],
        'Alexandria': ['Sidi Gaber', 'El-Raml', 'Montaza', 'Al Mamurah', 'Abu Qir', 'El-Agamy']
    };
    
    areaTranslations = {
        'Zagazig': 'الزقازيق',
        'Maadi': 'المعادي',
        'Nasr City': 'مدينة نصر',
        'New Cairo': 'القاهرة الجديدة'
    };
}

// ==================== عرض القوائم ====================

function populateCities() {
    const citySelect = document.getElementById('city');
    if (!citySelect) return;
    
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
    
    console.log(`✅ تم تعبئة ${sortedCities.length} مدينة`);
}

function updateAreasAndShipping() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    if (!citySelect || !areaSelect) return;
    
    const selectedCity = citySelect.value;
    
    areaSelect.innerHTML = '<option value="">اختر المنطقة</option>';
    
    if (selectedCity && areasData[selectedCity]) {
        // ترتيب المناطق أبجدياً
        const sortedAreas = areasData[selectedCity].sort();
        
        sortedAreas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;  // الإنجليزية
            
            // ترجمة المنطقة للعربية إذا كانت متوفرة
            const arabicArea = areaTranslations[area] || area;
            option.textContent = arabicArea;
            option.setAttribute('data-arabic', arabicArea);
            
            areaSelect.appendChild(option);
        });
        
        areaSelect.disabled = false;
        console.log(`📍 تم تعبئة ${sortedAreas.length} منطقة لـ ${selectedCity}`);
    } else {
        areaSelect.disabled = true;
        console.log(`⚠️  لا توجد مناطق لـ ${selectedCity}`);
    }
    
    // تحديث الشحن
    updateShippingCost();
}

// ==================== المنتج والطلب ====================

async function loadProductData(productId) {
    try {
        showLoading(true, 'جاري تحميل بيانات المنتج...');
        
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
            throw new Error(data.error || 'بيانات المنتج غير صحيحة');
        }
        
        showLoading(false);
        
    } catch (error) {
        showError(`خطأ في تحميل المنتج: ${error.message}`);
        showLoading(false);
    }
}

function updateProductDisplay() {
    if (!currentProduct) return;
    
    document.getElementById('product-title').textContent = 
        currentProduct.name || currentProduct.title || 'منتج بدون اسم';
    
    document.getElementById('product-price').textContent = 
        (currentProduct.price || 0).toLocaleString();
    
    const merchantName = currentProduct.merchant_name || 
                        currentProduct.merchant_id || 
                        'Argento Store';
    document.getElementById('product-merchant').textContent = `التاجر: ${merchantName}`;
    
    document.getElementById('product-description').textContent = 
        currentProduct.description || 'لا يوجد وصف مفصل للمنتج.';
    
    const productImage = document.getElementById('product-image');
    if (currentProduct.image_url) {
        productImage.src = currentProduct.image_url;
        productImage.alt = currentProduct.name;
    } else {
        productImage.src = 'https://via.placeholder.com/400x400/2c3e50/ecf0f1?text=Argento+Store';
    }
}

function calculateShipping(city, area) {
    let baseCost = SHIPPING_RATES[city] || SHIPPING_RATES['default'];
    currentShippingCost = baseCost + 5; // رسوم المناولة
    
    const shippingElement = document.getElementById('shipping-cost');
    if (shippingElement) {
        shippingElement.textContent = `${currentShippingCost.toLocaleString()} جنيه`;
        shippingElement.style.fontWeight = 'bold';
    }
    
    return currentShippingCost;
}

function updateShippingCost() {
    const city = document.getElementById('city').value;
    const area = document.getElementById('area').value;
    
    if (city) {
        calculateShipping(city, area);
        updateOrderSummary();
    }
}

function updateOrderSummary() {
    if (!currentProduct) return;
    
    const productPrice = currentProduct.price || 0;
    const total = productPrice + currentShippingCost;
    
    const summaryPrice = document.getElementById('summary-price');
    const summaryShipping = document.getElementById('summary-shipping');
    const summaryTotal = document.getElementById('summary-total');
    
    if (summaryPrice) summaryPrice.textContent = `${productPrice.toLocaleString()} ج`;
    if (summaryShipping) summaryShipping.textContent = `${currentShippingCost.toLocaleString()} ج`;
    if (summaryTotal) summaryTotal.textContent = `${total.toLocaleString()} ج`;
}

function setupOrderForm() {
    const orderForm = document.getElementById('order-form');
    if (!orderForm) return;
    
    orderForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        if (!validateForm()) return;
        
        const orderData = collectOrderData();
        await submitOrder(orderData);
    });
}

function validateForm() {
    const requiredFields = ['customer-name', 'customer-phone', 'city', 'area', 'address'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field || !field.value.trim()) {
            if (field) field.style.borderColor = '#e74c3c';
            isValid = false;
        } else if (field) {
            field.style.borderColor = '#3498db';
        }
    });
    
    // التحقق من رقم الهاتف
    const phone = document.getElementById('customer-phone');
    if (phone && !/^01[0-9]{9}$/.test(phone.value.trim())) {
        showError('يرجى إدخال رقم هاتف صحيح (11 رقم تبدأ بـ 01)');
        return false;
    }
    
    // التحقق من اختيار المدينة والمنطقة
    const city = document.getElementById('city');
    const area = document.getElementById('area');
    if (city && city.value && area && !area.value) {
        showError('يرجى اختيار المنطقة');
        return false;
    }
    
    return isValid؛
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
    
    console.log('📱 رسالة واتساب جاهزة:', whatsappUrl);
                                          
}
    
// ==================== وظائف مساعدة ====================

function showLoading(show, message = 'جاري التحميل...') {
    const submitBtn = document.getElementById('submit-btn');
    if (!submitBtn) return;
    
    if (show) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> تأكيد الطلب والدفع عند الاستلام';
    }
}

function showError(message) {
    // إزالة أي رسائل خطأ سابقة
    const existingError = document.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    // إنشاء رسالة الخطأ الجديدة
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    errorDiv.style.cssText = `
        background: #e74c3c;
        color: white;
        padding: 12px;
        border-radius: 5px;
        margin: 15px 0;
        text-align: center;
        font-weight: bold;
    `;
    
    // إضافة الرسالة أعلى النموذج
    const form = document.getElementById('order-form');
    if (form && form.parentNode) {
        form.parentNode.insertBefore(errorDiv, form);
    }
    
    // إزالة الرسالة بعد 5 ثواني
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

function showSuccessModal(orderId) {
    const orderIdElement = document.getElementById('order-id');
    const modal = document.getElementById('success-modal');
    
    if (orderIdElement) orderIdElement.textContent = orderId;
    if (modal) modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('success-modal');
    if (modal) modal.style.display = 'none';
}

// ==================== أحداث إضافية ====================

// إغلاق النافذة عند النقر خارجها
window.addEventListener('click', function(event) {
    const modal = document.getElementById('success-modal');
    if (event.target === modal) closeModal();
});

// إغلاق النافذة بالزر Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') closeModal();
});

// تنسيق أرقام الهواتف أثناء الكتابة
['customer-phone', 'customer-whatsapp'].forEach(id => {
    const element = document.getElementById(id);
    if (element) {
        element.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.substring(0, 11);
            e.target.value = value;
        });
    }
});

// تسليط الضوء على الحقول المطلوبة
document.querySelectorAll('[required]').forEach(field => {
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

console.log('🚀 صفحة الهبوط جاهزة للتشغيل!');
