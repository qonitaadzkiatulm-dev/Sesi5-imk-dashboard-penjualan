# Analisis Kebutuhan & User Persona (Modul 5)

> Persona di bawah ini **fiktif** dan dibuat untuk keperluan studi kasus. Pada proyek nyata,
> persona harus disusun dari data riset empiris (wawancara, observasi, kuesioner), bukan asumsi perancang.

## Persona: Budi Pratama

| Elemen | Isi |
|---|---|
| **Profil demografi** | 29 tahun, Data Analyst di perusahaan ritel regional, S1 Statistika, bekerja dengan laptop 14" dan sesekali presentasi di ruang rapat |
| **Goals** | Menyajikan ringkasan kinerja penjualan ke manajer setiap awal bulan; menemukan wilayah/kategori yang perlu perhatian; mengambil keputusan promosi berbasis data |
| **Pain points** | Laporan Excel lama terlalu padat dan sulit dipindai; sulit membandingkan periode; manajer sering bertanya "kenapa naik/turun?" dan Budi harus menggali manual; grafik pie 3D dari laporan lama membingungkan |
| **Behaviors** | Terbiasa dengan filter dan shortcut; mengutamakan efisiensi; sering mengekspor data untuk analisis lanjutan; membuka dasbor di sela rapat sehingga waktu terbatas |

## Kebutuhan Fungsional (FR)

| ID | Kebutuhan | Diwujudkan oleh |
|---|---|---|
| FR-01 | Menampilkan ringkasan KPI (total omzet, jumlah transaksi, rata-rata per transaksi, perubahan vs periode sebelumnya) di layar utama | `hitung_kpi`, baris metrik pada `app.py` |
| FR-02 | Memfilter data berdasarkan periode, wilayah, dan kategori | Sidebar + `filter_data` |
| FR-03 | Menampilkan tren omzet bulanan | `grafik_tren` |
| FR-04 | Membandingkan omzet antar kategori dan antar wilayah | `grafik_kategori`, `grafik_wilayah` |
| FR-05 | Menampilkan proporsi omzet per kategori | `grafik_proporsi` |
| FR-06 | Menguji hubungan diskon dengan jumlah item | `grafik_scatter`, `korelasi_diskon_volume` |
| FR-07 | Menampilkan angka akurat saat kursor diarahkan ke grafik | `hovertemplate` pada semua grafik |
| FR-08 | Melihat data rinci dan mengunduhnya sebagai CSV | Expander + `st.download_button` |
| FR-09 | Mengatur ulang semua filter dengan satu klik | Tombol "Reset semua filter" |

## Kebutuhan Non-Fungsional (NFR)

| ID | Kebutuhan | Cara pemenuhan / hasil ukur |
|---|---|---|
| NFR-01 | Waktu muat < 2 detik | Data di-cache (`st.cache_data`). Terukur di mesin pengembangan: muat data sekitar 21 ms, filter + KPI + 5 grafik sekitar 180 ms |
| NFR-02 | Kontras dan keterbacaan sesuai WCAG | Teks gelap pada latar putih; palet Okabe-Ito yang aman bagi buta warna |
| NFR-03 | Informasi tidak bergantung pada warna saja | Nilai tertinggi diberi label teks ("Puncak") dan angka pada batang |
| NFR-04 | Skala grafik jujur | Sumbu bar chart selalu mulai dari nol (diuji otomatis di `tests/test_app.py`) |
| NFR-05 | Pesan yang jelas saat data kosong | Peringatan dengan petunjuk tindakan, bukan layar kosong |

## Skenario Penggunaan (Context → Trigger → Action → Outcome)

| Tahap | Uraian |
|---|---|
| **Context** | Senin pagi, 15 menit sebelum rapat bulanan. Budi di meja kerjanya, dengan koneksi kantor yang stabil. |
| **Trigger** | Manajer meminta ringkasan kinerja 2025 dan bertanya mengapa omzet Maret melonjak. |
| **Action** | Budi membuka dasbor dan langsung melihat KPI serta "Sekilas temuan" (Overview First). Ia membaca bahwa Maret adalah puncak, memilih periode Januari–April 2025, lalu menyaring kategori Elektronik dan wilayah Jawa (Zoom & Filter). Ia mengarahkan kursor ke titik puncak untuk angka tepatnya (Details-on-Demand), lalu mengunduh CSV terfilter untuk lampiran presentasi. |
| **Outcome** | Budi menjawab pertanyaan manajer dengan data dalam hitungan menit, tanpa menyusun ulang laporan Excel. |
