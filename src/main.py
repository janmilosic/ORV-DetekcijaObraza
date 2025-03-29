import cv2 as cv
import numpy as np
import time

def zmanjsaj_sliko(slika, sirina, visina):
    return cv.resize(slika, (sirina, visina))

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    pass

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    pass

if __name__ == '__main__':
    kamera = cv.VideoCapture(0)
    ret, slika = kamera.read()
    slika = zmanjsaj_sliko(slika, 340, 220)
