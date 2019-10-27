import cv2 as cv
import numpy as np
import os
import sys
import time
import colors


class OSD():

    def __init__(self, ROOT_DIR, VIDEO, Spots, MAX_TRY):

        self.ROOT_DIR = ROOT_DIR
        self.VIDEO = VIDEO
        self.model = OSD.Create_Model(self)
        self.MAX_TRY = MAX_TRY
        self.Data = OSD.Create_Data(self, Spots)

    time = 0


    #Создаем модель
    def Create_Model(self):
        sys.path.append(self.ROOT_DIR)  # To find local version of the library
        from mrcnn import utils
        import mrcnn.model as modellib

        # Import COCO config
        sys.path.append(os.path.join(self.ROOT_DIR, "samples/coco/"))  # To find local version
        import coco

        # Directory to save logs and trained model
        MODEL_DIR = os.path.join(self.ROOT_DIR, "logs")

        # Local path to trained weights file
        COCO_MODEL_PATH = os.path.join(self.ROOT_DIR, "mask_rcnn_coco.h5")
        # Download COCO trained weights from Releases if needed
        if not os.path.exists(COCO_MODEL_PATH):
            utils.download_trained_weights(COCO_MODEL_PATH)

        class InferenceConfig(coco.CocoConfig):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1

        config = InferenceConfig()
        config.display()

        # Create model object in inference mode.
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

        # Load weights trained on MS-COCO
        model.load_weights(COCO_MODEL_PATH, by_name=True)

        return model



    # Фильтруем список результатов распознавания, чтобы остались только автомобили.
    def get_car_boxes(self, boxes, class_ids):
        car_boxes = []

        for i, box in enumerate(boxes):
            # Если найденный объект не автомобиль, то пропускаем его.
            if class_ids[i] in [3, 8, 6]:
                car_boxes.append(box)

        return np.array(car_boxes)



    # Отображаем каждую рамку на кадре.
    def Draw_Rectangles_Frame(self, frame, boxes, color):
        # Отображаем каждую рамку на кадре.
        for box in boxes:

            y1, x1, y2, x2 = box

            if color == "blue":
                cv.rectangle(frame, (x1, y1), (x2, y2), colors.COLOR_BLUE, 2)
            if color == "green":
                cv.rectangle(frame, (x1, y1), (x2, y2), colors.COLOR_GREEN, 2)
            if color == "red":
                cv.rectangle(frame, (x1, y1), (x2, y2), colors.COLOR_RED, 2)

        return frame



    # Ищем среднее между двумя точками
    def Mid_Points_Search(self, points):

        internal_points = []
        mid_points = []
        min_match = 0
        max_match = 0
        min_point = min(points)
        max_point = max(points)
        for point in points:
            if (min_point < point) and (point < max_point):
                internal_points.append(point)
            if (min_point == point):
                min_match += 1
            if (max_point == point):
                max_match += 1
        if min_match == 2:
            internal_points.append(min_point)
        if max_match == 2:
            internal_points.append(max_point)

        internal_min_point = min(internal_points)
        internal_max_point = max(internal_points)


        mid_points.append(int((min_point + internal_min_point) / 2))
        mid_points.append(int((max_point + internal_max_point) / 2))
        return mid_points



    # Для отображениея квадратов (y1,x1,y2,x2)
    def Spot2Box(self, Coordinates):


        Box = [0, 0, 0, 0]
        for i in range(2):
            points = [Coordinates[0][i], Coordinates[1][i], Coordinates[2][i], Coordinates[3][i]]
            mid_points = OSD.Mid_Points_Search(self, points)
            Box[1-i] = mid_points[0]
            Box[3-i] = mid_points[1]

        return Box


    # Формируем данные
    def Create_Data(self, Spots):

        Data = []
        print(Spots)
        for Spot in Spots:
            Data_Spot = {'id': Spot['id'],
                         'box_coordinates': OSD.Spot2Box(self, Spot['coordinates']),
                         'occuped': False,
                         'time': {'hours' : 0, 'minute' : 0, 'second' : 0},
                         'try': 0}

            Data.append(Data_Spot)

        return Data



    #Детектируем машины на кадре
    def Detect_Car(self, frame):

        # Конвертируем изображение из цветовой модели BGR (используется OpenCV) в RGB.
        rgb_image = frame[:, :, ::-1]

        # Подаём изображение модели Mask R-CNN для получения результата.
        results = self.model.detect([rgb_image], verbose=0)

        # Mask R-CNN предполагает, что мы распознаём объекты на множественных изображениях.
        # Мы передали только одно изображение, поэтому извлекаем только первый результат.
        r = results[0]

        # Переменная r теперь содержит результаты распознавания:
        # - r['rois'] — ограничивающая рамка для каждого распознанного объекта;
        # - r['class_ids'] — идентификатор (тип) объекта;
        # - r['scores'] — степень уверенности;
        # - r['masks'] — маски объектов (что даёт вам их контур).

        # Фильтруем результат для получения рамок автомобилей.
        car_boxes = OSD.get_car_boxes(self, r['rois'], r['class_ids'])

        return car_boxes



    def Search_Match(self, car_boxes):

        import mrcnn

        PERCENT = 0.20

        Spot_boxes = []

        for Spot in self.Data:
            Spot_box = Spot.get("box_coordinates")
            Spot_boxes.append(Spot_box)

        Spot_boxes = np.array(Spot_boxes)
        overlaps = mrcnn.utils.compute_overlaps(Spot_boxes, car_boxes)
        print("\n\n")
        print(overlaps)
        i = 0

        for Spot_box, overlap_areas in zip(Spot_boxes, overlaps):

            # Ищем максимальное значение пересечения с любой обнаруженной
            # на кадре машиной (неважно, какой).
            max_IoU_overlap = np.max(overlap_areas)

            # Проверяем, занято ли место, проверив значение IoU.
            if PERCENT < max_IoU_overlap:

                self.Data[i]['occuped'] = True

            else:
                self.Data[i]['occuped'] = False

            i += 1



    def Time_Occupation(self):

        i = 0

        for Spot in self.Data:
            if Spot['occuped'] == True:
                self.Data[i]['time']['second'] = self.Data[i]['time']['second'] + OSD.time
                self.Data[i]['try'] = 0
            else:
                if Spot['try'] == self.MAX_TRY:
                    self.Data[i]['time']['second'] = 0
                    self.Data[i]['time']['minute'] = 0
                    self.Data[i]['time']['hours'] = 0
                    self.Data[i]['try'] = 0
                else:
                    self.Data[i]['try'] += 1

            if self.Data[i]['time']['second'] >= 60:
                self.Data[i]['time']['second'] = self.Data[i]['time']['second'] - 60
                self.Data[i]['time']['minute'] += 1
            if self.Data[i]['time']['minute'] >= 60:
                self.Data[i]['time']['minute'] = self.Data[i]['time']['minute'] - 60
                self.Data[i]['time']['hours'] += 1

            print(self.Data[i])
            i += 1


    def Occupation_Detect(self):

        from threading import Thread
        video_capture = cv.VideoCapture(self.VIDEO)



        while video_capture.isOpened():


            timeBegin = time.time()
            Time_Occupation = Thread(target=OSD.Time_Occupation, args=(self,))
            Time_Occupation.start()

            success, frame = video_capture.read()
            if not success:
                break

            car_boxes = OSD.Detect_Car(self, frame)

            occ_spot_boxes = []
            free_spot_boxes = []

            for Spot in self.Data:
                if Spot['occuped'] == True:
                    occ_spot_boxes.append(Spot['box_coordinates'])
                    print(1)
                else:
                    free_spot_boxes.append(Spot['box_coordinates'])
                    print(2)


            frame = OSD.Draw_Rectangles_Frame(self, frame, occ_spot_boxes, "red")
            frame = OSD.Draw_Rectangles_Frame(self, frame, free_spot_boxes, "green")

            # Отображаем каждую рамку на кадре.
            frame = OSD.Draw_Rectangles_Frame(self, frame, car_boxes, "blue")

            OSD.Search_Match(self, car_boxes)

            Time_Occupation.join()
            OSD.time = time.time() - timeBegin


            cv.putText(frame, "Average Seconds=" + str(OSD.time), (30, 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                       colors.COLOR_BLUE, 5)

            # Показываем кадр на экране.
            cv.imshow('Video', frame)

            # Нажмите 'q', чтобы выйти.
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # Очищаем всё после завершения.
        video_capture.release()
        cv.destroyAllWindows()