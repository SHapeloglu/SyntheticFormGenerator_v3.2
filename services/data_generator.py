from __future__ import annotations

import copy
import random
from datetime import date, timedelta
from typing import Any

from faker import Faker

fake = Faker("tr_TR")

# ---------------------------------------------------------------------------
# Form şeması: matbu EK-2 formundaki her kutu = bir satır.
# (OCR alan adı = faz1-trocr-main sablon_koordinatlari.json anahtarı, kart etiketi, sayfa, kart bölümü)
# Kart etiketi kayıtta anahtar olarak kullanılır; OCR dışa aktarımı OCR alan adıyla yazar.
# ---------------------------------------------------------------------------

ANAMNEZ1 = [
    ("anamnez1_balgamli_oksuruk", "Balgamlı öksürük"),
    ("anamnez1_nefes_darligi", "Nefes darlığı"),
    ("anamnez1_gogus_agrisi", "Göğüs ağrısı"),
    ("anamnez1_carpinti", "Çarpıntı"),
    ("anamnez1_sirt_agrisi", "Sırt ağrısı"),
    ("anamnez1_ishal_kabizlik", "İshal / kabızlık"),
    ("anamnez1_eklemlerde_agri", "Eklemlerde ağrı"),
    ("anamnez1_diger", "Diğer şikâyet"),
]
ANAMNEZ2 = [
    ("anamnez2_kalp_hastaligi", "Kalp hastalığı"),
    ("anamnez2_seker_hastaligi", "Şeker hastalığı"),
    ("anamnez2_sarilik", "Sarılık"),
    ("anamnez2_bobrek_hastaligi", "Böbrek hastalığı"),
    ("anamnez2_mide_ulser", "Mide-on iki parmak ülseri"),
    ("anamnez2_isitme_kaybi", "İşitme kaybı"),
    ("anamnez2_gorme_bozuklugu", "Görme bozukluğu"),
    ("anamnez2_sinir_sistemi", "Sinir sistemi hastalığı"),
    ("anamnez2_deri_hastaligi", "Deri hastalığı"),
    ("anamnez2_besin_zehirlenmesi", "Besin zehirlenmesi"),
    ("anamnez2_diger", "Diğer hastalık"),
]
OYKU_SORULARI = [
    ("hastanede_yattiniz_mi", "Hastanede yattınız mı"),
    ("ameliyat_oldunuz_mu", "Ameliyat oldunuz mu"),
    ("is_kazasi_gecirdiniz_mi", "İş kazası geçirdiniz mi"),
    ("meslek_hastaligi_suphesi", "Meslek hastalığı şüphesiyle tetkik"),
    ("maluliyet_aldiniz_mi", "Maluliyet aldınız mı"),
    ("su_anda_tedavi_goruyor_mu", "Şu anda tedavi görüyor mu"),
    ("sigara_iciyor_musunuz", "Sigara (adet/yıl)"),
    ("alkol_aliyor_musunuz", "Alkol"),
]
MUAYENE = [
    ("muayene_goz", "Göz"),
    ("muayene_kbb", "Kulak-Burun-Boğaz"),
    ("muayene_deri", "Deri"),
    ("muayene_kardiyovaskuler", "Kardiyovasküler sistem"),
    ("muayene_solunum", "Solunum sistemi"),
    ("muayene_sindirim", "Sindirim sistemi"),
    ("muayene_urogenital", "Ürogenital sistem"),
    ("muayene_kas_iskelet", "Kas-iskelet sistemi"),
    ("muayene_norolojik", "Nörolojik muayene"),
    ("muayene_psikiyatrik", "Psikiyatrik muayene"),
    ("muayene_diger", "Diğer muayene"),
]
LAB = [
    ("lab_kan", "Kan"),
    ("lab_idrar", "İdrar"),
    ("lab_gaita", "Gaita"),
    ("lab_radyolojik", "Radyolojik analiz"),
    ("lab_odyometre", "Odyometri"),
    ("lab_sft", "SFT"),
    ("lab_psikolojik", "Psikolojik test"),
    ("lab_diger", "Diğer tetkik"),
]

