# SyntheticFormGenerator v3.1

Bu sürüm hafta sonu el yazısı veri toplama çalışması için kritik kimlik ve tutarlılık düzeltmelerini içerir.

## Değişiklikler

- Form numarası kalıcıdır; uygulama kapatılıp açılsa da kaldığı yerden devam eder.
- Her formun sentetik T.C. numarası global form numarasına bağlı ve benzersizdir.
- Önceki iş tarihleri kronolojik, yaşla uyumlu ve birbiriyle çakışmayacak biçimde üretilir.
- Ayrıntılı muayene ifadeleri matbu alanlara daha rahat sığacak şekilde kısaltılmıştır.
- Batch kimliğinde mikrosaniye kullanılarak aynı saniyede oluşabilecek klasör çakışması önlenmiştir.

## Önemli

`config/sequence.json` dosyasını silmeyin. Bu dosya sıradaki form numarasını saklar.
Eski v3 test kartlarını kullanmayın; v3.1 ile yeni kartlar üretin.
