# -*- coding: windows-1251 -*

import json
import csv


# функция для перевода из csv в массив
def csv_to_array(filename):
    array_of_arrays = []
    count = 0

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)

        # Пропускаем заголовок
        next(csv_reader)

        for row in csv_reader:
            # Преобразование значений в нужный тип данных, если требуется
            density = 1.0
            length = float(row[2])
            width = float(row[3])
            height = float(row[4])
            x = float(row[5])
            y = float(row[6])
            z = float(row[7])
            coef_fr = 0.3

            # Создание массива значений
            array = [count, density, length, width, height, x, y, z, coef_fr]
            count += 1
            array_of_arrays.append(array)

    return array_of_arrays


# Функция для сортировки блоков от верхнего к нижнему
def sort_blocks_by_height(blocks):
    sorted_blocks = sorted(blocks, key=lambda x: x.z, reverse=True)
    return sorted_blocks


# Функция для сортировки блоков по возрастанию id
def sort_blocks_by_id(blocks):
    sorted_blocks = sorted(blocks, key=lambda x: x.block_id)
    return sorted_blocks



# Функция для проверки на соприкосновение блоков
def check_rectangle_intersection(a, b):
    rect1_x = a.x
    rect1_y = a.y
    rect1_length = a.length
    rect1_width = a.width
    rect2_x = b.x
    rect2_y = b.y
    rect2_length = b.length
    rect2_width = b.width

    rect1_right = rect1_x + rect1_length
    rect1_top = rect1_y + rect1_width

    rect2_right = rect2_x + rect2_length
    rect2_top = rect2_y + rect2_width

    if (rect1_x < rect2_right and rect1_right > rect2_x and
            rect1_y < rect2_top and rect1_top > rect2_y):
        return True  # Прямоугольники пересекаются
    else:
        return False  # Прямоугольники не пересекаются


# Функция для подсчета площади пересечения
def calculate_intersection_area(rect1, rect2):

    x_overlap = max(0, min(rect1.x + rect1.length, rect2.x + rect2.length) - max(rect1.x, rect2.x))
    y_overlap = max(0, min(rect1.y + rect1.width, rect2.y + rect2.width) - max(rect1.y, rect2.y))

    intersection_area = x_overlap * y_overlap
    return intersection_area


# Функция для обозначения соседей
def neighbour_detect(blocks):
    for block in blocks:
        for i in block.blocks_under:
            blocks[i].update_neighbour(block_id=block.blocks_under)
            blocks[i].remove_neighbour(block_id=i)
    return blocks


# Функция для расстановки id блоков сверху и снизу
def id_positions(blocks):
    blocks = sort_blocks_by_height(blocks=blocks)
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            if blocks[j].z + blocks[j].height == blocks[i].z:
                if check_rectangle_intersection(blocks[i], blocks[j]):
                    blocks[i].add_block_under(blocks[j].block_id)
                    blocks[j].update_block_above(blocks[i].blocks_above)
                    blocks[j].add_block_above(blocks[i].block_id)
                    blocks[i].add_square_under(calculate_intersection_area(blocks[i], blocks[j]))
        if blocks[i].z == 0:
            blocks[i].add_square_under(blocks[i].length * blocks[i].width)
    blocks = sort_blocks_by_id(blocks=blocks)
    blocks = neighbour_detect(blocks=blocks)
    return blocks