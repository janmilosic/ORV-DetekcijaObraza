import numpy as np
from main import zmanjsaj_sliko, doloci_barvo_koze, prestej_piksle_z_barvo_koze

def test_zmanjsaj_sliko():
    slika = np.zeros((200, 300, 3), dtype=np.uint8)
    nova = zmanjsaj_sliko(slika, 100, 100)
    assert nova.shape == (100, 100, 3)

def test_doloci_barvo_koze():
    slika = np.full((10, 10, 3), 100, dtype=np.uint8)
    spodnja, zgornja = doloci_barvo_koze(slika, (0, 0), (10, 10))
    assert spodnja.shape == (1, 3)
    assert zgornja.shape == (1, 3)
    assert (spodnja <= zgornja).all()

def test_prestej_piksle_z_barvo_koze():
    slika = np.full((10, 10, 3), 100, dtype=np.uint8)
    barva = doloci_barvo_koze(slika, (0, 0), (10, 10))
    st = prestej_piksle_z_barvo_koze(slika, barva)
    assert st == 10