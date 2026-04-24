# Yapay Sinir Ağları Projesi - Veri Toplama Modülü

Bu proje, yapay sinir ağları projeleri için YouTube üzerinden müzik verisi ve bu videolara ait istatistiksel metadataları otomatik olarak toplayan bir Python aracıdır.

## Özellikler

- Belirtilen YouTube linklerinden videoları en iyi ses kalitesinde (mp3 formatında) indirir.
- YouTube Data API v3 kullanarak indirilen videolara ait istatistikleri (izlenme sayısı, beğeni sayısı, favori sayısı, yorum sayısı) çeker.
- İstatistik verilerini toplu olarak (bulk) ve hızlı bir şekilde alır.
- Çekilen istatistikleri bir CSV dosyasına kaydeder.

## Proje Yapısı

```
Yapay-Sinir-Aglari-Proje/
│
├── .env                    # YouTube API anahtarını içeren ortam değişkenleri dosyası
├── requirements.txt        # Gerekli Python kütüphaneleri
│
└── src/
    └── data_collection/
        ├── collect_data.py # Ana veri toplama ve indirme betiği
        ├── youtube_api.py  # YouTube API ve indirme işlemlerini yöneten yardımcı modül
        └── links.txt       # İndirilecek YouTube linklerinin listesi
```

## Gereksinimler

Bu projeyi çalıştırabilmek için bilgisayarınızda [Python](https://www.python.org/downloads/) yüklü olmalıdır. Ek olarak, bir YouTube Data API v3 anahtarına ihtiyacınız vardır.

- Python 3.7+
- FFmpeg (Ses dosyalarını mp3'e çevirmek için yt-dlp tarafından gereklidir)

## Kurulum

1. **Depoyu klonlayın veya indirin:**
   ```bash
   git clone <repo-url>
   cd Yapay-Sinir-Aglari-Proje
   ```

2. **Gerekli Python kütüphanelerini yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg kurulumu:**
   `yt-dlp`'nin videoları mp3 formatına çevirebilmesi için sisteminizde FFmpeg kurulu ve yolunun (PATH) tanımlı olması gerekmektedir.
   - **MacOS:** `brew install ffmpeg`
   - **Windows:** [FFmpeg indir](https://ffmpeg.org/download.html) ve ortam değişkenlerine ekle.
   - **Linux:** `sudo apt install ffmpeg`

4. **API Anahtarını ayarlayın:**
   Proje ana dizininde `.env` adında bir dosya oluşturun ve içerisine YouTube API anahtarınızı ekleyin:
   ```env
   YOUTUBE_API_KEY=sizin_api_anahtariniz_buraya
   ```

## Kullanım

1. `src/data_collection/links.txt` dosyasını açın ve her satıra bir tane gelecek şekilde indirmek istediğiniz YouTube linklerini ekleyin.

2. Veri toplama betiğini çalıştırın:
   ```bash
   python src/data_collection/collect_data.py
   ```

## Çıktılar

- **Ses Dosyaları:** İndirilen ses dosyaları `data/raw/music/` dizinine kaydedilir.
- **İstatistikler:** Çekilen video istatistikleri `data/raw/` dizinindeki `video_statistics.csv` dosyasına kaydedilir.
