# task.md — Synthetic Form Generator Görevleri

## 🔜 Sıradaki

- [ ] Koordinat editörünü tamamla: `config/coordinates.json`'a page1/page2 alanlarını gir. **Engel:** `static/forms/page1.jpeg`/`page2.jpeg` boş şablon değil, elle doldurulmuş ve eğik çekilmiş form fotoğrafı; önizleme ancak **boş form taramasıyla** anlamlı olur. Başlangıç için faz1-trocr-main `sablon_koordinatlari.json` (oransal kutular, 48+44 alan) alan adları eşlenerek aktarılabilir.

## 🚧 Devam Eden

_(şu anda boş)_

## ✅ Tamamlanan

- [x] 2026-10-08 — **v3.3: üretici gerçek EK-2 formuna hizalandı** (faz1-trocr-main'de bulunan eksikler):
  - Şema = `sablon_koordinatlari.json`'ın 92 alanı (eksik olan 19 anamnez hücresi, hekim adı, onay tarihi, işveren alanları eklendi); kart etiketi ↔ OCR alan adı `FORM_SCHEMA`'da
  - Yazım biçimleri gerçek etiketlerden: tarih `gg/aa/yyyy` (ISO değil), "Doğum yeri ve tarihi" tek kutu, önceki işler `A / B` ve `2015-2018 / 2019-2023`, TA `120/80` (diastolik kutusu boş), kan grubu `A +`, telefon 11 hane bitişik, sigara/alkol `adet/yıl` (`1/20`), anamnezde `NFM` / `Hastalık (ICD) gg.aa.yyyy`
  - Kartta artık sigara, alkol, 6 öykü sorusu (Hayır dairesi ayrı satır), tetkikler, işveren, hekim, onay tarihi görünüyor (önceden hiç yazdırılmıyordu)
  - Serbest metin çeşitliliği: normal dışı muayene bulguları, sayısal tahlil yazımları, muayene türüne göre kanaat
  - Tutarlılık: kronik hastalık ↔ anamnez hücresi ↔ "tedavi görüyor" ↔ tansiyon; yaş 18–58; önceki işler muayene yılından önce
  - Muayene türü (işe giriş / periyodik / iş değişikliği / işe dönüş) ve **aynı kişinin birden fazla formu** (`repeat_rate`, varsayılan %10)
  - Test seti ayrımı (`test_count`, varsayılan 10; aynı kişinin formları bölünmez), kartta "TEST SETİ" ve "Dolduran" satırı
  - 07/09 ay yanlılığı (~%20) — rakam karışıklığı ölçümü için
  - `ocr_ground_truth/<sfgNNNNN>.json`: faz1 `data/cikti/ground_truth/` biçimi (boş kutu = `boş`); elle etiketleme ve "Ekrik/Eksik" türü yazım hatası gerekmez
  - Kart her form için 2 A4 (form sayfa 1/2); eski yazdırma kuralı 297 mm'de kesiyordu
  - 28 test (6 yeni: şema = faz1 şablonu, biçim/tutarlılık 60 tohum, tekrar muayene, test ayrımı, batch çıktıları)
- [x] 2026-10-08 — İlk 50'lik batch: `BATCH-20261008_113109_843050` (FORM-00001…00050, 45 kişi, 10 test formu), `kartlar.pdf` 100 sayfa

- [x] 2026-10-08 — `render_page` route'a bağlandı: `GET /batch/<batch_id>/preview/<form_id>/<page_key>` (JPEG, `outputs/batches/<batch>/preview/` altına yazar)
- [x] 2026-10-08 — Boş kalıntı dosyalar kaldırıldı: `config/fields.json`, `config/jobs.json`, `config/outputs`
- [x] 2026-10-08 — `app.secret_key` artık `SFG_SECRET_KEY` ortam değişkeninden okunuyor (yoksa yerel sabit yedek)
- [x] 2026-10-08 — Birim testleri (`tests/`, 22 test): `synthetic_tc` bağımsız TC kontrolüyle, `reserve_sequence` 40 iş parçacığıyla eşzamanlılık, `validate_batch` hata senaryoları, önizleme route'u

- [x] 2026-10-05 — Çalışma dosyaları kod okunarak yeniden yazıldı
- [x] 2026-08-03 — v3.2 baseline: batch yönetimi, arama, ZIP indirme, bütünlük kontrolü, arşiv/geri al
