"""Intégrité des données brutes : chaque fichier présent doit correspondre au manifeste.

Détecte une corruption, une modification manuelle ou le remplacement d'un fichier
SIM révisé par Météo-France sans mise à jour tracée du manifeste.
Lecture de ~2,3 Go : quelques secondes.
"""

import csv

import pytest

from atlas.download import ROOT, sha256_of_file

MANIFEST = ROOT / "docs" / "manifest_raw.csv"
with open(MANIFEST, newline="") as f:
    ROWS = list(csv.DictReader(f))


def test_manifest_has_no_duplicate_files():
    files = [r["file"] for r in ROWS]
    assert len(files) == len(set(files))


@pytest.mark.parametrize("row", ROWS, ids=[r["file"].rsplit("/", 1)[1] for r in ROWS])
def test_raw_file_matches_manifest(row):
    path = ROOT / row["file"]
    if not path.exists():
        pytest.skip(f"{row['file']} absent (non téléchargé)")
    assert path.stat().st_size == int(row["size_bytes"])
    assert sha256_of_file(path) == row["sha256"]
