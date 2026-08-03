# Synthetic Form Generator v2

## Kurulum
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Tarayıcı: http://127.0.0.1:5000

## Yeni akış
1. Form sayısını ve doluluk oranını seçin.
2. Detaylı veya sade doldurma kartlarını açın.
3. Kartları yazdırın ve boş matbu formlarla eşleştirin.
4. Katılımcı karttaki değerleri kendi el yazısıyla forma aktarır.
5. `FORM-00001` benzeri Form ID matbu formun sağ üst köşesine yazılır.
6. Excel/JSON ground truth dosyasını OCR sonuçlarını karşılaştırmak için saklayın.

## İki kart görünümü
- **Detaylı kart:** Kullanıcının talep ettiği geniş alan listesini verir.
- **Sade kart:** Gerçek formlarda daha sık doldurulan temel alanlara odaklanan alternatif sayfadır.

Koordinat editörü ve eski renderer kodu korunmuştur.
