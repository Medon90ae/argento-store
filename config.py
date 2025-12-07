# إعدادات المشروع
# ملف config.py
# الإعدادات الرئيسية للمشروع - الجزء الأول: قوائم المدن والمناطق

"""
قوائم المدن والمناطق الرسمية لمصر
المصدر: Speedaf / التطبيق المصري الرسمي
التنسيق: City (الإنجليزية) -> Area (الإنجليزية)
"""

# ============================================================
# القائمة الرئيسية: City -> قائمة Areas
# ============================================================
OFFICIAL_CITIES_AREAS = {
    # الشرقية
    "Sharqia": [
        "Zagazig",
        "Minya El Qamh",
        "Mashtol Al Souq",
        "Hihya",
        "El Qurein",
        "El Qanayat",
        "El Ibrahimiya",
        "Diyarb Negm",
        "Bilbeis",
        "Abu Hammad"
    ],
    
    # القاهرة والجيزة
    "Cairo": [
        "Downtown",
        "Nasr City",
        "New Cairo",
        "Maadi",
        "Helwan",
        "Shorouk",
        "Ain Shams",
        "El Marg",
        "El Nozha",
        "Masr El Gadida",
        "Heliopolis",
        "Zamalek",
        "Dokki",
        "Mohandisen",
        "Manial",
        "Faisal",
        "Haram",
        "Hadayk Ahram",
        "Zayton",
        "El Basatin",
        "El Katameya",
        "El Mokattam"
    ],
    
    "Giza": [
        "Faisal",
        "Haram",
        "Hadayk Ahram",
        "Dokki",
        "Mohandisen",
        "Imbaba",
        "Bolak Al Dakrour",
        "Al Agouzah",
        "Warak",
        "Omrania",
        "Kerdasa",
        "Abou Rawash"
    ],
    
    # الإسكندرية
    "Alexandria": [
        "Al-agamy",
        "Alex",
        "Moharram Bek",
        "Sidi Gaber",
        "El-Raml",
        "Montaza",
        "Al Mamurah",
        "Abu Qir",
        "El-Agamy",
        "Dekhela",
        "Borg al arab",
        "Smouha",
        "Sidi Bishr",
        "Miami",
        "Stanley",
        "Camp Shezar",
        "Cleopatra",
        "Gleem",
        "Laurent",
        "Mandara",
        "Asafra",
        "Al Anfoushi",
        "Al Attarin",
        "Al Gomrok",
        "Bab Sharqi",
        "Karmouz"
    ],
    
    # المدن الكبرى
    "Aswan": [
        "Aswan city",
        "New Aswan",
        "Kom Umbu",
        "Edfu",
        "Draw",
        "Nasr City",
        "Al Gaafrah"
    ],
    
    "Asyut": [
        "Asyut city",
        "New Asyut",
        "Abnub",
        "Abu Tij",
        "El-Ghanayem",
        "Manfalut",
        "Sahel Selim"
    ],
    
    "Banha": [
        "Banha",
        "Tukh",
        "Shibin El Qanater",
        "Qalyub",
        "Kafr Shukr",
        "El Qanater El Khayreya"
    ],
    
    "Behira": [
        "Damanhour",
        "Kafr El Dawwar",
        "Rasheed",
        "Edku",
        "Abu Hummus",
        "Itay Al Barud",
        "Shubrakhit",
        "Mahmoudiyah",
        "Kom Hamada",
        "Al Delengat",
        "Badr"
    ],
    
    "BeniSuef": [
        "Beni Suef city",
        "New Beni Suef",
        "Biba",
        "Al Fashn",
        "Ihnasiya",
        "Sumusta",
        "Nasser"
    ],
    
    "Damietta": [
        "Damietta",
        "New Damietta",
        "Ras El Bar",
        "Kafr Saad",
        "Kafr El Battikh",
        "Faraskur"
    ],
    
    "Faiyum": [
        "Faiyum center",
        "New Faiyum",
        "Ibsheway",
        "Itsa",
        "Sinnuris",
        "Tamiyyah",
        "Kufur an Nil"
    ],
    
    "Gharbia": [
        "Tanta",
        "El Mahalla El Kubra",
        "Zefta",
        "Kafr El Zayat",
        "Basyoun",
        "Qutur",
        "El Santa"
    ],
    
    "Ismailia": [
        "Ismailia",
        "Fayed",
        "El Qantara",
        "Tell El Kebir",
        "Abu Suwir",
        "Abu Sultan"
    ],
    
    "Kafr El-Sheikh": [
        "Kafr El-Shaikh",
        "Desouk",
        "Biyala",
        "Baltiem",
        "El Reyad",
        "El-Hamoul",
        "Burullus"
    ],
    
    "Luxor": [
        "Luxor City",
        "New Luxor",
        "Armant",
        "Esna",
        "Al Qarnah",
        "Al Madamoud"
    ],
    
    "Mansoura": [
        "El Mansoura",
        "Mit Ghamr",
        "Talkha",
        "Aga",
        "El-Senbellawein",
        "Belqas",
        "Gamasa"
    ],
    
    "Menya": [
        "Minya City",
        "New Menya",
        "Beni Mazar",
        "Matay",
        "Maghagha",
        "Samalut",
        "Abu Qurqas"
    ],
    
    "Monufia": [
        "Shibin el Kom",
        "Menouf",
        "Tala",
        "El Sadat City",
        "Ashmoun",
        "El Bagour",
        "Quwaysna"
    ],
    
    "Port Said": [
        "Port Said",
        "Port Fuad",
        "El Dawahy",
        "El Zohur",
        "El Sharq",
        "Al Ganoub"
    ],
    
    "Qena": [
        "Qena",
        "New Qena",
        "Nagaa Hammadi",
        "Dishna",
        "Qus",
        "Qift",
        "Naqada"
    ],
    
    "Sohag": [
        "Sohag",
        "New Sohag",
        "Akhmim",
        "New Akhmim",
        "Tahta",
        "Tima",
        "Al Minshah"
    ],
    
    "Suez": [
        "Suez",
        "Port Tawfik",
        "Arbaeen",
        "Attaka",
        "Faisal",
        "Ganayen"
    ],
    
    # مدن الصحراء والسواحل
    "Red Sea": [
        "Hurghada",
        "Sharm El-Sheikh",
        "Marsa Alam",
        "Safaga",
        "El Qusair",
        "Ras Gharib"
    ],
    
    "Matrouh": [
        "Marsa Matruh",
        "El-Alamein",
        "El Hamam",
        "Sidi Barrani",
        "Sallum",
        "El Dabaa"
    ],
    
    "New Valley": [
        "Kharga",
        "Dakhla",
        "Farafra",
        "Baris"
    ],
    
    "South Sinai": [
        "Sharm El-Sheikh",
        "Dahab",
        "Nuweiba",
        "Taba",
        "Ras Sedr",
        "Abu Redis",
        "Saint Catherine"
    ],
    
    "North Sinai": [
        "El Arish",
        "Sheikh Zuweid",
        "Rafah",
        "Bir al-Abd"
    ],
    
    # المدن الجديدة
    "6th of October": [
        "Sheikh Zayed City",
        "6th of October City",
        "Smart Village",
        "West Somid"
    ],
    
    "10th of Ramadan City": [
        "10th of Ramadan City",
        "Industrial Zones",
        "Residential Districts"
    ],
    
    "New Administrative Capital": [
        "Government District",
        "Business District",
        "Residential Districts",
        "Diplomatic Quarter"
    ],
    
    "El Sheikh Zayed": [
        "Sheikh Zayed City",
        "Arkan",
        "Celia",
        "Vinci"
    ],
    
    "Badr City": [
        "Badr City",
        "Industrial Zone",
        "Residential Areas"
    ],
    
    "El Obour": [
        "El Obour City",
        "Industrial Zone",
        "Residential Areas"
    ],
    
    # مناطق أخرى
    "North Coast": [
        "Marina",
        "Hacienda",
        "Marassi",
        "Sidi Abdelrahman",
        "Al Alamein",
        "Ras El Hekma"
    ],
    
    "Ain Sokhna": [
        "Ain Sokhna",
        "Port Said",
        "El Alamein"
    ],
    
    "El Gouna": [
        "El Gouna",
        "Marina",
        "Downtown"
    ]
}

