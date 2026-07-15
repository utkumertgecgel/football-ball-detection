# =============================================================
# PROJE 1: Futbol Topu & Oyuncu Tespiti — YOLO ile
# =============================================================
# Bu dosya ne yapar?
#   1. YOLOv8 modelini yükler (internetten otomatik indirir)
#   2. Bir video dosyasını frame frame okur
#   3. Her frame'de top ve oyuncuları tespit eder
#   4. Tespit edilen nesnelerin üzerine kutu + label çizer
#   5. Sonucu yeni bir video olarak kaydeder
# =============================================================

# --- KÜTÜPHANELER ---
# cv2 = OpenCV. Video/görüntü okuma, yazma, çizim işlemleri
import cv2

# YOLO = Ultralytics'in YOLO sınıfı. Modeli yüklemek + çalıştırmak için
from ultralytics import YOLO

# time = FPS hesaplamak için zaman ölçeceğiz
import time

# os = dosya yollarını kontrol etmek için
import os


# =============================================================
# AYARLAR — Buradan her şeyi değiştirebilirsin
# =============================================================

# Hangi YOLO modelini kullanalım?
# yolov8n.pt = nano (en küçük, en hızlı — 4GB VRAM için ideal)
# yolov8s.pt = small (biraz daha doğru ama yavaş)
# yolov8m.pt = medium (daha doğru, daha fazla VRAM ister)
MODEL_PATH = "yolov8n.pt"

# Video dosyası yolu (aşağıda sample video indireceğiz)
VIDEO_PATH = "sample_football.mp4"

# Çıktı videosu nereye kaydedilsin?
OUTPUT_PATH = "output/detected.mp4"

# Kaç confidence (güven skoru) üstündeki tespitleri gösterelim?
# 0.0 = her şeyi göster (çok gürültülü)
# 0.5 = %50 emin olan tespitleri göster (makul)
# 0.8 = sadece çok emin olunca göster
CONFIDENCE = 0.4

# COCO veri setinde hangi sınıfları tespit edelim?
# YOLO "COCO" veri setiyle eğitildi → 80 farklı nesne sınıfı var
# 0 = "person" (kişi / oyuncu)
# 32 = "sports ball" (top)
# Sadece bu ikisini görmek istiyoruz, gerisi ilgilendirmiyor
TARGET_CLASSES = [0, 32]

# Her sınıf için renk (BGR formatı — OpenCV'de RGB değil BGR kullanılır!)
# person = mavi, sports ball = kırmızı
COLORS = {
    0: (255, 100, 0),   # Oyuncu → Mavi
    32: (0, 0, 255),    # Top → Kırmızı
}

# Sınıf isimlerini Türkçeleştirelim
CLASS_NAMES = {
    0: "Oyuncu",
    32: "Top",
}


# =============================================================
# ADIM 1: Output klasörünü oluştur
# =============================================================
os.makedirs("output", exist_ok=True)
# os.makedirs → klasör oluşturur
# exist_ok=True → "klasör zaten varsa hata verme" demek


# =============================================================
# ADIM 2: YOLO Modelini Yükle
# =============================================================
print("[*] Model yukleniyor:", MODEL_PATH)
model = YOLO(MODEL_PATH)
# Bu satır ilk çalıştığında modeli internetten indirir (~6MB)
# Sonraki çalışmalarda cache'den yükler
print("[OK] Model hazir!")


# =============================================================
# ADIM 3: Videoyu Aç
# =============================================================
print("[*] Video aciliyor:", VIDEO_PATH)

# VideoCapture → OpenCV'nin video okuyucusu
# Argüman olarak dosya yolu veya 0 (webcam) alır
cap = cv2.VideoCapture(VIDEO_PATH)

# Video açıldı mı kontrol et
if not cap.isOpened():
    print("[HATA] Video acilamadi! Dosya mevcut mu?")
    print("       Beklenen konum:", os.path.abspath(VIDEO_PATH))
    exit()