FORM_SCHEMA: list[tuple[str, str, int, str]] = [
    ("isveren_unvani", "İşverenin Ünvanı", 1, "İşveren"),
    ("sgk_sicilno", "SGK Sicil No", 1, "İşveren"),
    ("isveren_adresi", "İşveren Adresi", 1, "İşveren"),
    ("calisan_adi_soyadi", "Adı Soyadı", 1, "Çalışan"),
    ("calisan_tc_no", "T.C. Kimlik No", 1, "Çalışan"),
    ("calisan_dogumyeri_ve_tarihi", "Doğum Yeri ve Tarihi", 1, "Çalışan"),
    ("calisan_cinsiyet", "Cinsiyeti", 1, "Çalışan"),
    ("calisan_egitim_durumu", "Eğitim Durumu", 1, "Çalışan"),
    ("calisan_ev_adresi", "Ev Adresi", 1, "Çalışan"),
    ("calisan_meslegi", "Mesleği", 1, "Çalışan"),
    ("calisan_medeni_durumu", "Medeni Durumu", 1, "Çalışan"),
    ("calisan_cep_tel", "Tel (Cep)", 1, "Çalışan"),
    ("calisan_yaptigi_is", "Yaptığı İş", 1, "Çalışan"),
    ("calisan_calistigi_bolum", "Çalıştığı Bölüm", 1, "Çalışan"),
    ("daha_once_yer", "Daha Önce Çalıştığı Yer(ler)", 1, "Önceki işler"),
    ("daha_once_iskolu", "Önceki İşkolu", 1, "Önceki işler"),
    ("daha_once_yaptigi_is", "Önceki Yaptığı İş", 1, "Önceki işler"),
    ("daha_once_giris_cikis_tarihi", "Giriş-Çıkış Tarihi", 1, "Önceki işler"),
    ("kan_grubu", "Kan Grubu", 1, "Sağlık geçmişi"),
    ("bilinen_alerji_oykusu", "Bilinen Alerji Öyküsü", 1, "Sağlık geçmişi"),
    ("konjenital_kronik_hastalik", "Konjenital / Kronik Hastalık", 1, "Sağlık geçmişi"),
    ("bagisiklama_tetanoz", "Tetanoz", 1, "Bağışıklama"),
    ("bagisiklama_hepatit_a", "Hepatit A", 1, "Bağışıklama"),
    ("bagisiklama_hepatit_b", "Hepatit B", 1, "Bağışıklama"),
    ("bagisiklama_diger", "Diğer Aşı", 1, "Bağışıklama"),
    ("soygecmisi_anne", "Soygeçmiş - Anne", 1, "Soygeçmiş"),
    ("soygecmisi_baba", "Soygeçmiş - Baba", 1, "Soygeçmiş"),
    ("soygecmisi_kardes", "Soygeçmiş - Kardeş", 1, "Soygeçmiş"),
    ("soygecmisi_cocuk", "Soygeçmiş - Çocuk", 1, "Soygeçmiş"),
    *[(key, f"Şikâyet: {label}", 1, "Anamnez - şikâyetler") for key, label in ANAMNEZ1],
    *[(key, f"Hastalık: {label}", 1, "Anamnez - geçirilmiş hastalıklar") for key, label in ANAMNEZ2],
    *[(key, label, 2, "Öykü, sigara, alkol") for key, label in OYKU_SORULARI],
    *[(f"{key}_hayir", f"{label} → Hayır'ı daire içine al", 2, "Öykü, sigara, alkol") for key, label in OYKU_SORULARI],
    *[(key, label, 2, "Fizik muayene") for key, label in MUAYENE],
    ("ta", "TA (tansiyon)", 2, "Ölçümler"),
    ("ta_diastolik", "TA diastolik kutusu", 2, "Ölçümler"),
    ("nb", "Nabız", 2, "Ölçümler"),
    ("boy", "Boy", 2, "Ölçümler"),
    ("kilo", "Kilo", 2, "Ölçümler"),
    ("bmi", "BMI", 2, "Ölçümler"),
    *[(key, f"Tetkik: {label}", 2, "Laboratuvar / tetkik") for key, label in LAB],
    ("kanaat_sonuc", "Kanaat ve Sonuç", 2, "Sonuç"),
    ("onay_tarihi", "Onay Tarihi", 2, "Sonuç"),
    ("hekim_adi_soyadi", "Hekim Adı Soyadı", 2, "Sonuç"),
]

OCR_FIELD_BY_LABEL = {label: key for key, label, _page, _section in FORM_SCHEMA}
SCHEMA_LABELS = [label for _key, label, _page, _section in FORM_SCHEMA]

# Forma yazılmayan, yalnız takip için tutulan sütunlar.
META_LABELS = ["Form ID", "OCR ID", "Kullanım", "Muayene Türü", "Kişi No", "Muayene Yazım Profili", "Dolduran", "Veri Durumu"]

# ---------------------------------------------------------------------------
# Değer havuzları (biçimler gerçek etiketlerin yazım biçimlerinden alındı, 2026-10-08)
# ---------------------------------------------------------------------------

IZMIR_DISTRICTS = [
    "Balçova", "Bornova", "Buca", "Karşıyaka", "Konak", "Bayraklı",
    "Gaziemir", "Çiğli", "Narlıdere", "Güzelbahçe", "Urla", "Menemen",
    "Torbalı", "Menderes", "Kemalpaşa", "Seferihisar", "Aliağa", "Foça",
    "Karabağlar",
]
BIRTH_PLACES = IZMIR_DISTRICTS + [
    "İzmir", "Manisa", "Aydın", "Denizli", "Uşak", "Muş", "Mardin", "Diyarbakır", "Erzurum",
    "Kars", "Ağrı", "Şanlıurfa", "Afyon", "Kütahya", "Balıkesir", "Ödemiş", "Tire", "Bergama",
]
NEIGHBORHOODS = ["Bostanlı", "Alsancak", "Evka-3", "Kızılçullu", "Hatay", "Mavişehir", "Şirinyer", "Gültepe", "Atakent", "Yeşilyurt"]

EMPLOYERS = [
    ("Migros T.A.Ş.", "Perakende"), ("CarrefourSA A.Ş.", "Perakende"), ("Şok Marketler T.A.Ş.", "Perakende"),
    ("Bim A.Ş.", "Perakende"), ("Metro Grossmarket A.Ş.", "Toptan"), ("Pınar Süt A.Ş.", "Gıda"),
]
PREVIOUS_EMPLOYERS = [
    "CarrefourSA", "ŞOK", "A101", "BİM", "File Market", "Metro", "Bizim Toptan", "Hakmar",
    "Onur Market", "Happy Center", "Kim Market", "Çağrı Market", "Pehlivanoğlu", "Mopaş",
    "Tekstil atölyesi", "Lokanta", "Kafe", "Kargo firması", "İnşaat",
]
PREVIOUS_SECTORS = ["Perakende", "Gıda", "Lojistik", "Tekstil", "Hizmet", "Turizm", "İnşaat", "Market"]

