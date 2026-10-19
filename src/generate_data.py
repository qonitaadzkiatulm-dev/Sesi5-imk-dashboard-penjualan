"""Membuat dataset penjualan sintetis (Jan 2024 - Des 2025) untuk studi kasus dasbor.

Jalankan:  python src/generate_data.py
Output  :  data/penjualan.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
RANGE_MULAI, RANGE_AKHIR = "2024-01-01", "2025-12-31"

KATEGORI = {
    # kategori: (harga_dasar, bobot_peluang)
    "Makanan": (35_000, 0.35),
    "Minuman": (22_000, 0.30),
    "Elektronik": (450_000, 0.10),
    "Fashion": (150_000, 0.15),
    "Alat Tulis": (18_000, 0.10),
}
WILAYAH = {
    "Sumatera": 0.25,
    "Jawa": 0.45,
    "Kalimantan": 0.12,
    "Sulawesi": 0.10,
    "Indonesia Timur": 0.08,
}


def buat_data(n_baris: int = 6000, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    awal = pd.Timestamp(RANGE_MULAI)
    akhir = pd.Timestamp(RANGE_AKHIR)
    n_hari = (akhir - awal).days + 1
    tanggal = awal + pd.to_timedelta(rng.integers(0, n_hari, n_baris), unit="D")

    kategori = rng.choice(list(KATEGORI), n_baris, p=[v[1] for v in KATEGORI.values()])
    wilayah = rng.choice(list(WILAYAH), n_baris, p=list(WILAYAH.values()))

    # Musiman: kenaikan menjelang Lebaran/akhir tahun + tren naik ringan
    bulan = tanggal.month.to_numpy()
    musim = np.where(np.isin(bulan, [3, 4, 11, 12]), 1.25, 1.0)
    tren = 1 + (tanggal - awal).days.to_numpy() / 3650

    harga_dasar = np.array([KATEGORI[k][0] for k in kategori])
    harga = harga_dasar * rng.normal(1, 0.08, n_baris)
    jumlah = np.clip(rng.poisson(2.2, n_baris), 1, None)
    diskon = rng.choice([0, 0.05, 0.10, 0.20], n_baris, p=[0.55, 0.2, 0.15, 0.10])
    omzet = harga * jumlah * (1 - diskon) * musim * tren

    df = pd.DataFrame(
        {
            "tanggal": tanggal,
            "wilayah": wilayah,
            "kategori": kategori,
            "jumlah": jumlah,
            "harga_satuan": harga.round(0),
            "diskon": diskon,
            "omzet": omzet.round(0),
        }
    ).sort_values("tanggal", ignore_index=True)
    return df


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "penjualan.csv"
    out.parent.mkdir(exist_ok=True)
    data = buat_data()
    data.to_csv(out, index=False)
    print(f"Tersimpan: {out} ({len(data):,} baris)")
