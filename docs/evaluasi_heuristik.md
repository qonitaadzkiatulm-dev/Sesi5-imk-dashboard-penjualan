# Evaluasi Heuristik (10 Prinsip Nielsen)

Evaluasi ini dilakukan sendiri oleh pengembang terhadap versi 1.0 sebagai **telaah awal**.
Evaluasi heuristik yang sebenarnya idealnya dilakukan oleh 3–5 pakar UX independen.

Skala keparahan: 0 = bukan masalah, 1 = kosmetik, 2 = minor, 3 = mayor, 4 = katastrofik.

| No | Heuristik | Temuan | Keparahan | Tindak lanjut |
|---|---|---|---|---|
| 1 | Visibilitas status sistem | Streamlit menampilkan indikator "Running" saat grafik dihitung ulang; rentang periode tampil di subjudul | 0 | – |
| 2 | Kesesuaian dengan dunia nyata | Istilah "omzet", "wilayah", format "Rp 1,41 M" sesuai bahasa pengguna | 0 | – |
| 3 | Kontrol & kebebasan pengguna | Ada tombol "Reset semua filter" | 0 | – |
| 4 | Konsistensi & standar | Warna kategori sama di donut dan scatter; bar selalu horizontal terurut | 1 | Samakan warna kategori pada bar chart jika diperlukan |
| 5 | Pencegahan kesalahan | Rentang tanggal dibatasi pada data yang ada; pemilihan tanggal setengah jalan diberi pesan | 1 | – |
| 6 | Mengenali daripada mengingat | Semua filter terlihat di sidebar | 0 | – |
| 7 | Fleksibilitas & efisiensi | Belum ada preset cepat (misalnya "3 bulan terakhir") untuk pengguna ahli | 2 | Tambahkan preset periode |
| 8 | Desain estetis & minimalis | Tidak ada elemen dekoratif; satu warna aksen | 0 | – |
| 9 | Membantu pengguna mengenali & memulihkan dari kesalahan | Filter yang menghasilkan data kosong menampilkan peringatan dengan saran perbaikan | 0 | – |
| 10 | Bantuan & dokumentasi | Hanya tooltip pada KPI perubahan; belum ada panduan singkat | 2 | Tambahkan panel "Cara membaca dasbor" |

**Catatan perilaku yang perlu diketahui:** mengosongkan pilihan wilayah atau kategori diperlakukan sebagai "tanpa filter"
(menampilkan semua), mengikuti kebiasaan umum komponen multiselect.