JOB_PROFILES: list[dict[str, str]] = [
    {"profession": "Kasiyer", "job": "Kasa", "department": "Kasalar"},
    {"profession": "Kasa Görevlisi", "job": "Kasa işlemleri", "department": "Kasalar"},
    {"profession": "Reyon Görevlisi", "job": "Reyon düzeni", "department": "Kuru Gıda"},
    {"profession": "Reyon Sorumlusu", "job": "Stok takibi", "department": "Kuru Gıda"},
    {"profession": "Manav Personeli", "job": "Manav", "department": "Manav"},
    {"profession": "Şarküteri Personeli", "job": "Şarküteri", "department": "Şarküteri"},
    {"profession": "Kasap", "job": "Et hazırlama", "department": "Et Reyonu"},
    {"profession": "Kasap Yardımcısı", "job": "Et reyonu destek", "department": "Et Reyonu"},
    {"profession": "Balık Reyonu Personeli", "job": "Balık temizleme", "department": "Balık Reyonu"},
    {"profession": "Fırın Personeli", "job": "Ekmek üretimi", "department": "Unlu Mamuller"},
    {"profession": "Depo Personeli", "job": "Depolama", "department": "Depo"},
    {"profession": "Mal Kabul Personeli", "job": "Mal kabul", "department": "Mal Kabul"},
    {"profession": "Forklift Operatörü", "job": "Forklift", "department": "Depo"},
    {"profession": "Sevkiyat Personeli", "job": "Sevkiyat", "department": "Sevkiyat"},
    {"profession": "Sipariş Toplama Personeli", "job": "Online sipariş", "department": "E-Ticaret"},
    {"profession": "Temizlik Personeli", "job": "Temizlik", "department": "Temizlik"},
    {"profession": "Güvenlik Görevlisi", "job": "Güvenlik", "department": "Güvenlik"},
    {"profession": "Vardiya Sorumlusu", "job": "Vardiya yönetimi", "department": "Operasyon"},
    {"profession": "Mağaza Müdür Yardımcısı", "job": "Mağaza yönetimi", "department": "Yönetim"},
    {"profession": "Şoför", "job": "Dağıtım", "department": "Lojistik"},
]

# Kronik durum → tutarlı alanlar (konjenital/kronik kutusu, anamnez hücresi, ICD, tedavi açıklaması)
CONDITIONS = [
    {"name": "Hipertansiyon", "short": "HT", "icd": "I10", "cell": "anamnez2_kalp_hastaligi", "treat": "HT tedavisi", "bp": True},
    {"name": "Tip 2 Diyabet", "short": "DM", "icd": "E11", "cell": "anamnez2_seker_hastaligi", "treat": "Metformin"},
    {"name": "Astım", "short": "Astım", "icd": "J45", "cell": "anamnez1_nefes_darligi", "treat": "İnhaler"},
    {"name": "Kronik Bronşit", "short": "KOAH", "icd": "J42", "cell": "anamnez1_balgamli_oksuruk", "treat": ""},
    {"name": "Lomber Disk Hernisi", "short": "Bel fıtığı", "icd": "M51.2", "cell": "anamnez1_sirt_agrisi", "treat": "Fizik tedavi"},
    {"name": "Gonartroz", "short": "Diz ağrısı", "icd": "M17", "cell": "anamnez1_eklemlerde_agri", "treat": ""},
    {"name": "Gastrit", "short": "Gastrit", "icd": "K29.7", "cell": "anamnez2_mide_ulser", "treat": "PPI"},
    {"name": "Hipotiroidi", "short": "Hipotiroidi", "icd": "E03.9", "cell": "anamnez2_diger", "treat": "Levotiron"},
    {"name": "Migren", "short": "Migren", "icd": "G43", "cell": "anamnez1_diger", "treat": ""},
    {"name": "Miyopi", "short": "Miyop", "icd": "H52.1", "cell": "anamnez2_gorme_bozuklugu", "treat": ""},
    {"name": "Egzama", "short": "Egzama", "icd": "L30.9", "cell": "anamnez2_deri_hastaligi", "treat": "Krem"},
    {"name": "Böbrek Taşı", "short": "Böbrek taşı", "icd": "N20.0", "cell": "anamnez2_bobrek_hastaligi", "treat": ""},
    {"name": "Epilepsi", "short": "Epilepsi", "icd": "G40", "cell": "anamnez2_sinir_sistemi", "treat": "Antiepileptik"},
    {"name": "İşitme Kaybı", "short": "İşitme kaybı", "icd": "H91.9", "cell": "anamnez2_isitme_kaybi", "treat": ""},
    {"name": "Taşikardi", "short": "Çarpıntı", "icd": "R00.0", "cell": "anamnez1_carpinti", "treat": ""},
]
EXTRA_ANAMNEZ = {
    "anamnez1_gogus_agrisi": ("Göğüs Ağrısı", "R07.4"),
    "anamnez1_ishal_kabizlik": ("İrritabl Bağırsak", "K58"),
    "anamnez2_sarilik": ("Hepatit A", "B15"),
    "anamnez2_besin_zehirlenmesi": ("Besin Zehirlenmesi", "A05.9"),
}

ALLERGIES = ["Yok", "Polen", "Ev tozu", "Penisilin", "Lateks", "Mevsimsel", "Polen alerjisi", "Toz akarı", "Aspirin", "Kedi tüyü"]
FAMILY = {
    "anne": ["Sağlıklı", "Sağlıklı", "HT", "DM", "Hipertansiyon", "Diyabet", "Vefat", "Tiroid", "Astım", "Kalp"],
    "baba": ["Sağlıklı", "Sağlıklı", "HT", "DM", "Kalp", "KAH", "Vefat", "Ca", "KOAH", "Hipertansiyon"],
    "kardes": ["Sağlıklı", "Sağlıklı", "Yok", "Astım", "DM", "Sağlıklı 2"],
    "cocuk": ["Yok", "Sağlıklı", "Sağlıklı", "2 sağlıklı", "Astım", "Yok"],
}

