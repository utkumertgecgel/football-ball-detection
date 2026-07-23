# Futbol Topu & Oyuncu Tespiti — YOLOv8 ile

>  Bu proje aktif geliştirme aşamasındadır.

---
## 🎯 Proje Nedir?

Bu proje, bir futbol maçı videosunu girdi olarak alır ve YOLOv8 derin öğrenme modeli kullanarak:

- 🔵 **Oyuncuları** tespit eder ve mavi kutu içine alır
- 🔴 **Topu** tespit eder ve kırmızı kutu içine alır
- 📹 Tespit edilen nesneleri işaretlenmiş şekilde **yeni bir video olarak kaydeder**

Temel amaç: Ham video → Nesne konumu verisi üretmek. Bu konum verisi üzerinden **mesafe analizi, ısı haritası, taktik analiz** gibi ileri seviye özellikler geliştirilebilir.

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Amaç |
|-----------|------|
| Python 3.12 | Ana programlama dili |
| YOLOv8n (Ultralytics) | Gerçek zamanlı nesne tespiti |
| OpenCV | Video okuma / yazma / görüntü işleme |
| PyTorch + CUDA 11.8 | GPU destekli model çalıştırma |

---

## ⚙️ Kurulum

### Gereksinimler
- Python 3.10+
- NVIDIA GPU (isteğe bağlı ama önerilir)
- CUDA 11.8 (GPU kullanımı için)

### Adımlar

```bash
# 1. Depoyu klonla
git clone https://github.com/KULLANICI_ADIN/football-ball-detection.git
cd football-ball-detection

# 2. Sanal ortam oluştur ve aktif et
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

# 3. PyTorch'u GPU desteğiyle kur (CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Sadece CPU kullanacaksan:
# pip install torch torchvision

# 4. Diğer bağımlılıkları kur
pip install ultralytics opencv-python matplotlib
```

---

## 🚀 Kullanım

### Resim Üzerinde Test

```bash
python detect_image.py
```

Çıktı: `output/zidane_detected.jpg`

### Video Üzerinde Tespit

1. Analiz etmek istediğin videoyu projenin ana klasörüne koy
2. Dosyayı `sample_football.mp4` olarak yeniden adlandır
3. Çalıştır:

```bash
python detect.py
```

Çıktı: `output/detected.mp4`

---

## 📁 DosyaYapısı

```
football-ball-detection/
│
├── detect.py              # Ana video tespit scripti
├── detect_image.py        # Tek resim tespit scripti (hızlı test)
├── check_gpu.py           # GPU kurulum doğrulama
├── create_test_video.py   # Sentetik test videosu oluşturucu
├── requirements.txt       # Bağımlılıklar
│
└── output/                # İşlenmiş çıktılar (git'e dahil değil)
```

---

## 🔍 Nasıl Çalışır?

```
Giriş Videosu
      ↓
  Frame Frame Oku (OpenCV)
      ↓
  YOLO'ya Her Frame'i Ver
      ↓
  "Burada oyuncu var" → Koordinatlar
  "Burada top var"   → Koordinatlar
      ↓
  Koordinatlara Kutu + Etiket Çiz
      ↓
Çıkış Videosu (işaretlenmiş)
```

YOLO (You Only Look Once), görüntüyü bir grid'e böler ve her hücre için nesne olasılığını **tek seferde** hesaplar. Bu sayede gerçek zamanlıya yakın hızda tespit yapabilir.

---

## 📊 Mevcut Durum & Bilinen Eksikler

- [x] Temel oyuncu tespiti
- [x] Top tespiti (kısmi — küçük ve hızlı toplarda kayıp yaşanabilir)
- [x] GPU desteği
- [ ] Oyuncu takibi (ID bazlı — ByteTrack entegrasyonu)
- [ ] Hakem / teknik direktör ayırt etme
- [ ] Forma rengiyle takım ayrımı
- [ ] Mesafe ve hız istatistikleri
- [ ] Isı haritası (heatmap) çıktısı
- [ ] Masaüstü / web arayüzü

---

## 🗺️ Yol Haritası

Gelecek güncellemeler:

1. **ByteTrack** ile oyuncu ID takibi
2. **Forma rengi** ile takım ayrımı
3. **Heatmap** çıktısı
4..?
.
.


---

## 🤝 Katkı

Proje geliştirme aşamasında olduğundan katkı ve öneriler memnuniyetle karşılanır. Issue açabilir veya pull request gönderebilirsiniz.


