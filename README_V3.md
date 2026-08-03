# Synthetic Form Generator v3

Bu sürüm, doktor olmayan kişilerin kartta gördüğü veriyi boş matbu işe giriş/periyodik muayene formuna aynen aktarması için geliştirilmiştir.

## Başlıca yenilikler
- Minimalist, normal, ayrıntılı veya rastgele dağıtılan pratisyen hekim yazım profili
- NFM, N, Doğal, Patoloji yok gibi kısa tıbbi ifadeler
- Her form içinde tutarlı muayene dili
- Alan bazlı gerçekçi boş bırakma oranları
- Boy/Kilo/BMI, kan grubu/Rh ve önceki iş gruplarında tutarlılık
- Unvansız çalışan adları
- 11 haneli sayısal sentetik test TC kimlik numarası
- Form tarihi olarak üretim günü
- Daha kompakt, tek sayfaya sığmaya odaklı kart görünümü
- Kartın üst ve alt bölümünde Form ID

## Çalıştırma
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Tarayıcı: http://127.0.0.1:5000

Önce 3–5 form üreterek detaylı kartların yazdırma önizlemesini kontrol edin. Sonra 50–60 form üretin.