EXAM_FIELDS = {
    "muayene_goz": {
        "minimal": ["NFM", "Normal", "Doğal", "N"],
        "normal": ["Doğal", "Görme doğal", "Gözlüklü", "Gözlükle normal"],
        "detailed": ["Konjonktivalar doğal, görme yeterli", "Gözlükle görme yeterli; patoloji yok"],
        "abnormal": ["Miyopi, gözlük kullanıyor", "Sağ göz pitozis", "Konjonktivit", "Renk körlüğü şüphesi"],
    },
    "muayene_kbb": {
        "minimal": ["NFM", "Normal", "Doğal", "N"],
        "normal": ["Doğal", "Orofarenks doğal", "KBB doğal", "Patoloji yok"],
        "detailed": ["Orofarenks ve nazal mukoza doğal", "KBB muayenesinde patoloji yok"],
        "abnormal": ["Septum deviasyonu", "Tonsil hipertrofisi", "Buşon (sağ)", "Farenks hiperemik"],
    },
    "muayene_deri": {
        "minimal": ["N", "Normal", "Doğal", "NFM"],
        "normal": ["Doğal", "Lezyon yok", "Patoloji yok", "Hafif kuruluk"],
        "detailed": ["Aktif dermatolojik lezyon yok", "Deri doğal, enfeksiyöz lezyon yok"],
        "abnormal": ["El sırtında egzama", "Akne", "Sol kolda skar", "Kontakt dermatit"],
    },
    "muayene_kardiyovaskuler": {
        "minimal": ["NFM", "Normal", "Doğal", "S1 S2 doğal"],
        "normal": ["S1-S2 doğal", "Ritmik, ek ses yok", "KVS doğal", "Ritmik"],
        "detailed": ["S1-S2 doğal ve ritmik, ek ses yok", "Kalp sesleri doğal; nabızlar açık"],
        "abnormal": ["2/6 sistolik üfürüm", "Aritmik", "Taşikardik", "Bacaklarda varis"],
    },
    "muayene_solunum": {
        "minimal": ["NFM", "Normal", "Doğal", "Ral yok"],
        "normal": ["Solunum sesleri doğal", "Raller yok", "Akciğer doğal", "Ek ses yok"],
        "detailed": ["Solunum eşit; ral ve ronküs yok", "Solunum sesleri bilateral doğal"],
        "abnormal": ["Bilateral ronküs", "Ekspiryum uzun", "Bazalde ral", "Sibilan ronküs"],
    },
    "muayene_sindirim": {
        "minimal": ["NFM", "Normal", "Doğal", "Batın rahat"],
        "normal": ["Batın rahat", "Hassasiyet yok", "GİS doğal", "Doğal"],
        "detailed": ["Batın rahat; defans, rebound yok", "Barsak sesleri doğal; hassasiyet yok"],
        "abnormal": ["Epigastrik hassasiyet", "Göbek fıtığı", "Apendektomi skarı"],
    },
    "muayene_urogenital": {
        "minimal": ["NFM", "Normal", "Doğal", "Yakınma yok"],
        "normal": ["Doğal", "Yakınma yok", "ÜGS doğal", "Patoloji yok"],
        "detailed": ["Ürogenital yakınma yok; muayene olağan", "Ürogenital sistemde özellik yok"],
        "abnormal": ["KVAH (+) sağ", "Dizüri tarifliyor"],
    },
    "muayene_kas_iskelet": {
        "minimal": ["NFM", "Normal", "Doğal", "EHA açık"],
        "normal": ["Eklem hareketleri açık", "Kas gücü tam", "Bel hareketleri doğal", "KİS doğal"],
        "detailed": ["Eklem hareketleri tam, kas gücü doğal", "Omurga ve ekstremite hareketleri doğal"],
        "abnormal": ["Lomber hassasiyet", "Sağ diz krepitasyon", "Skolyoz", "Lasegue (+) sol"],
    },
    "muayene_norolojik": {
        "minimal": ["NFM", "Normal", "Doğal", "Defisit yok"],
        "normal": ["Nörolojik defisit yok", "Bilinç açık", "Refleksler doğal", "Nörolojik doğal"],
        "detailed": ["Bilinç açık, koopere; defisit yok", "Kraniyal sinirler ve refleksler doğal"],
        "abnormal": ["İnce tremor", "DTR hipoaktif"],
    },
    "muayene_psikiyatrik": {
        "minimal": ["NFM", "Normal", "Doğal", "Koopere"],
        "normal": ["Koopere ve oryante", "Duygudurum doğal", "İletişimi uygun", "Psikiyatrik doğal"],
        "detailed": ["Koopere, oryante; duygudurum doğal", "İletişimi uygun; psikopatoloji yok"],
        "abnormal": ["Anksiyöz", "Depresif duygudurum"],
    },
    "muayene_diger": {
        "minimal": ["Yok", "N", "NFM", "Yok"],
        "normal": ["Ek bulgu yok", "Yok", "Doğal", "Özellik yok"],
        "detailed": ["Ek patolojik muayene bulgusu yok", "Diğer sistem muayenelerinde özellik yok"],
        "abnormal": ["Sol bacak varis", "Obez", "Tiroid nodülü palpe"],
    },
}
EXAM_PROBABILITY = {
    "muayene_goz": 0.86, "muayene_kbb": 0.86, "muayene_deri": 0.75,
    "muayene_kardiyovaskuler": 0.90, "muayene_solunum": 0.90, "muayene_sindirim": 0.65,
    "muayene_urogenital": 0.40, "muayene_kas_iskelet": 0.70, "muayene_norolojik": 0.55,
    "muayene_psikiyatrik": 0.45, "muayene_diger": 0.35,
}

