# -*- coding: windows-1251 -*
import math


# Функция для подсчета центра масс
def calculate_center_of_mass(blocks):
    total_mass = 0
    total_x = 0
    total_y = 0
    total_z = 0

    for block in blocks:
        total_mass += block.mass
        total_x += (block.x + block.length / 2) * block.mass
        total_y += (block.y + block.width / 2) * block.mass
        total_z += (block.z + block.height / 2) * block.mass

    center_of_mass_x = total_x / total_mass
    center_of_mass_y = total_y / total_mass
    center_of_mass_z = total_z / total_mass

    return center_of_mass_x, center_of_mass_y, center_of_mass_z


# Функция для подсчета угла падения
def calculate_fall_angle(length, width, height, square, touch_square, coeff):

    """Функция берет высоту центра масс и делит ее на ширину или длину конструкции (в зависимости от того, что больше). После этого умножает на коэффициент соприкосновения (соотношение площади блока, которая соприкасается с нижними блоками ко всей площади блока) и на коэффициент отклонения (находится из положения координат x,y центра масс и средней точки опоры)"""

    a = length
    b = width
    l = max(a, b)
    angle = math.atan(height / l * touch_square / square * coeff)
    angle = math.degrees(angle)

    print('angle:', angle)
    return angle


# Функция для нахождения центра площади пересечения двух прямоуголтников
def find_intersection_center(rect1_x, rect1_y, rect1_width, rect1_height, rect2_x, rect2_y, rect2_width, rect2_height):
    # Находим координаты правого верхнего угла для каждого прямоугольника
    rect1_right = rect1_x + rect1_width
    rect1_top = rect1_y + rect1_height
    rect2_right = rect2_x + rect2_width
    rect2_top = rect2_y + rect2_height

    # Находим координаты левого верхнего угла пересечения
    intersection_left = max(rect1_x, rect2_x)
    intersection_top = max(rect1_y, rect2_y)

    # Находим координаты правого нижнего угла пересечения
    intersection_right = min(rect1_right, rect2_right)
    intersection_bottom = min(rect1_top, rect2_top)

    # Проверяем, есть ли пересечение
    if intersection_left < intersection_right and intersection_bottom > intersection_top:
        # Находим координаты центра площади пересечения
        center_x = (intersection_left + intersection_right) / 2
        center_y = (intersection_bottom + intersection_top) / 2
        return center_x, center_y
    else:
        # Если нет пересечения, возвращаем None
        return None


# Функция для нахождения средней опорной точки
def find_average_support_point(points_x, points_y):
    points = []
    for i in range(len(points_x)):
        points.append((points_x[i], points_y[i]))
    # Проверяем, что список точек не пуст
    if not points:
        return None

    # Инициализируем суммы координат
    sum_x = 0
    sum_y = 0

    # Считаем суммы координат для всех точек
    for point in points:
        sum_x += point[0]
        sum_y += point[1]

    # Вычисляем среднюю точку опоры
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)

    return avg_x, avg_y


# Основная функция для подсчета углов падения и выявления наименьшего
def detecting_construction(blocks):
    angle = 90
    for block in blocks:
        min_x = block.x
        max_x = block.x + block.length
        min_y = block.y
        max_y = block.y + block.width

        blocks_list = set()
        blocks_list.add(block.block_id)
        blocks_list.update(block.blocks_above)
        blocks_list.update(block.neighbour)
        for i in block.neighbour:
            blocks_list.update(blocks[i].blocks_above)
        mas = []
        for i in blocks_list:
            mas.append(blocks[i])
        print()

        square = 0
        touch_square = 0
        for i in mas:
            square += i.length * i.width
            touch_square += i.square_under

            print(i)
            print()

        x, y, z = calculate_center_of_mass(mas)  # центр масс

        support_points_x = []
        support_points_y = []

        for i in block.blocks_under:
            x_, y_ = find_intersection_center(rect1_x=block.x, rect1_y=block.y, rect1_width=block.length, rect1_height=block.width, rect2_x=blocks[i].x, rect2_y=blocks[i].y, rect2_width=blocks[i].length, rect2_height=blocks[i].width)
            support_points_x.append(x_)
            support_points_y.append(y_)

        for i in block.neighbour:
            for j in blocks[i].blocks_under:
                x_, y_ = find_intersection_center(rect1_x=blocks[j].x, rect1_y=blocks[j].y, rect1_width=blocks[j].length, rect1_height=blocks[j].width, rect2_x=blocks[i].x, rect2_y=blocks[i].y, rect2_width=blocks[i].length, rect2_height=blocks[i].width)
                support_points_x.append(x_)
                support_points_y.append(y_)

        if block.blocks_under == set():
            x_ = block.x + block.length / 2
            y_ = block.y + block.width / 2
            support_points_x.append(x_)
            support_points_y.append(y_)

            for i in block.neighbour:
                x_ = (blocks[i].x + blocks[i].length) / 2
                y_ = (blocks[i].y + blocks[i].width) / 2
                support_points_x.append(x_)
                support_points_y.append(y_)

        x_support, y_support = find_average_support_point(points_x=support_points_x, points_y=support_points_y)

        min_x = block.x
        max_x = block.x + block.length
        min_y = block.y
        max_y = block.y + block.width
        for i in block.neighbour:
            min_x = min(min_x, blocks[i].x)
            max_x = max(max_x, blocks[i].x + blocks[i].length)
            min_y = min(min_y, blocks[i].y)
            max_y = max(max_y, blocks[i].y + blocks[i].width)

        a = min(max_x - x, x - min_x)
        b = min(max_y - y, y - min_y)
        dif_x = min(max_x - x_support, x_support - min_x)
        dif_y = min(max_y - y_support, y_support - min_y)
        a = dif_x / a
        b = dif_y / b

        coeff = min(a, b)

        angle = min(angle, calculate_fall_angle(length=max_x - min_x, width= max_y - min_y, height=z - block.z, square=square, touch_square=touch_square, coeff=coeff))
    return angle


# def calculate_fall_angle(weight_coefficients, contact_areas, block_areas):
#
#     fall_angle = math.atan(weight_coefficients * contact_areas / block_areas)
#     return math.degrees(fall_angle)


# def calculating(blocks):
#     angle = 90
#
#     # Значаение весового коэфицента
#     weight_cefficient = 0.2
#
#     for block in blocks:
#         blocks_list = set()
#         blocks_list.add(block.block_id)
#         blocks_list.update(block.blocks_above)
#         blocks_list.update(block.neighbour)
#         for i in block.neighbour:
#             blocks_list.update(blocks[i].blocks_above)
#         mas = []
#         for i in blocks_list:
#             mas.append(blocks[i])
#
#         s = 0.0
#         s_touch = 0.0
#         for i in mas:
#             s += i.width * i.length
#             s_touch += i.square_under
#
#         new_angle = calculate_fall_angle(weight_coefficients=weight_cefficient, contact_areas=s_touch, block_areas=s)
#         print(block.block_id, block.x, block.y, block.z, new_angle)
#         angle = min(angle, new_angle)
#
#     return angle

