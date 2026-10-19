# Pemetaan Materi Sesi 5 ke Implementasi

| Modul | Konsep | Penerapan pada dasbor |
|---|---|---|
| 1. Pengantar IMK | Siklus interaksi: input, pemrosesan, output, feedback | Ubah filter → data diproses → grafik dan KPI diperbarui → pengguna menilai hasil |
| 1. Pengantar IMK | UCD: "pengguna bukanlah Anda" | Desain berangkat dari persona Budi Pratama, bukan selera pengembang |
| 2. Kognitif & Persepsi | Working memory 7±2 chunks | KPI dibatasi 4 angka; tiap grafik hanya memuat satu pesan |
| 2. Kognitif & Persepsi | Extraneous load harus diperkecil | Format rupiah ringkas ("Rp 1,41 M"), tanpa dekorasi, tata letak konsisten |
| 2. Kognitif & Persepsi | Germane load dioptimalkan | Kotak "Sekilas temuan" menerjemahkan data menjadi kalimat |
| 2. Kognitif & Persepsi | Atribut preattentive | Hanya nilai tertinggi diberi warna aksen; sisanya abu-abu |
| 2. Kognitif & Persepsi | Prinsip Gestalt | Proximity: KPI berkelompok; Similarity: warna kategori konsisten antar grafik; Enclosure: kotak temuan; Figure/Ground: latar putih polos |
| 3. Interaksi Sosial & Konteks | Aksesibilitas (POUR) | Palet aman buta warna, kontras tinggi, label teks selain warna; komponen input bawaan Streamlit (belum diuji formal untuk navigasi keyboard dan pembaca layar) |
| 3. Interaksi Sosial & Konteks | Etika desain | Sumbu mulai dari nol, tanpa dark pattern, hasil "tidak ada korelasi" dilaporkan apa adanya |
| 4. Proses Desain & Evaluasi | Siklus Analisis → Desain → Prototipe → Evaluasi | Dokumen persona → kode dasbor → evaluasi heuristik dan usability testing |
| 4. Proses Desain & Evaluasi | 5 prinsip desain interaksi | Visibility (filter selalu tampak), Feedback (peringatan data kosong), Constraints (rentang tanggal dibatasi), Consistency, Affordance (tombol tampak dapat diklik) |
| 4. Proses Desain & Evaluasi | Heuristic evaluation & usability testing | `docs/evaluasi_heuristik.md`, `src/usability.py` |
| 5. Analisis Kebutuhan & Persona | FR/NFR, persona, skenario | `docs/persona_dan_kebutuhan.md` |
| 6. Visualisasi Data | Taksonomi grafik | Line = tren, bar = komparasi, scatter = korelasi, donut = proporsi |
| 6. Visualisasi Data | Tufte: data-ink ratio, tanpa chartjunk | Tanpa 3D/bayangan, gridline tipis, legend hanya jika perlu |
| 6. Visualisasi Data | Mantra Shneiderman | Overview first (KPI + tren), zoom and filter (sidebar), details-on-demand (hover dan tabel rinci) |
