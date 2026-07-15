# check_gpu.py — GPU kurulumunu doğrula
# Bu scripti çalıştırarak her şeyin hazır olduğundan emin oluruz

import torch

print("=" * 50)
print("PYTORCH VERSIYON:", torch.__version__)
print("=" * 50)

# CUDA (GPU destegi) kontrol
if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"[OK] GPU BULUNDU: {gpu_name}")
    print(f"[OK] GPU BELLEK: {gpu_memory:.1f} GB")
    print(f"[OK] CUDA VERSIYON: {torch.version.cuda}")
else:
    print("[!!] GPU bulunamadi -- CPU modu kullanilacak")

print("=" * 50)