# ============================================================
# القائمة المسطحة للبحث السريع: City -> Area
# ============================================================
OFFICIAL_CITY_AREA_PAIRS = [
    ("Sharqia", "Zagazig"),
    ("Sharqia", "Minya El Qamh"),
    ("Sharqia", "Mashtol Al Souq"),
    ("Sharqia", "Hihya"),
    ("Sharqia", "El Qurein"),
    ("Sharqia", "El Qanayat"),
    ("Sharqia", "El Ibrahimiya"),
    ("Sharqia", "Diyarb Negm"),
    ("Sharqia", "Bilbeis"),
    ("Sharqia", "Abu Hammad"),
    
    ("Cairo", "Downtown"),
    ("Cairo", "Nasr City"),
    ("Cairo", "New Cairo"),
    ("Cairo", "Maadi"),
    ("Cairo", "Helwan"),
    ("Cairo", "Shorouk"),
    ("Cairo", "Ain Shams"),
    ("Cairo", "El Marg"),
    ("Cairo", "El Nozha"),
    ("Cairo", "Masr El Gadida"),
    ("Cairo", "Heliopolis"),
    ("Cairo", "Zamalek"),
    ("Cairo", "Dokki"),
    ("Cairo", "Mohandisen"),
    ("Cairo", "Manial"),
    
    ("Giza", "Faisal"),
    ("Giza", "Haram"),
    ("Giza", "Hadayk Ahram"),
    ("Giza", "Dokki"),
    ("Giza", "Mohandisen"),
    ("Giza", "Imbaba"),
    ("Giza", "Bolak Al Dakrour"),
    ("Giza", "Al Agouzah"),
    ("Giza", "Warak"),
    ("Giza", "Omrania"),
    
    ("Alexandria", "Al-agamy"),
    ("Alexandria", "Alex"),
    ("Alexandria", "Moharram Bek"),
    ("Alexandria", "Sidi Gaber"),
    ("Alexandria", "El-Raml"),
    ("Alexandria", "Montaza"),
    ("Alexandria", "Al Mamurah"),
    ("Alexandria", "Abu Qir"),
    ("Alexandria", "El-Agamy"),
    ("Alexandria", "Dekhela"),
    
    ("Aswan", "Aswan city"),
    ("Aswan", "New Aswan"),
    ("Aswan", "Kom Umbu"),
    ("Aswan", "Edfu"),
    ("Aswan", "Draw"),
    
    ("Asyut", "Asyut city"),
    ("Asyut", "New Asyut"),
    ("Asyut", "Abnub"),
    ("Asyut", "Abu Tij"),
    ("Asyut", "El-Ghanayem"),
    
    ("Banha", "Banha"),
    ("Banha", "Tukh"),
    ("Banha", "Shibin El Qanater"),
    ("Banha", "Qalyub"),
    ("Banha", "Kafr Shukr"),
    
    ("Behira", "Damanhour"),
    ("Behira", "Kafr El Dawwar"),
    ("Behira", "Rasheed"),
    ("Behira", "Edku"),
    ("Behira", "Abu Hummus"),
    
    ("BeniSuef", "Beni Suef city"),
    ("BeniSuef", "New Beni Suef"),
    ("BeniSuef", "Biba"),
    ("BeniSuef", "Al Fashn"),
    ("BeniSuef", "Ihnasiya"),
    
    ("Damietta", "Damietta"),
    ("Damietta", "New Damietta"),
    ("Damietta", "Ras El Bar"),
    ("Damietta", "Kafr Saad"),
    ("Damietta", "Kafr El Battikh"),
    
    ("Faiyum", "Faiyum center"),
    ("Faiyum", "New Faiyum"),
    ("Faiyum", "Ibsheway"),
    ("Faiyum", "Itsa"),
    ("Faiyum", "Sinnuris"),
    
    ("Gharbia", "Tanta"),
    ("Gharbia", "El Mahalla El Kubra"),
    ("Gharbia", "Zefta"),
    ("Gharbia", "Kafr El Zayat"),
    ("Gharbia", "Basyoun"),
    
    ("Ismailia", "Ismailia"),
    ("Ismailia", "Fayed"),
    ("Ismailia", "El Qantara"),
    ("Ismailia", "Tell El Kebir"),
    ("Ismailia", "Abu Suwir"),
    
    ("Kafr El-Sheikh", "Kafr El-Shaikh"),
    ("Kafr El-Sheikh", "Desouk"),
    ("Kafr El-Sheikh", "Biyala"),
    ("Kafr El-Sheikh", "Baltiem"),
    ("Kafr El-Sheikh", "El Reyad"),
    
    ("Luxor", "Luxor City"),
    ("Luxor", "New Luxor"),
    ("Luxor", "Armant"),
    ("Luxor", "Esna"),
    ("Luxor", "Al Qarnah"),
    
    ("Mansoura", "El Mansoura"),
    ("Mansoura", "Mit Ghamr"),
    ("Mansoura", "Talkha"),
    ("Mansoura", "Aga"),
    ("Mansoura", "El-Senbellawein"),
    
    ("Menya", "Minya City"),
    ("Menya", "New Menya"),
    ("Menya", "Beni Mazar"),
    ("Menya", "Matay"),
    ("Menya", "Maghagha"),
    
    ("Monufia", "Shibin el Kom"),
    ("Monufia", "Menouf"),
    ("Monufia", "Tala"),
    ("Monufia", "El Sadat City"),
    ("Monufia", "Ashmoun"),
    
    ("Port Said", "Port Said"),
    ("Port Said", "Port Fuad"),
    ("Port Said", "El Dawahy"),
    ("Port Said", "El Zohur"),
    ("Port Said", "El Sharq"),
    
    ("Qena", "Qena"),
    ("Qena", "New Qena"),
    ("Qena", "Nagaa Hammadi"),
    ("Qena", "Dishna"),
    ("Qena", "Qus"),
    
    ("Sohag", "Sohag"),
    ("Sohag", "New Sohag"),
    ("Sohag", "Akhmim"),
    ("Sohag", "New Akhmim"),
    ("Sohag", "Tahta"),
    
    ("Suez", "Suez"),
    ("Suez", "Port Tawfik"),
    ("Suez", "Arbaeen"),
    ("Suez", "Attaka"),
    ("Suez", "Faisal"),
    
    ("Red Sea", "Hurghada"),
    ("Red Sea", "Sharm El-Sheikh"),
    ("Red Sea", "Marsa Alam"),
    ("Red Sea", "Safaga"),
    ("Red Sea", "El Qusair"),
    
    ("Matrouh", "Marsa Matruh"),
    ("Matrouh", "El-Alamein"),
    ("Matrouh", "El Hamam"),
    ("Matrouh", "Sidi Barrani"),
    ("Matrouh", "Sallum"),
    
    ("New Valley", "Kharga"),
    ("New Valley", "Dakhla"),
    ("New Valley", "Farafra"),
    ("New Valley", "Baris"),
    
    ("South Sinai", "Sharm El-Sheikh"),
    ("South Sinai", "Dahab"),
    ("South Sinai", "Nuweiba"),
    ("South Sinai", "Taba"),
    
    ("North Sinai", "El Arish"),
    ("North Sinai", "Sheikh Zuweid"),
    ("North Sinai", "Rafah"),
    ("North Sinai", "Bir al-Abd"),
    
    ("6th of October", "Sheikh Zayed City"),
    ("6th of October", "6th of October City"),
    ("6th of October", "Smart Village"),
    ("6th of October", "West Somid"),
    
    ("10th of Ramadan City", "10th of Ramadan City"),
    ("10th of Ramadan City", "Industrial Zones"),
    ("10th of Ramadan City", "Residential Districts"),
    
    ("New Administrative Capital", "Government District"),
    ("New Administrative Capital", "Business District"),
    ("New Administrative Capital", "Residential Districts"),
    
    ("El Sheikh Zayed", "Sheikh Zayed City"),
    ("El Sheikh Zayed", "Arkan"),
    ("El Sheikh Zayed", "Celia"),
    ("El Sheikh Zayed", "Vinci"),
    
    ("Badr City", "Badr City"),
    ("Badr City", "Industrial Zone"),
    ("Badr City", "Residential Areas"),
    
    ("El Obour", "El Obour City"),
    ("El Obour", "Industrial Zone"),
    ("El Obour", "Residential Areas"),
    
    ("North Coast", "Marina"),
    ("North Coast", "Hacienda"),
    ("North Coast", "Marassi"),
    ("North Coast", "Sidi Abdelrahman"),
    
    ("Ain Sokhna", "Ain Sokhna"),
    ("Ain Sokhna", "Port Said"),
    ("Ain Sokhna", "El Alamein"),
    
    ("El Gouna", "El Gouna"),
    ("El Gouna", "Marina"),
    ("El Gouna", "Downtown")
]

