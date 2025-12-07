// landing/script.js - النسخة المعدلة
const API_BASE_URL = 'https://speedafargento.com';
let currentProduct = null;
let currentShippingCost = 0;

// متغيرات تخزين بيانات المدن والمناطق
let citiesData = {};      // الإنجليزية ← العربية
let areasData = {};       // المدينة ← قائمة المناطق
let areaTranslations = {}; // الإنجليزية ← العربية للمناطق

// عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 صفحة الهبوط جاهزة للتشغيل');
    
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
});

// ========== قراءة ملف Excel ==========

async function loadCitiesFromExcel() {
    try {
        console.log('📂 جاري تحميل بيانات المدن من ملف Excel...');
        
        // مسار ملف Excel على GitHub
        const excelUrl = 'https://raw.githubusercontent.com/Medon90ae/argento-store/main/data/addresses.xlsx';
        console.log('📁 مسار الملف:', excelUrl);
        
        // تحميل ملف Excel
        const response = await fetch(excelUrl);
        console.log('📥 حالة التحميل:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`خطأ HTTP: ${response.status} - ${response.statusText}`);
        }
        
        const arrayBuffer = await response.arrayBuffer();
        console.log('✅ تم تحميل ملف Excel:', arrayBuffer.byteLength, 'بايت');
        
        // قراءة ملف Excel باستخدام SheetJS
        console.log('🔍 جاري قراءة ملف Excel...');
        const workbook = XLSX.read(arrayBuffer, { type: 'array' });
        console.log('📊 أوراق الملف:', workbook.SheetNames);
        
        // البحث عن الورقة الصحيحة
        let sheetName = workbook.SheetNames.find(name => 
            name.toLowerCase().includes('speedaf') || 
            name.toLowerCase().includes('address')
        );
        
        if (!sheetName && workbook.SheetNames.length > 0) {
            sheetName = workbook.SheetNames[0];
        }
        
        console.log('📄 الورقة المستخدمة:', sheetName);
        
        if (!sheetName) {
            throw new Error('لم يتم العثور على أي ورقة في الملف');
        }
        
        const worksheet = workbook.Sheets[sheetName];
        
        // تحويل إلى JSON
        const jsonData = XLSX.utils.sheet_to_json(worksheet);
        console.log(`✅ تم تحميل ${jsonData.length} صف من البيانات`);
        
        if (jsonData.length === 0) {
            throw new Error('الملف فارغ أو لا يحتوي على بيانات');
        }
        
        // معالجة البيانات
        processExcelData(jsonData);
        
        // تعبئة قائمة المدن
        populateCities();
        
    } catch (error) {
        console.error('❌ خطأ في تحميل ملف Excel:', error);
        showError(`خطأ في تحميل قوائم المدن: ${error.message}`);
    }
}

