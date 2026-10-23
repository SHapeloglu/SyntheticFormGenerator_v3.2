# session.md — Synthetic Form Generator Oturum Günlüğü

---

## 2026-10-08 (2) — v3.3 ve ilk 50 form

**Yapılanlar:** Üretici faz1-trocr-main'in 92 alanlık şablonuna hizalandı (ayrıntı task.md). İlk batch `BATCH-20261008_113109_843050` üretildi; `kartlar.pdf` (wkhtmltopdf, `--zoom 1.4`, 100 sayfa).
**Kararlar / neden:** Değer biçimleri gerçek ground truth'un *biçim kalıplarından* alındı (harf→a, rakam→9; gerçek değerler okunmadı/basılmadı). Kişi no ve TC Form ID aralığından gelir → batch'ler arası çakışma yok. Taramalar faz1 kuralıyla `<OCR ID><sayfa>` (ör. `sfg000011.jpeg`) adlandırılır.
**Açık sorunlar:** wkhtmltopdf CSS grid'i işlemiyor → kart düzeni inline-block. Faker'ın bazı adları sıra dışı (ör. "İncifir") — el yazısı için sorun değil.
**Sıradaki adım:** Formlar doldurulup taranınca `ocr_ground_truth/*.json` faz1 `data/cikti/ground_truth/`'a, taramalar giriş klasörüne; 10 test formu `--test-formlari` ile ayrılır.

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

## 2026-10-23 — kart sırası, tam dolu mod, kısa ev adresi
**Yapılanlar:** (1) Kartlar matbu formun okuma sırasında (sayfa, yukarıdan aşağı, soldan sağa; `MATBU_SIRA`, faz1 `sablon_koordinatlari.json`'dan) — 92 alandan 20'si eski sıradan farklıydı (soygeçmiş, Hayır daireleri). (2) `fill_rate=100` artık **tam dolu**: muayene, tetkik, anamnez, aşı, bilgi kutuları hep dolu (kalan boşlar "Yok"); Hayır daireli sorular (hastanede yattınız mı, sigara, alkol…) ve TA diastolik kutusu doğal olarak boş kalır. (3) **Bekârda çocuk soygeçmişi hiçbir modda yazılmaz.** (4) **Ev adresi yalnız ilçe ve il** ("Buca / İzmir"); mahalle/sokak yok (işveren adresi aynı kaldı).
**Kararlar / neden:** Eski %100 seçeneğinde bile alanların ~%27'si boştu (muayene/tetkik olasılıkları sabitti, gerçek hekim boşluğunu taklit ediyordu). Gönüllünün kartı boş formda atlamadan doldurması ve OCR'a dolu veri vermesi için tam dolu mod eklendi; %85-90 seçenekleri eski davranışta.
**Sıradaki adım:** 50 yeni form üret (doluluk %100), PDF'e çevir, doldurulup taranınca `ocr_ground_truth/*.json` faz1'e (önce üretici batch'i EK-2 kayıtlarıyla eşleştirilebilir: etiketleme önerisi olarak kullanılabilir).
**Ek (aynı gün):** Anamnez (şikâyet/hastalık) hücrelerinde "NFM" yazılacak yerlerin %15'i **✓ (tik)**, %15'i **N** oldu (`NFM_TIK_ORANI`, `NFM_N_ORANI`); kalan %70 NFM. Muayene/tetkik varyantlarında N zaten vardı. Not: OCR tarafı etiket sözlüğünde metin hücresindeki tik için kural yok → etiketlerken değer `✓` yazılacak (ETIKETLEME_SOZLUGU'na eklenmeli).
