# session.md — Synthetic Form Generator Oturum Günlüğü

---

## 2026-10-08

**Yapılanlar:** Kalıntı config dosyaları silindi; `secret_key` ortam değişkenine taşındı; `render_page` önizleme route'una bağlandı; `tests/` altında 22 birim testi (`venv/bin/python -m pytest -q`).
**Kararlar / neden:** TC testi üretim fonksiyonunu kopyalamıyor, kurallardan bağımsız kontrol yazıldı. Testler `BATCH_DIR`/`SEQUENCE_PATH`'i geçici klasöre yönlendiriyor; gerçek `sequence.json` etkilenmez.
**Açık sorunlar:** Form görselleri boş şablon değil, doldurulmuş form fotoğrafı; koordinat girişi boş taramayı bekliyor.
**Sıradaki adım:** Boş form taraması gelince koordinatları gir (faz1-trocr-main `sablon_koordinatlari.json`'dan aktarım).

---

## 2026-10-05

- Şablondan üretilmiş çalışma dosyaları kod okunarak yeniden yazıldı.
- Tespitler: `render_page` kullanılmıyor ve koordinat dosyası boş (editör hazır, veri yok); `config/` altında boş kalıntı dosyalar.

---

## Önceki Sürümler (README_V*.md'den)

- **v2** — ilk web arayüzü.
- **v3** — hekim yazım profilleri, NFM/N/Doğal gibi kısa ifadeler, alan bazlı boş bırakma, BMI/kan grubu tutarlılığı, sentetik TC, kompakt kart.
- **v3.1** — (README_V3_1.md).
- **v3.2** (2026-08-03 baseline commit) — batch yönetimi, Form ID arama, ZIP indirme, bütünlük kontrolü, arşiv/geri alma.

---

### Kayıt Şablonu

```markdown
## YYYY-AA-GG
**Yapılanlar:** ...
**Kararlar / neden:** ...
**Açık sorunlar:** ...
**Sıradaki adım:** ...
```
