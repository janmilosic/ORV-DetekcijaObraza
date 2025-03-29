import cv2 as cv
import numpy as np
import time

risanje = False
p_zacetek = (0, 0)
p_konec = (0, 0)

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
    spodnja, zgornja = barva_koze
    maska = cv.inRange(slika, spodnja, zgornja)
    return cv.countNonZero(maska)

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    pass

def mouse_callback(event, x, y, flags, param):
    global risanje, p_zacetek, p_konec
    if event == cv.EVENT_LBUTTONDOWN:
        risanje = True
        p_zacetek = (x, y)
    elif event == cv.EVENT_MOUSEMOVE and risanje:
        p_konec = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        risanje = False
        p_konec = (x, y)

if __name__ == '__main__':
    kamera = cv.VideoCapture(0)
    ret, slika = kamera.read()
    slika = zmanjsaj_sliko(slika, 340, 220)

    cv.namedWindow("Izberi obmocje koze")
    cv.setMouseCallback("Izberi obmocje koze", mouse_callback)

    # Uporabnik izbere obocje, kjer je koza
    while True:
        temp_slika = slika.copy()
        if p_zacetek != p_konec:
            cv.rectangle(temp_slika, p_zacetek, p_konec, (255, 0, 0), 2)
        cv.imshow("Izberi obmocje koze", temp_slika)
        if cv.waitKey(1) & 0xFF == ord('y'):
            break

    cv.destroyWindow("Izberi obmocje koze")

    # Pretvori koordinati v urejen par
    levo_zgoraj = (min(p_zacetek[0], p_konec[0]), min(p_zacetek[1], p_konec[1]))
    desno_spodaj = (max(p_zacetek[0], p_konec[0]), max(p_zacetek[1], p_konec[1]))
    barva_koze = doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj)