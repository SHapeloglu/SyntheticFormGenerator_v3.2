from __future__ import annotations

import random
from datetime import date, timedelta
from typing import Any

from faker import Faker

fake = Faker("tr_TR")

IZMIR_DISTRICTS = [
    "Balçova", "Bornova", "Buca", "Karşıyaka", "Konak", "Bayraklı",
    "Gaziemir", "Çiğli", "Narlıdere", "Güzelbahçe", "Urla", "Menemen",
    "Torbalı", "Menderes", "Kemalpaşa", "Seferihisar", "Aliağa", "Foça",
    "Karabağlar",
]

IZMIR_STORES = [
    {"district": district, "store": f"Migros {random.choice(['Jet', 'MMM', '3M'])} {district}"}
    for district in IZMIR_DISTRICTS
]

JOB_PROFILES: list[dict[str, str]] = [
    {"profession": "Kasiyer", "job": "Kasa işlemleri ve müşteri ödemeleri", "department": "Kasalar", "previous_sector": "Perakende", "previous_job": "Kasiyer"},
    {"profession": "Kasa Görevlisi", "job": "Kasa açılış, kapanış ve ödeme işlemleri", "department": "Kasalar", "previous_sector": "Perakende", "previous_job": "Kasa Görevlisi"},
    {"profession": "Reyon Görevlisi", "job": "Raf düzenleme ve ürün yerleştirme", "department": "Kuru Gıda", "previous_sector": "Perakende", "previous_job": "Reyon Görevlisi"},
    {"profession": "Reyon Sorumlusu", "job": "Reyon düzeni ve stok takibi", "department": "Kuru Gıda", "previous_sector": "Perakende", "previous_job": "Reyon Sorumlusu"},
    {"profession": "Manav Personeli", "job": "Meyve sebze hazırlama ve reyon düzeni", "department": "Manav", "previous_sector": "Gıda Perakendeciliği", "previous_job": "Manav Personeli"},
    {"profession": "Şarküteri Personeli", "job": "Şarküteri ürünlerini hazırlama ve satış", "department": "Şarküteri", "previous_sector": "Gıda Perakendeciliği", "previous_job": "Şarküteri Personeli"},
    {"profession": "Kasap", "job": "Et ürünlerini hazırlama ve satış", "department": "Et Reyonu", "previous_sector": "Gıda", "previous_job": "Kasap"},
    {"profession": "Kasap Yardımcısı", "job": "Et hazırlama ve reyon desteği", "department": "Et Reyonu", "previous_sector": "Gıda", "previous_job": "Kasap Yardımcısı"},
    {"profession": "Balık Reyonu Personeli", "job": "Balık temizleme, hazırlama ve satış", "department": "Balık Reyonu", "previous_sector": "Gıda", "previous_job": "Balık Reyonu Personeli"},
    {"profession": "Unlu Mamuller Personeli", "job": "Ekmek ve unlu mamul hazırlama", "department": "Unlu Mamuller", "previous_sector": "Gıda", "previous_job": "Fırın Personeli"},
    {"profession": "Depo Personeli", "job": "Ürün kabul, istifleme ve depolama", "department": "Depo", "previous_sector": "Lojistik", "previous_job": "Depo Personeli"},
    {"profession": "Mal Kabul Personeli", "job": "Gelen ürünleri teslim alma ve kontrol", "department": "Mal Kabul", "previous_sector": "Lojistik", "previous_job": "Mal Kabul Elemanı"},
    {"profession": "Stok Kontrol Personeli", "job": "Sayım ve stok kontrol işlemleri", "department": "Depo", "previous_sector": "Lojistik", "previous_job": "Stok Kontrol Personeli"},
    {"profession": "Forklift Operatörü", "job": "Palet taşıma, yükleme ve istifleme", "department": "Depo", "previous_sector": "Lojistik", "previous_job": "Forklift Operatörü"},
    {"profession": "Sevkiyat Personeli", "job": "Ürün sevki ve mağaza transferi", "department": "Sevkiyat", "previous_sector": "Lojistik", "previous_job": "Sevkiyat Personeli"},
    {"profession": "Online Sipariş Toplama Personeli", "job": "Online sipariş ürünlerini toplama", "department": "E-Ticaret", "previous_sector": "Perakende", "previous_job": "Sipariş Toplama Personeli"},
    {"profession": "Temizlik Personeli", "job": "Mağaza ve ortak alan temizliği", "department": "Temizlik", "previous_sector": "Hizmet", "previous_job": "Temizlik Görevlisi"},
    {"profession": "Güvenlik Görevlisi", "job": "Mağaza güvenliği ve giriş kontrolü", "department": "Güvenlik", "previous_sector": "Güvenlik", "previous_job": "Güvenlik Görevlisi"},
    {"profession": "Vardiya Sorumlusu", "job": "Vardiya planlama ve operasyon yönetimi", "department": "Operasyon", "previous_sector": "Perakende", "previous_job": "Reyon Sorumlusu"},
    {"profession": "Mağaza Müdür Yardımcısı", "job": "Mağaza operasyon ve ekip yönetimi", "department": "Yönetim", "previous_sector": "Perakende", "previous_job": "Vardiya Sorumlusu"},
]

