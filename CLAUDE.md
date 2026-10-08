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
- `services/data_generator.py` — Faker `tr_TR`; İzmir ilçeleri + perakende iş profilleri, önceki işyerleri, muayene alanları (`EXAM_FIELDS`), hekim yazım profili (`minimal/normal/detailed/random`), `fill_rate` ile alan boş bırakma, `synthetic_tc` (algoritmik olarak geçerli **sahte** TC).
- `services/sequence_manager.py` — `config/sequence.json` içindeki `next_form_number`'ı rezerve eder → `FORM-00001` biçiminde benzersiz Form ID.
- `services/batch_storage.py` — `outputs/batches/<BATCH-…>/` kaydet/yükle/doğrula/ara/arşivle/geri al.
- `services/excel_exporter.py` — ground truth Excel.
- `services/form_renderer.py` + `/coordinates` — form görseline alan koordinatı yerleştirme editörü ve `render_page` (görsel üzerine yazdırma); önizleme: `GET /batch/<batch_id>/preview/<form_id>/<page_key>`. `config/coordinates.json`'da alan tanımı henüz yok; `static/forms/` görselleri boş şablon değil, doldurulmuş form fotoğrafı.

## Kurallar ve Tuzaklar

- **`config/sequence.json`'u silme / sıfırlama** — Form ID'ler global benzersiz olmalı; sıfırlanırsa eski taramalarla çakışır.
- `outputs/` gitignore'da ve ground truth'u tutar; yedeksiz silme. Arşiv `outputs/archive/`'a taşır (silmez).
- Üretilen her batch otomatik `validate_batch`'ten geçer (Form ID tekrarı, metadata tutarlılığı); doğrulama kuralı eklersen orada.
- Alan adları (ör. `"Form ID"`, `"a) Göz"`) Excel başlığı ve kart etiketi olarak kullanılıyor; değiştirmek mevcut ground truth ile uyumu bozar — OCR tarafıyla birlikte değiştir.
- Gerçek kişisel veri kullanma; TC, isim, telefon tamamen sentetik kalmalı.
- Form verisi `data_generator.py` sabitlerinde (config altında ayrı veri dosyası yok).
- Ağa açılırsa `SFG_SECRET_KEY` ortam değişkeni verilmeli; `debug=True` kapatılmalı.
- Oturum sonunda `session.md`'ye kayıt düş, `task.md`'yi güncelle.
