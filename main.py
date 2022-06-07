from World import *
from Dragon import *


if __name__ == '__main__':
    world = World(20, 21)
    world.print_status()

    dragon = Dragon(world, "e2", 60)
    dragon.time_to_eat()

    world.print_status()
    dragon.print_status()