LAB_VALUES = {
    "lab_kan": ["Hemogram N", "NFM", "Normal", "Hb:13.5 Plt:250", "Hb: 11.2 Plt: 310 WBC: 7.4", "Hb 14.1 WBC 6.8",
                "Glukoz: 96", "Hb:12.0 Glukoz:108", "Kolesterol 245", "AKŞ 132"],
    "lab_idrar": ["TİT N", "NFM", "Normal", "Lökosit (+), Eritrosit (+)", "Protein > negatif", "Dansite 1020", "TİT normal"],
    "lab_gaita": ["İstenmedi", "Negatif", "NFM", "Parazit (-)", "Gaitada parazit yok"],
    "lab_radyolojik": ["AC grafisi N", "PA AC: Normal", "NFM", "İstenmedi", "AC grafi doğal", "Kardiyotorasik oran normal"],
    "lab_odyometre": ["Normal", "NFM", "Bilateral normal", "Sağ hafif SNİK", "İstenmedi", "Sol 4 kHz çentik"],
    "lab_sft": ["Normal", "NFM", "FEV1/FVC 82", "Hafif obstrüksiyon", "İstenmedi", "FEV1 %88"],
    "lab_psikolojik": ["Uygulanmadı", "Normal", "İstenmedi", "-"],
    "lab_diger": ["Yok", "EKG normal", "EKG: NSR", "Gözdibi doğal", "Ek tetkik yok"],
}

EXAM_TYPES = ["İşe giriş", "Periyodik", "İş değişikliği", "İşe dönüş"]
CONCLUSIONS = {
    "İşe giriş": ["Çalışabilir", "İşe uygundur", "Yapacağı işe uygundur.", "İşe girişinde sakınca yoktur",
                  "Gece çalışabilir", "Yüksekte çalışamaz", "Gözlükle çalışabilir", "Ağır yük kaldıramaz"],
    "Periyodik": ["Çalışabilir", "Periyodik muayene uygundur", "Çalışmasına engel yoktur",
                  "Kontrol önerilir", "Dahiliye kontrolü önerildi", "Çalışabilir, 1 yıl sonra kontrol"],
    "İş değişikliği": ["Yeni görevine uygundur", "Yeni işinde çalışabilir", "Görev değişikliği uygun"],
    "İşe dönüş": ["İşe dönmesinde sakınca yoktur", "İşe dönebilir", "Hafif işte çalışabilir"],
}

PROFILE_LABELS = {
    "minimal": "Minimalist (kısa tıbbi ifadeler)",
    "normal": "Normal (orta ayrıntı)",
    "detailed": "Ayrıntılı",
}
PROFILE_WEIGHTS = ["minimal"] * 4 + ["normal"] * 4 + ["detailed"] * 2

# Yazım profiline göre: tablolarda "NFM" yazma eğilimi (gerçek formlarda anamnez hücrelerinin ~%85'i NFM).
NFM_RATE = {"minimal": 0.85, "normal": 0.70, "detailed": 0.55}


# ---------------------------------------------------------------------------
# Yardımcılar
# ---------------------------------------------------------------------------

def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, max(0, (end - start).days)))


def biased_date(start: date, end: date) -> date:
    """Rakam karışıklığını (09→07) ölçebilmek için ayların ~%20'si 07/09'a çekilir."""
    value = random_date(start, end)
    if random.random() < 0.20:
        month = random.choice([7, 9])
        day = min(value.day, 30)
        try:
            candidate = value.replace(month=month, day=day)
        except ValueError:
            candidate = value
        if start <= candidate <= end:
            value = candidate
    return value


def format_date(value: date, separator: str = "/") -> str:
    return f"{value.day:02d}{separator}{value.month:02d}{separator}{value.year}"


def fake_phone() -> str:
    return f"05{random.randint(30, 55):02d}{random.randint(1000000, 9999999)}"


def synthetic_tc(index: int) -> str:
    """Algoritmik olarak geçerli biçimde 11 rakamlı, yalnızca test amaçlı numara üretir."""
    seed = 100_000_000 + index
    first9 = [int(c) for c in str(seed)[:9]]
    tenth = ((sum(first9[0::2]) * 7) - sum(first9[1::2])) % 10
    eleventh = (sum(first9) + tenth) % 10
    return "".join(map(str, first9 + [tenth, eleventh]))


def maybe(value: Any, probability: float) -> Any:
    return value if random.random() < probability else ""


def choose_profile(requested: str) -> str:
    return random.choice(PROFILE_WEIGHTS) if requested == "random" else requested


def blood_group() -> str:
    group = random.choices(["A", "0", "B", "AB"], weights=[43, 33, 16, 8])[0]
    return f"{group} {random.choices(['+', '-'], weights=[85, 15])[0]}"


def doctor_pool(size: int = 5) -> list[str]:
    names = []
    for _ in range(size):
        first = fake.first_name_female() if random.random() < 0.5 else fake.first_name_male()
        name = f"{first} {fake.last_name()}"
        names.append(f"Dr. {name}" if random.random() < 0.4 else name)
    return names


# ---------------------------------------------------------------------------
# Kişi (formdan bağımsız kalıcı bilgiler) ve form üretimi
# ---------------------------------------------------------------------------

