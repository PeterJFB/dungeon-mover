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
            e_x = randint(4, self.room.size[0] - 5) if typ in ['start', 'end'] else randint(1, self.room.size[0] - 2)
            e_y = randint(4, self.room.size[1] - 5) if typ in ['start', 'end'] else randint(1, self.room.size[1] - 2)

            room_pix[e_x, e_y] = RED
            self.enemies_pos.append([e_x, e_y])

        # Add area characteristic
        s = Image.open("startAndEnd.png")
        if typ == 'start':
            self.room.paste(s, (1, 1))

        if typ == 'end':
            e = s.rotate(180)
            self.room.paste(e, (self.room.size[0] - 4, self.room.size[1] - 4))

        # Final quality check
        left = 2 * len(exits) + len(self.enemies_pos) - 1
        if typ in ['start', 'end']:
            left += 4
        area_used = [[0 for y in range(self.room.size[0])]for x in range(self.room.size[1])]
        active = [[(size[0] - 1) // 2 * (1 + exits[0][0]) + (1 + exits[0][0]) // 2,
                   (size[1] - 1) // 2 * (1 + exits[0][1]) + (1 + exits[0][1]) // 2]]
        area_used[active[0][0]][active[0][1]] = 1
        while active:
            a = active[0]
            for d_x in range(-1, 2):
                for d_y in range(-1, 2):
                    if abs(d_x) == abs(d_y):
                        continue
                    if not 0 <= a[0] + d_x < self.room.size[0] or not 0 <= a[1] + d_y < self.room.size[1]:
                        continue
                    if room_pix[a[0] + d_x, a[1] + d_y] == BLACK:
                        continue
                    if area_used[a[0] + d_x][a[1] + d_y]:
                        continue
                    if room_pix[a[0] + d_x, a[1] + d_y] in [GREEN, RED, BLUE]:
                        left -= 1
                    area_used[a[0] + d_x][a[1] + d_y] = 1
                    active.append([a[0] + d_x, a[1] + d_y])
            if left == 0:
                break
            active = active[1:]
        if left != 0:
            new = generateRoom(size, exits, cluster, enemies, typ, show=False)
            self.room, self.enemies_pos = new.room, new.enemies_pos



        # Display image if requested
        if show:
            self.room = self.room.resize((self.room.size[0] * 100, self.room.size[1] * 100), Image.NEAREST)
            self.room.show()
# generateRoom((10, 10), [[0, -1], [0, 1],], 20, 3, show=True)
