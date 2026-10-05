# Synthetic Form Generator v3.2

El yazısı tanıma (OCR) modelleri için **sentetik işe giriş / periyodik muayene formu** verisi üreten yerel web uygulaması.

Uygulama her form için gerçekçi ama tamamen sahte bir kişi ve muayene kaydı üretir ve bunu yazdırılabilir bir **kart** olarak gösterir. Gönüllüler kartı boş matbu forma elle doldurur; taranan formlar, uygulamanın ürettiği **ground truth** (Excel/JSON) ile eşleştirilerek OCR eğitimi ve değerlendirmesinde kullanılır (bkz. TrOCR projesi).

## Özellikler

- Türkçe sentetik veri (Faker `tr_TR`): ad-soyad, algoritmik olarak geçerli **sahte** TC kimlik no, telefon, adres, meslek/işyeri geçmişi.
- Muayene alanları için hekim yazım profilleri: **minimal** (NFM, N, Doğal…), **normal**, **ayrıntılı** veya rastgele; bir form içinde tutarlı dil.
- Alan doluluk oranı ayarı (`fill_rate`) — gerçekçi boş bırakılmış alanlar.
- Boy/kilo/BMI, kan grubu/Rh ve önceki iş bilgileri arasında tutarlılık.
- Global artan **Form ID** (`FORM-00001` …) — taranan formu kayda bağlayan anahtar.
- **Batch yönetimi:** geçmiş batch'ler, Form ID arama, bütünlük doğrulaması, arşivle/geri al.
- İndirme: Excel ground truth, JSON veya tüm batch'i içeren ZIP.
- Form görseli üzerinde alan koordinatı düzenleme ekranı (`/coordinates`).

## Kurulum ve çalıştırma

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Tarayıcı: <http://127.0.0.1:5000>

Önce 3–5 form üretip kartların yazdırma önizlemesini kontrol edin, sonra 50–60'lık batch'ler üretin.

## Klasörler

| Yol | İçerik |
|---|---|
| `app.py` | Web uygulaması (Flask) |
| `services/` | Veri üretimi, batch saklama/doğrulama, Excel, form ID sırası, form görseli işleme |
| `templates/` | Arayüz |
| `static/forms/` | Boş form görselleri (sayfa 1–2) |
| `config/sequence.json` | Sıradaki Form ID — **silmeyin** |
| `outputs/batches/` | Üretilen batch'ler ve ground truth (git'e girmez) |
| `outputs/archive/` | Arşivlenmiş batch'ler |

## Sürüm notları

- [README_V2.md](README_V2.md)
- [README_V3.md](README_V3.md) — hekim profilleri, tutarlılık kuralları, sahte TC
- [README_V3_1.md](README_V3_1.md)
- [README_V3_2.md](README_V3_2.md) — batch yönetimi, arama, ZIP, bütünlük kontrolü

## Not

Üretilen tüm kişisel veriler **sahtedir**. Uygulamaya gerçek kişi verisi girmeyin.
