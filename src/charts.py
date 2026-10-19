"""Fungsi pembuat grafik Plotly. Setiap keputusan desain dikaitkan dengan materi IMK.

Prinsip yang diterapkan:
- Tufte / data-ink ratio : tanpa 3D, tanpa bayangan, gridline minimal, tanpa legend yang berlebihan
- Preattentive (warna)   : satu warna aksen menyorot nilai tertinggi, sisanya abu-abu netral
- Skala jujur (etika)    : sumbu bar chart selalu mulai dari nol
- Aksesibilitas (WCAG)   : palet Okabe-Ito (aman buta warna), kontras teks tinggi
- Details-on-Demand      : hovertemplate berisi angka akurat
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from analytics import diskon_vs_volume, omzet_bulanan, omzet_per

AKSEN = "#D55E00"      # oranye-merah (Okabe-Ito vermillion) -> sorotan
NETRAL = "#9AA0A6"     # abu-abu -> konteks
BIRU = "#0072B2"       # Okabe-Ito blue -> garis tren
TEKS = "#1F2933"
# Warna tetap per kategori -> Gestalt "Similarity": kategori yang sama selalu berwarna sama di semua grafik
WARNA_KATEGORI = {
    "Alat Tulis": "#56B4E9",
    "Elektronik": "#0072B2",
    "Fashion": "#CC79A7",
    "Makanan": "#E69F00",
    "Minuman": "#009E73",
}
_CADANGAN = "#6B7280"


def warna_kategori(nama: str) -> str:
    return WARNA_KATEGORI.get(nama, _CADANGAN)


def _tata_letak(fig: go.Figure, judul: str, tinggi: int = 340) -> go.Figure:
    fig.update_layout(
        title=dict(text=judul, x=0, font=dict(size=16, color=TEKS)),
        height=tinggi,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=TEKS, size=13),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, linecolor="#CBD2D9")
    fig.update_yaxes(gridcolor="#EEF1F4", zeroline=False)
    return fig


def grafik_tren(df: pd.DataFrame) -> go.Figure:
    """Line chart: tren berbasis waktu (time-series)."""
    d = omzet_bulanan(df)
    fig = go.Figure(
        go.Scatter(
            x=d["bulan"], y=d["omzet"] / 1e6, mode="lines+markers",
            line=dict(color=BIRU, width=3), marker=dict(size=6),
            hovertemplate="%{x|%B %Y}<br>Omzet: Rp %{y:,.1f} jt<extra></extra>",
        )
    )
    if len(d):
        i = d["omzet"].idxmax()
        fig.add_trace(
            go.Scatter(
                x=[d.loc[i, "bulan"]], y=[d.loc[i, "omzet"] / 1e6], mode="markers+text",
                marker=dict(size=13, color=AKSEN), text=["Puncak"], textposition="top center",
                hoverinfo="skip",
            )
        )
    fig.update_yaxes(title="Omzet (juta Rp)", rangemode="tozero")
    return _tata_letak(fig, "Tren omzet bulanan")


def _bar_horizontal(d: pd.DataFrame, kolom: str, judul: str) -> go.Figure:
    d = d.sort_values("omzet", ascending=True)  # terbesar di atas
    warna = [NETRAL] * len(d)
    if len(d):
        warna[-1] = AKSEN  # preattentive: hanya nilai tertinggi yang berwarna
    fig = go.Figure(
        go.Bar(
            x=d["omzet"] / 1e6, y=d[kolom], orientation="h", marker_color=warna,
            text=[f"{v / 1e6:,.1f}" for v in d["omzet"]], textposition="outside",
            hovertemplate="%{y}<br>Omzet: Rp %{x:,.1f} jt<extra></extra>",
        )
    )
    fig.update_xaxes(title="Omzet (juta Rp)", range=[0, max(d["omzet"].max() / 1e6 * 1.18, 1) if len(d) else 1])
    fig.update_yaxes(showgrid=False)
    return _tata_letak(fig, judul)


def grafik_kategori(df: pd.DataFrame) -> go.Figure:
    """Bar chart: komparasi antar kategori."""
    return _bar_horizontal(omzet_per(df, "kategori"), "kategori", "Omzet per kategori")


def grafik_wilayah(df: pd.DataFrame) -> go.Figure:
    """Bar chart: komparasi antar wilayah."""
    return _bar_horizontal(omzet_per(df, "wilayah"), "wilayah", "Omzet per wilayah")


def grafik_proporsi(df: pd.DataFrame) -> go.Figure:
    """Donut chart: proporsi bagian dari keseluruhan (hanya 5 irisan agar tetap terbaca)."""
    d = omzet_per(df, "kategori")
    fig = go.Figure(
        go.Pie(
            labels=d["kategori"], values=d["omzet"], hole=0.55, sort=False,
            marker=dict(colors=[warna_kategori(k) for k in d["kategori"]], line=dict(color="white", width=2)),
            textinfo="label+percent", textposition="outside",
            hovertemplate="%{label}<br>Rp %{value:,.0f}<br>%{percent}<extra></extra>",
        )
    )
    return _tata_letak(fig, "Proporsi omzet per kategori")


def grafik_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot: korelasi dua variabel numerik (diskon vs rata-rata item per transaksi)."""
    d = diskon_vs_volume(df)
    fig = go.Figure()
    for kat, g in d.groupby("kategori"):
        fig.add_trace(
            go.Scatter(
                x=g["diskon_persen"], y=g["rata_jumlah"], mode="markers", name=kat,
                marker=dict(size=11, color=warna_kategori(kat)),
                hovertemplate=f"{kat}<br>Diskon: %{{x:.0f}}%<br>Rata-rata item: %{{y:.2f}}<extra></extra>",
            )
        )
    fig.update_xaxes(title="Diskon (%)", dtick=5)
    fig.update_yaxes(title="Rata-rata item per transaksi", rangemode="tozero")
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.25))
    return _tata_letak(fig, "Apakah diskon mendorong jumlah item?", tinggi=380)
