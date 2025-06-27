# Hungarian Method Calculator

🎯 **Aplikasi Web untuk Menyelesaikan Assignment Problem menggunakan Hungarian Method**

Aplikasi web berbasis Flask yang interaktif untuk menyelesaikan masalah penugasan (assignment problem) menggunakan implementasi manual Hungarian Method dari nol, tanpa menggunakan library built-in.

## 🚀 Live Demo

 inde- **GitHub Repository**: [https://github.com/novalbahri17/hungarian](https://github.com/novalbahri17/hungarian)
- **Local Development**: Aplikasi berjalan di `http://localhost:5001`

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
- [Instalasi dan Setup](#-instalasi-dan-setup)
- [Struktur Proyek](#-struktur-proyek)
- [Penggunaan Aplikasi](#-penggunaan-aplikasi)
- [Format File CSV](#-format-file-csv)
- [Algoritma Hungarian Method](#-algoritma-hungarian-method)
- [Testing](#-testing)
- [Analisis Kompleksitas](#-analisis-kompleksitas)
- [Endpoints Aplikasi](#-endpoints-aplikasi)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
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
- **Manual Input**: Input matriks secara manual melalui interface web
- **Random Data Generator**: Generate data random untuk testing dan demonstrasi
- **Matrix Validation**: Validasi otomatis untuk memastikan data valid
- **Sample Data**: Tersedia file contoh di folder `data/` untuk referensi format

### 📈 Visualisasi dan Laporan
- **Interactive Tables**: Tabel interaktif untuk menampilkan hasil
- **Heatmap Visualization**: Visualisasi matriks dalam bentuk heatmap
- **Step-by-step Process**: Tampilan proses algoritma langkah demi langkah
- **Assignment Visualization**: Visualisasi hasil penugasan optimal
- **Cost Analysis**: Analisis biaya total dan individual

### 🚀 Development Ready
- **Local Development**: Mudah dijalankan secara lokal untuk development
- **Modular Architecture**: Arsitektur modular untuk maintainability
- **GitHub Integration**: Integrasi dengan GitHub untuk version control
- **Production Ready**: Konfigurasi yang dapat disesuaikan untuk production

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

### Data Processing & Reports
- **JSON**: Format pertukaran data API
- **Manual Input**: Input data langsung melalui interface
- **ReportLab**: Generate laporan PDF
- **Base64 Encoding**: Untuk visualisasi gambar dalam response

### Development & Deployment
- **Local Development**: Flask development server
- **GitHub**: Version control

### Testing & Quality
- **Pytest**: Unit testing dan integration testing (untuk development lokal)

## 📁 Struktur Proyek

```
hungarian3/
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
├── data/
│   ├── sample_input.csv      # Sample data kecil
│   ├── sample_input_large.csv # Sample data besar
│   └── sample_unbalanced.csv # Sample data tidak seimbang
├── tests/
│   ├── test_hungarian.py     # Unit tests
│   └── blackbox_test.py      # Black box tests
├── uploads/                  # Upload directory
├── reports/                  # Generated reports
├── requirements.txt          # Dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── CHANGELOG.md             # Change log
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # License file
└── README.md                # Dokumentasi ini
```

## 📦 Instalasi dan Setup

### Menjalankan Secara Lokal

1. **Prasyarat**
   - Python 3.8 atau lebih tinggi
   - pip (Python package installer)

2. **Clone Repository**
   ```bash
   git clone https://github.com/novalbahri17/hungarian.git
   cd hungarian3
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment (Opsional)**
   ```bash
   # Copy file environment template
   cp .env.example .env
   # Edit .env sesuai kebutuhan
   ```

5. **Jalankan Aplikasi**
   ```bash
   # Menggunakan Flask CLI
   set FLASK_APP=app.main:app
   flask run --host=0.0.0.0 --port=5001
   
   # Atau langsung dengan Python
   python app/main.py
   ```

6. **Akses Aplikasi**
   - Buka browser dan kunjungi: `http://localhost:5001`
   - Interface kalkulator tersedia di halaman utama

## 📖 Cara Penggunaan

### 1. Input Data Matriks
- **Manual Input**: Klik "Generate Matrix" dan masukkan ukuran matriks, lalu isi nilai secara manual
- **Random Data**: Klik "Fill Random Data" untuk mengisi matriks dengan data acak untuk testing

### 2. Menjalankan Algoritma
- Klik tombol "Hitung Solusi" untuk menjalankan Hungarian Method
- Hasil akan ditampilkan dalam bentuk tabel assignment optimal
- Total biaya minimum akan ditampilkan

### 3. Melihat Proses
- Klik "Lihat Langkah" untuk melihat step-by-step proses algoritma
- Setiap langkah akan dijelaskan secara detail

### 4. Reset
- Gunakan tombol "Reset" untuk membersihkan semua data dan memulai dari awal

## 📄 Format Data Sample

Untuk referensi format data, tersedia file sample di folder `data/`:

### Format Data:
- **Format**: CSV dengan separator koma (,)
- **Structure**: Matriks numerik tanpa header
- **Usage**: Sebagai referensi untuk input manual

### Contoh Format Data:
```csv
4,2,8
2,4,1
8,2,4
```

### File Sample Tersedia:
Tersedia file contoh di folder `data/` untuk referensi:
- `sample_input.csv`: Matriks 3x3 sederhana
- `sample_input_large.csv`: Matriks yang lebih besar
- `sample_unbalanced.csv`: Matriks tidak seimbang (akan diseimbangkan otomatis)

**Catatan**: 
- File sample ini digunakan sebagai referensi format untuk input manual di interface kalkulator
- Endpoint upload file (`/api/upload`) tersedia di backend untuk pengembangan masa depan, tetapi saat ini interface web hanya mendukung input manual dan generate random data

## 🔧 Konfigurasi

### File Konfigurasi
- `app/config.py`: Konfigurasi aplikasi Flask
- `requirements.txt`: Dependencies Python
- `.env.example`: Template untuk environment variables
- `.gitignore`: File dan folder yang diabaikan Git

### Environment Variables
- `FLASK_ENV`: Environment aplikasi (development/production)
- `FLASK_APP`: Entry point aplikasi Flask
- Tidak memerlukan database atau API key eksternal



## 🎮 Penggunaan Aplikasi

### 1. Menggunakan Kalkulator Hungarian

#### Input Manual:
1. Akses halaman utama aplikasi
2. Klik "Generate Matrix" dan tentukan ukuran matriks
3. Isi nilai-nilai matriks secara manual
4. Pilih tipe problem (Minimization/Maximization)
5. Klik "Hitung Solusi"

#### Generate Random Data:
1. Klik "Fill Random Data" untuk mengisi matriks dengan data acak
2. Pilih tipe problem (Minimisasi/Maksimisasi)
3. Klik "Hitung Solusi"

#### Menggunakan Sample Data:
1. Gunakan file contoh dari folder `data/` sebagai referensi
2. Salin nilai dari file sample dan input secara manual ke interface
3. Pilih tipe problem
4. Klik "Hitung Solusi"

### 2. Melihat Hasil
- **Assignment Table**: Tabel penugasan optimal
- **Total Cost**: Biaya total minimum/maksimum
- **Execution Time**: Waktu komputasi
- **Step-by-step Process**: Langkah-langkah detail algoritma

### 3. Generate Laporan
- Klik "Generate PDF Report" setelah perhitungan
- Laporan berisi:
  - Input data dan parameter
  - Hasil optimal
  - Visualisasi step-by-step
  - Analisis kompleksitas

### 4. Reset
- Gunakan tombol "Reset" untuk membersihkan semua data dan memulai dari awal

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
- Analisis kompleksitas dapat dilakukan melalui testing
- Gunakan script test untuk mengukur performa pada berbagai ukuran matriks
- Hasil dapat dilihat melalui output console atau log file

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

## 🔌 Endpoints Aplikasi

Aplikasi ini menggunakan Flask dengan routing sederhana:

### Main Routes
- **GET /**: Halaman utama dengan interface kalkulator
- **GET /calculator**: Interface kalkulator Hungarian Method
- **GET /dashboard**: Dashboard aplikasi
- **POST /api/solve**: Endpoint untuk menyelesaikan assignment problem
- **POST /api/get_steps**: Endpoint untuk melihat langkah-langkah detail
- **POST /api/generate_report**: Endpoint untuk generate PDF report
- **GET /api/complexity_analysis**: Endpoint untuk analisis kompleksitas
- **POST /api/upload**: Endpoint untuk upload file (tersedia untuk pengembangan masa depan)

### Response Format
Semua endpoint menggunakan format JSON response:
```json
{
  "success": true/false,
  "message": "Status message",
  "data": {...}
}
```

## ❓ FAQ & Troubleshooting

### Masalah Umum

**Q: Aplikasi tidak bisa dijalankan?**
A: Pastikan semua dependencies sudah terinstall dengan `pip install -r requirements.txt`

**Q: Error saat upload CSV?**
A: Pastikan format CSV sesuai (tanpa header, separator koma, data numerik)

**Q: Hasil tidak sesuai ekspektasi?**
A: Periksa apakah tipe problem (minimization/maximization) sudah benar

**Q: Matriks tidak persegi?**
A: Aplikasi akan otomatis menyeimbangkan matriks dengan menambah dummy rows/columns

### Performance Tips
- Untuk matriks besar (>20x20), proses mungkin membutuhkan waktu lebih lama
- Gunakan data sample untuk testing awal
- Monitor penggunaan memori untuk matriks sangat besar

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
- NumPy dan Pandas untuk komputasi numerik yang efisien
- Matplotlib, Seaborn, dan Plotly untuk visualisasi data
- ReportLab untuk pembuatan laporan PDF

---

⭐ **Jika proyek ini membantu, jangan lupa berikan star di GitHub!** ⭐