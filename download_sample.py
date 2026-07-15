# download_sample.py — Test videosu indir
# Ultralytics'in kendi assets sistemini kullanıyoruz

from ultralytics.utils import ASSETS
import urllib.request
import os
import sys

# YouTube'dan kısa bir futbol klibi indir (yt-dlp kullanmadan)
# Wikimedia Commons'tan ücretsiz futbol videosu
URL = "https://upload.wikimedia.org/wikipedia/commons/transcoded/a/a3/Brazil_and_Germany_match_at_the_FIFA_World_Cup_2014-07-08_%28cropped%29.webm/Brazil_and_Germany_match_at_the_FIFA_World_Cup_2014-07-08_%28cropped%29.webm.360p.webm"
OUTPUT = "sample_football.mp4"

if os.path.exists(OUTPUT):
    print(f"[OK] Video zaten mevcut: {OUTPUT}")
    sys.exit(0)

print("[*] Futbol videosu indiriliyor...")
print("    Kaynak: Wikimedia Commons (FIFA World Cup 2014)")

def progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        pct = min(downloaded / total_size * 100, 100)
        print(f"\r    Ilerleme: {pct:.1f}% ({downloaded//1024//1024}MB / {total_size//1024//1024}MB)", end="", flush=True)

try:
    urllib.request.urlretrieve(URL, OUTPUT, reporthook=progress)
    print(f"\n[OK] Indirildi: {OUTPUT}")
except Exception as e:
    print(f"\n[HATA] {e}")
    print("Manuel olarak bir futbol videosu 'sample_football.mp4' adıyla klasöre koy.")