PREVIOUS_EMPLOYERS = [
    "CarrefourSA", "ŞOK Marketler", "A101 Yeni Mağazacılık", "BİM Birleşik Mağazalar",
    "File Market", "Metro Türkiye", "Bizim Toptan", "Hakmar Express", "Onur Market",
    "Happy Center", "Kim Market", "Çağrı Market", "Pehlivanoğlu Market", "Mopaş Market",
    "Migros Ticaret A.Ş.",
]

EXAM_FIELDS = {
    "a) Göz": {
        "minimal": ["NFM", "Normal", "Doğal", "N"],
        "normal": ["Doğal", "Görme doğal", "Konjonktiva doğal", "Gözlükle görme yeterli"],
        "detailed": ["Konjonktivalar doğal, görme yeterli", "Gözlükle görme yeterli; patoloji yok"],
    },
    "a) Kulak-Burun-Boğaz": {
        "minimal": ["NFM", "Normal", "Doğal", "N"],
        "normal": ["Doğal", "Orofarenks doğal", "KBB doğal", "Patoloji yok"],
        "detailed": ["Orofarenks ve nazal mukoza doğal", "KBB muayenesinde patoloji yok"],
    },
    "a) Deri": {
        "minimal": ["N", "Normal", "Doğal", "Lezyon yok"],
        "normal": ["Doğal", "Aktif lezyon yok", "Patoloji yok", "Hafif kuruluk"],
        "detailed": ["Aktif dermatolojik lezyon yok", "Deri doğal, enfeksiyöz lezyon yok"],
    },
    "b) Kardiyovasküler Sistem": {
        "minimal": ["NFM", "Normal", "Doğal", "S1 S2 doğal"],
        "normal": ["S1-S2 doğal", "Ritmik, ek ses yok", "KVS doğal", "Periferik nabızlar açık"],
        "detailed": ["S1-S2 doğal ve ritmik, ek ses yok", "Kalp sesleri doğal; nabızlar açık"],
    },
    "c) Solunum Sistemi": {
        "minimal": ["NFM", "Normal", "Doğal", "Ral yok"],
        "normal": ["Solunum sesleri doğal", "Raller yok", "Akciğer doğal", "Ek ses yok"],
        "detailed": ["Solunum eşit; ral ve ronküs yok", "Solunum sesleri bilateral doğal"],
    },
    "d) Sindirim Sistemi": {
        "minimal": ["NFM", "Normal", "Doğal", "Batın rahat"],
        "normal": ["Batın rahat", "Hassasiyet yok", "Barsak sesleri doğal", "GİS doğal"],
        "detailed": ["Batın rahat; defans, rebound yok", "Barsak sesleri doğal; hassasiyet yok"],
    },
    "e) Ürogenital Sistem": {
        "minimal": ["NFM", "Normal", "Doğal", "Yakınma yok"],
        "normal": ["Doğal", "Yakınma yok", "ÜGS doğal", "Patoloji yok"],
        "detailed": ["Ürogenital yakınma yok; muayene olağan", "Ürogenital sistemde özellik yok"],
    },
    "f) Kas-İskelet Sistemi": {
        "minimal": ["NFM", "Normal", "Doğal", "EHA açık"],
        "normal": ["Eklem hareketleri açık", "Kas gücü tam", "Bel hareketleri doğal", "KİS doğal"],
        "detailed": ["Eklem hareketleri tam, kas gücü doğal", "Omurga ve ekstremite hareketleri doğal"],
    },
    "g) Nörolojik Muayene": {
        "minimal": ["NFM", "Normal", "Doğal", "Defisit yok"],
        "normal": ["Nörolojik defisit yok", "Bilinç açık", "Refleksler doğal", "Nörolojik doğal"],
        "detailed": ["Bilinç açık, koopere; defisit yok", "Kraniyal sinirler ve refleksler doğal"],
    },
    "h) Psikiyatrik Muayene": {
        "minimal": ["NFM", "Normal", "Doğal", "Koopere"],
        "normal": ["Koopere ve oryante", "Duygudurum doğal", "İletişimi uygun", "Psikiyatrik doğal"],
        "detailed": ["Koopere, oryante; duygudurum doğal", "İletişimi uygun; psikopatoloji yok"],
    },
    "i) Diğer Muayene": {
        "minimal": ["Yok", "-", "N", "Ek yok"],
        "normal": ["Ek bulgu yok", "Yok", "Doğal", "Özellik yok"],
        "detailed": ["Ek patolojik muayene bulgusu yok", "Diğer sistem muayenelerinde özellik yok"],
    },
}

