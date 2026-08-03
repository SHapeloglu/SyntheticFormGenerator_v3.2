# SyntheticFormGenerator v3.2 — Batch Management

## Eklenenler

- Geçmiş batch yönetim ekranı (`/batches`)
- FORM ID arama (`/search`)
- Batch detayında tüm formların listesi
- Excel, JSON ve tüm batch içeriğini kapsayan ZIP indirme
- Batch bütünlük kontrolü
- Form ID tekrar ve metadata tutarlılık denetimi
- Güvenli arşivleme ve geri alma
- Yeni batch üretiminden sonra otomatik doğrulama

## Çalıştırma

```bash
pip install -r requirements.txt
python app.py
```

Tarayıcı: `http://127.0.0.1:5000`

## Önemli

- `config/sequence.json` silinmemelidir.
- `outputs/batches` ground truth kayıtlarını içerir.
- Arşivlenen kayıtlar `outputs/archive` altına taşınır.
