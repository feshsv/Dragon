from random import randint
from Island import *


class World:
    def __init__(self, from_size, to_size, world=None, islands=None):
        if world is None:
            world = []
        if islands is None:
            islands = set()
        self.from_size = from_size
        self.to_size = to_size
        self.world = world
        self.islands = islands
        self.get_world()
        self.generate_islands_set()

    # эта функция создаёт мир
    def get_world(self):
        #self.world.append([0, 0, 0, 0, 0, 0])
        #self.world.append([0, 0, 0, 0, 0, 0])
        #self.world.append([0, 0, 0, 0, 0, 0])
        #self.world.append([0, 0, 0, 0, 0, 0])
        #self.world.append([0, 0, 0, 0, 0, 0])
        #self.world.append([0, 0, 0, 0, 0, 0])

        world_size = randint(self.from_size, self.to_size)  # мир квадратный. тут получаем случайное число являющееся размером одной стороны мира
        one_horizontal_line = []
        for vertical in range(world_size + 1):
            if len(one_horizontal_line) > 0:  # если горизонтальная линия наполнена значениями (островами)
                self.world.append(one_horizontal_line)  # добавляем острова на карту мира
            one_horizontal_line = []  # обнуляем горизонтальную линию островов для дальнейшего наполнения новыми данными
            for horizontal in range(world_size):
                one_horizontal_line.append(randint(0, 1))  # случайным образом наполнем горизонтальную линию данными о наличии островов

    # эта функция принимает созданный мир, проверяет является ли ячейка мира островом,
    # создаёт экземпляр острова, добавляет в него координаты, добавляет экземпляр острова в
    # экземпляр хранящий экземпляры островов.
    def generate_islands_set(self):
        vertical_index = -1
        horizontal_index = -1
        one_island = Island()

        for one_horizontal_line in self.world:
            is_pre_position_island_true = 0
            if (horizontal_index + 1) == len(self.world):
                horizontal_index = -1
            vertical_index += 1
            for one_position in one_horizontal_line:
                horizontal_index += 1
                if one_position == 1:
                    if is_pre_position_island_true == 1:
                        one_island = self.is_position_already_in_some_island(vertical_index,
                                                                             horizontal_index,
                                                                             one_island,
                                                                             is_pre_position_island_true,
                                                                             self.islands)
                        one_island.add_coordinates([vertical_index, horizontal_index])
                    else:
                        one_island = self.is_position_already_in_some_island(vertical_index,
                                                                             horizontal_index,
                                                                             Island(),
                                                                             0,
                                                                             self.islands)
                        one_island.add_coordinates([vertical_index, horizontal_index])
                        if one_island not in self.islands:
                            self.islands.add(one_island)
                        is_pre_position_island_true = 1
                else:
                    is_pre_position_island_true = 0

    # если сначала алгоритм определил что остров является отдельностоящим, но при дальнейшей обработке
    # выяснилось, что это часть уже определённого ранее острова, то объеденяет новый остров с ранее созданным
    # и удаляет новый остров из экземпляра хранящего экземпляры островов.
    def is_position_already_in_some_island(self, vertPosition, horPosition, island, isPrePositionTrue, islandsMain):
        if len(islandsMain) > 0:
            for oneIsland in islandsMain:
                for coordinates in oneIsland.get_coordinates():
                    vertical = coordinates[0]
                    horizontal = coordinates[1]
                    if vertical == vertPosition - 1:
                        if horizontal == horPosition:
                            if isPrePositionTrue == 1:
                                if oneIsland != island:
                                    for one_pear in island.coordinates:
                                        oneIsland.add_coordinates(one_pear)
                                    if len(islandsMain) > 1:
                                        islandsMain.discard(island)
                                return oneIsland
                            return oneIsland
        return island

    def print_status(self):
        print("Актуальная карта")
        for one_position in self.world:
            print(one_position)
        print("Всего островов: " + str(len(self.islands)))
        print("\n")
