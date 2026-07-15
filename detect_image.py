# detect_image.py — Önce tek bir resim üzerinde test edelim
# Ultralytics'in kendi zidane.jpg dosyasını kullanıyoruz (Zidane futbol oynarken!)

import cv2
from ultralytics import YOLO
import os

# Model yükle
model = YOLO("yolov8n.pt")

# Ultralytics'in kendi resim dosyasını bul
import ultralytics
assets_path = os.path.join(os.path.dirname(ultralytics.__file__), "assets")
image_path = os.path.join(assets_path, "zidane.jpg")

print("[*] Resim uzerinde tespit yapiliyor:", image_path)

# YOLO'yu çalıştır — tüm nesneleri tespit et
results = model(image_path, conf=0.4, verbose=False)

# Sonuçları göster
result = results[0]
print(f"[OK] Tespit tamamlandi!")
print(f"     Bulunan nesne sayisi: {len(result.boxes)}")
print()

# Her tespiti yazdır
for i, box in enumerate(result.boxes):
    class_id = int(box.cls[0])
    class_name = model.names[class_id]  # model.names = COCO sınıf isimleri
    confidence = float(box.conf[0])
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    print(f"  [{i+1}] {class_name} | Guven: %{confidence*100:.0f} | Konum: ({x1},{y1}) -> ({x2},{y2})")

# Ultralytics'in kendi görselleştirmesini kullanalım (en kolay yol)
os.makedirs("output", exist_ok=True)
annotated = result.plot()  # result.plot() = üzerine kutular çizilmiş resim döner

# Kaydet
output_path = "output/zidane_detected.jpg"
cv2.imwrite(output_path, annotated)
print()
print(f"[OK] Sonuc kaydedildi: {os.path.abspath(output_path)}")
print("     Dosyayi ac ve kutulari gor!")