# ============================================================
# الخرائط للتحويل من العربية إلى الإنجليزية (للواجهة)
# ============================================================
CITY_TRANSLATIONS_AR_TO_EN = {
    # محافظات
    "الشرقية": "Sharqia",
    "القاهرة": "Cairo",
    "الجيزة": "Giza",
    "الإسكندرية": "Alexandria",
    "أسوان": "Aswan",
    "أسيوط": "Asyut",
    "بني سويف": "BeniSuef",
    "البحيرة": "Behira",
    "دمياط": "Damietta",
    "الفيوم": "Faiyum",
    "الغربية": "Gharbia",
    "الإسماعيلية": "Ismailia",
    "كفر الشيخ": "Kafr El-Sheikh",
    "الأقصر": "Luxor",
    "المنوفية": "Monufia",
    "المنيا": "Menya",
    "القليوبية": "Qalyubia",
    "قنا": "Qena",
    "البحر الأحمر": "Red Sea",
    "المنصورة": "Mansoura",
    "بورسعيد": "Port Said",
    "سوهاج": "Sohag",
    "السويس": "Suez",
    "مطروح": "Matrouh",
    "شمال سيناء": "North Sinai",
    "جنوب سيناء": "South Sinai",
    "الوادي الجديد": "New Valley",
    
    # مدن
    "الزقازيق": "Zagazig",
    "بنها": "Banha",
    "طنطا": "Tanta",
    "المحلة الكبرى": "El Mahalla El Kubra",
    "دمنهور": "Damanhour",
    "المنصورة": "El Mansoura",
    "أسيوط": "Asyut city",
    "سوهاج": "Sohag",
    "قنا": "Qena",
    "الأقصر": "Luxor City",
    "أسوان": "Aswan city",
    "العريش": "El Arish",
    "شرم الشيخ": "Sharm El-Sheikh",
    "الغردقة": "Hurghada",
    "مرسى مطروح": "Marsa Matruh",
    "العين السخنة": "Ain Sokhna",
    "مدينة السادس من أكتوبر": "6th of October",
    "مدينة العاشر من رمضان": "10th of Ramadan City",
    "العاصمة الإدارية": "New Administrative Capital",
    "مدينة الشيخ زايد": "El Sheikh Zayed",
    "مدينة بدر": "Badr City",
    "مدينة العبور": "El Obour",
    "الساحل الشمالي": "North Coast",
    "الجونة": "El Gouna",
    
    # مناطق القاهرة
    "وسط البلد": "Downtown",
    "مدينة نصر": "Nasr City",
    "القاهرة الجديدة": "New Cairo",
    "المعادي": "Maadi",
    "حلوان": "Helwan",
    "الشروق": "Shorouk",
    "عين شمس": "Ain Shams",
    "المرج": "El Marg",
    "النزهة": "El Nozha",
    "مصر الجديدة": "Masr El Gadida",
    "هليوبوليس": "Heliopolis",
    "الزمالك": "Zamalek",
    "الدقي": "Dokki",
    "المهندسين": "Mohandisen",
    "المنيل": "Manial",
    
    # مناطق الجيزة
    "فيصل": "Faisal",
    "الهرم": "Haram",
    "حدائق الأهرام": "Hadayk Ahram",
    "إمبابة": "Imbaba",
    "بولاق الدكرور": "Bolak Al Dakrour",
    "العجوزة": "Al Agouzah",
    "الوراق": "Warak",
    "عمرانية": "Omrania",
    "كرداسة": "Kerdasa",
    "أبو رواش": "Abou Rawash",
    
    # مناطق الإسكندرية
    "العامرية": "Al-agamy",
    "سيدي جابر": "Sidi Gaber",
    "الرمل": "El-Raml",
    "المنتزة": "Montaza",
    "المعمورة": "Al Mamurah",
    "أبو قير": "Abu Qir",
    "العجمي": "El-Agamy",
    "الدخيلة": "Dekhela",
    "برج العرب": "Borg al arab",
    "سموحة": "Smouha",
    "سيدي بشر": "Sidi Bishr",
    "ميامي": "Miami",
    "ستانلي": "Stanley",
    "كامب شيزار": "Camp Shezar",
    "كليوباترا": "Cleopatra",
    "جليم": "Gleem",
    "لوران": "Laurent",
    "المندرة": "Mandara",
    "العصافرة": "Asafra",
    "الأنفوشي": "Al Anfoushi",
    "العطارين": "Al Attarin",
    "الجمرك": "Al Gomrok",
    "باب شرقي": "Bab Sharqi",
    "كرموز": "Karmouz",
    
    # مناطق أخرى
    "كفر الشيخ": "Kafr El-Shaikh",
    "دسوق": "Desouk",
    "فوة": "Fuwwah",
    "قلين": "Qallin",
    "مطوبس": "Metoubes",
    "سيدي سالم": "Sidi Salem",
    "الرحمانية": "Rahmaniya",
    "دكرنس": "Dikirnis",
    "منية النصر": "Menyet El Nasr",
    "شربين": "Shirbin",
    "ميت سلسيل": "Mit Salsil",
    "المطرية": "El Matareya",
    "المنزلة": "El Manzala",
    "الجميلية": "El Gamaliya",
    "بني عبيد": "Bani Ebeid",
    "الكرودي": "El Kurdi",
    
    "فاقوس": "Faqous",
    "أبو كبير": "Abu Kebir",
    "الحسينية": "El Husseiniya",
    "الصالحية": "El Salheya",
    "أولاد صقر": "Awlad Saqr",
    "كفر صقر": "Kafr Saqr",
    "منشأة أبو عمر": "Monshaat Abou Omar",
    "صان الحجر": "San Al Hagar",
    "تانيس": "Tanis",
    "ههيا": "Hihya",
    "أبو حماد": "Abu Hammad",
    "بلبيس": "Bilbeis",
    "ديرب نجم": "Diyarb Negm",
    "الإبراهيمية": "El Ibrahimiya",
    "القنايات": "El Qanayat",
    "القرين": "El Qurein",
    "منيا القمح": "Minya El Qamh",
    "مشتول السوق": "Mashtol Al Souq",
}

