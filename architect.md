# architect.md — Synthetic Form Generator v2 Mimari Referansı

Bu dosya projenin yapısının hızlı-referans özetidir. Kod değiştikçe güncel tutun.

## Genel Bakış

python -m venv venv

## Teknoloji Yığını

- Flask
- openpyxl

## Dizin Yapısı

```
.gitignore
README_V2.md
README_V3.md
README_V3_1.md
README_V3_2.md
app.py
config/
  coordinates.json
  fields.json
  jobs.json
  outputs
  sequence.json
requirements.txt
services/
  __init__.py
  batch_storage.py
  data_generator.py
  excel_exporter.py
  form_renderer.py
  sequence_manager.py
static/
templates/
  _base_style.html
  batch.html
  batches.html
  cards.html
  coordinates.html
  index.html
  search.html
```

## Modüller / Kaynak Dosyalar

- `app.py`
- `services/batch_storage.py`
- `services/data_generator.py`
- `services/excel_exporter.py`
- `services/form_renderer.py`
- `services/sequence_manager.py`

## Giriş Noktaları ve Yapılandırma

- `app.py`
- `requirements.txt`
- `templates/index.html`

## Dağıtım / Çalışma Ortamı

- GitHub: https://github.com/SHapeloglu/SyntheticFormGenerator_v3.2

## Diğer Dokümanlar

- `README_V2.md`
- `README_V3.md`
- `README_V3_1.md`
- `README_V3_2.md`

## Mimari Kararlar

_Önemli tasarım kararlarını ve gerekçelerini buraya ekleyin (ör. "X yerine Y seçildi çünkü ...")._
