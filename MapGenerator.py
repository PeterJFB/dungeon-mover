import numpy as np
from random import randint
from PIL import Image
import RoomGenerator as rm


def generateMap(size, room_size, start, show=False):
    # define size of grid
    cell_grid = (size[0] * 2 - 1, size[1] * 2 - 1)
    # define starting position
    cell_pos = np.array([start[0] * 2, start[1] * 2])

    # generate image
    maze = Image.new("RGBA", cell_grid, "black")
    maze_pix = maze.load()

    # color codes
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    BLUE = (0, 0, 255, 255)

    def freeCells():
        # Find avaliable cells around main cell
        d = []
        for d_x in range(-2, 3, 2):
            for d_y in range(-2, 3, 2):
                if abs(d_x) == abs(d_y):
                    continue
                if not (maze.size[0] > d_x + cell_pos[0] >= 0) or not (maze.size[1] > d_y + cell_pos[1] >= 0):
                    continue
                if maze_pix[int(d_x + cell_pos[0]), int(d_y + cell_pos[1])] != BLACK:
                    continue

                d.append(np.array([d_x, d_y]))
        return d

    def backCell():
        # Used when the main cell needs to go back
        for d_x in range(-1, 2):
            for d_y in range(-1, 2):
                if not (maze.size[0] > d_x + cell_pos[0] >= 0) or not (maze.size[1] > d_y + cell_pos[1] >= 0):
                    continue
                if maze_pix[int(d_x + cell_pos[0]), int(d_y + cell_pos[1])] == BLUE:
                    return np.array([d_x, d_y])

        # Returns blank list if it has failed
        return []

    # main
    generating = True
    while generating:
        nextCell = freeCells()
        # if a neighboring cell is available
        if nextCell:
            cell_next = nextCell[randint(0, len(nextCell) - 1)]
            maze_pix[int(cell_pos[0]), int(cell_pos[1])] = BLUE
            maze_pix[int(cell_pos[0] + cell_next[0] / 2), int(cell_pos[1] + cell_next[1] / 2)] = BLUE
            cell_pos += cell_next

        # if there's no available cell/begin backtracking
        else:
            cell_next = backCell()
            if list(cell_next):
                maze_pix[int(cell_pos[0]), int(cell_pos[1])] = WHITE
                maze_pix[int(cell_pos[0] + cell_next[0]), int(cell_pos[1] + cell_next[1])] = WHITE
                cell_pos += cell_next * 2
            # Will end if there's no cell to backtrack to
            else:
                break

    # Create world

    def findExits(x, y):
        d = []
        for d_x in range(-1, 2):
            for d_y in range(-1, 2):
                if abs(d_x) == abs(d_y):
                    continue
                if not (maze.size[0] > d_x + x * 2 >= 0) or not (maze.size[1] > d_y + y * 2 >= 0):
                    continue
                if maze_pix[int(x * 2 + d_x), int(y * 2 + d_y)] == WHITE:
                    d.append([d_x, d_y])
        return d

    world = Image.new("RGBA", (size[0] * room_size[0], size[1] * room_size[1]), "black")

    rooms = []
    enemies_pos = []
    for y in range(0, size[1]):
        rooms_temp = []
        enemies_pos_temp = []
        for x in range(0, size[0]):

            if (x, y) == (0, 0):
                typ = 'start'
            elif (x + 1, y + 1) == size:
                typ = 'end'
            else:
                typ = 'other'

            room = rm.generateRoom(size=room_size,
                                        exits=findExits(x, y),
                                        cluster=20,
                                        enemies=randint(1, 4),
                                        typ=typ,
                                   show=False)

            world.paste(room.room,  (x * room_size[0], y * room_size[1]))
            rooms_temp.append(room)
            enemies_pos_temp.append(room.enemies_pos)
        rooms.append(rooms_temp)
        enemies_pos.append(enemies_pos_temp)
    # Display image if requested
    if show:
        w = world.resize((100 * world.size[0], 100 * world.size[1]), Image.NEAREST)
        w.show()
    return world, rooms, enemies_pos

# generateMap((3, 3), (2, 2), True)
