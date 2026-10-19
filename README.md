# Dasbor Interaktif Analitik Penjualan

**Studi Kasus Interaksi Manusia dan Komputer (IMK) & Visualisasi Data**
Berdasarkan materi Sesi 5 (Modul 1–6): pengantar IMK, aspek kognitif & persepsi, interaksi sosial & konteks,
proses desain & evaluasi, analisis kebutuhan & user persona, serta prinsip visualisasi data & dasbor interaktif.

## 1. Latar Belakang

Laporan penjualan berbasis spreadsheet sering padat, sulit dipindai, dan tidak menjawab pertanyaan
"mengapa naik atau turun?". Pengguna harus menggali manual sehingga beban kognitif tinggi dan keputusan
menjadi lambat. Studi kasus ini merancang dan membangun **dasbor analitik penjualan** yang berangkat dari
kebutuhan pengguna (User-Centered Design), bukan dari selera pengembang.

**Rumusan masalah:** bagaimana merancang dasbor yang membuat seorang analis data dapat memahami kinerja penjualan
dengan cepat, menyaring data sesuai kebutuhan, dan mempercayai grafik yang ditampilkan?

## 2. Tujuan

1. Menerapkan siklus desain interaksi: Analisis → Desain → Prototipe → Evaluasi.
2. Menerjemahkan persona dan kebutuhan pengguna menjadi fitur nyata.
3. Menerapkan prinsip kognitif, Gestalt, Tufte, aksesibilitas, dan etika visualisasi.
4. Mengevaluasi hasil dengan evaluasi heuristik dan usability testing (SUS, success rate, task time).

## 3. Ringkasan Desain

Dasbor mengikuti **mantra Shneiderman**:

| Tahap | Wujud pada dasbor |
|---|---|
| **Overview first** | 4 kartu KPI, kotak "Sekilas temuan" otomatis, dan tren omzet bulanan di bagian atas |
| **Zoom and filter** | Sidebar: periode, wilayah, kategori, tombol reset |
| **Details-on-demand** | Tooltip berisi angka akurat pada tiap grafik dan tabel rinci yang dapat diunduh sebagai CSV |

Pemilihan grafik mengikuti taksonomi: **line** untuk tren waktu, **bar** untuk komparasi kategori/wilayah,
**donut** untuk proporsi (hanya 5 irisan), dan **scatter** untuk korelasi diskon dengan jumlah item.

Keputusan desain utama:

- **Data-ink ratio (Tufte):** tanpa efek 3D, tanpa bayangan, gridline tipis.
- **Preattentive:** hanya nilai tertinggi yang diberi warna aksen; selebihnya abu-abu.
- **Skala jujur:** sumbu bar chart selalu dimulai dari nol (dijaga oleh tes otomatis).
- **Aksesibilitas:** palet Okabe-Ito yang aman bagi buta warna, kontras tinggi, dan label teks selain warna.
- **Konsistensi (Gestalt Similarity):** satu kategori selalu memakai warna yang sama di semua grafik (dijaga tes otomatis).
- **Etika:** hasil "tidak ada korelasi" antara diskon dan volume dilaporkan apa adanya, tidak dipoles.

Pemetaan lengkap materi ke implementasi ada di [`docs/pemetaan_materi.md`](docs/pemetaan_materi.md).

## 4. Analisis Kebutuhan & Persona

Persona **Budi Pratama** (Data Analyst), kebutuhan fungsional FR-01 s.d. FR-09, kebutuhan non-fungsional
NFR-01 s.d. NFR-05, serta skenario penggunaan (Context → Trigger → Action → Outcome) ada di
[`docs/persona_dan_kebutuhan.md`](docs/persona_dan_kebutuhan.md).

## 5. Struktur Proyek

```
imk-dashboard-penjualan/
├── data/
│   ├── penjualan.csv            # dataset sintetis (6.000 transaksi, 2024–2025)
│   ├── usability_testing.csv    # data simulasi uji usability (success rate, waktu)
│   └── sus_responden.csv        # data simulasi kuesioner SUS
├── docs/
│   ├── persona_dan_kebutuhan.md
│   ├── pemetaan_materi.md
│   └── evaluasi_heuristik.md
├── src/
│   ├── generate_data.py         # pembuat dataset sintetis
│   ├── analytics.py             # filter, KPI, insight (logika murni, tanpa UI)
│   ├── charts.py                # grafik Plotly + keputusan desain
│   ├── app.py                   # antarmuka Streamlit
│   └── usability.py             # perhitungan SUS, success rate, task time
├── tests/test_app.py
├── requirements.txt
└── README.md
```

## 6. Cara Menjalankan

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/generate_data.py        # opsional: membuat ulang dataset
streamlit run src/app.py           # membuka dasbor di browser
python src/usability.py            # ringkasan hasil usability testing (data simulasi)
pytest -q                          # menjalankan tes
```

## 7. Evaluasi

**Evaluasi heuristik (Nielsen).** Telaah awal oleh pengembang: tidak ditemukan masalah mayor; dua temuan minor
(belum ada preset periode cepat dan belum ada panduan membaca dasbor). Rincian di
[`docs/evaluasi_heuristik.md`](docs/evaluasi_heuristik.md).

**Usability testing.** Skrip analisis menghitung SUS, success rate, dan task time dari `data/*.csv`.

> **Catatan penting:** file CSV usability pada repositori ini adalah **data simulasi** untuk mendemonstrasikan
> alur analisis. Hasilnya (SUS ≈ 77,5; success rate 87,5–100%) **bukan** hasil uji dengan pengguna nyata.
> Untuk laporan akhir, lakukan uji dengan responden sungguhan (disarankan 5–8 orang, metode *think-aloud*)
> lalu ganti isi CSV dengan data tersebut.

**Kinerja.** Di mesin pengembangan, muat data sekitar 21 ms dan filter + KPI + 5 grafik sekitar 180 ms
(di bawah target NFR-01, 2 detik). Angka ini bergantung pada perangkat dan belum diuji di jaringan lain.

## 8. Keterbatasan & Pengembangan Lanjut

- Dataset sintetis; pola musiman dan tren ditanam oleh generator, bukan data bisnis nyata.
- Persona dan skenario fiktif; belum dari riset pengguna sungguhan.
- Aksesibilitas belum diuji dengan pembaca layar atau audit WCAG formal.
- Pengembangan: preset periode cepat, panel "Cara membaca dasbor", mode kontras tinggi, dan uji dengan responden nyata.

## 9. Referensi Materi

Materi kuliah Sesi 5 (Modul 1–6): Card, Moran & Newell (Model Human Processor), Tufte (data-ink ratio),
Shneiderman (Visual Information-Seeking Mantra), Nielsen (10 heuristik), WCAG (POUR).