def generate_identity(index: int, optional_rate: float, first_exam: date) -> dict[str, Any]:
    gender = "Erkek" if index % 2 else "Kadın"
    first = fake.first_name_male() if gender == "Erkek" else fake.first_name_female()
    # İlk muayenede 18–58 yaş (hekim.md: geçerli yaş aralığı 15–75)
    birth = biased_date(date(first_exam.year - 58, 1, 1), date(first_exam.year - 18, first_exam.month, min(first_exam.day, 28)))
    district = random.choice(IZMIR_DISTRICTS)
    address = random.choice([
        f"{district} / İzmir", district, f"{random.choice(NEIGHBORHOODS)} Mah. {district}",
        f"{random.randint(1000, 9999)} Sok. No:{random.randint(1, 80)} {district}",
    ])
    height = random.randint(165, 192) if gender == "Erkek" else random.randint(152, 176)
    conditions = random.sample(CONDITIONS, k=random.choices([0, 1, 2], weights=[62, 30, 8])[0])
    return {
        "person_no": index,
        "gender": gender,
        "name": f"{first} {fake.last_name()}",
        "tc": synthetic_tc(index),
        "birth": birth,
        "birth_place": random.choice(BIRTH_PLACES),
        "birth_sep": "." if random.random() < 0.08 else "/",
        "education": random.choice(["İlkokul", "Ortaokul", "Lise", "Lise", "Meslek Lisesi", "Önlisans", "Üniversite", "Lisans"]),
        "address": maybe(address, optional_rate),
        "married": maybe(random.choice(["Evli", "Bekar", "Bekâr", "Evli"]), min(0.98, optional_rate + 0.12)),
        "phone": fake_phone(),
        "height": height,
        "base_weight": random.randint(60, 112) if gender == "Erkek" else random.randint(48, 92),
        "blood": blood_group(),
        "allergy": maybe(random.choice(ALLERGIES), optional_rate - 0.25),
        "conditions": conditions,
        "family": {k: maybe(random.choice(v), optional_rate if k in ("anne", "baba") else optional_rate - 0.2) for k, v in FAMILY.items()},
        "smoker": random.choices(["hayir", "evet", "birakmis"], weights=[55, 33, 12])[0],
        "smoke_qty": random.choice([1, 5, 10, 10, 15, 20, 20, 30]),
        "smoke_since": random.randint(birth.year + 15, first_exam.year - 1),
        "alcohol": random.choices(["hayir", "evet", "sosyal"], weights=[70, 15, 15])[0],
        "previous": previous_jobs(birth.year, first_exam.year, optional_rate),
    }


def previous_jobs(birth_year: int, exam_year: int, optional_rate: float) -> dict[str, str]:
    """Matbu formda önceki işler tek kutuda; iki iş ' / ' ile ayrılır (gerçek formlardaki gibi)."""
    empty = {"yer": "", "iskolu": "", "is": "", "tarih": ""}
    if random.random() >= min(0.9, optional_rate):
        return empty
    earliest = max(2000, birth_year + 16)
    latest = exam_year  # önceki iş en geç muayene yılında biter
    if earliest > latest - 2:
        return empty
    count = 2 if random.random() < 0.45 and earliest <= latest - 6 else 1
    years: list[tuple[int, int]] = []
    start = random.randint(earliest, latest - 3 * count + 1)
    for _ in range(count):
        end = random.randint(start + 1, min(start + 6, latest))
        years.append((start, end))
        start = min(end + random.randint(0, 1), latest - 1)
    employers = random.sample(PREVIOUS_EMPLOYERS, k=count)
    sectors = [random.choice(PREVIOUS_SECTORS) for _ in range(count)]
    jobs = [random.choice(JOB_PROFILES)["profession"] for _ in range(count)]
    tarih = " / ".join(f"{a}-{b}" for a, b in years)
    if random.random() < 0.08:  # yarım bırakılmış "2019-" yazımı
        tarih = f"{years[-1][0]}-"
    return {
        "yer": " / ".join(employers), "iskolu": " / ".join(sectors),
        "is": " / ".join(jobs), "tarih": tarih,
    }


def anamnez_cell(field: str, identity: dict[str, Any], profile: str, exam_date: date) -> str:
    for condition in identity["conditions"]:
        if condition["cell"] == field:
            year = max(identity["birth"].year + 10, exam_date.year - random.randint(1, 12))
            diag = biased_date(date(year, 1, 1), date(year, 12, 28))
            return random.choice([
                f"{condition['name']} ({condition['icd']}) {format_date(diag, '.')}",
                f"{condition['name']} ({condition['icd']})",
                condition["icd"],
            ])
    if field in EXTRA_ANAMNEZ and random.random() < 0.04:
        name, icd = EXTRA_ANAMNEZ[field]
        return f"{name} ({icd})"
    roll = random.random()
    if roll < NFM_RATE[profile]:
        return "NFM"
    return "Hayır" if roll < NFM_RATE[profile] + 0.10 else ""


