from Island import *


class Dragon:
    def __init__(self,
                 world,
                 actual_coordinates,
                 dragon_size,
                 how_many_island_eat=0,
                 how_many_positions_eat=0,
                 is_home_find=0,
                 home_coordinates=Island(),
                 already_viewed=None):  # , eating_islands={}):
        self.world = world
        self.actual_coordinates = self.convert_start_coordinates_to_array_index(actual_coordinates, self.world)
        self.dragon_size = dragon_size
        self.how_many_island_eat = how_many_island_eat
        self.how_many_positions_eat = how_many_positions_eat
        self.is_home_find = is_home_find
        self.home_coordinates = home_coordinates
        if already_viewed is None:
            already_viewed = set()
        self.already_viewed = already_viewed
        # self.eating_islands = eating_islands  # возможно настроить хранение съеденых островов

    # w = 0
    # s = максимальный индекс в World.world
    # n = 0 индекс в World.world
    # e = максимальный индекс в World.world[position]
    def convert_start_coordinates_to_array_index(self, start_coord, world):
        dragon_position = []
        side_of_the_world = start_coord[0: 1]
        position = int(start_coord[1:])
        if side_of_the_world == "w":
            dragon_position = [position, 0]
        elif side_of_the_world == "s":
            dragon_position = [(len(world.world) - 1), position]
        elif side_of_the_world == "n":
            dragon_position = [0, position]
        elif side_of_the_world == "e":
            dragon_position = [position, (len(world.world[0]) - 1)]
        return dragon_position

    def radar(self, dragon_place, already_viewed):
        points_to_find_island = []
        l = [dragon_place[0], dragon_place[1] - 1]       # лево
        ul = [dragon_place[0] - 1, dragon_place[1] - 1]  # лево верх
        u = [dragon_place[0] - 1, dragon_place[1]]       # верх
        ur = [dragon_place[0] - 1, dragon_place[1] + 1]  # право верх
        r = [dragon_place[0], dragon_place[1] + 1]       # право
        rd = [dragon_place[0] + 1, dragon_place[1] + 1]  # право низ
        d = [dragon_place[0] + 1, dragon_place[1]]       # низ
        dl = [dragon_place[0] + 1, dragon_place[1] - 1]  # лево низ
        temp_points_to_find_island = [l, ul, u, ur, r, rd, d, dl]
        for one in temp_points_to_find_island:
            if len(already_viewed) > 0:
                if one not in already_viewed:
                    if (-1 < one[0] < len(self.world.world)) and (-1 < one[1] < len(self.world.world[0])):
                        points_to_find_island.append(one)
            else:
                if (-1 < one[0] < len(self.world.world)) and (-1 < one[1] < len(self.world.world[0])):
                    points_to_find_island.append(one)
        return points_to_find_island

    def find_the_nearest_island(self):
        temp_pints = []
        while len(self.world.islands) > 0:
            one_time_ago_points = []
            for one_time_ago_point in temp_pints:
                one_time_ago_points.append(one_time_ago_point)

            temp_pints = []
            if len(one_time_ago_points) == 0:
                self.already_viewed = self.radar(self.actual_coordinates, self.already_viewed)
                self.already_viewed.append(self.actual_coordinates)
                for coordinates in self.already_viewed:
                    temp_pints.append(coordinates)
            elif len(self.already_viewed) > 0:
                for one_coordinates in one_time_ago_points:
                    for one_new_point in self.radar(one_coordinates, self.already_viewed):
                        if one_new_point not in self.already_viewed:
                            self.already_viewed.append(one_new_point)
                            temp_pints.append(one_new_point)

            for one_island in self.world.islands:
                for one_position in one_island.get_coordinates():
                    if one_position in temp_pints:
                        if len(one_island.coordinates) > 0:
                            return one_island

    def eat_island(self, island):
        for one_position in island.get_coordinates():
            vertical = one_position[0]
            horizontal = one_position[1]
            self.world.world[vertical][horizontal] = 8  # дракон сьедает ячейку острова. отражаем это на карте
            self.actual_coordinates = [vertical, horizontal]  # обновляю текущие координаты дракона
            self.how_many_positions_eat += 1  # добавляю клетку острова к числу съеденых драконом
            if self.how_many_positions_eat % 5 == 0:
                self.dragon_size += 1

            # как вариант раскомментировать код ниже и выводить каждое изменение на карте
            # for one_line_actual_world in self.world.world:
            #   print(one_line_actual_world)
            # print("")

        self.how_many_island_eat += 1  # увеличиваю количество съеденых островов
        # self.eating_islands.update({self.is_iam_in_island})  # возможно настроить хранение съеденых островов
        self.world.islands.discard(island)

    def set_home(self, island):
        self.home_coordinates = island
        self.is_home_find = 1
        for one_coord in self.home_coordinates.coordinates:
            self.world.world[one_coord[0]][one_coord[1]] = 3  # остров на котором поселился дракон выделяем на карте

    def eat_island_or_find_home(self, island):
        if len(island.coordinates) > 0:
            if len(island.get_coordinates()) <= self.dragon_size and len(island.get_coordinates()) != 0:  # если размер острова меньше размера дракона
                self.eat_island(island)
            elif len(island.get_coordinates()) > self.dragon_size:  # если размер острова больше размера дракона
                self.set_home(island)

    def time_to_eat(self):
        while (len(self.world.islands) > 0) and (self.is_home_find == 0):
            nearest_island = self.find_the_nearest_island()
            self.eat_island_or_find_home(nearest_island)

    def print_status(self):
        print("Количество островов, которые съел дракон " + str(self.how_many_island_eat))
        print("Количество единиц суши, которое съел дракон " + str(self.how_many_positions_eat))
        print("Размер дракона " + str(self.dragon_size))
        print("Дракон не нашёл дом :(" if self.is_home_find == 0 else "Дракон нашёл дом :)")
        if len(self.home_coordinates.get_coordinates()) > 0:
            print("Координаты острова")
            for one_position in self.home_coordinates.get_coordinates():
                print((str(one_position) + ' '), end='')
