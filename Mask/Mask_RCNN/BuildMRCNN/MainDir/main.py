import yaml
import cv2
from coordinates_generator import CoordinatesGenerator
import colors
import logging
from tkinter import *
import tkinter as tk
import os.path
from Occupation_Spot_Detector import OSD
import threading

global MAIN_DIR
global VIDEO

def createyaml():
        data_file = "data.yaml"
        try:
            File = open(data_file)
            File.close
        except FileNotFoundError:
            File = open(data_file, 'w')
            File.close
            print("IOError")
        cap = cv2.VideoCapture(VIDEO)

        if cap.isOpened():
            for i in range(30):
                read_flag, img = cap.read()
            cv2.imwrite("image.png", img)
            cap.release()
            image_file = "image.png"
            with open(data_file, "w+") as points:
                    generator = CoordinatesGenerator(image_file, points, colors.COLOR_RED)
                    generator.generate()
                    start.configure(state=NORMAL)
        else:
            print("Error. Video camera not connected")
        

def main():
    logging.basicConfig(level=logging.INFO)
    data_file = "data.yaml"   #test
    with open(data_file, "r") as data:
        Spots = yaml.load(data)
        print(Spots)
    Detector = OSD(MAIN_DIR, VIDEO, Spots, MAX_TRY = 5)
    Detector.Occupation_Detect()




MAIN_DIR = os.path.abspath("../../")
VIDEOS_DIR = os.path.join(MAIN_DIR, "videos")
VIDEO = os.path.join(VIDEOS_DIR, "Parking_lot_1.mp4")
print(VIDEO)

picname = None
root = Tk()
root.resizable(width=False, height=False)
root.geometry("800x600")
root.title('Menu')
ChooseButton = tk.Button(root, bg='#fff7ea', fg='black', relief=RAISED, text='Определить парковочные места', font=("Arial Bold", 9),
                          width=25, height=2, command=createyaml)
start = tk.Button(root, bg='#fff7ea', fg='black', relief=RAISED, text='start', font=("Arial Bold", 9),
                         width=22, height=2, command=main, state=DISABLED)
if os.path.exists("data.yaml"):
        start.configure(state=NORMAL)
ChooseButton.place(x=122, y=150)
start.place(x=24, y=290)
root.mainloop()




