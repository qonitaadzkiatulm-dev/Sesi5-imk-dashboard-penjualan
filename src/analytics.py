"""Logika analitik murni (tanpa UI) agar mudah diuji."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "penjualan.csv"


def muat_data(path: Path | str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["tanggal"])
    df["bulan"] = df["tanggal"].dt.to_period("M").dt.to_timestamp()
    return df


def filter_data(
    df: pd.DataFrame,
    mulai: pd.Timestamp,
    akhir: pd.Timestamp,
    wilayah: list[str] | None = None,
    kategori: list[str] | None = None,
) -> pd.DataFrame:
    """Zoom & Filter (Shneiderman): saring data berdasarkan periode, wilayah, kategori."""
    mask = (df["tanggal"] >= pd.Timestamp(mulai)) & (df["tanggal"] <= pd.Timestamp(akhir))
    if wilayah:
        mask &= df["wilayah"].isin(wilayah)
    if kategori:
        mask &= df["kategori"].isin(kategori)
    return df.loc[mask]


@dataclass
class KPI:
    total_omzet: float
    jumlah_transaksi: int
    rata_omzet: float
    pertumbuhan: float | None  # vs periode sebelumnya dengan panjang sama; None jika tak ada pembanding


def hitung_kpi(df_semua: pd.DataFrame, df_terfilter: pd.DataFrame, mulai, akhir) -> KPI:
    """Overview First: ringkasan makro untuk layar utama."""
    total = float(df_terfilter["omzet"].sum())
    n = int(len(df_terfilter))
    rata = total / n if n else 0.0

    mulai, akhir = pd.Timestamp(mulai), pd.Timestamp(akhir)
    panjang = akhir - mulai + pd.Timedelta(days=1)
    prev_akhir = mulai - pd.Timedelta(days=1)
    prev_mulai = prev_akhir - panjang + pd.Timedelta(days=1)

    prev = df_semua[(df_semua["tanggal"] >= prev_mulai) & (df_semua["tanggal"] <= prev_akhir)]
    # pembanding harus memakai filter wilayah/kategori yang sama
    if not df_terfilter.empty:
        prev = prev[
            prev["wilayah"].isin(df_terfilter["wilayah"].unique())
            & prev["kategori"].isin(df_terfilter["kategori"].unique())
        ]
    prev_total = float(prev["omzet"].sum())
    growth = (total - prev_total) / prev_total * 100 if prev_total > 0 else None
    return KPI(total, n, rata, growth)


def omzet_bulanan(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("bulan", as_index=False)["omzet"].sum().sort_values("bulan")


def omzet_per(df: pd.DataFrame, kolom: str) -> pd.DataFrame:
    return (
        df.groupby(kolom, as_index=False)["omzet"].sum().sort_values("omzet", ascending=False)
    )


def diskon_vs_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Data untuk scatter: apakah diskon lebih tinggi diikuti jumlah item lebih besar?"""
    g = df.groupby(["kategori", "diskon"], as_index=False).agg(
        rata_jumlah=("jumlah", "mean"), transaksi=("jumlah", "size")
    )
    g["diskon_persen"] = g["diskon"] * 100
    return g


def korelasi_diskon_volume(df: pd.DataFrame) -> float | None:
    if len(df) < 3 or df["diskon"].nunique() < 2:
        return None
    return float(df["diskon"].corr(df["jumlah"]))


def format_rupiah(nilai: float) -> str:
    """Format ringkas untuk mengurangi extraneous load: Rp 1,23 M / 4,5 jt / 120 rb."""
    a = abs(nilai)
    if a >= 1e9:
        s = f"{nilai / 1e9:,.2f} M"
    elif a >= 1e6:
        s = f"{nilai / 1e6:,.1f} jt"
    elif a >= 1e3:
        s = f"{nilai / 1e3:,.0f} rb"
    else:
        s = f"{nilai:,.0f}"
    # gaya Indonesia: koma desimal, titik ribuan
    s = s.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"Rp {s}"


def buat_insight(df: pd.DataFrame) -> list[str]:
    """Teks insight otomatis: membantu Germane Load (membangun pemahaman), bukan sekadar angka."""
    if df.empty:
        return []
    out: list[str] = []
    kat = omzet_per(df, "kategori")
    top_k = kat.iloc[0]
    out.append(
        f"Kategori **{top_k['kategori']}** menyumbang omzet terbesar "
        f"({top_k['omzet'] / kat['omzet'].sum():.0%} dari total)."
    )
    wil = omzet_per(df, "wilayah")
    out.append(f"Wilayah teratas: **{wil.iloc[0]['wilayah']}** ({format_rupiah(wil.iloc[0]['omzet'])}).")
    bln = omzet_bulanan(df)
    if len(bln) >= 2:
        puncak = bln.loc[bln["omzet"].idxmax()]
        out.append(f"Omzet bulanan tertinggi terjadi pada **{puncak['bulan']:%B %Y}**.")
    r = korelasi_diskon_volume(df)
    if r is not None:
        if abs(r) < 0.1:
            out.append("Diskon **tidak menunjukkan hubungan berarti** dengan jumlah item per transaksi.")
        else:
            arah = "positif" if r > 0 else "negatif"
            out.append(f"Diskon berkorelasi {arah} dengan jumlah item (r = {r:.2f}).")
    return out