function processExcelData(jsonData) {
    console.log('🔧 جاري معالجة بيانات Excel...');
    
    // مسح المتغيرات
    citiesData = {};
    areasData = {};
    areaTranslations = {};
    
    // تخزين المدن الفريدة
    const uniqueCities = new Set();
    let processedRows = 0;
    
    // عرض أول صف لفهم الهيكل
    if (jsonData.length > 0) {
        console.log('📋 هيكل الصف الأول:', jsonData[0]);
    }
    
    jsonData.forEach((row, index) => {
        try {
            let city = null;
            let area = null;
            
            // البحث في جميع أعمدة الصف
            for (const [key, value] of Object.entries(row)) {
                if (value === null || value === undefined) continue;
                
                const val = String(value).trim();
                if (!val || val === 'undefined' || val === 'null' || val === 'NaN') continue;
                
                console.log(`📝 الصف ${index}، العمود "${key}": "${val}"`);
                
                // محاولة التعرف على نوع البيانات
                if (key.toLowerCase().includes('city') || 
                    key.toLowerCase().includes('المدينة') || 
                    key.toLowerCase().includes('المحافظة')) {
                    city = val;
                } else if (key.toLowerCase().includes('area') || 
                          key.toLowerCase().includes('المنطقة') || 
                          key.toLowerCase().includes('location')) {
                    area = val;
                }
            }
            
            // إذا لم نتعرف، نستخدم أول عمودين
            if (!city || !area) {
                const values = Object.values(row).filter(v => 
                    v !== null && 
                    v !== undefined && 
                    String(v).trim() && 
                    String(v).trim() !== 'undefined' && 
                    String(v).trim() !== 'null' && 
                    String(v).trim() !== 'NaN'
                );
                
                if (values.length >= 2) {
                    city = String(values[0]).trim();
                    area = String(values[1]).trim();
                    console.log(`⚡ استخدام القيمتين الأولتين: المدينة="${city}", المنطقة="${area}"`);
                } else {
                    console.log(`⏭️  تخطي الصف ${index} - بيانات غير كافية`);
                    return;
                }
            }
            
            if (!city || !area) {
                console.log(`⏭️  تخطي الصف ${index} - مدينة أو منطقة فارغة`);
                return;
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
            
            processedRows++;
            
        } catch (e) {
            console.warn(`⚠️ خطأ في معالجة الصف ${index}:`, e, 'البيانات:', row);
        }
    });
    
    console.log(`✅ تم معالجة ${processedRows} صف من أصل ${jsonData.length}`);
    console.log(`🏙️  عدد المدن الفريدة: ${uniqueCities.size}`);
    console.log('📊 المدن:', Array.from(uniqueCities));
    
    // ترتيب المناطق أبجدياً
    for (const city in areasData) {
        areasData[city].sort();
        console.log(`📍 المناطق في ${city}:`, areasData[city]);
    }
    
    // ترجمة أسماء المدن المعروفة
    translateCityNames();
    
    // ترجمة المناطق المعروفة
    translateAreaNames();
}

function cleanText(text) {
    if (!text || typeof text !== 'string') return '';
    
    // إزالة المسافات الزائدة
    return text.replace(/\s+/g, ' ').trim();
}

function translateCityNames() {
    console.log('🔤 جاري ترجمة أسماء المدن...');
    
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
        'Qena': 'قنا',
        'Red Sea': 'البحر الأحمر',
        'New Valley': 'الوادي الجديد',
        'Matrouh': 'مطروح',
        'North Sinai': 'شمال سيناء',
        'South Sinai': 'جنوب سيناء',
        'Luxor': 'الأقصر',
        'Sohag': 'سوهاج'
    };
    
    // تحديث ترجمات المدن
    const newCitiesData = {};
    let translatedCount = 0;
    
    for (const [enCity, arCity] of Object.entries(cityTranslations)) {
        // البحث بأحرف كبيرة وصغيرة
        const foundKey = Object.keys(citiesData).find(key => 
            key.toLowerCase() === enCity.toLowerCase()
        );
        
        if (foundKey) {
            newCitiesData[foundKey] = arCity;
            translatedCount++;
            console.log(`🌍 ترجمة: ${foundKey} → ${arCity}`);
        }
    }
    
    // إضافة المدن التي لم يتم ترجمتها
    for (const city in citiesData) {
        if (!newCitiesData[city]) {
            newCitiesData[city] = city;
        }
    }
    
    citiesData = newCitiesData;
    console.log(`✅ تمت ترجمة ${translatedCount} مدينة`);
}

function translateAreaNames() {
    console.log('🔤 جاري ترجمة أسماء المناطق...');
    
    // قاموس ترجمة المناطق
    const translations = {
        'Zagazig': 'الزقازيق',
        'Maadi': 'المعادي',
        'Nasr City': 'مدينة نصر',
        'New Cairo': 'القاهرة الجديدة',
        'Dokki': 'الدقي',
        'Mohandisen': 'المهندسين',
        'Sidi Gaber': 'سيدي جابر',
        'El-Raml': 'الرمل'
    };
    
    let translatedCount = 0;
    
    for (const [enArea, arArea] of Object.entries(translations)) {
        if (areaTranslations[enArea]) {
            areaTranslations[enArea] = arArea;
            translatedCount++;
            console.log(`📍 ترجمة منطقة: ${enArea} → ${arArea}`);
        }
    }
    
    console.log(`✅ تمت ترجمة ${translatedCount} منطقة`);
}