PROFILE_LABELS = {
    "minimal": "Minimalist (kısa tıbbi ifadeler)",
    "normal": "Normal (orta ayrıntı)",
    "detailed": "Ayrıntılı",
}

PROFILE_WEIGHTS = ["minimal"] * 4 + ["normal"] * 4 + ["detailed"] * 2


def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, max(0, (end - start).days)))


def fake_phone() -> str:
    return f"05{random.randint(30, 55):02d} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}"


def fake_name(gender: str) -> str:
    first = fake.first_name_male() if gender == "Erkek" else fake.first_name_female()
    return f"{first} {fake.last_name()}"


def synthetic_tc(index: int) -> str:
    """Algoritmik olarak geçerli biçimde 11 rakamlı, yalnızca test amaçlı numara üretir."""
    seed = 100_000_000 + index
    first9 = [int(c) for c in str(seed)[:9]]
    tenth = ((sum(first9[0::2]) * 7) - sum(first9[1::2])) % 10
    eleventh = (sum(first9) + tenth) % 10
    return "".join(map(str, first9 + [tenth, eleventh]))


def maybe(value: Any, probability: float) -> Any:
    return value if random.random() < probability else ""


def empty_previous_job() -> dict[str, Any]:
    return {"İşyeri": "", "İşkolu": "", "Yaptığı İş/Mesleği": "", "Giriş-Çıkış": ""}