# Video metadata'sını oku
# CAP_PROP_FPS = saniyedeki kare sayısı (Frame Per Second)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Video genişliği (pixel)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Video yüksekliği (pixel)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"[OK] Video: {width}x{height} @ {fps:.1f} FPS | Toplam kare: {total_frames}")


# =============================================================
# ADIM 4: Çıktı Videosunu Hazırla
# =============================================================
# VideoWriter → işlenmiş kareleri video dosyasına yazar
# 'mp4v' = MP4 formatı için codec
fourcc = cv2.VideoWriter.fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))


# =============================================================
# ADIM 5: Ana Döngü — Her Kareyi İşle
# =============================================================
print("[*] Tespit basliyor...")
frame_count = 0

while True:
    # cap.read() → videodan bir kare okur
    # ret = True/False (kare okunabildi mi?)
    # frame = numpy array (o karenin piksel verisi)
    ret, frame = cap.read()

    # ret False ise video bitti demek → döngüden çık
    if not ret:
        break

    frame_count += 1

    # Her 30 karede bir ilerleme göster
    if frame_count % 30 == 0:
        print(f"    Isleniyor: {frame_count}/{total_frames} kare")

    # --- YOLO'yu Çalıştır ---
    # model() → bu kareyi YOLO'ya ver, tespit et
    # classes=TARGET_CLASSES → sadece person ve top'u ara
    # conf=CONFIDENCE → güven eşiği
    # verbose=False → her kare için terminal'e çıktı yazma (çok gürültülü olur)
    # device='cuda' → GPU kullan (yoksa 'cpu')
    results = model(
        frame,
        classes=TARGET_CLASSES,
        conf=CONFIDENCE,
        verbose=False,
        device="cuda"
    )

    # --- Tespitleri Üzerine Çiz ---
    # results[0] → ilk (ve tek) frame'in sonuçları
    # .boxes → tespit edilen tüm kutular
    for box in results[0].boxes:
        # Kutu koordinatlarını al (xyxy formatı: sol-üst x, y → sağ-alt x, y)
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Sınıf id'si (0=person, 32=sports ball)
        class_id = int(box.cls[0])

        # Güven skoru (0.0 - 1.0 arası)
        confidence = float(box.conf[0])

        # Bu sınıf için rengi al
        color = COLORS.get(class_id, (0, 255, 0))

        # Label metni: "Oyuncu %87" gibi
        label = f"{CLASS_NAMES.get(class_id, 'Nesne')} %{confidence*100:.0f}"

        # Dikdörtgeni çiz
        # frame = üzerine çizeceğimiz görüntü
        # (x1, y1) = sol üst köşe
        # (x2, y2) = sağ alt köşe
        # color = renk
        # 2 = çizgi kalınlığı (pixel)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Label için arka plan kutusu çiz (okunabilir olsun diye)
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        cv2.rectangle(
            frame,
            (x1, y1 - label_size[1] - 8),
            (x1 + label_size[0] + 4, y1),
            color,
            -1  # -1 = içini doldur
        )

        # Label yazısını yaz
        cv2.putText(
            frame,
            label,
            (x1 + 2, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,  # font
            0.6,   # font boyutu
            (255, 255, 255),  # beyaz yazı
            1,     # kalınlık
            cv2.LINE_AA  # anti-aliasing (pürüzsüz kenar)
        )

    # --- Frame Sayacı Ekle ---
    cv2.putText(
        frame,
        f"Kare: {frame_count}/{total_frames}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (200, 200, 200),
        2,
        cv2.LINE_AA
    )

    # İşlenmiş kareyi çıktı videosuna yaz
    out.write(frame)


# =============================================================
# ADIM 6: Temizlik
# =============================================================
cap.release()   # Video okuyucuyu kapat
out.release()   # Video yazıcıyı kapat (dosyayı kaydet!)

print()
print("=" * 50)
print(f"[OK] Tamamlandi! {frame_count} kare islendi.")
print(f"[OK] Cikti kaydedildi: {os.path.abspath(OUTPUT_PATH)}")
print("=" * 50)
