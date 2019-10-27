import cv2
import numpy as np
import os

ROOT_DIR = os.path.abspath("../../")
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
IMG_NAME = os.path.join(IMAGE_DIR, "Spot20.jpg") #Parking_lot.jpg Spot

if __name__ == '__main__':
    def nothing(*arg):
        pass

cv2.namedWindow("result")  # создаем главное окно
cv2.namedWindow("settings")  # создаем окно настроек

# создаем 6 бегунков для настройки начального и конечного цвета фильтра
cv2.createTrackbar('h1', 'settings', 0, 255, nothing)
cv2.createTrackbar('l1', 'settings', 0, 255, nothing)
cv2.createTrackbar('s1', 'settings', 0, 255, nothing)
cv2.createTrackbar('h2', 'settings', 255, 255, nothing)
cv2.createTrackbar('l2', 'settings', 255, 255, nothing)
cv2.createTrackbar('s2', 'settings', 255, 255, nothing)
crange = [0, 0, 0, 0, 0, 0]


while True:
    img = cv2.imread(IMG_NAME)
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # считываем значения бегунков
    h1 = cv2.getTrackbarPos('h1', 'settings')
    l1 = cv2.getTrackbarPos('l1', 'settings')
    s1 = cv2.getTrackbarPos('s1', 'settings')
    h2 = cv2.getTrackbarPos('h2', 'settings')
    l2 = cv2.getTrackbarPos('l2', 'settings')
    s2 = cv2.getTrackbarPos('s2', 'settings')

    # формируем начальный и конечный цвет фильтра
    h_min = np.array((h1, l1, s1), np.uint8)
    h_max = np.array((h2, l2, s2), np.uint8)

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hls, h_min, h_max)

    cv2.imshow('result', thresh)

    ch = cv2.waitKey(5)
    if ch == 27:
        break

cv2.destroyAllWindows()