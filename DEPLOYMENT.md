# Deployment Guide untuk Hungarian Method Calculator

## Masalah yang Diperbaiki

### 1. Error pip install dengan Python 3.12
**Masalah:** Vercel menggunakan Python 3.12 yang menyebabkan konflik dependency
**Solusi:** 
- Mengubah `runtime.txt` ke `python-3.11`
- Menyederhanakan `requirements.txt` dengan versi yang kompatibel

### 2. Struktur File yang Diperbaiki
```
api/
└── index.py          # Entry point untuk Vercel
app/
├── main.py           # Aplikasi Flask utama
├── config.py         # Konfigurasi
├── hungarian.py      # Algoritma Hungarian
└── utils.py          # Utilities
runtime.txt           # Versi Python
requirements.txt      # Dependencies minimal
vercel.json           # Konfigurasi Vercel
.vercelignore         # File yang diabaikan
```

## Langkah Deployment ke Vercel

### 1. Commit dan Push ke GitHub
```bash
git add .
git commit -m "Fix Vercel deployment configuration"
git push origin main
```

### 2. Konfigurasi di Vercel Dashboard
1. **Build and Output Settings:**
   - Build Command: (kosongkan)
   - Output Directory: (kosongkan)
   - Install Command: `pip install -r requirements.txt`

2. **Environment Variables:**
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `your-secret-key-here`

### 3. Deploy
Klik "Deploy" dan tunggu proses selesai.

## Troubleshooting

### Jika masih error:
1. Periksa Build Logs di Vercel
2. Pastikan semua file sudah ter-push ke GitHub
3. Coba redeploy dengan "Redeploy" button

### Error umum:
- **Module not found:** Pastikan struktur import sudah benar
- **Dependency conflict:** Gunakan versi yang lebih lama atau hapus dependency yang tidak perlu
- **Python version:** Gunakan Python 3.11 atau 3.10

## File Penting

### requirements.txt (minimal)
```
flask==2.3.2
werkzeug==2.3.6
numpy==1.24.3
pandas==2.0.3
openpyxl==3.1.2
```

### runtime.txt
```
python-3.11
```

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

## Setelah Deployment Berhasil

1. Test semua fitur aplikasi
2. Periksa console browser untuk error JavaScript
3. Test upload file dan perhitungan Hungarian Method
4. Verifikasi download hasil berfungsi

## Tips Optimasi

1. **Performance:** Gunakan caching untuk hasil perhitungan
2. **Security:** Jangan hardcode secret keys
3. **Monitoring:** Setup error tracking dengan Sentry
4. **Analytics:** Tambahkan Google Analytics jika diperlukan

Dengan konfigurasi ini, aplikasi Hungarian Method Calculator seharusnya dapat di-deploy dengan sukses ke Vercel.