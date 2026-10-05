# backlog.md — Synthetic Form Generator Fikir Havuzu

- Tamamen sentetik görsel üretimi: koordinatlara el yazısı fontlarıyla (çeşitli fontlar, eğim, gürültü) yazdırıp OCR için otomatik veri.
- faz1-trocr ile doğrudan dışa aktarım formatı (alan kırpıntısı + etiket satırları).
- Farklı form şablonları (yalnız işe giriş değil; ör. İSG eğitim katılım formu) — şablon tanımı JSON'dan.
- Farklı il/sektör profilleri (şu an İzmir perakende).
- Batch başına üretim parametrelerinden "tekrar üretilebilir" seed.

## Ekleme Şablonu

```markdown
### Başlık
- **Kategori:** yeni özellik / iyileştirme / teknik borç / araştırma
- **Neden:** kısa gerekçe
- **Notlar:** büyüklük, bağımlılıklar, riskler
```
