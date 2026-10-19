"""Dasbor Interaktif Analitik Penjualan  -  Studi Kasus IMK & Visualisasi Data.

Jalankan:  streamlit run src/app.py
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analytics as an  # noqa: E402
import charts as ch  # noqa: E402

st.set_page_config(page_title="Dasbor Penjualan | Studi Kasus IMK", page_icon="📊", layout="wide")


@st.cache_data  # NFR: loading time < 2 detik -> data di-cache
def _data() -> pd.DataFrame:
    return an.muat_data()


df = _data()
MIN_T, MAX_T = df["tanggal"].min().date(), df["tanggal"].max().date()
SEMUA_WILAYAH = sorted(df["wilayah"].unique())
SEMUA_KATEGORI = sorted(df["kategori"].unique())

# ---------- Sidebar: Zoom & Filter (Shneiderman) ----------
st.sidebar.header("Filter data")


def _reset() -> None:
    st.session_state["periode"] = (MIN_T, MAX_T)
    st.session_state["wilayah"] = SEMUA_WILAYAH
    st.session_state["kategori"] = SEMUA_KATEGORI


st.session_state.setdefault("periode", (MIN_T, MAX_T))
st.session_state.setdefault("wilayah", SEMUA_WILAYAH)
st.session_state.setdefault("kategori", SEMUA_KATEGORI)

periode = st.sidebar.date_input("Periode", min_value=MIN_T, max_value=MAX_T, key="periode")
wilayah = st.sidebar.multiselect("Wilayah", SEMUA_WILAYAH, key="wilayah")
kategori = st.sidebar.multiselect("Kategori", SEMUA_KATEGORI, key="kategori")
st.sidebar.button("Reset semua filter", on_click=_reset, width="stretch")  # kontrol & kebebasan pengguna

# date_input mengembalikan 1 tanggal saat pengguna baru memilih tanggal awal
if isinstance(periode, tuple) and len(periode) == 2:
    mulai, akhir = periode
else:
    mulai = akhir = periode[0] if isinstance(periode, tuple) else periode
    st.sidebar.info("Pilih tanggal akhir untuk menyelesaikan rentang periode.")  # feedback

dff = an.filter_data(df, mulai, akhir, wilayah, kategori)

# ---------- Header ----------
st.title("Dasbor Analitik Penjualan")
st.caption(
    f"Periode {mulai:%d %b %Y} – {akhir:%d %b %Y} · {len(dff):,} transaksi. "
    "Data sintetis untuk studi kasus mata kuliah IMK."
)

if dff.empty:
    # Feedback + pencegahan kebingungan: jelaskan penyebab dan cara keluar
    st.warning("Tidak ada data untuk kombinasi filter ini. Perluas periode atau pilih lebih banyak wilayah/kategori.")
    st.stop()

# ---------- 1) OVERVIEW FIRST ----------
kpi = an.hitung_kpi(df, dff, mulai, akhir)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total omzet", an.format_rupiah(kpi.total_omzet))
c2.metric("Jumlah transaksi", f"{kpi.jumlah_transaksi:,}".replace(",", "."))
c3.metric("Rata-rata per transaksi", an.format_rupiah(kpi.rata_omzet))
c4.metric(
    "Vs periode sebelumnya",
    "—" if kpi.pertumbuhan is None else f"{kpi.pertumbuhan:+.1f}%".replace(".", ","),
    help="Dibandingkan periode dengan panjang hari yang sama tepat sebelum periode terpilih.",
)

with st.container(border=True):
    st.markdown("**Sekilas temuan**")
    for teks in an.buat_insight(dff):
        st.markdown(f"- {teks}")

st.plotly_chart(ch.grafik_tren(dff), width="stretch")

# ---------- 2) ZOOM & FILTER: perbandingan ----------
a, b = st.columns(2)
a.plotly_chart(ch.grafik_kategori(dff), width="stretch")
b.plotly_chart(ch.grafik_wilayah(dff), width="stretch")

d, e = st.columns(2)
d.plotly_chart(ch.grafik_proporsi(dff), width="stretch")
e.plotly_chart(ch.grafik_scatter(dff), width="stretch")

# ---------- 3) DETAILS-ON-DEMAND ----------
with st.expander("Lihat data rinci & unduh"):
    tampil = dff.drop(columns=["bulan"]).sort_values("tanggal", ascending=False)
    st.dataframe(tampil, width="stretch", hide_index=True)
    st.download_button(
        "Unduh CSV (data terfilter)",
        tampil.to_csv(index=False).encode("utf-8"),
        file_name="penjualan_terfilter.csv",
        mime="text/csv",
    )
