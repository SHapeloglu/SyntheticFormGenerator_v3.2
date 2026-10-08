# task.md — Synthetic Form Generator Görevleri

## 🔜 Sıradaki

- [ ] Koordinat editörünü tamamla: `config/coordinates.json`'a page1/page2 alanlarını gir. **Engel:** `static/forms/page1.jpeg`/`page2.jpeg` boş şablon değil, elle doldurulmuş ve eğik çekilmiş form fotoğrafı; önizleme ancak **boş form taramasıyla** anlamlı olur. Başlangıç için faz1-trocr-main `sablon_koordinatlari.json` (oransal kutular, 48+44 alan) alan adları eşlenerek aktarılabilir.

## 🚧 Devam Eden

_(şu anda boş)_

## ✅ Tamamlanan

- [x] 2026-10-08 — `render_page` route'a bağlandı: `GET /batch/<batch_id>/preview/<form_id>/<page_key>` (JPEG, `outputs/batches/<batch>/preview/` altına yazar)
- [x] 2026-10-08 — Boş kalıntı dosyalar kaldırıldı: `config/fields.json`, `config/jobs.json`, `config/outputs`
- [x] 2026-10-08 — `app.secret_key` artık `SFG_SECRET_KEY` ortam değişkeninden okunuyor (yoksa yerel sabit yedek)
- [x] 2026-10-08 — Birim testleri (`tests/`, 22 test): `synthetic_tc` bağımsız TC kontrolüyle, `reserve_sequence` 40 iş parçacığıyla eşzamanlılık, `validate_batch` hata senaryoları, önizleme route'u

- [x] 2026-10-05 — Çalışma dosyaları kod okunarak yeniden yazıldı
- [x] 2026-08-03 — v3.2 baseline: batch yönetimi, arama, ZIP indirme, bütünlük kontrolü, arşiv/geri al
