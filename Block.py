# -*- coding: windows-1251 -*

class Block:
    def __init__(self, block_id, density, length, width, height, x, y, z, coef_fr):
        self.block_id = block_id  # сам генерим
        self.density = density   # плотность
        self.length = length
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z
        self.mass = density * length * width * height
        self.blocks_above = set()  # Все блоки, опирающиеся на этот блок
        self.blocks_under = set()  # Все блоки, на которые опирается этот блок
        self.neighbour = set()  # Соседние блоки
        self.coef_cont = 0   # коэфициент площади соприкосновения с нижним блоком к площади нижней стороны блока
        self.square_under = 0   # площадь соприкосновения с нижними блоками
        self.coef_fr = coef_fr   # Коэфицент трения

    def add_block_above(self, block_id):
        self.blocks_above.add(block_id)

    def add_block_under(self, block_id):
        self.blocks_under.add(block_id)

    def update_block_above(self, block_id):
        self.blocks_above.update(block_id)

    def remove_neighbour(self, block_id):
        self.neighbour.remove(block_id)

    def update_neighbour(self, block_id):
        self.neighbour.update(block_id)

    def add_square_under(self, square):
        self.square_under += square
        self.coef_cont = self.square_under / (self.width * self.length)

    def change_mass(self, mass):
        self.mass = mass

    def __str__(self):
        return f"Block ID: {self.block_id}\nDensity: {self.density}\nMass: {self.mass}\nLength: {self.length}\nWidth: {self.width}\nHeight: {self.height}\nCoordinates (x, y, z): ({self.x}, {self.y}, {self.z})\nBlocks Above: {self.blocks_above}\nBlocks Under: {self.blocks_under}\nNeighbour Blocks: {self.neighbour}\nCoefficient of contact: {self.coef_cont}\nSquare under: {self.square_under}\nCoefficient friction: {self.coef_fr}"

