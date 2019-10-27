import cv2 as cv
import numpy as np
import os






ROOT_DIR = os.path.abspath("../../")
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
IMG_NAME = os.path.join(IMAGE_DIR, "Spot24.jpg") #Parking_lot.jpg Spot   11


img = cv.imread(IMG_NAME)
img2 = cv.imread(IMG_NAME)
img3 = cv.imread(IMG_NAME)
img5 = cv.imread(IMG_NAME)
img10 = cv.imread(IMG_NAME)
#cv.imshow("img", img)



def Filter_Function(img, green_mod):
    image = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    # white color mask
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv.inRange(image, lower, upper)


    # yellow color mask
    lower = np.uint8([10, 0, 100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv.inRange(image, lower, upper)

    # blue color mask
    lower = np.uint8([90, 90, 160])
    upper = np.uint8([165, 255, 255])
    blue_mask = cv.inRange(image, lower, upper)


    # green color mask
    lower = np.uint8([25, 15, 50])
    upper = np.uint8([100, 115, 250])
    green_mask = cv.inRange(image, lower, upper)


    # combine the mask
    mask = cv.bitwise_or(white_mask, yellow_mask)
    mask = cv.bitwise_or(mask, blue_mask)

    # Test
    #if (green_mod == 0):
        #cv.imshow("filter_pred", mask)
        #ret, green_mask = cv.threshold(green_mask, 40, 255, cv.THRESH_BINARY_INV)
        #cv.imshow("green_mask", green_mask)
        #mask = cv.bitwise_and(mask, green_mask)
        #cv.imshow("filter_post", mask)
        #cv.waitKey(0)
    if (green_mod == 1):
        mask = cv.bitwise_or(mask, green_mask)
    # Test

    return mask


def Stabilize_Function(img,mod):
    blur_gray = cv.GaussianBlur(img, ksize=(33, 33), sigmaX=0)  # 27 27

    if(mod == 0):
        ret, thresh = cv.threshold(blur_gray, 40, 255, cv.THRESH_BINARY_INV)  # 50 THRESH_BINARY_INV 255
        closed = cv.erode(thresh, None, iterations=15)  # 10 15
        closed = cv.dilate(closed, None, iterations=12)  # 10 15
        ret, thresh = cv.threshold(closed, 40, 255, cv.THRESH_BINARY_INV)  # 50 THRESH_BINARY_INV 255
    else:
        return blur_gray

    return thresh



thresh1 = Filter_Function(img, 0)


contours, _ =cv.findContours(thresh1, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_KCOS)
cv.drawContours(img2, contours, -1, (0, 255, 0), 3)
for cnt in contours:
    rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
    box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
    box = np.int0(box)  # округление координат
    cv.fillPoly(img3, pts=[box], color=(255,255,255))  # рисуем прямоугольник  2
img3 = Filter_Function(img3, 0)
img3 = cv.GaussianBlur(img3, ksize=(81, 81), sigmaX=0) #71
img3 = cv.erode(img3, None, iterations =15)
ret, img3 = cv.threshold(img3, 20, 255, cv.THRESH_BINARY_INV) #220


razmetka_parkovki = Stabilize_Function(Filter_Function(img10,1),0)
mask = cv.bitwise_or(img3, razmetka_parkovki) #white_mask


mask = cv.GaussianBlur(mask, ksize=(33, 33), sigmaX=0) #33 43
closed = cv.erode(mask, None, iterations =10) # 15
razmetk = Filter_Function(img10,1)
closed = cv.bitwise_or(closed, razmetk)
#cv.imshow("thresh3", closed)


contours, _ =cv.findContours(closed, cv.RETR_LIST, cv.CHAIN_APPROX_TC89_KCOS)
cv.drawContours(img2, contours, -1, (0, 255, 0), 3)



img4 = img3
# перебираем все найденные контуры в цикле
for cnt in contours:
    #box = cv.boundingRect(cnt)
    rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
    box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
    box = np.int0(box)  # округление координат

    i = 0
    suma = [0,0,0,0]
    y = [0,0,0,0]
    x = [0,0,0,0]
    for point in box:
        print(point)
        x[i] = point[0]
        y[i] = point[1]
        suma[i] = x[i] + y[i]
        i+=1

    print(suma)
    max_i =suma.index(max(suma))
    print("max = "+ str(max_i)+"\n")
    min_i = suma.index(min(suma))
    print("min = "+ str(min_i)+"\n")
    img4 = cv.rectangle(img10, (x[min_i],y[min_i]), (x[max_i],y[max_i]), (255,255,255), 4)
    print("\n")

    #print(box)
    cv.drawContours(img5, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник

#cv.imshow("img4", img4)
cv.imshow("img5", img5)

cv.waitKey(0)