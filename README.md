
# Fiş Okuma ve Bilgi Çıkarma Sistemi

Bu proje, alışveriş fişlerini okuyarak içerdikleri bilgileri (tarih, saat, mağaza adı, ürünler, KDV, toplam tutar vb.) çıkaran bir API servisidir. Mistral AI'nin görüntü işleme yeteneklerini kullanarak fişlerden yapılandırılmış veri elde eder.

## 🚀 Özellikler

- Fiş görüntülerini işleme ve metin çıkarma
- Çıkarılan metinden yapılandırılmış JSON verisi oluşturma
- Otomatik mağaza tipi sınıflandırması (gıda, petrol, giyim, elektronik, diğer)
- RESTful API endpoint'leri
- Base64 görüntü kodlama desteği

## 📋 Ön Koşullar

- Python 3.10.11
- pip (Python paket yöneticisi)
- OpenRouter API anahtarı

## 🔧 Kurulum

1. Depoyu klonlayın:
```bash
git clone <repository-url>
cd fis-okuma-sistemi
```

2. Sanal ortam oluşturun ve etkinleştirin:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Ortam değişkenlerini ayarlayın:
   
   `.env` dosyası oluşturun ve OpenRouter API anahtarınızı ekleyin:
   ```
   OPENAI_API_KEY=your_openrouter_api_key_here
   ```

## 🏃‍♂️ Çalıştırma

1. Uygulamayı başlatın:
```bash
uvicorn main:app --reload
```

2. Tarayıcınızda API dokümantasyonuna erişin:
```
http://localhost:8000/docs
```

## 📊 API Kullanımı

### Fiş Yükleme Endpoint'i

**POST** `/upload`

Fiş görüntüsünü yüklemek ve bilgileri çıkarmak için bu endpoint'i kullanın.

**Request:**
- Form-data: `file` (görüntü dosyası)

**Response:**
```json
{
  "tarih": "13/05/2025",
  "saat": "14:30",
  "magaza": "A101 Market",
  "urunler": [
    {"ad": "Jeli Port 114G", "fiyat": "12,50"},
    {"ad": "NSCF 3ü1 FINDIKLI 17", "fiyat": "9,75"}
  ],
  "toplam_kdv": "5,25",
  "toplam": "22,25",
  "fis_tipi": "gida"
}
```

### Örnek İstek (cURL)

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@receipt.jpg"
```

### Örnek İstek (Python)

```python
import requests

url = "http://localhost:8000/upload"
files = {"file": open("receipt.jpg", "rb")}
response = requests.post(url, files=files)

print(response.json())
```


## ⚙️ Yapılandırma

Proje, aşağıdaki yapılandırma seçeneklerini destekler:

- `OPENAI_API_KEY`: OpenRouter API anahtarınız (gerekli)
- Varsayılan model: `mistralai/mistral-small-3.1-24b-instruct:free`


## 🛠️ Geliştirme

Projeyi geliştirmek için:

1. Depoyu fork'layın
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişiklikleri commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun


## ❓ Sorun Giderme

### Sık Karşılaşılan Sorunlar

1. **API anahtarı hatası**: `.env` dosyasında doğru API anahtarınızın olduğundan emin olun
2. **Görüntü formatı hatası**: JPEG, PNG veya WebP formatlarını kullanın
3. **Bağımlılık hataları**: Tüm gereksinimleri doğru yüklediğinizden emin olun

### Hata Ayıklama

Detaylı loglar için uygulamayı debug modunda çalıştırın:
```bash
uvicorn main:app --reload --log-level debug
```

**Not**: Bu proje geliştirme aşamasındadır ve performans iyileştirmeleri yapılmaktadır.