AREA_TRANSLATIONS_AR_TO_EN = {
    # مناطق الشرقية
    "الزقازيق": "Zagazig",
    "أبو كبير": "Abu Kabir",
    "ههيا": "Hehya",
    "فاقوس": "Faqous",
    "الصالحية": "El Salheya",
    "ديرب نجم": "Deirb Negm",
    "الحسينية": "El Husseiniya",
    "أولاد صقر": "Awlad Saqr",
    "كفر صقر": "Kafr Saqr",
    "بلبيس": "Bilbeis",
    "أبو حماد": "Abu Hammad",
    "الإبراهيمية": "El Ibrahimiya",
    "القنايات": "El Qanayat",
    "القرين": "El Qurein",
    "منيا القمح": "Minya El Qamh",
    "مشتول السوق": "Mashtol Al Souq",
    "صان الحجر": "San Al Hagar",
    "تانيس": "Tanis",
    "منشأة أبو عمر": "Monshaat Abou Omar",
    
    # مناطق القاهرة
    "المعادي": "Maadi",
    "المهندسين": "Mohandisen",
    "وسط البلد": "Downtown",
    "مدينة نصر": "Nasr City",
    "الشيخ زايد": "Sheikh Zayed",
    "السادس من أكتوبر": "6th of October",
    "العبور": "El Obour",
    "الرحاب": "Al Rehab",
    "التجمع الخامس": "The 5th Settlement",
    "التجمع الثالث": "The 3th Settlement",
    "التجمع الأول": "The 1th Settlement",
    "الشروق": "Al Shorouk",
    "مدينتي": "Madinaty",
    "المستقبل": "Future City",
    "بدر": "Badr City",
    "القاهرة الجديدة": "New Cairo",
    "الزمالك": "Zamalek",
    "المنيل": "Manial",
    "الفسطاط": "Al Fustat",
    "الدراسة": "Eldrasa",
    "باب اللوق": "Bab El loq",
    "الجزيرة": "Al Gezira",
    "الزاوية الحمراء": "El Zawya El Hamra",
    "الشرابية": "El Sharabiya",
    "شبرا": "Shubra",
    "الوايلي": "El Weili",
    "العباسية": "El-Abaseya",
    "الظاهر": "El Daher",
    "الساحل": "Elsahel",
    "بولاق": "Bulaq",
    "غمرة": "Ghamra",
    "حدائق القبة": "Hadaiq El Qobbah",
    "الزيتون": "El Zayton",
    "عين شمس": "Ain Shams",
    "المرج": "El Marg",
    "المطرية": "El Matareya",
    "السلام": "El Salam",
    "الشهداء": "El Shohada",
    "المنتزة": "El Montaza",
    "الأميرية": "El Amireya",
    "الخليفة": "El Khalifa",
    "المقطم": "El Mokattam",
    "البساتين": "El Basatin",
    "دار السلام": "Dar El Salam",
    "طرة": "Tura",
    "حلوان": "Helwan",
    "المعصرة": "El Maasara",
    "التبين": "Al Tebin",
    "15 مايو": "15 May City",
    
    # مناطق الجيزة
    "الدقي": "Dokki",
    "العجوزة": "Al Agouzah",
    "المهندسين": "Mohandisen",
    "إمبابة": "Imbaba",
    "بولاق الدكرور": "Bolak Al Dakrour",
    "أكتوبر": "October",
    "الحوامدية": "Al-Hawamidiyya",
    "البدرشين": "Badrashin",
    "الصف": "El Saf",
    "أطفيح": "Atfeh",
    "العياط": "El Ayat",
    "الوراق": "Al Warak",
    "كرداسة": "Kerdasa",
    "أبو النمرس": "Abu AL Numros",
    "الهرم": "Haram",
    "فيصل": "Faisal",
    "حدائق الأهرام": "Hadayk Ahram",
    "العمرانية": "Omrania",
    "أبو رواش": "Abou Rawash",
    "منشية البكري": "Monshaat Al Bakkari",
    "كيت كات": "Kit Kat",
    "المنيب": "Munib",
    "ترسة": "Tersa",
    "الطالبية": "El Talbeya",
    "المريوطية": "El Maryoutia",
    "الليثي": "Libyan",
    "ساقية مكي": "Saqiyet Mekki",
      # مناطق الإسكندرية
    "سيدي جابر": "Sidi Gaber",
    "الرمل": "El-Raml",
    "المعمورة": "Al Mamurah",
    "العجمي": "El-Agamy",
    "الدخيلة": "Dekhela",
    "برج العرب": "Borg al arab",
    "العامرية": "Al ameriya",
    "أبو قير": "Abu Qir",
    "المندرة": "Mandara",
    "العصافرة": "Asafra",
    "سيدي بشر": "Sidi Bishr",
    "المكس": "El Max",
    "المنتزة": "Montaza",
    "البيطاش": "El Biyoutash",
    "كرموز": "Karmouz",
    "محرم بك": "Moharram Bek",
    "الجمرك": "Al Gomrok",
    "العطارين": "Al Attarin",
    "باب شرقي": "Bab Sharqi",
    "اللبان": "El Labban",
    "المنشية": "El Mansheya",
    "الظاهرية": "El Zahireya",
    "القباري": "El Qabary",
    "الورديان": "El Wardian",
    "الأنفوشي": "Al Anfoushi",
    "الأزاريطة": "El Azarita",
    "بولكلي": "Bolkly",
    "كامب شيزار": "Camp Shezar",
    "ستانلي": "Stanley",
    "سموحة": "Smouha",
    "فلمنج": "Fleming",
    "زيزينيا": "Zizinia",
    "سابا باشا": "Saba Pasha",
    "جليم": "Gleem",
    "لوران": "Laurent",
    "سان ستيفانو": "San Stefano",
    "رشدي": "Roshdy",
    "سبورتنج": "Sporting",
    "الإبراهيمية": "El Ibrahimiya",
    "فيكتوريا": "Victoria",
    "سيدي كرير": "Sidi Kerir",
    "العامرية": "Al-agamy",
    
    # مناطق أخرى
    "طنطا": "Tanta",
    "المحلة الكبرى": "El Mahalla El Kubra",
    "زفتى": "Zefta",
    "كفر الزيات": "Kafr El Zayat",
    "بسيون": "Basyoun",
    "قطور": "Qutur",
    "سنبلاوين": "El-Senbellawein",
    "بلقاس": "Belqas",
    "ميت غمر": "Mit Ghamr",
    "أجا": "Aga",
    "تلا": "Tala",
    "شبرا الخيمة": "Shoubara El Khima",
    "الخانكة": "Al Khankah",
    "القناطر الخيرية": "El Qanater El Khayreya",
    "قليوب": "Qalyub",
    "شبين القناطر": "Shibin El Qanater",
    "كفر شكر": "Kafr Shukr",
    "طوخ": "Tukh",
    "بنها": "Banha",
    "قويسنا": "Quwaysna",
    "السادات": "El Sadat City",
    "أشمون": "Ashmoun",
    "الباجور": "El Bagour",
    "منوف": "Menouf",
    "سرس الليانة": "Sirs Al Layyanah",
    "شبين الكوم": "Shibin el Kom",
    "بركة السبع": "Birket El Sab",
    "الخَطاطبة": "Al Khatatbah",
    
    "دمنهور": "Damanhour",
    "كفر الدوار": "Kafr El Dawwar",
    "رشيد": "Rasheed",
    "إدكو": "Edku",
    "أبو حمص": "Abu Hummus",
    "إيتاي البارود": "Itay Al Barud",
    "شبراخيت": "Shubrakhit",
    "المحمودية": "Mahmoudiyah",
    "كوم حمادة": "Kom Hamada",
    "الدلنجات": "Al Delengat",
    "بدر": "Badr",
    
    "دمياط": "Damietta",
    "دمياط الجديدة": "New Damietta",
    "رأس البر": "Ras El Bar",
    "كفر سعد": "Kafr Saad",
    "كفر البطيخ": "Kafr El Battikh",
    "فارسكور": "Faraskur",
    "الروضة": "El Rodah",
    "السرو": "El Sarw",
    "الزرقا": "El Zarqa",
    
    "الفيوم": "Faiyum center",
    "الفيوم الجديدة": "New Faiyum",
    "إبشواي": "Ibsheway",
    "إطسا": "Itsa",
    "سنورس": "Sinnuris",
    "طامية": "Tamiyyah",
    "كفر عنجر": "Kufur an Nil",
    "يوسف الصديق": "youssef Elsdyq",
    "وادي الريان": "Wadi El-Rayyan",
    
    "الإسماعيلية": "Ismailia",
    "فايد": "Fayed",
    "القنطرة": "El Qantara",
    "التل الكبير": "Tell El Kebir",
    "أبو صوير": "Abu Suwir",
    "أبو سلطان": "Abu Sultan",
    "القصاصين": "El-Kasasin",
    "التجمعات الصناعية": "Industrial Zone in Ismailia",
    "المنطقة الحرة": "Ismailia Free Zone",
    "كسرفريت": "Ksarfrit",
    
    "كفر الشيخ": "Kafr El-Shaikh",
    "دسوق": "Desouk",
    "فوة": "Fuwwah",
    "قلين": "Qallin",
    "مطوبس": "Metoubes",
    "سيدي سالم": "Sidi Salem",
    "الرحمانية": "Rahmaniya",
    "الحامول": "El-Hamoul",
    "الرياض": "El Reyad",
    "برلس": "Burullus",
    "بيلا": "Biyala",
    "بلطيم": "Baltiem",
    
    "الأقصر": "Luxor City",
    "الأقصر الجديدة": "New Luxor",
    "أرمنت": "Armant",
    "إسنا": "Esna",
    "القرنة": "Al Qarnah",
    "المدامود": "Al Madamoud",
    "الطود": "Al Toud City",
    "الرادونية": "Al-Radwaniya",
    "البغدادي": "El-Boghdady",
    "مدينة البياضية": "Madinet Al Bayadeyah",
    "منشأة العماري": "Minshat Al Ammari",
    "طيبة": "Teba",
    "الهبيل": "Al Hebeel",
    
    "المنصورة": "El Mansoura",
    "ميت غمر": "Mit Ghamr",
    "طلخا": "Talkha",
    "أجا": "Aga",
    "سنبلاوين": "El-Senbellawein",
    "بلقاس": "Belqas",
    "جمصة": "Gamasa",
    "نبروه": "Nabaruh",
    "تمي الأمديد": "Tamai El Amadid",
    
    "المنيا": "Minya City",
    "المنيا الجديدة": "New Menya",
    "بني مزار": "Beni Mazar",
    "مطاي": "Matay",
    "مغاغة": "Maghagha",
    "سمالوط": "Samalut",
    "أبو قرقاص": "Abu Qurqas",
    "مدينة الأضواء": "Madinet Al Adwah",
    
    "بني سويف": "Beni Suef city",
    "بني سويف الجديدة": "New Beni Suef",
    "ببا": "Biba",
    "الفسطاط": "El Fashn",
    "إهناسيا": "Ihnasiya",
    "سمسطا": "Sumusta",
    "ناصر": "Nasser",
    "وادي النطرون": "Natrn Valley",
    "طريق الفيوم": "ELFAYOM ROAD",
    "عزيز مقبل": "Aziz Moqbel",
    "صلاح سالم": "Salah Salem",
    "عبد السلام عارف": "Abd El-Salam Aref",
    
    "بورسعيد": "Port Said",
    "بورفؤاد": "Port Fuad",
    "الضواحي": "El Dawahy",
    "الزهور": "El Zohur",
    "الشرق": "El Sharq",
    "المنسرة": "El Manasra",
    "المناخ": "El Manakh",
    "العمارة": "El Hay Elamarty",
    "الغرب": "EL GHARB",
    "الجنوب": "Al Ganoub",
    "العرب": "Qism El-Arab",
    "بورفؤاد 2": "Port Fuad 2",
    "حي مبارك": "Mubarak Neighborhood",
    
    "قنا": "Qena",
    "قنا الجديدة": "New Qena",
    "نجع حمادي": "Nagaa Hammadi",
    "دشنا": "Dishna",
    "قوص": "Qus",
    "قفط": "Qift",
    "نقادة": "Naqada",
    "الوقف": "Al Waqf",
    
    "سوهاج": "Sohag",
    "سوهاج الجديدة": "New Sohag",
    "أخميم": "Akhmim",
    "أخميم الجديدة": "New Akhmim",
    "طهطا": "Tahta",
    "طما": "Tima",
    "المنشأة": "Al Minshah",
    "المراغة": "Al Maraghah",
    "جهينة الغربية": "Juhaynah West",
    "جهينة": "Geheinah",
    "الكوتور": "El Kawtar",
    "العسيرات": "Aserat",
    "شندويل": "Shandawil",
    "ساقلتة": "Saqultah",
    
    "السويس": "Suez",
    "بورتوفيق": "Port Tawfik",
    "الأربعين": "Arbaeen",
    "عتاقة": "Attaka",
    "فيصل": "Faisal",
    "الجناين": "Ganayen",
    
    "أسوان": "Aswan city",
    "أسوان الجديدة": "New Aswan",
    "كوم أمبو": "Kom Umbu",
    "إدفو": "Edfu",
    "دراو": "Draw",
    "مدينة ناصر": "Nasr City",
    "مدينة نصر النوبة": "Madinet Nasr an Nobah",
    "الجعافرة": "Al Gaafrah",
    "طوشكى الجديدة": "New Tushka",
    
    "أسيوط": "Asyut city",
    "أسيوط الجديدة": "New Asyut",
    "أبنوب": "Abnub",
    "أبو تيج": "Abu Tij",
    "الغنايم": "El-Ghanayem",
    "منفلوط": "Manfalut",
    "ساحل سليم": "Sahel Selim",
    "صدفا": "Sodfa",
    "البداري": "Al Badari",
    "المعبدة": "Al Maabdah",
    "أسيوط غرب": "Asyut gharb",
    "أسيوط شرق": "Asyut Sharq",
    "الفتح": "EL Fateh",
    
    "شرم الشيخ": "Sharm El-Sheikh",
    "دهب": "Dahab",
    "نويبع": "Nuweiba",
    "طابا": "Taba",
    "رأس سدر": "Ras Sedr",
    "أبو رديس": "Abu Redis",
    "سانت كاترين": "Saint Catherine",
    "نخل": "Nakhl",
    
    "الغردقة": "Hurghada",
    "سفاجا": "Safaga",
    "مرسى علم": "Marsa Alam",
    "القصير": "El Qusair",
    "رأس غارب": "Ras Gharib",
    "ساحل حشيش": "Sahl Hasheesh",
    
    "مرسى مطروح": "Marsa Matruh",
    "العلمين": "El-Alamein",
    "الحمام": "El Hamam",
    "سيدي براني": "Sidi Barrani",
    "السلوم": "Sallum",
    "الضبعة": "El Dabaa",
    
    "الخارجة": "Kharga",
    "الداخلة": "Dakhla",
    "الفرافرة": "Farafra",
    "باريس": "Baris",
    "بلاط": "Balat",
    
    "العريش": "El Arish",
    "شيخ زويد": "Sheikh Zuweid",
    "رفح": "Rafah",
    "بئر العبد": "Bir al-Abd",
    "الحسنة": "El Hassana",
    "نخل": "Nakhl",
    
    "العين السخنة": "Ain Sokhna",
    "بورتوفيق": "Port Said",
    "العلمين": "El Alamein",
    "الزعفرانة": "Zaafarana",
    
    "الجونة": "El Gouna",
    "مارينا": "Marina",
    "وسط المدينة": "Downtown",
    "الكرم": "El Karm",
    
    "الساحل الشمالي": "North Coast",
    "مارينا": "Marina",
    "هاسيندا": "Hacienda",
    "مراسي": "Marassi",
    "سيدي عبدالرحمن": "Sidi Abdelrahman",
    "رأس الحكمة": "Ras El Hekma",
    "علم الرومي": "Alam El Rum",
    
    "مدينة الشيخ زايد": "Sheikh Zayed City",
    "أركان": "Arkan",
    "سيليا": "Celia",
    "فينشي": "Vinci",
    "الشروق": "Al Shorouk",
    "الأندلس": "Andalus",
    "الحي الأول": "First District",
    "الحي الثاني": "Second District",
    "الحي الثالث": "Third District",
    "الحي الرابع": "Fourth District",
    "الحي الخامس": "Fifth District",
    "الحي السادس": "Sixth District",
    "الحي السابع": "Seventh District",
    "الحي الثامن": "Eighth District",
    "الحي التاسع": "Ninth District",
    "الحي العاشر": "Tenth District",
    "القرية الذكية": "Smart Village",
    "غرب سوميد": "West Somid",
    "حي المتميز": "District motameez",
    
    "مدينة العاشر من رمضان": "10th of Ramadan City",
    "الحي الأول": "Neighborhoods 1 to 17",
    "الحي الثاني": "Neighborhoods 18 to 34",
    "الحي الثالث": "Neighborhoods 35 to 50",
    "الحي الرابع": "Neighborhoods 51 to 66",
    "الحي الخامس": "Neighborhoods 67 to 99",
    "المنطقة الصناعية الأولى": "First Industrial Zone",
    "المنطقة الصناعية الثانية": "Second Industrial Zone",
    "المنطقة الصناعية الثالثة": "Third Industrial Zone",
    "الحي 11": "district 11",
    "الحي 12": "district 12",
    "الحي 10": "district 10",
    "الحي 13": "district 13",
    "الحي 14": "district 14",
    "الحي 15": "district 15",
    "الحي 16": "district 16",
    "الحي 28": "district 28",
    "الحي 29": "district 29",
    "الحي 30": "district 30",
    "الحي 31": "district 31",
    "الحي 32": "district 32",
    "الحي 33": "district 33",
    "حي الأندلس": "Andalus district",
    "منطقة الشهابي": "Al-Shahabi Area",
    "صناعية مصر النور": "Sanyia Misr Al-Nour",
    "صناعية مصر الحجاز": "Sanyia Misr Al-Hijaz",
    "الأردنية": "Al-Urduniya",
    "صدنوي": "Sidnawi",
    
    "العاصمة الإدارية": "New Administrative Capital",
    "الحي الحكومي": "Government District",
    "الحي المالي": "Business District",
    "الحي الدبلوماسي": "Diplomatic Quarter",
    "الأحياء السكنية": "Residential Districts",
    "الحي الأول": "First District",
    "الحي الثاني": "Second District",
    "الحي الثالث": "Third District",
    "الرابعة": "Fourth District",
    "الخامسة": "Fifth District",
    "المنطقة المركزية": "Central District",
    "المنطقة الشرقية": "Eastern District",
    "المنطقة الغربية": "Western District",
    
    "مدينة بدر": "Badr City",
    "المنطقة الصناعية": "Industrial Zone",
    "الأحياء السكنية": "Residential Areas",
    "الحي الأول": "First District",
    "الحي الثاني": "Second District",
    "الحي الثالث": "Third District",
    "الحي الرابع": "Fourth District",
    
    "مدينة العبور": "El Obour City",
    "المنطقة الصناعية": "Industrial Zone",
    "الأحياء السكنية": "Residential Areas",
    "الحي الأول": "First District",
    "الحي الثاني": "Second District",
    "الحي الثالث": "Third District",
    "الحي الرابع": "Fourth District",
    "الحي الخامس": "Fifth District",
    
    "القاهرة الجديدة": "New Cairo",
    "التجمع الخامس": "The 5th Settlement",
    "التجمع الثالث": "The 3th Settlement",
    "التجمع الأول": "The 1th Settlement",
    "الرحاب": "Al Rehab",
    "المستقبل": "Future City",
    "مدينتي": "Madinaty",
    "الشروق": "Al Shorouk",
    "الروبيكي": "El Robeiki",
    "العبور": "El Obour",
    
    "مدينة نصر": "Nasr City",
    "الحي الأول": "First District",
    "الحي الثاني": "Second District",
    "الحي الثالث": "Third District",
    "الحي الرابع": "Fourth District",
    "الحي الخامس": "Fifth District",
    "الحي السادس": "Sixth District",
    "الحي السابع": "Seventh District",
    "الحي الثامن": "Eighth District",
    "الحي التاسع": "Ninth District",
    "الحي العاشر": "Tenth District",
    "الحي الحادي عشر": "Eleventh District",
    "الحي الثاني عشر": "Twelfth District",
    "المنطقة الصناعية": "Industrial Zone",
    "المنطقة الخضراء": "Green Area",
    "المنطقة الحرة": "Free Zone",
    "المنطقة التجارية": "Commercial Zone",
    "المنطقة السكنية": "Residential Zone",
    "المنطقة السياحية": "Touristic Zone",
    "المنطقة التعليمية": "Educational Zone",
    "المنطقة الطبية": "Medical Zone",
    "المنطقة الرياضية": "Sports Zone",
    "المنطقة الثقافية": "Cultural Zone",
    "المنطقة الترفيهية": "Entertainment Zone",
    "المنطقة الدينية": "Religious Zone",
    "المنطقة الحكومية": "Governmental Zone",
    "المنطقة العسكرية": "Military Zone",
    "المنطقة الأمنية": "Security Zone",
    "المنطقة الدبلوماسية": "Diplomatic Zone",
    "المنطقة الدولية": "International Zone",
    "المنطقة العربية": "Arab Zone",
    "المنطقة الأفريقية": "African Zone",
    "المنطقة الآسيوية": "Asian Zone",
    "المنطقة الأوروبية": "European Zone",
    "المنطقة الأمريكية": "American Zone",
    "المنطقة العالمية": "Global Zone",
    "المنطقة المحلية": "Local Zone",
    "المنطقة الإقليمية": "Regional Zone",
    "المنطقة الوطنية": "National Zone",
    "المنطقة القومية": "Nationalist Zone",
    "المنورة الشعبية": "Popular Zone",
    "المنورة الرسمية": "Official Zone",
    "المنورة الخاصة": "Private Zone",
    "المنورة العامة": "Public Zone",
    "المنورة المختلطة": "Mixed Zone",
    "المنورة المغلقة": "Closed Zone",
    "المنورة المفتوحة": "Open Zone",
    "المنورة المحمية": "Protected Zone",
    "المنورة المؤقتة": "Temporary Zone"}

