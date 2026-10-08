# CLAUDE.md — Synthetic Form Generator v3.2

El yazısı OCR veri seti üretimi için sentetik **işe giriş / periyodik muayene formu** verisi üreten yerel Flask uygulaması. Uygulama her form için gerçekçi ama sahte bir kişi + muayene kaydı üretir, bunu yazdırılabilir "kart" olarak gösterir; insanlar kartı boş matbu forma elle doldurur, taranan formlar **ground truth** (`ground_truth.xlsx` / JSON) ile eşleştirilir. Hedef kullanım: **faz1-trocr** (TrOCR / PaddleOCR eğitim-değerlendirme) projesi.

- GitHub: https://github.com/SHapeloglu/SyntheticFormGenerator_v3.2 (tek baseline commit, 2026-08-03)
- Sürüm notları: `README_V2.md` → `README_V3.md` → `README_V3_1.md` → `README_V3_2.md` (en güncel)
- Mimari: `architect.md` · Görevler: `task.md` · Fikirler: `backlog.md` · Günlük: `session.md`

## Komutlar

```bash
python -m venv venv && . venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py      # http://127.0.0.1:5000 (debug=True, sadece localhost)
pip install pytest && python -m pytest -q      # birim testleri (tests/)
```

Önce 3–5 form üretip kart yazdırma önizlemesini kontrol et, sonra 50–60'lık batch'ler üret (README_V3).

## Dosyalar

- `app.py` — route'lar, kart gruplama (`card_groups`, `simplified_fields`), batch oluşturma/indirme/arşiv.
- `services/data_generator.py` — `FORM_SCHEMA`: matbu formun 92 kutusu (faz1 OCR alan adı ↔ kart etiketi ↔ sayfa ↔ bölüm). Kişi (`generate_identity`) + form (`generate_form`); `repeat_rate` ile aynı kişinin sonraki muayeneleri, `assign_test_split` test seti, `ocr_ground_truth` faz1 biçimi. Faker `tr_TR`, hekim yazım profili (`minimal/normal/detailed/random`), `fill_rate`, `synthetic_tc` (algoritmik olarak geçerli **sahte** TC).
- `services/sequence_manager.py` — `config/sequence.json` içindeki `next_form_number`'ı rezerve eder → `FORM-00001` biçiminde benzersiz Form ID.
- `services/batch_storage.py` — `outputs/batches/<BATCH-…>/` kaydet/yükle/doğrula/ara/arşivle/geri al.
- `services/excel_exporter.py` — ground truth Excel.
- `services/form_renderer.py` + `/coordinates` — form görseline alan koordinatı yerleştirme editörü ve `render_page` (görsel üzerine yazdırma); önizleme: `GET /batch/<batch_id>/preview/<form_id>/<page_key>`. `config/coordinates.json`'da alan tanımı henüz yok; `static/forms/` görselleri boş şablon değil, doldurulmuş form fotoğrafı.

## Kurallar ve Tuzaklar

- **`config/sequence.json`'u silme / sıfırlama** — Form ID'ler global benzersiz olmalı; sıfırlanırsa eski taramalarla çakışır.
- `outputs/` gitignore'da ve ground truth'u tutar; yedeksiz silme. Arşiv `outputs/archive/`'a taşır (silmez).
- Üretilen her batch otomatik `validate_batch`'ten geçer (Form ID tekrarı, metadata tutarlılığı); doğrulama kuralı eklersen orada.
- Kart etiketleri Excel başlığıdır; OCR alan adları (`FORM_SCHEMA` ilk sütunu) faz1-trocr-main `sablon_koordinatlari.json` ile **birebir aynı** olmalı (`tests/test_form_schema.py` denetler). Değer biçimleri gerçek etiketlerin yazımını izler (tarih `gg/aa/yyyy`, `A +`, `10/15`, `NFM`) — ISO tarihe dönme.
- Batch çıktısı: `ground_truth.json/.xlsx`, `ocr_ground_truth/<sfgNNNNN>.json` (faz1'e kopyalanır), kart PDF'i: `wkhtmltopdf --encoding utf-8 -s A4 -B 0 -T 0 -L 0 -R 0 --zoom 1.4 kartlar.html kartlar.pdf`.
- Gerçek kişisel veri kullanma; TC, isim, telefon tamamen sentetik kalmalı.
- Form verisi `data_generator.py` sabitlerinde (config altında ayrı veri dosyası yok).
- Ağa açılırsa `SFG_SECRET_KEY` ortam değişkeni verilmeli; `debug=True` kapatılmalı.
- Oturum sonunda `session.md`'ye kayıt düş, `task.md`'yi güncelle.
