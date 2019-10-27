import cv2 as cv
import math
import copy



def Search_Min_Distance(figure):    # Ищет минимальное расстояние между двумя точками фигур.
    min_distance = 4000             # Возвращает точки принадлежащие минимальному расстоянию.
    first_figure = figure[0]          # Сначала возвращает координаты точки первой фигуры потом координаты второй.
    second_figure = figure[1]
    for first_point in first_figure:
        for second_point in second_figure:
            distance = math.sqrt((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2)
            if (distance < min_distance):
                first_min_point = first_point
                second_min_point = second_point
                min_distance = distance
    return first_min_point, second_min_point


def Search_Vectors(rect):
    vector_list = []

    first_min_point, second_min_point = Search_Min_Distance(rect)
    first_vector = [a - b for a, b in
                    zip(second_min_point, first_min_point)]  # Вычисляем координаты вектора расстояния между местами
    vector_list.append(first_vector)


    previous_two_points = [first_min_point, second_min_point]  # Сохраняем координаты предыдущих точек
    rect[0].remove(first_min_point)
    rect[1].remove(second_min_point)

    first_min_point, second_min_point = Search_Min_Distance(rect)# Получаем координаты последней пары точек минимальных отрезков
    rect[0].remove(first_min_point)
    rect[1].remove(second_min_point) # Получили пару точек первого и второго квадратов не входящих в мин. отрезки

    projection_axis_x = int(
        (((previous_two_points[0][0] + first_min_point[0]) / 2 - (rect[0][0][0] + rect[0][1][0]) / 2) +
         ((rect[1][0][0] + rect[1][1][0]) / 2) - (previous_two_points[1][0] + second_min_point[0]) / 2) / 2)

    projection_axis_y = int(
        (((previous_two_points[0][1] + first_min_point[1]) / 2 - (rect[0][0][1] + rect[0][1][1]) / 2) +
         ((rect[1][0][1] + rect[1][1][1]) / 2) - (previous_two_points[1][1] + second_min_point[1]) / 2) / 2)

    second_vector = [projection_axis_x, projection_axis_y]
    vector_list.append(second_vector)

    front_points = copy.deepcopy(rect[1])  # Это точки от которых впоследствии можно откладывать вектора и находить следующие точки
    rect[:] = []

    return vector_list, front_points


def Clone_Spots(vectors, begin_points, num_iterations):

    rects = []
    spot = []
    for i in range(int(num_iterations)):
        spot[:] = []
        for j in range(2):

            begin_point_x = begin_points[j][0] + vectors[0][0]
            begin_point_y = begin_points[j][1] + vectors[0][1]
            begin_point = [begin_point_x, begin_point_y]

            end_point_x = begin_point_x + vectors[1][0]
            end_point_y = begin_point_y + vectors[1][1]
            end_point = [end_point_x, end_point_y]

            begin_points[j][0] = end_point_x
            begin_points[j][1] = end_point_y

            spot.append(begin_point)
            spot.append(end_point)
        print(spot)
        rects.append(copy.deepcopy(spot))
    return rects


def Auto_Create_Spots(rect_coordinates, add_rect):

    rect = []  # Преводим из кортежа в список
    for tuple_coordinates in rect_coordinates:
        list_point = []
        for tuple_point in tuple_coordinates:
            list_point.append(list(tuple_point))
        rect.append(copy.deepcopy(list_point))



    vectors, front_points = Search_Vectors(rect)

    list_result = Clone_Spots(vectors, front_points, add_rect)



    tuple_result = [] # Переводим из списка в кортеж
    for list_spot in list_result:
        tuple_point = []
        for list_point in list_spot:
            tuple_point.append(tuple(list_point))
        tuple_result.append(copy.deepcopy(tuple_point))




    return tuple_result