# ============================================================
# دوال مساعدة للتعامل مع القوائم
# ============================================================

def get_cities_list():
    """الحصول على قائمة المدن المتاحة."""
    return sorted(list(OFFICIAL_CITIES_AREAS.keys()))

def get_areas_by_city(city):
    """الحصول على قائمة المناطق لمدينة معينة."""
    return OFFICIAL_CITIES_AREAS.get(city, [])

def translate_city_ar_to_en(arabic_city):
    """ترجمة المدينة من العربية إلى الإنجليزية."""
    return CITY_TRANSLATIONS_AR_TO_EN.get(arabic_city, arabic_city)

def translate_area_ar_to_en(arabic_area):
    """ترجمة المنطقة من العربية إلى الإنجليزية."""
    return AREA_TRANSLATIONS_AR_TO_EN.get(arabic_area, arabic_area)

def translate_city_en_to_ar(english_city):
    """ترجمة المدينة من الإنجليزية إلى العربية."""
    # البحث العكسي
    for ar, en in CITY_TRANSLATIONS_AR_TO_EN.items():
        if en == english_city:
            return ar
    return english_city

def translate_area_en_to_ar(english_area):
    """ترجمة المنطقة من الإنجليزية إلى العربية."""
    # البحث العكسي
    for ar, en in AREA_TRANSLATIONS_AR_TO_EN.items():
        if en == english_area:
            return ar
    return english_area

