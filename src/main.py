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
    visina, sirina, _ = slika.shape
    st_vrstic = visina // visina_skatle
    st_stolpcev = sirina // sirina_skatle
    rezultat = []
    for i in range(st_vrstic):
        vrstica = []
        for j in range(st_stolpcev):
            x = j * sirina_skatle
            y = i * visina_skatle
            skatla = slika[y:y+visina_skatle, x:x+sirina_skatle]
            st_pikslov = prestej_piksle_z_barvo_koze(skatla, barva_koze)
            vrstica.append(st_pikslov)
        rezultat.append(vrstica)
    return rezultat

def narisi_skatle(slika, seznam, sirina_skatle, visina_skatle, prag=500):
    for i, vrstica in enumerate(seznam):
        for j, st_pikslov in enumerate(vrstica):
            if st_pikslov > prag:
                x = j * sirina_skatle
                y = i * visina_skatle
                cv.rectangle(slika, (x, y), (x+sirina_skatle, y+visina_skatle), (0, 255, 0), 2)

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

    st_koze = prestej_piksle_z_barvo_koze(slika, barva_koze)
    print("Number of skin pixels:", st_koze)