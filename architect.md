# architect.md — Synthetic Form Generator v3.2 Mimarisi

```
/ (form: adet, fill_rate, doctor_profile)
   │ POST /batch/create (= /generate)
   ▼
reserve_sequence(config/sequence.json, n) ──► start_number
generate_records(n, fill_rate, doctor_profile, start_index)
   │ her kayda "Form ID" = FORM-%05d
   ▼
save_batch → outputs/batches/BATCH-<YYYYmmdd_HHMMSS_ffffff>/ (records + metadata JSON)
create_excel → …/ground_truth.xlsx
validate_batch → hata varsa 500
   ▼
batch.html (özet) · /batch/<id>/cards (yazdırılabilir kartlar) · /batch/<id>/download/<excel|json|zip>
```

## Route'lar

| Route | İşlev |
|---|---|
| `GET /` | Üretim formu + son 10 batch |
| `POST /batch/create`, `POST /generate` | Batch üret |
| `GET /batch/<id>` / `…/cards` | Özet / kart görünümü |
| `GET /batch/<id>/download/<kind>` | Excel, JSON veya tüm klasör ZIP |
| `GET /batches` | Aktif + arşiv batch listesi |
| `GET /search?form_id=` | Form ID ile kayıt bulma |
| `POST /batch/<id>/archive` / `restore` | `outputs/archive` ↔ `outputs/batches` |
| `GET /batch/<id>/validate` | Bütünlük kontrolü (JSON) |
| `GET /coordinates`, `POST /coordinates/upload|save|delete` | Form görseli yükleme ve alan koordinatı düzenleme (`config/coordinates.json`, `static/forms/page{1,2}.jpeg`) |

## Veri Üretimi (`data_generator.py`)

- Kimlik: cinsiyete göre ad, `synthetic_tc(index)` (TC algoritmasına uygun 10./11. hane, test amaçlı).
- İş: `JOB_PROFILES` (perakende mağaza/depo pozisyonları), `IZMIR_STORES`, `PREVIOUS_EMPLOYERS`, önceki iş grupları tutarlılığı.
- Muayene: `EXAM_FIELDS` alan başına `minimal/normal/detailed` ifade havuzları; form içinde tek hekim profili (tutarlı dil); Boy/Kilo/BMI ve kan grubu/Rh tutarlılığı.
- Eksiklik: `fill_rate` (% doluluk, min %30) ile isteğe bağlı alanlar boş bırakılır.

## Mimari Kararlar

- **DB yok, klasör = batch**: ground truth taşınabilir, ZIP ile paylaşılabilir.
- **Global artan Form ID** (JSON dosyasında): taranan form ↔ kayıt eşleşmesi için tek anahtar.
- **İnsan eliyle doldurma**: gerçek el yazısı çeşitliliği; sentetik render (koordinat editörü) ileride tamamen otomatik veri için hazırlanıyor.