def is_valid_city_area_pair(city, area):
    """التحقق من أن المدينة والمنطقة متطابقتان."""
    if city in OFFICIAL_CITIES_AREAS:
        return area in OFFICIAL_CITIES_AREAS[city]
    return False

def get_suggestions_for_city(city_query):
    """الحصول على اقتراحات لمدينة بناءً على بحث."""
    suggestions = []
    city_query_lower = city_query.lower()
    
    # البحث في المدن الإنجليزية
    for city in OFFICIAL_CITIES_AREAS.keys():
        if city_query_lower in city.lower():
            suggestions.append(city)
    
    # البحث في الترجمات العربية
    for arabic_city, english_city in CITY_TRANSLATIONS_AR_TO_EN.items():
        if city_query_lower in arabic_city.lower():
            if english_city not in suggestions:
                suggestions.append(english_city)
    
    return suggestions[:10]  # إرجاع أول 10 اقتراحات فقط

def get_suggestions_for_area(area_query, city=None):
    """الحصول على اقتراحات لمنطقة بناءً على بحث."""
    suggestions = []
    area_query_lower = area_query.lower()
    
    if city and city in OFFICIAL_CITIES_AREAS:
        # البحث في مناطق مدينة محددة
        for area in OFFICIAL_CITIES_AREAS[city]:
            if area_query_lower in area.lower():
                suggestions.append(area)
    else:
        # البحث في جميع المناطق
        for areas_list in OFFICIAL_CITIES_AREAS.values():
            for area in areas_list:
                if area_query_lower in area.lower() and area not in suggestions:
                    suggestions.append(area)
    
    # البحث في الترجمات العربية
    for arabic_area, english_area in AREA_TRANSLATIONS_AR_TO_EN.items():
        if area_query_lower in arabic_area.lower():
            if english_area not in suggestions:
                suggestions.append(english_area)
    
    return suggestions[:10]  # إرجاع أول 10 اقتراحات فقط
