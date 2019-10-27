import cv2 as open_cv
import numpy as np
import Lines2
import Tkinter
import copy


from colors import COLOR_WHITE
from drawing_utils import draw_contours
from tkinter import *
from tkinter import messagebox as mb

class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")


    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color
        self.image = open_cv.imread(self.caption).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []
        self.iteration = 0        # Доработка
        self.pre_coordinates = [] # Доработка

        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)
        open_cv.setMouseCallback(self.caption, self.__mouse_callback)


    def generate(self):
        while True:
            open_cv.imshow(self.caption, self.image)
            key = open_cv.waitKey() #25 #113
            #key1 = open_cv.waitKey()
            if key == CoordinatesGenerator.KEY_RESET:
                self.image = open_cv.imread(self.caption).copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):

        if event == open_cv.EVENT_LBUTTONDOWN:
            self.coordinates.append((x, y))
            self.click_count += 1



            if self.click_count >= 4:
                self.iteration += 1              # Доработка
                self.__handle_done()

            if self.iteration == 2:              # Доработка
                self.iteration += 1              # Доработка
                print(self.pre_coordinates)      # Доработка
                # Тут ткинтер должен спрашивать на сколько мест надо продолжить и записать введенное в add_rect
                add_rect = Tkinter.Enter_Digit()
                add_rects = Lines2.Auto_Create_Spots(self.pre_coordinates, add_rect)  # Доработка
                print(add_rects)                 # Доработка
                for add_rect in add_rects:       # Доработка
                    self.coordinates = add_rect  # Доработка
                    self.__handle_done()         # Доработка
                for i in range(0, 2):            # Доработка
                    self.pre_coordinates.pop()   # Доработка
                self.iteration = 0               # Доработка


            elif self.click_count > 1:
                self.__handle_click_progress()

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255,0,0), 1)


    def __handle_done(self):
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color,
                     1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color,
                     1)

        self.click_count = 0

        coordinates = np.array(self.coordinates)
        print(coordinates)


        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        #draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)  # Доработка

        if self.iteration != 3:                                           # Доработка
            self.pre_coordinates.append(copy.deepcopy(self.coordinates))  # Доработка


        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1

