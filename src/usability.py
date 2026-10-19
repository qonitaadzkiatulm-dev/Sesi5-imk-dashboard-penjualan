"""Analisis hasil usability testing (Modul 4): SUS, Success Rate, dan Task Time.

Jalankan:  python src/usability.py
Membaca data/usability_testing.csv (contoh data simulasi; ganti dengan data uji nyata Anda).
"""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "usability_testing.csv"


def skor_sus(jawaban: list[int]) -> float:
    """System Usability Scale: 10 butir skala 1-5. Butir ganjil: (nilai-1); genap: (5-nilai); total x 2,5."""
    if len(jawaban) != 10 or not all(1 <= j <= 5 for j in jawaban):
        raise ValueError("SUS membutuhkan 10 jawaban bernilai 1-5")
    total = sum((j - 1) if i % 2 == 0 else (5 - j) for i, j in enumerate(jawaban))
    return total * 2.5


def interpretasi_sus(skor: float) -> str:
    if skor >= 80.3:
        return "Sangat baik (A)"
    if skor >= 68:
        return "Di atas rata-rata (dapat diterima)"
    if skor >= 51:
        return "Di bawah rata-rata (perlu perbaikan)"
    return "Buruk"


def ringkas_tugas(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("tugas")
        .agg(
            responden=("responden", "nunique"),
            success_rate=("berhasil", lambda s: s.mean() * 100),
            waktu_rata_detik=("waktu_detik", "mean"),
            waktu_median_detik=("waktu_detik", "median"),
        )
        .round(1)
        .reset_index()
    )


if __name__ == "__main__":
    df = pd.read_csv(DATA)
    print("=== Success Rate & Task Time per tugas ===")
    print(ringkas_tugas(df).to_string(index=False))

    sus_cols = [f"sus{i}" for i in range(1, 11)]
    sus = pd.read_csv(DATA.with_name("sus_responden.csv"))
    sus["skor_sus"] = sus[sus_cols].apply(lambda r: skor_sus(r.tolist()), axis=1)
    rata = sus["skor_sus"].mean()
    print(f"\n=== SUS ({len(sus)} responden) ===")
    print(f"Rata-rata skor SUS: {rata:.1f} -> {interpretasi_sus(rata)}")