def history_answers(identity: dict[str, Any], exam_date: date, fill: float) -> dict[str, tuple[str, str]]:
    """(yazı kutusu, Hayır dairesi) çiftleri."""
    texts = {
        "hastanede_yattiniz_mi": ["Doğum", "Apandisit", "Pnömoni", "Doğum 2018", "Trafik kazası", "Böbrek taşı"],
        "ameliyat_oldunuz_mu": ["Apandektomi", "Sezaryen", "Kolesistektomi", "Menisküs 2019", "Fıtık ameliyatı", "Bademcik"],
        "is_kazasi_gecirdiniz_mi": ["El kesisi", "Ayak burkulması", "Düşme 2021", "Parmak ezilmesi"],
        "meslek_hastaligi_suphesi": ["Tetkik edildi, yok", "İşitme tetkiki"],
        "maluliyet_aldiniz_mi": ["%20 maluliyet", "Var"],
        "su_anda_tedavi_goruyor_mu": [],
    }
    rates = {"hastanede_yattiniz_mi": 0.15, "ameliyat_oldunuz_mu": 0.18, "is_kazasi_gecirdiniz_mi": 0.07,
             "meslek_hastaligi_suphesi": 0.03, "maluliyet_aldiniz_mi": 0.02}
    treat = [c["treat"] for c in identity["conditions"] if c["treat"]]
    result: dict[str, tuple[str, str]] = {}
    for key, options in texts.items():
        if key == "su_anda_tedavi_goruyor_mu":
            positive = bool(treat)
            text = random.choice(treat) if treat else ""
        else:
            positive = random.random() < rates[key]
            text = random.choice(options)
            if positive and random.random() < 0.35 and not any(ch.isdigit() for ch in text):
                text = f"{text} {random.randint(min(exam_date.year, identity['birth'].year + 15), exam_date.year)}"
        if positive:
            result[key] = (text, "")
        elif random.random() < fill:
            result[key] = ("", "Hayır")
        else:
            result[key] = ("", "")  # hiç işaretlenmemiş (gerçek formların ~%25'i)

    years_smoking = max(1, exam_date.year - identity["smoke_since"])
    if identity["smoker"] == "evet":
        result["sigara_iciyor_musunuz"] = (f"{identity['smoke_qty']}/{years_smoking}", "")
    elif identity["smoker"] == "birakmis":
        quit_year = random.randint(min(exam_date.year, identity["birth"].year + 18), exam_date.year)
        result["sigara_iciyor_musunuz"] = (random.choice([f"Bırakmış {quit_year}", f"{identity['smoke_qty']}/{years_smoking} bıraktı"]), "")
    else:
        result["sigara_iciyor_musunuz"] = ("", "Hayır" if random.random() < fill else "")

    if identity["alcohol"] == "evet":
        result["alkol_aliyor_musunuz"] = (random.choice(["1/5", "2/10", "1/20", "3/8", "1/1 2015"]), "")
    elif identity["alcohol"] == "sosyal":
        result["alkol_aliyor_musunuz"] = (random.choice(["Sosyal", "Nadiren", "Ayda bir"]), "")
    else:
        result["alkol_aliyor_musunuz"] = ("", "Hayır" if random.random() < fill else "")
    return result


def vaccine_values(exam_date: date, rate: float) -> dict[str, str]:
    tetanus_year = random.randint(2012, exam_date.year)
    return {
        "bagisiklama_tetanoz": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor", f"{tetanus_year} rapel", f"{tetanus_year} Td", "Yok"]), rate - 0.15),
        "bagisiklama_hepatit_a": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor", "Yok"]), rate - 0.35),
        "bagisiklama_hepatit_b": maybe(random.choice(["Tam", "Eksik", "Hatırlamıyor", "3 doz", "Anti-HBs (+)"]), rate - 0.30),
        "bagisiklama_diger": maybe(random.choice(["Yok", "Grip", "COVID-19 3 doz", "Covid 2 doz", "Kızamık"]), rate - 0.45),
    }