def previous_job_groups(
    profile: dict[str, str],
    birth_year: int,
    first_probability: float,
    second_probability: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Generate up to two chronological, non-overlapping previous jobs."""
    if random.random() >= first_probability:
        return empty_previous_job(), empty_previous_job()

    earliest = max(2008, birth_year + 16)
    latest_end = 2025
    if earliest >= latest_end:
        return empty_previous_job(), empty_previous_job()

    use_second = random.random() < second_probability and earliest <= latest_end - 4
    employers = random.sample(PREVIOUS_EMPLOYERS, k=2 if use_second else 1)

    if use_second:
        # Job 1 is the older job; Job 2 is the newer one. At least one year
        # separates their date ranges, so they never overlap.
        first_start_max = latest_end - 4
        first_start = random.randint(earliest, first_start_max)
        first_end = random.randint(first_start + 1, min(first_start + 5, latest_end - 2))
        second_start = random.randint(first_end + 1, latest_end - 1)
        second_end = random.randint(second_start + 1, latest_end)
        ranges = ((first_start, first_end), (second_start, second_end))
    else:
        start = random.randint(earliest, latest_end - 1)
        end = random.randint(start + 1, latest_end)
        ranges = ((start, end),)

    groups: list[dict[str, Any]] = []
    for employer, (start_year, end_year) in zip(employers, ranges):
        groups.append({
            "İşyeri": employer,
            "İşkolu": profile["previous_sector"],
            "Yaptığı İş/Mesleği": profile["previous_job"],
            "Giriş-Çıkış": f"{start_year} - {end_year}",
        })

    if len(groups) == 1:
        groups.append(empty_previous_job())
    return groups[0], groups[1]


def choose_profile(requested: str) -> str:
    return random.choice(PROFILE_WEIGHTS) if requested == "random" else requested


def add_exam(record: dict[str, Any], profile: str) -> None:
    # Gerçek formlarda tüm sistemlerin her zaman doldurulmamasını taklit eder.
    probabilities = {
        "a) Göz": 0.86, "a) Kulak-Burun-Boğaz": 0.86, "a) Deri": 0.72,
        "b) Kardiyovasküler Sistem": 0.88, "c) Solunum Sistemi": 0.88,
        "d) Sindirim Sistemi": 0.58, "e) Ürogenital Sistem": 0.28,
        "f) Kas-İskelet Sistemi": 0.62, "g) Nörolojik Muayene": 0.42,
        "h) Psikiyatrik Muayene": 0.30, "i) Diğer Muayene": 0.36,
    }
    for field, variants in EXAM_FIELDS.items():
        record[field] = random.choice(variants[profile]) if random.random() < probabilities[field] else ""

    result_options = {
        "minimal": ["Çalışabilir", "İşe uygundur", "Periyodik muayene uygundur", "Kontrol önerilir"],
        "normal": ["Yapacağı işe uygundur.", "Sağlık yönünden çalışmasında sakınca yoktur.", "Periyodik kontrol ile çalışabilir.", "Gözlük kullanımıyla çalışabilir."],
        "detailed": ["Yapacağı işte çalışmasında sakınca yoktur.", "Önlemler ve periyodik kontrollerle çalışabilir.", "Ek değerlendirme sonrası yeniden değerlendirilmelidir."],
    }
    record["Kanaat ve Sonuç"] = random.choice(result_options[profile])


def generate_person(index: int, fill_rate: int = 85, doctor_profile: str = "random") -> dict[str, Any]:
    if doctor_profile not in {"random", "minimal", "normal", "detailed"}:
        raise ValueError("Geçersiz doktor profili.")

    gender = "Erkek" if index % 2 else "Kadın"
    store = random.choice(IZMIR_STORES)
    job = random.choice(JOB_PROFILES)
    profile = choose_profile(doctor_profile)
    birth_date = random_date(date(1974, 1, 1), date(2004, 12, 31))
    height = random.randint(165, 195) if gender == "Erkek" else random.randint(155, 178)
    weight = random.randint(58, 118) if gender == "Erkek" else random.randint(48, 92)
    bmi = round(weight / ((height / 100) ** 2), 1)
    optional_rate = max(0.30, min(1.0, fill_rate / 100))

    prev1, prev2 = previous_job_groups(
        job,
        birth_year=birth_date.year,
        first_probability=min(0.95, optional_rate + 0.10),
        second_probability=max(0.20, optional_rate - 0.25),
    )
    today = date.today()

    record: dict[str, Any] = {
        "Kayıt No": f"TEST-{index:05d}",
        "Veri Durumu": "SENTETİK OCR/HTR TEST VERİSİ",
        "Muayene Yazım Profili": PROFILE_LABELS[profile],
        "İşyeri Ünvanı": "Migros Ticaret A.Ş.",
        "SGK Sicil No": f"TEST-SGK-{random.randint(100000, 999999)}",
        "İşyeri Adresi": f"{store['store']}, {store['district']} / İzmir",
        "İşyeri Tel/Faks": fake_phone(),
        "Çalışanın Adı Soyadı": fake_name(gender),
        "T.C. Kimlik No": synthetic_tc(index),
        "Doğum Yeri": random.choice(IZMIR_DISTRICTS),
        "Doğum Tarihi": birth_date,
        "Cinsiyeti": gender,
        "Eğitim Durumu": random.choice(["İlköğretim", "Ortaokul", "Lise", "Meslek Lisesi", "Ön Lisans", "Lisans"]),
        "Ev Adresi": maybe(f"{store['district']} Mah. {random.randint(100,999)} Sok. No:{random.randint(1,80)} D:{random.randint(1,20)} {store['district']} / İzmir", optional_rate),
        "Mesleği": job["profession"],
        "Medeni Durumu": maybe(random.choice(["Bekâr", "Evli"]), min(0.98, optional_rate + 0.12)),
        "Tel (Cep)": fake_phone(),
        "Yaptığı İş": job["job"],
        "Çalıştığı Bölüm": job["department"],
        "Bilinen Alerji Öyküsü": maybe(random.choice(["Yok", "Polen", "Ev tozu", "Lateks", "Penisilin", "Mevsimsel alerji"]), optional_rate),
        "Konjenital / Kronik Hastalık": maybe(random.choice(["Yok", "Astım öyküsü", "Migren öyküsü", "Hipertansiyon öyküsü", "Reflü öyküsü"]), optional_rate),
        "Kan Grubu": random.choice(["A", "B", "AB", "0"]),
        "Rh": random.choice(["(+)", "(-)"]),
        "Tetanoz": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor", "2024 rapel"]), optional_rate),
        "Hepatit A": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor"]), max(0.35, optional_rate - 0.20)),
        "Hepatit B": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor", "3 doz"]), max(0.40, optional_rate - 0.15)),
        "Diğer Aşı": maybe(random.choice(["Yok", "Grip", "COVID-19 3 doz"]), max(0.25, optional_rate - 0.30)),
        "Soygeçmiş - Anne": maybe(random.choice(["Sağlıklı", "Hipertansiyon", "Diyabet", "Vefat"]), optional_rate),
        "Soygeçmiş - Baba": maybe(random.choice(["Sağlıklı", "Hipertansiyon", "Kalp hastalığı", "Vefat"]), optional_rate),
        "Soygeçmiş - Kardeş": maybe(random.choice(["Sağlıklı", "Yok", "Astım"]), max(0.35, optional_rate - 0.15)),
        "Soygeçmiş - Çocuk": maybe(random.choice(["Yok", "Sağlıklı"]), max(0.35, optional_rate - 0.15)),
        "TA": f"{random.randint(105,145)}/{random.randint(65,95)}",
        "Nabız": random.randint(60, 96),
        "Boy": height,
        "Kilo": weight,
        "BMI": bmi,
        "Form Tarihi": today,
    }

    for number, group in ((1, prev1), (2, prev2)):
        for suffix, value in group.items():
            record[f"Önceki İş {number} - {suffix}"] = value

    # Checkbox ağırlıklı anamnez alanları: kartta yalnızca işaretlenecek değer saklanır.
    history_questions = [
        "Hastanede Yattınız mı", "Ameliyat Oldunuz mu", "İş Kazası Geçirdiniz mi",
        "Meslek Hastalığı Tetkiki", "Maluliyet Aldınız mı", "Tedavi Görüyor musunuz",
    ]
    for question in history_questions:
        yes = random.random() < 0.10
        record[f"{question} - Hayır"] = "X" if not yes else ""
        record[f"{question} - Evet"] = "X" if yes else ""
        record[f"{question} - Açıklama"] = random.choice(["Geçmiş öykü", "Kontrol altında", "Operasyon öyküsü"]) if yes else ""

    record.update({
        "Sigara - Hayır": "X", "Sigara - Bırakmış": "", "Sigara - Evet": "",
        "Sigara - Adet/Gün": "", "Sigara - Yıl": "",
        "Alkol - Hayır": "X", "Alkol - Bırakmış": "", "Alkol - Evet": "",
        "Alkol - Miktar": "", "Alkol - Yıl": "",
    })

    add_exam(record, profile)

    # Laboratuvar alanları gerçek kullanıma uygun biçimde çoğunlukla boş kalır.
    lab_probability = {"minimal": 0.12, "normal": 0.22, "detailed": 0.35}[profile]
    lab_fields = {
        "a) Biyolojik Analizler - Kan": ["N", "Normal", "Hemogram doğal"],
        "a) Biyolojik Analizler - İdrar": ["N", "Negatif", "İdrar doğal"],
        "a) Biyolojik Analizler - Gaita": ["İstenmedi", "Negatif", "Doğal"],
        "b) Radyolojik Analizler": ["AC grafisi doğal", "İstenmedi", "Patoloji yok"],
        "c) Fizyolojik Analizler - Odyometri": ["Normal", "İstenmedi", "N"],
        "c) Fizyolojik Analizler - SFT": ["Normal", "İstenmedi", "N"],
        "d) Psikolojik Testler": ["Uygulanmadı", "Normal", "-"],
        "e) Diğer Laboratuvar": ["Yok", "-", "Ek tetkik yok"],
    }
    for field, options in lab_fields.items():
        record[field] = random.choice(options) if random.random() < lab_probability else ""

    return record


def generate_records(count: int, fill_rate: int = 85, doctor_profile: str = "random", start_index: int = 1) -> list[dict[str, Any]]:
    if count < 1:
        raise ValueError("Kayıt sayısı en az 1 olmalıdır.")
    if count > 50_000:
        raise ValueError("Tek seferde en fazla 50.000 kayıt üretilebilir.")
    if not 0 <= fill_rate <= 100:
        raise ValueError("Doluluk oranı 0 ile 100 arasında olmalıdır.")
    if start_index < 1:
        raise ValueError("Başlangıç numarası en az 1 olmalıdır.")
    return [
        generate_person(index=i, fill_rate=fill_rate, doctor_profile=doctor_profile)
        for i in range(start_index, start_index + count)
    ]
