# -*- coding: windows-1251 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Visualisation:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")

    def plot_blocks(self, blocks, angle):
        for block in blocks:
            x = block["x"]
            y = block["y"]
            z = block["z"]
            width = block["width"]
            height = block["height"]
            length = block["length"]
            color = block["color"]

            vertices = [
                [x, y, z],
                [x + length, y, z],
                [x + length, y + width, z],
                [x, y + width, z],
                [x, y, z + height],
                [x + length, y, z + height],
                [x + length, y + width, z + height],
                [x, y + width, z + height]
            ]

            faces = [
                [vertices[0], vertices[1], vertices[2], vertices[3]],  # ������� ����� 1
                [vertices[4], vertices[5], vertices[6], vertices[7]],  # ������� ����� 2
                [vertices[0], vertices[1], vertices[5], vertices[4]],  # ���
                [vertices[2], vertices[3], vertices[7], vertices[6]],  # ����
                [vertices[1], vertices[2], vertices[6], vertices[5]],  # �������� �����
                [vertices[0], vertices[3], vertices[7], vertices[4]]  # ������ �����
            ]

            collection = Poly3DCollection(faces, linewidths=1, edgecolors="k", alpha=0.5)
            collection.set_facecolor("C" + str(color))

            self.ax.add_collection3d(collection)

        self.ax.set_xlim([0, 100])  # ���������� ������ ������� ��� ��� X
        self.ax.set_ylim([0, 100])  # ���������� ������ ������� ��� ��� Y
        self.ax.set_zlim([0, 100])  # ���������� ������ ������� ��� ��� Z

        # ������� ���� �������
        self.ax.text2D(0.05, 0.95, f"���� �������: {angle} �������� \n", transform=self.ax.transAxes)
        plt.show()

