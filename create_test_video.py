# create_test_video.py
# Eğer video indirilemezse, sentetik bir test videosu oluşturuyoruz
# Gerçek futbol videosu olmasa da YOLO'nun çalıştığını görürüz
# Sonra istediğin bir videoyu manuel koyarsın

import cv2
import numpy as np
import os

OUTPUT = "sample_football.mp4"

if os.path.exists(OUTPUT):
    print(f"[OK] Video zaten mevcut: {OUTPUT}")
    import sys; sys.exit(0)

print("[*] Sentetik test videosu olusturuluyor...")

# Video ayarları
WIDTH, HEIGHT = 1280, 720
FPS = 30
DURATION_SEC = 10  # 10 saniye
TOTAL_FRAMES = FPS * DURATION_SEC

# Yeşil saha rengi
FIELD_COLOR = (34, 139, 34)  # BGR: yeşil

# Video yazıcı
fourcc = cv2.VideoWriter.fourcc(*"mp4v")
out = cv2.VideoWriter(OUTPUT, fourcc, FPS, (WIDTH, HEIGHT))

# Top pozisyonu (hareket edecek)
ball_x, ball_y = 200, 360
ball_vx, ball_vy = 8, 5  # hız (pixel/kare)
ball_radius = 20

# Oyuncu pozisyonları (3 oyuncu)
players = [
    {"x": 300, "y": 200, "vx": 3, "vy": 2, "color": (255, 50, 50)},   # Mavi
    {"x": 700, "y": 450, "vx": -4, "vy": 3, "color": (255, 50, 50)},  # Mavi
    {"x": 1000, "y": 300, "vx": -2, "vy": -4, "color": (50, 50, 200)}, # Kırmızı
]

for frame_num in range(TOTAL_FRAMES):
    # Saha çiz (yeşil zemin + çizgiler)
    frame = np.full((HEIGHT, WIDTH, 3), FIELD_COLOR, dtype=np.uint8)

    # Orta çizgi
    cv2.line(frame, (WIDTH//2, 0), (WIDTH//2, HEIGHT), (255, 255, 255), 2)

    # Orta daire
    cv2.circle(frame, (WIDTH//2, HEIGHT//2), 100, (255, 255, 255), 2)

    # Ceza sahası sol
    cv2.rectangle(frame, (0, HEIGHT//4), (150, 3*HEIGHT//4), (255, 255, 255), 2)

    # Ceza sahası sağ
    cv2.rectangle(frame, (WIDTH-150, HEIGHT//4), (WIDTH, 3*HEIGHT//4), (255, 255, 255), 2)

    # Kale sol
    cv2.rectangle(frame, (0, HEIGHT//3), (50, 2*HEIGHT//3), (255, 255, 255), 3)

    # Kale sağ
    cv2.rectangle(frame, (WIDTH-50, HEIGHT//3), (WIDTH, 2*HEIGHT//3), (255, 255, 255), 3)

    # Oyuncuları hareket ettir ve çiz
    for p in players:
        p["x"] += p["vx"]
        p["y"] += p["vy"]

        # Sınırları kontrol et
        if p["x"] < 30 or p["x"] > WIDTH - 30:
            p["vx"] *= -1
        if p["y"] < 30 or p["y"] > HEIGHT - 30:
            p["vy"] *= -1

        # Oyuncu çiz (dikdörtgen + gövde)
        px, py = int(p["x"]), int(p["y"])
        cv2.rectangle(frame, (px-15, py-40), (px+15, py+20), p["color"], -1)  # gövde
        cv2.circle(frame, (px, py-50), 15, (200, 160, 100), -1)  # kafa

    # Topu hareket ettir
    ball_x += ball_vx
    ball_y += ball_vy

    if ball_x < ball_radius or ball_x > WIDTH - ball_radius:
        ball_vx *= -1
    if ball_y < ball_radius or ball_y > HEIGHT - ball_radius:
        ball_vy *= -1

    # Topu çiz (siyah-beyaz futbol topu gibi)
    cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, (255, 255, 255), -1)
    cv2.circle(frame, (int(ball_x), int(ball_y)), ball_radius, (0, 0, 0), 2)

    # Frame sayacı
    cv2.putText(frame, f"TEST VIDEO - Kare {frame_num+1}/{TOTAL_FRAMES}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    out.write(frame)

    if (frame_num + 1) % 60 == 0:
        print(f"    {frame_num+1}/{TOTAL_FRAMES} kare olusturuldu")

out.release()
print(f"[OK] Test videosu hazir: {OUTPUT} ({TOTAL_FRAMES} kare, {DURATION_SEC} saniye)")
print("[!]  NOT: Bu sentetik bir video. YOLO buradaki 'nesneleri' tanimayabilir.")
print("     Gercek futbol videosu icin bir mp4 dosyasini 'sample_football.mp4'")
print("     adıyla bu klasore kopyala, sonra detect.py'i calistir.")
