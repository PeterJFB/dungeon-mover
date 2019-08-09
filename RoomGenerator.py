from random import randint
from PIL import Image

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)


class generateRoom(object):
    def __init__(self, size, exits, cluster, enemies, typ='other',  show=False):
        self.size = size
        self.exits = exits
        self.enemies = enemies
        self.enemies_pos = []
        self.typ = typ
        self.room = Image.new("RGBA", size, "black")
        self.size = size
        self.open = False
        room_pix = self.room.load()

        # Create frame
        self.room.paste(WHITE, (1, 1, self.room.size[0] - 1, self.room.size[1] - 1))

        # Create exits
        for ex in exits:
            area = (size[0] // 2 * (1 + ex[0]) - 1,
                    size[1] // 2 * (1 + ex[1]) - 1,
                    size[0] // 2 * (1 + ex[0]) + 1,
                    size[1] // 2 * (1 + ex[1]) + 1)
            self.room.paste(GREEN, area)

        # Cluster
        for c in range(cluster):
            room_pix[randint(1, self.room.size[0] - 2), randint(1, self.room.size[1] - 2)] = BLACK

        # Enemies
        for e in range(self.enemies):
            e_x = randint(1, self.room.size[0] - 2) if typ not in ['start', 'end'] else randint(4, self.room.size[0] - 5)
            e_y = randint(1, self.room.size[1] - 2) if typ not in ['start', 'end'] else randint(4, self.room.size[1] - 5)

            room_pix[e_x, e_y] = RED
            self.enemies_pos.append([e_x, e_y])

        # Add area characteristic
        s = Image.open("startAndEnd.png")
        if typ == 'start':
            self.room.paste(s, (1, 1))

        if typ == 'end':
            e = s.rotate(180)
            self.room.paste(e, (self.room.size[0] - 4, self.room.size[1] - 4))

        # Display image if requested
        if show:
            self.room = self.room.resize((self.room.size[0] * 100, self.room.size[1] * 100), Image.NEAREST)
            self.room.show()

# generateRoom((12, 12), [[0, -1], [1, 0]], 20, 3, True)
