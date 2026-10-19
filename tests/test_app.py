import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import analytics as an  # noqa: E402
import charts as ch  # noqa: E402
import usability  # noqa: E402


@pytest.fixture(scope="module")
def df():
    return an.muat_data()


def test_filter_periode_dan_kategori(df):
    d = an.filter_data(df, "2025-01-01", "2025-03-31", kategori=["Makanan"])
    assert d["tanggal"].between("2025-01-01", "2025-03-31").all()
    assert set(d["kategori"]) == {"Makanan"}


def test_filter_kosong_tidak_error(df):
    d = an.filter_data(df, "2025-01-01", "2025-01-01", wilayah=["Sumatera"], kategori=["Elektronik"])
    k = an.hitung_kpi(df, d, "2025-01-01", "2025-01-01")
    assert k.jumlah_transaksi == len(d)
    assert an.buat_insight(d) == [] or len(d) > 0


def test_pertumbuhan_pakai_periode_sebelumnya(df):
    d = an.filter_data(df, "2025-01-01", "2025-06-30")
    k = an.hitung_kpi(df, d, "2025-01-01", "2025-06-30")
    prev = an.filter_data(df, "2024-07-04", "2024-12-31")  # 181 hari sebelum 1 Jan 2025
    assert k.pertumbuhan is not None
    assert k.total_omzet == pytest.approx(d["omzet"].sum())
    assert prev["omzet"].sum() > 0


def test_pertumbuhan_none_jika_tak_ada_pembanding(df):
    d = an.filter_data(df, "2024-01-01", "2024-03-31")
    assert an.hitung_kpi(df, d, "2024-01-01", "2024-03-31").pertumbuhan is None


@pytest.mark.parametrize(
    "nilai,harapan",
    [(1_410_000_000, "Rp 1,41 M"), (4_500_000, "Rp 4,5 jt"), (120_000, "Rp 120 rb"), (950, "Rp 950")],
)
def test_format_rupiah(nilai, harapan):
    assert an.format_rupiah(nilai) == harapan


def test_semua_grafik_terbentuk_dan_bar_mulai_dari_nol(df):
    for f in (ch.grafik_tren, ch.grafik_kategori, ch.grafik_wilayah, ch.grafik_proporsi, ch.grafik_scatter):
        assert f(df) is not None
    for f in (ch.grafik_kategori, ch.grafik_wilayah):
        assert f(df).layout.xaxis.range[0] == 0  # skala jujur (etika desain)


def test_bar_hanya_satu_warna_aksen(df):
    warna = list(ch.grafik_kategori(df).data[0].marker.color)
    assert warna.count(ch.AKSEN) == 1


def test_sus_skor_rentang():
    assert usability.skor_sus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1]) == 100
    assert usability.skor_sus([1, 5, 1, 5, 1, 5, 1, 5, 1, 5]) == 0
    assert usability.skor_sus([3] * 10) == 50


def test_warna_kategori_konsisten_antar_grafik(df):
    donut = ch.grafik_proporsi(df).data[0]
    peta_donut = dict(zip(donut.labels, donut.marker.colors))
    for tr in ch.grafik_scatter(df).data:
        assert tr.marker.color == peta_donut[tr.name]