// ========== عرض القوائم ==========

function populateCities() {
    const citySelect = document.getElementById('city');
    if (!citySelect) {
        console.error('❌ لم يتم العثور على عنصر city');
        return;
    }
    
    console.log('🔄 جاري تعبئة قائمة المدن...');
    
    citySelect.innerHTML = '<option value="">اختر المحافظة</option>';
    
    if (Object.keys(citiesData).length === 0) {
        console.error('❌ لا توجد بيانات للمدن');
        citySelect.innerHTML += '<option value="">لا توجد مدن متاحة</option>';
        return;
    }
    
    // ترتيب المدن أبجدياً حسب العربية
    const sortedCities = Object.entries(citiesData)
        .sort((a, b) => a[1].localeCompare(b[1]));
    
    sortedCities.forEach(([enName, arName]) => {
        const option = document.createElement('option');
        option.value = enName;
        option.textContent = arName;
        option.setAttribute('data-arabic', arName);
        citySelect.appendChild(option);
    });
    
    console.log(`✅ تم تعبئة ${sortedCities.length} مدينة في القائمة`);
    
    // إضافة حدث التغيير
    citySelect.addEventListener('change', updateAreasAndShipping);
}

function updateAreasAndShipping() {
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    
    if (!citySelect || !areaSelect) return;
    
    const selectedCity = citySelect.value;
    
    console.log(`🔄 تغيير المدينة إلى: ${selectedCity}`);
    
    areaSelect.innerHTML = '<option value="">اختر المنطقة</option>';
    
    if (selectedCity && areasData[selectedCity]) {
        // ترتيب المناطق أبجدياً
        const sortedAreas = areasData[selectedCity].sort();
        
        console.log(`📍 المناطق المتاحة لـ ${selectedCity}:`, sortedAreas);
        
        sortedAreas.forEach(area => {
            const option = document.createElement('option');
            option.value = area;
            
            // ترجمة المنطقة للعربية
            const arabicArea = areaTranslations[area] || area;
            option.textContent = arabicArea;
            option.setAttribute('data-arabic', arabicArea);
            
            areaSelect.appendChild(option);
        });
        
        areaSelect.disabled = false;
        console.log(`✅ تم تعبئة ${sortedAreas.length} منطقة`);
    } else {
        areaSelect.disabled = true;
        console.warn(`⚠️  لا توجد مناطق لـ ${selectedCity}`);
    }
    
    // تحديث الشحن
    updateShippingCost();
}

// ========== بقية الدوال ==========

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
        showError('تعذر تحميل بيانات المنتج');
    }
}

function updateProductDisplay() {
    if (!currentProduct) return;
    
    console.log('🎨 جاري تحديث عرض المنتج...');
    
    // تحديث العناصر
    const title = currentProduct.name || currentProduct.title || 'منتج بدون اسم';
    document.getElementById('product-title').textContent = title;
    
    const price = currentProduct.price || 0;
    document.getElementById('product-price').textContent = price.toLocaleString();
    
    console.log(`✅ المنتج: ${title} - السعر: ${price}`);
}

function updateShippingCost() {
    const city = document.getElementById('city')?.value;
    
    if (city) {
        // حساب الشحن البسيط
        currentShippingCost = 50;
        document.getElementById('shipping-cost').textContent = `${currentShippingCost} جنيه`;
        console.log(`💰 تكلفة الشحن لـ ${city}: ${currentShippingCost}`);
    }
}

function setupOrderForm() {
    console.log('📝 جاري إعداد نموذج الطلب...');
    
    const orderForm = document.getElementById('order-form');
    if (!orderForm) {
        console.error('❌ لم يتم العثور على نموذج الطلب');
        return;
    }
    
    orderForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        console.log('📤 تم إرسال النموذج');
        
        // هنا كود إرسال الطلب
        alert('سيتم إرسال الطلب عندما تكتمل القوائم');
    });
    
    console.log('✅ تم إعداد نموذج الطلب');
}

function showError(message) {
    console.error('❌ خطأ:', message);
    alert(message);
}

console.log('🚀 تم تحميل script.js بنجاح');