def generate_form(identity: dict[str, Any], exam_type: str, exam_date: date, profile: str,
                  fill_rate: int, employer: tuple[str, str], doctor: str, job: dict[str, str]) -> dict[str, Any]:
    rate = max(0.30, min(1.0, fill_rate / 100))
    age = exam_date.year - identity["birth"].year
    weight = max(42, identity["base_weight"] + random.randint(-3, 3) + max(0, age - 35) // 6)
    bmi = round(weight / ((identity["height"] / 100) ** 2), 1)
    hypertensive = any(c.get("bp") for c in identity["conditions"]) or (age > 45 and random.random() < 0.25)
    systolic = random.randint(135, 170) if hypertensive else random.randint(100, 135)
    diastolic = random.randint(85, 105) if hypertensive else random.randint(60, 85)
    systolic -= systolic % 5 if random.random() < 0.7 else 0  # hekimler çoğunlukla 5'e yuvarlar
    diastolic -= diastolic % 5 if random.random() < 0.7 else 0
    previous = identity["previous"]
    district = random.choice(IZMIR_DISTRICTS)
    chronic = " + ".join(random.choice([c["name"], c["short"]]) for c in identity["conditions"])

    values: dict[str, Any] = {
        "isveren_unvani": maybe(employer[0], rate),
        "sgk_sicilno": maybe(" ".join(str(random.randint(10 ** (n - 1), 10 ** n - 1)) for n in (1, 4, 2, 2, 7, 3)), 0.12),
        "isveren_adresi": maybe(random.choice([f"{district} İzmir", f"{district} / İzmir", district, f"{random.randint(1000, 9999)} Sk. {district}"]), rate - 0.10),
        "calisan_adi_soyadi": identity["name"],
        "calisan_tc_no": identity["tc"],
        "calisan_dogumyeri_ve_tarihi": f"{identity['birth_place']} {format_date(identity['birth'], identity['birth_sep'])}",
        "calisan_cinsiyet": identity["gender"],
        "calisan_egitim_durumu": identity["education"],
        "calisan_ev_adresi": identity["address"],
        "calisan_meslegi": job["profession"],
        "calisan_medeni_durumu": identity["married"],
        "calisan_cep_tel": identity["phone"],
        "calisan_yaptigi_is": job["job"],
        "calisan_calistigi_bolum": job["department"],
        "daha_once_yer": previous["yer"],
        "daha_once_iskolu": previous["iskolu"],
        "daha_once_yaptigi_is": previous["is"],
        "daha_once_giris_cikis_tarihi": previous["tarih"],
        "kan_grubu": identity["blood"],
        "bilinen_alerji_oykusu": identity["allergy"],
        "konjenital_kronik_hastalik": chronic if chronic else maybe("Yok", rate - 0.4),
        **vaccine_values(exam_date, rate),
        "soygecmisi_anne": identity["family"]["anne"],
        "soygecmisi_baba": identity["family"]["baba"],
        "soygecmisi_kardes": identity["family"]["kardes"],
        "soygecmisi_cocuk": identity["family"]["cocuk"] if age > 22 else "",
        "ta": f"{systolic}/{diastolic}",
        "ta_diastolik": "",
        "nb": random.randint(88, 110) if any(c["icd"] == "R00.0" for c in identity["conditions"]) else random.randint(58, 96),
        "boy": identity["height"],
        "kilo": weight,
        "bmi": maybe(f"{bmi:.1f}", 0.70),
        "kanaat_sonuc": random.choice(CONCLUSIONS[exam_type]),
        "onay_tarihi": format_date(exam_date),
        "hekim_adi_soyadi": maybe(doctor, 0.95),
    }

    for key, _label in ANAMNEZ1 + ANAMNEZ2:
        values[key] = anamnez_cell(key, identity, profile, exam_date)

    for key, (text, no) in history_answers(identity, exam_date, rate).items():
        values[key] = text
        values[f"{key}_hayir"] = no

    abnormal_rate = 0.10 + (0.05 if identity["conditions"] else 0)
    for key, variants in EXAM_FIELDS.items():
        if random.random() >= EXAM_PROBABILITY[key]:
            values[key] = ""
        elif random.random() < abnormal_rate:
            values[key] = random.choice(variants["abnormal"])
        else:
            values[key] = random.choice(variants[profile])

    lab_probability = {"minimal": 0.25, "normal": 0.35, "detailed": 0.50}[profile]
    for key, options in LAB_VALUES.items():
        values[key] = random.choice(options) if random.random() < lab_probability else ""

    record: dict[str, Any] = {label: "" for label in META_LABELS}
    record.update({
        "Kişi No": f"KISI-{identity['person_no']:05d}",
        "Muayene Türü": exam_type,
        "Muayene Yazım Profili": PROFILE_LABELS[profile],
        "Veri Durumu": "SENTETİK OCR/HTR TEST VERİSİ",
    })
    for key, label, _page, _section in FORM_SCHEMA:
        value = values.get(key, "")
        record[label] = "" if value is None else str(value)
    return record


def generate_records(count: int, fill_rate: int = 85, doctor_profile: str = "random",
                     start_index: int = 1, repeat_rate: int = 10) -> list[dict[str, Any]]:
    """`count` form üretir; ~`repeat_rate`% form daha önceki bir kişinin sonraki muayenesidir
    (aynı kimlik, daha geç onay tarihi, periyodik / iş değişikliği / işe dönüş)."""
    if count < 1:
        raise ValueError("Kayıt sayısı en az 1 olmalıdır.")
    if count > 50_000:
        raise ValueError("Tek seferde en fazla 50.000 kayıt üretilebilir.")
    if not 0 <= fill_rate <= 100:
        raise ValueError("Doluluk oranı 0 ile 100 arasında olmalıdır.")
    if start_index < 1:
        raise ValueError("Başlangıç numarası en az 1 olmalıdır.")
    if not 0 <= repeat_rate <= 50:
        raise ValueError("Tekrar muayene oranı 0 ile 50 arasında olmalıdır.")
    if doctor_profile not in {"random", "minimal", "normal", "detailed"}:
        raise ValueError("Geçersiz doktor profili.")

    rate = max(0.30, min(1.0, fill_rate / 100))
    repeats = round(count * repeat_rate / 100) if count >= 4 else 0
    firsts = count - repeats
    doctors = doctor_pool()
    employer = random.choice(EMPLOYERS)
    last_day = date.today() - timedelta(days=1)

    people: list[tuple[dict[str, Any], dict[str, str], date]] = []
    records: list[dict[str, Any]] = []
    for offset in range(firsts):
        exam_date = biased_date(date(2019, 1, 2), last_day - timedelta(days=400))
        identity = generate_identity(start_index + offset, rate, exam_date)
        job = random.choice(JOB_PROFILES)
        exam_type = random.choices(EXAM_TYPES, weights=[55, 35, 5, 5])[0]
        people.append((identity, job, exam_date))
        records.append(generate_form(identity, exam_type, exam_date, choose_profile(doctor_profile),
                                     fill_rate, employer, random.choice(doctors), job))

    for _ in range(repeats):
        identity, job, previous_date = random.choice(people)
        exam_type = random.choices(["Periyodik", "İş değişikliği", "İşe dönüş"], weights=[70, 15, 15])[0]
        if exam_type == "İş değişikliği":
            job = random.choice([j for j in JOB_PROFILES if j["department"] != job["department"]])
        later = biased_date(previous_date + timedelta(days=200), last_day)
        identity = copy.deepcopy(identity)
        if random.random() < 0.3 and len(identity["conditions"]) < 2:  # aradan geçen sürede yeni tanı
            identity["conditions"].append(random.choice([c for c in CONDITIONS if c not in identity["conditions"]]))
        records.append(generate_form(identity, exam_type, later, choose_profile(doctor_profile),
                                     fill_rate, employer, random.choice(doctors), job))

    random.shuffle(records)
    return records


def assign_test_split(records: list[dict[str, Any]], test_count: int) -> list[str]:
    """`test_count` kadar formu (aynı kişinin formları bir arada) test setine ayırır."""
    if test_count <= 0:
        for record in records:
            record["Kullanım"] = "eğitim"
        return []
    people = sorted({r["Kişi No"] for r in records})
    random.shuffle(people)
    chosen: set[str] = set()
    total = 0
    for person in people:
        size = sum(1 for r in records if r["Kişi No"] == person)
        if total + size > test_count:
            continue
        chosen.add(person)
        total += size
        if total == test_count:
            break
    for record in records:
        record["Kullanım"] = "test" if record["Kişi No"] in chosen else "eğitim"
    return [r["Form ID"] for r in records if r["Kullanım"] == "test"]


def ocr_ground_truth(record: dict[str, Any]) -> dict[str, str]:
    """faz1-trocr-main ground_truth biçimi: düz {ocr_alan: değer}; boş kutu = "boş"."""
    result = {}
    for key, label, _page, _section in FORM_SCHEMA:
        value = str(record.get(label, "")).strip()
        result[key] = value if value else "boş"
    return result
