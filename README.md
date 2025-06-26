# Hungarian Method Calculator

🎯 **Aplikasi Web untuk Menyelesaikan Assignment Problem menggunakan Hungarian Method**

Aplikasi web berbasis Flask yang interaktif untuk menyelesaikan masalah penugasan (assignment problem) menggunakan implementasi manual Hungarian Method dari nol, tanpa menggunakan library built-in.

## 🚀 Live Demo

- **GitHub Repository**: [https://github.com/novalbahri17/hungarian](https://github.com/novalbahri17/hungarian)
- **Vercel Deployment**: Ready for deployment to Vercel

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Instalasi dan Setup](#-instalasi-dan-setup)
- [Struktur Proyek](#-struktur-proyek)
- [Penggunaan Aplikasi](#-penggunaan-aplikasi)
- [Algoritma Hungarian Method](#-algoritma-hungarian-method)
- [Testing](#-testing)
- [Analisis Kompleksitas](#-analisis-kompleksitas)
- [API Documentation](#-api-documentation)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## ✨ Fitur Utama

### 🎯 Antarmuka Web Modern
- **Responsive Design**: Antarmuka yang dapat diakses dari desktop, tablet, dan mobile
- **Interactive UI**: Elemen interaktif dengan feedback real-time
- **Modern Bootstrap**: Menggunakan Bootstrap 5 untuk tampilan yang profesional
- **User-Friendly**: Interface yang mudah digunakan untuk semua kalangan

### 🧮 Implementasi Manual Hungarian Method
- **From Scratch**: Implementasi algoritma Hungarian Method dari nol tanpa library built-in
- **Step-by-Step Visualization**: Visualisasi setiap langkah algoritma
- **Matrix Operations**: Operasi matriks manual untuk pembelajaran
- **Cost Minimization**: Fokus pada minimisasi biaya assignment
- **Real-time Calculation**: Perhitungan langsung dengan hasil instan

### 📊 Input Data Fleksibel
- **Manual Input**: Input matriks secara manual melalui interface
- **CSV Upload**: Upload file CSV untuk data yang lebih besar
- **Random Data**: Generate data random untuk testing
- **Matrix Validation**: Validasi otomatis untuk memastikan data valid

### 📈 Visualisasi Hasil
- **Interactive Tables**: Tabel interaktif untuk menampilkan hasil
- **Step-by-step Process**: Tampilan proses algoritma langkah demi langkah
- **Assignment Visualization**: Visualisasi hasil penugasan optimal
- **Cost Analysis**: Analisis biaya total dan individual

### 🚀 Deployment Ready
- **Vercel Compatible**: Siap deploy ke Vercel dengan konfigurasi otomatis
- **Serverless Architecture**: Arsitektur serverless untuk skalabilitas
- **GitHub Integration**: Integrasi dengan GitHub untuk CI/CD
- **Production Ready**: Konfigurasi production yang optimal

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**: Bahasa pemrograman utama
- **Flask**: Framework web untuk API dan routing
- **NumPy**: Komputasi numerik dan operasi matriks
- **Pandas**: Manipulasi dan analisis data
- **Matplotlib & Seaborn**: Visualisasi data dan grafik
- **Plotly**: Grafik interaktif
- **Werkzeug**: WSGI utilities untuk Flask
- **Jinja2**: Template engine

### Frontend
- **HTML5**: Struktur halaman web
- **CSS3**: Styling dan layout responsif
- **JavaScript (ES6+)**: Interaktivitas dan AJAX
- **Bootstrap 5**: Framework CSS untuk UI responsif

### Data Processing
- **CSV/Excel**: Import/export data menggunakan pandas dan openpyxl
- **JSON**: Format pertukaran data API

### Deployment
- **Vercel**: Platform deployment serverless
- **GitHub**: Version control dan CI/CD

### Testing & Quality
- **Pytest**: Unit testing dan integration testing (untuk development lokal)

## 📁 Struktur Proyek

```
hungarian/
├── api/
│   └── index.py              # Entry point untuk Vercel
├── app/
│   ├── main.py               # Aplikasi Flask utama
│   ├── config.py             # Konfigurasi aplikasi
│   ├── hungarian.py          # Implementasi Hungarian Method
│   ├── utils.py              # Utility functions
│   └── templates/
│       ├── index.html        # Halaman utama
│       ├── calculator.html   # Interface kalkulator
│       ├── 404.html          # Error 404
│       └── 500.html          # Error 500
├── static/
│   └── images/               # Asset gambar
├── data/
│   └── *.csv                 # Sample data
├── tests/
│   └── *.py                  # Test files
├── uploads/                  # Upload directory
├── reports/                  # Generated reports
├── requirements.txt          # Dependencies
├── vercel.json              # Konfigurasi Vercel
└── README.md
```

## 📦 Instalasi dan Setup

### Deployment ke Vercel

1. **Fork atau Clone Repository**
   ```bash
   git clone https://github.com/novalbahri17/hungarian.git
   cd hungarian
   ```

2. **Deploy ke Vercel**
   - Login ke [Vercel](https://vercel.com)
   - Import repository dari GitHub
   - Vercel akan otomatis mendeteksi konfigurasi dari `vercel.json`
   - Deploy akan berjalan otomatis

3. **Konfigurasi Vercel**
   - File `vercel.json` sudah dikonfigurasi untuk Flask
   - Entry point: `api/index.py`
   - Environment: Production

### Menjalankan Secara Lokal

1. **Prasyarat**
   - Python 3.8 atau lebih tinggi
   - pip (Python package installer)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**
   ```bash
   python app/main.py
   ```

4. **Akses Aplikasi**
   - Buka browser dan kunjungi: `http://localhost:5001`
   - Interface kalkulator tersedia di halaman utama

## 📖 Cara Penggunaan

### 1. Input Data Matriks
- **Manual Input**: Klik "Generate Matrix" dan masukkan ukuran matriks, lalu isi nilai secara manual
- **Upload CSV**: Gunakan tombol "Upload CSV" untuk mengupload file data
- **Random Data**: Klik "Fill Random Data" untuk mengisi matriks dengan data acak

### 2. Menjalankan Algoritma
- Klik tombol "Hitung Solusi" untuk menjalankan Hungarian Method
- Hasil akan ditampilkan dalam bentuk tabel assignment optimal
- Total biaya minimum akan ditampilkan

### 3. Melihat Proses
- Klik "Lihat Langkah" untuk melihat step-by-step proses algoritma
- Setiap langkah akan dijelaskan secara detail

### 4. Reset
- Gunakan tombol "Reset" untuk membersihkan semua data dan memulai dari awal

## 🔧 Konfigurasi

### File Konfigurasi
- `app/config.py`: Konfigurasi aplikasi Flask
- `vercel.json`: Konfigurasi deployment Vercel
- `requirements.txt`: Dependencies Python

### Environment Variables
- `FLASK_ENV`: Environment aplikasi (development/production)
- Tidak memerlukan database atau API key eksternal

## 📁 Struktur Proyek

```
hungarian3/
├── app/
│   ├── main.py                 # Entry point aplikasi Flask
│   ├── hungarian.py            # Implementasi algoritma Hungarian
│   ├── utils.py                # Fungsi bantu (I/O, visualisasi, laporan)
│   ├── models.py               # Model database SQLAlchemy
│   ├── config.py               # Konfigurasi aplikasi
│   ├── templates/              # Template HTML
│   │   ├── base.html          # Template dasar
│   │   ├── index.html         # Landing page
│   │   ├── login.html         # Halaman login
│   │   ├── register.html      # Halaman registrasi
│   │   ├── dashboard.html     # Dashboard pengguna
│   │   ├── calculator.html    # Kalkulator Hungarian
│   │   ├── history.html       # Riwayat perhitungan
│   │   └── admin.html         # Dashboard admin
│   └── static/                # File statis (CSS, JS, images)
├── tests/
│   ├── test_hungarian.py      # Unit tests (White Box)
│   ├── blackbox_test.py       # Functional tests (Black Box)
│   └── coverage_report/       # Laporan coverage
├── reports/                   # Laporan PDF yang dihasilkan
├── data/                      # Data sample dan uploads
│   └── sample_input.csv
├── requirements.txt           # Dependencies Python
└── README.md                  # Dokumentasi ini
```

## 🎮 Penggunaan Aplikasi

### 1. Registrasi dan Login
- Akses halaman utama aplikasi
- Klik "Register" untuk membuat akun baru
- Atau login dengan akun yang sudah ada
- Admin dapat mengakses dashboard admin

### 2. Menggunakan Kalkulator Hungarian

#### Input Manual:
1. Pilih "Manual Input" di halaman calculator
2. Tentukan ukuran matriks (rows x columns)
3. Isi nilai-nilai matriks
4. Pilih tipe problem (Minimization/Maximization)
5. Klik "Calculate Assignment"

#### Upload File:
1. Pilih "File Upload" di halaman calculator
2. Upload file CSV atau Excel
3. Preview data yang diupload
4. Pilih tipe problem
5. Klik "Calculate Assignment"

### 3. Melihat Hasil
- **Summary**: Ringkasan solusi optimal
- **Assignment**: Tabel penugasan worker-task
- **Total Cost/Profit**: Nilai optimal
- **Execution Time**: Waktu komputasi
- **Heatmap**: Visualisasi matriks
- **Steps**: Langkah-langkah detail algoritma

### 4. Generate Laporan
- Klik "Generate PDF Report" setelah perhitungan
- Laporan berisi:
  - Input data dan parameter
  - Hasil optimal
  - Visualisasi step-by-step
  - Analisis kompleksitas
  - Kesimpulan

### 5. Analisis Kompleksitas
- Akses melalui dashboard atau menu
- Pilih range ukuran matriks untuk dianalisis
- Lihat grafik waktu eksekusi vs ukuran input
- Download laporan analisis

## 🧮 Algoritma Hungarian Method

### Deskripsi
Hungarian Method adalah algoritma optimisasi untuk menyelesaikan assignment problem dalam waktu polinomial O(n³). Algoritma ini menemukan penugasan optimal yang meminimalkan (atau memaksimalkan) total biaya.

### Langkah-langkah Algoritma

1. **Preprocessing**
   - Validasi dan konversi input
   - Penyeimbangan matriks (jika tidak persegi)
   - Konversi maksimisasi ke minimisasi

2. **Reduksi Baris**
   - Kurangi setiap baris dengan nilai minimum baris tersebut
   - Tujuan: Membuat minimal satu nol di setiap baris

3. **Reduksi Kolom**
   - Kurangi setiap kolom dengan nilai minimum kolom tersebut
   - Tujuan: Membuat minimal satu nol di setiap kolom

4. **Pencarian Assignment**
   - Cari assignment menggunakan nol-nol yang ada
   - Gunakan algoritma matching untuk menemukan assignment maksimal

5. **Covering Lines**
   - Jika assignment belum optimal, cari minimum covering lines
   - Gunakan algoritma König untuk menemukan vertex cover minimum

6. **Update Matriks**
   - Kurangi elemen yang tidak tercakup dengan nilai minimum
   - Tambahkan nilai minimum ke elemen yang tercakup dua kali

7. **Iterasi**
   - Ulangi langkah 4-6 hingga assignment optimal ditemukan

### Flowchart Algoritma

```
[Start] → [Input Matrix] → [Validate Input]
    ↓
[Balance Matrix] → [Convert Max to Min] → [Row Reduction]
    ↓
[Column Reduction] → [Find Assignment] → [Assignment Complete?]
    ↓                                           ↓ Yes
[Find Covering Lines] ← No                [Calculate Cost] → [End]
    ↓
[Update Matrix] → [Back to Find Assignment]
```

### Kompleksitas
- **Time Complexity**: O(n³)
- **Space Complexity**: O(n²)
- **Worst Case**: Matriks dengan distribusi nilai yang memerlukan banyak iterasi
- **Best Case**: Matriks yang sudah optimal setelah reduksi awal

## 🧪 Testing

### Menjalankan Tests

#### Unit Tests (White Box)
```bash
# Jalankan semua unit tests
python -m pytest tests/test_hungarian.py -v

# Atau menggunakan unittest
python tests/test_hungarian.py
```

#### Black Box Tests
```bash
# Jalankan functional tests
python tests/blackbox_test.py -v

# Jalankan hanya fast tests
python tests/blackbox_test.py --fast
```

#### Code Coverage
```bash
# Generate coverage report
coverage run -m pytest tests/
coverage report
coverage html  # Generate HTML report
```

### Test Categories

#### White Box Testing
- **Unit Tests**: Testing setiap fungsi individual
- **Integration Tests**: Testing interaksi antar modul
- **Code Coverage**: Memastikan semua kode tertest

#### Black Box Testing
- **Functional Tests**: Testing input-output behavior
- **Boundary Tests**: Testing edge cases dan boundary conditions
- **Property-based Tests**: Testing menggunakan Hypothesis
- **Performance Tests**: Testing waktu eksekusi dan memory usage

#### Test Cases
1. **Input Validation**
   - Matriks valid dan invalid
   - Berbagai tipe data
   - Boundary conditions

2. **Algorithm Correctness**
   - Matriks persegi dan tidak persegi
   - Minimisasi dan maksimisasi
   - Nilai positif, negatif, dan nol

3. **Performance**
   - Berbagai ukuran matriks
   - Stress testing
   - Memory usage

4. **Integration**
   - End-to-end workflow
   - Database operations
   - File processing

## 📊 Analisis Kompleksitas

### Kompleksitas Teoritis
- **Hungarian Algorithm**: O(n³)
- **Matrix Operations**: O(n²)
- **Assignment Finding**: O(n³) worst case
- **Covering Lines**: O(n³)

### Pengukuran Praktis

#### Menjalankan Analisis
```bash
# Melalui web interface
# Akses Dashboard → Complexity Analysis

# Atau melalui API
curl -X POST http://localhost:5000/api/analyze_complexity \
  -H "Content-Type: application/json" \
  -d '{"min_size": 3, "max_size": 15, "step": 2}'
```

#### Metrics yang Diukur
1. **Execution Time**: Waktu total eksekusi
2. **Memory Usage**: Penggunaan memori peak
3. **Iteration Count**: Jumlah iterasi algoritma
4. **Step Count**: Jumlah langkah detail

#### Visualisasi
- **Time vs Size**: Grafik waktu eksekusi vs ukuran matriks
- **Memory vs Size**: Grafik penggunaan memori vs ukuran
- **Complexity Curve**: Fitting kurva O(n³)
- **Performance Comparison**: Perbandingan dengan implementasi lain

### Tools Analisis
- **timeit**: Pengukuran waktu eksekusi presisi tinggi
- **cProfile**: Profiling detail fungsi
- **memory_profiler**: Monitoring penggunaan memori
- **radon**: Analisis cyclomatic complexity

## 🔌 API Documentation

### Authentication Endpoints

#### POST /api/login
Login pengguna

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "is_admin": true
  }
}
```

### Hungarian Algorithm Endpoints

#### POST /api/solve
Menyelesaikan assignment problem

**Request:**
```json
{
  "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
  "is_maximization": false,
  "save_to_history": true
}
```

**Response:**
```json
{
  "success": true,
  "assignment": [0, 1, 2],
  "total_cost": 15,
  "execution_time": 0.001234,
  "steps": [
    {
      "step": 1,
      "description": "Original matrix",
      "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    }
  ],
  "calculation_id": 123
}
```

#### POST /api/upload
Upload dan proses file matriks

**Request:** Multipart form dengan file

**Response:**
```json
{
  "success": true,
  "matrix": [[1, 2, 3], [4, 5, 6]],
  "rows": 2,
  "cols": 3,
  "preview": "2x3 matrix uploaded successfully"
}
```

### Analysis Endpoints

#### POST /api/analyze_complexity
Analisis kompleksitas algoritma

**Request:**
```json
{
  "min_size": 3,
  "max_size": 15,
  "step": 2,
  "iterations": 5
}
```

**Response:**
```json
{
  "success": true,
  "analysis_data": [
    {
      "size": 3,
      "avg_time": 0.001,
      "memory_usage": 1024,
      "iterations": 2
    }
  ],
  "complexity_curve": "O(n^3)",
  "chart_data": {...}
}
```

#### GET /api/steps/{calculation_id}
Mendapatkan langkah-langkah detail perhitungan

**Response:**
```json
{
  "success": true,
  "steps": [
    {
      "step": 1,
      "description": "Row reduction",
      "matrix": [[0, 1, 2], [0, 1, 2], [0, 1, 2]],
      "explanation": "Subtract minimum value from each row"
    }
  ]
}
```

### Report Endpoints

#### POST /api/generate_report
Generate PDF report

**Request:**
```json
{
  "calculation_id": 123,
  "include_steps": true,
  "include_analysis": true
}
```

**Response:**
```json
{
  "success": true,
  "report_url": "/reports/calculation_123_report.pdf",
  "filename": "hungarian_report_2024.pdf"
}
```

### History Endpoints

#### GET /api/history
Mendapatkan riwayat perhitungan pengguna

**Query Parameters:**
- `page`: Nomor halaman (default: 1)
- `per_page`: Item per halaman (default: 10)
- `type`: Filter tipe (minimization/maximization)
- `search`: Pencarian

**Response:**
```json
{
  "success": true,
  "calculations": [
    {
      "id": 123,
      "created_at": "2024-01-01T10:00:00Z",
      "matrix_size": "3x3",
      "problem_type": "minimization",
      "total_cost": 15,
      "execution_time": 0.001234
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 5,
    "per_page": 10,
    "total": 50
  }
}
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines Kontribusi
- Pastikan kode mengikuti style guide Python (PEP 8)
- Tambahkan tests untuk fitur baru
- Update dokumentasi jika diperlukan
- Pastikan semua tests pass sebelum submit PR

## 🐛 Bug Reports & Feature Requests

Jika menemukan bug atau ingin request fitur baru:
- Buka issue di GitHub repository
- Berikan deskripsi yang jelas dan detail
- Sertakan langkah reproduksi untuk bug
- Sertakan screenshot jika memungkinkan

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👨‍💻 Author

**Noval Bahri**
- GitHub: [@novalbahri17](https://github.com/novalbahri17)
- Repository: [hungarian](https://github.com/novalbahri17/hungarian)

## 🙏 Acknowledgments

- Terima kasih kepada komunitas open source
- Bootstrap untuk framework CSS yang excellent
- Flask untuk framework web yang powerful
- Vercel untuk platform deployment yang mudah

---

⭐ **Jika proyek ini membantu, jangan lupa berikan star di GitHub!** ⭐