import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    x1, y1 = levo_zgoraj
    x2, y2 = desno_spodaj
    izrez = slika[y1:y2, x1:x2]
    povprecje = np.mean(izrez, axis=(0, 1))  # Povprecna barva v obmocju
    razpon = 40

    # Meje koze
    spodnja_meja = np.clip(povprecje - razpon, 0, 255).astype(np.uint8).reshape(1, 3)
    zgornja_meja = np.clip(povprecje + razpon, 0, 255).astype(np.uint8).reshape(1, 3)
    return spodnja_meja, zgornja_meja

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    pass

if __name__ == '__main__':
    kamera = cv.VideoCapture(0)
    ret, slika = kamera.read()
    slika = zmanjsaj_sliko(slika, 340, 220)
