# -*- coding: windows-1251 -*

from visualisation import Visualisation
from data_transition import id_positions, csv_to_array
from Block import Block
from algoritms import detecting_construction


# ОШИБКА В 4, 5, 7, 11, 14 табицах
# Пример использования функции
input_filename = 'data/Garpix_data_1 - 6.csv'  # Имя входного scv файла

mas = csv_to_array(input_filename)   # массив с данными из csv фаыйла

blocks = []
for i in mas:
    blocks.append(Block(block_id=i[0], density=i[1], length=i[2], width=i[3], height=i[4], x=i[5], y=i[6], z=i[7], coef_fr=i[8]))


blocks = id_positions(blocks)
# for i in blocks:
#     print(i)
#     print()

print()
angle = detecting_construction(blocks=blocks)
print()
print('angle:', angle)
print()

blocks_vis = []
for i in mas:
    blocks_vis.append({"x": i[5], "y": i[6], "z": i[7], "width": i[3], "height": i[4], "length": i[2], "color": i[0] % 10})


vis = Visualisation()
vis.plot_blocks(blocks=blocks_vis, angle=angle)

