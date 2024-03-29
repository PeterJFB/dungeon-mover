# -*- coding: utf-8 -*-
"""
Created on Sun May 19 17:41:22 2019

@author: v1504flpe
"""
import pygame as pg
from PIL import Image
import time

import MapGenerator as mg
"""DEVTOOL
import HeatmapGenerator as hg
"""
pg.init()

# World
world_size = (5, 5)
room_size = (10, 10)

# Window
tile_size = 32
scale = 2
tile_scale = tile_size * scale

win_tiles = 11
win_size = win_tiles * tile_scale

win_center = int(win_tiles / 2)

win = pg.display.set_mode((win_size, win_size))
pg.display.set_caption("W A S D")

# Timer
clock = pg.time.Clock()

# Load tileset
tileset = pg.image.load("Tileset.png")
tileset_dim = tileset.get_size()

tiles = []
for y in range(tileset_dim[1] // tile_size):
    tiles_temp = []
    for x in range(tileset_dim[0] // tile_size):
        tile_dim = (x * tile_size, y * tile_size, tile_size, tile_size)
        tiles_temp.append(tileset.subsurface(tile_dim))
    tiles.append(tiles_temp)

tiles_all = [[pg.transform.scale(t, (tile_scale, tile_scale)) for t in tile] for tile in tiles]


# counter
counter_font = pg.font.Font("OdeToIdleGamingFont.ttf", 32)
counter_font_menu = pg.font.Font("OdeToIdleGamingFont.ttf", 64)

# Frame
frame_final = pg.image.load("frame.png")

"""DEVTOOL
heat = False
"""
# World

class GenerateWorld(object):
    def __init__(self):
        # Draw
        self.world, self.rooms, self.enemies_pos = mg.generateMap(world_size, room_size, (3, 3), True)
        self.pixels = self.world.load()
        self.size = self.world.size
        self.tiles = tiles_all[0][0:4]
        self.enemy = tiles_all[2][0]

        # Tiles Color Code
        self.tile_code = {"(0, 0, 0, 255)": self.tiles[0],         # WALL
                          "(255, 255, 255, 255)": self.tiles[1],   # FLOOR
                          "(0, 0, 255, 255)": self.tiles[2],       # STARTEND
                          "(0, 255, 0, 255)": self.tiles[3],       # GATE
                          "(255, 0, 0, 255)": self.tiles[1]}       # ENEMY/FLOOR
        self.WALL = (0, 0, 0, 255)
        self.FLOOR = (255, 255, 255, 255)
        self.STARTEND = (0, 0, 255, 255)
        self.GATE = (0, 255, 0, 255)
        self.ENEMY = (255, 0, 0, 255)

        # Other
        self.enemies = []
        self.enemies_left = {}

        # Game Over
        self.GO = 0.5  # Seconds
        self.GO_time = time.time()

    def draw(self, x, y):
        # Draw Tiles
        for win_x in range(win_tiles):
            for win_y in range(win_tiles):
                # Wall Boundaries
                if not 0 <= x - win_center + win_x < self.size[0] or not 0 <= y - win_center + win_y < self.size[1]:
                    win.blit(self.tiles[0], (win_x * tile_scale, win_y * tile_scale))
                # Wall in Maze
                else:
                    color_code = str(self.pixels[x - win_center + win_x, y - win_center + win_y])
                    win.blit(self.tile_code[color_code], (win_x * tile_scale, win_y * tile_scale))

        # Draw Entities
        for p in particles[:]:
            p.update()
        for enemy in world.enemies:
            if x - win_center <= enemy.x < x + win_center + 1 and y - win_center <= enemy.y < y + win_center + 1:
                enemy.draw((enemy.x - x + win_center) * tile_scale, (enemy.y - y + win_center) * tile_scale)
        if mip.hp <= 0 and not particles:
            if time.time() - self.GO_time < 1:
                self.GO -= time.time() - self.GO_time
            self.GO_time = time.time()
        if self.GO <= 0:
            global mode
            mode = "GO"


    def openExits(self, x, y): # Open exit of specific room
        room = self.rooms[y][x]
        if not room.open:
            for ex in room.exits:
                area = (room.size[0] // 2 * (1 + ex[0]) - 1 + x * room.size[0],
                        room.size[1] // 2 * (1 + ex[1]) - 1 + y * room.size[1],
                        room.size[0] // 2 * (1 + ex[0]) + 1 + x * room.size[0],
                        room.size[1] // 2 * (1 + ex[1]) + 1 + y * room.size[1])
                self.world.paste(self.FLOOR, area)
            room.open = True


# Player
class player(object):
    def __init__(self, x, y):
        # Traits
        self.start_hp = 15
        self.hp = 15

        # Position
        self.x = x
        self.y = y
        self.room_x = x // room_size[0]
        self.room_y = y // room_size[1]
        self.visited = {}

        # Movement
        self.pressed = {}
        self.counter = 0

        # Draw
        self.standby_fps = 4
        self.standby_time = time.time()
        self.standby_frame = 0
        self.standby_nof = 2
        self.standby = tiles_all[2][0:2]
        self.attack = []
        self.attack_time = time.time()
        self.hp_bar = []
        for img in tiles_all[6][0:2]:
            self.hp_bar.append(pg.transform.scale(img, (int(win_size * 0.60 // self.start_hp), int(win_size * 0.05))))

    def draw(self, x=win_center, y=win_center):
        # Draw Player
        t = time.time() - self.attack_time
        if self.attack and not -1 * t**2 + 0.1*t <= 0 and not mip.hp <= 0:
            d_x = int(self.attack[0] * 3600 * (-1 * t**2 + 0.1*t)) * 2 * scale
            d_y = int(self.attack[1] * 3600 * (-1 * t**2 + 0.1*t)) * 2 * scale
            win.blit(self.standby[self.standby_frame], (d_x + x * tile_scale, d_y + y * tile_scale))
        elif not mip.hp <= 0:
            self.standby_frame = int((time.time() - self.standby_time) * self.standby_fps % self.standby_nof)
            win.blit(self.standby[self.standby_frame], (x * tile_scale, y * tile_scale))
        # Draw Healthbar
        hb_width, hb_height = self.hp_bar[0].get_rect().size
        for d in range(self.start_hp):
            hb_offset = (-hb_width * self.start_hp + win_size) / 2
            win.blit(self.hp_bar[0 if self.hp > d else 1], (d * hb_width + hb_offset, win_size * 0.01))
        # Draw Counter
        counter_text = counter_font.render(str(self.counter), False, (155, 188, 15))
        counter_rect = counter_text.get_rect()
        counter_rect.center = (win_size // 2, 70)
        counter_text_outline = counter_font.render(str(self.counter), False, (15, 56, 15))
        for d_x in range(-1, 2):
            for d_y in range(-1, 2):
                win.blit(counter_text_outline, (counter_rect.x + d_x * 4, counter_rect.y + d_y * 4))
        win.blit(counter_text, counter_rect)

    def action(self, d_x, d_y):
        self.counter += 1
        self.attack = []
        for enemy in world.enemies:
            if [self.x + d_x, self.y + d_y] == [enemy.x, enemy.y]:
                enemy.hp -= 1
                self.attack = [d_x, d_y]
                enemy.attacked = [d_x, d_y]
                self.attack_time = time.time()
                break

        else:
            if world.pixels[self.x + d_x, self.y + d_y] not in [world.WALL, world.GATE]:
                self.x, self.y = self.x + d_x, self.y + d_y

        # Enemies
        world.enemies.sort(key=lambda e: abs(e.x - self.x) + abs(e.y - self.y))
        for enemy in world.enemies:
            enemy.action()

        # Particles
        global area_time
        area_time = time.time()

        # Update room position / Generate enemies
        self.room_x = self.x // room_size[0]
        self.room_y = self.y // room_size[1]

        if str(self.room_x) + str(self.room_y) not in world.enemies_left:
            left = 0
            for e_pos in world.enemies_pos[self.room_y][self.room_x]:
                left += 1
                world.enemies.append(basicEnemy(e_pos[0] + self.room_x * room_size[0],
                                                e_pos[1] + self.room_y * room_size[1]))
            world.enemies_left[str(self.room_x)+str(self.room_y)] = left

    def controls(self):

        if keyPress("K_a"):
            self.action(-1, 0)
        elif keyPress("K_d"):
            self.action(1, 0)
        elif keyPress("K_w"):
            self.action(0, -1)
        elif keyPress("K_s"):
            self.action(0, 1)

            """DEVTOOLS
        elif keyPress("K_k"): # Open exit of first room
            world.openExits(0, 0)
        elif keyPress("K_e"): # Update enemy action with heatmap (move, hurt or die)
            global heat
            heat = True
            for enemy in world.enemies[:]:
                enemy.action()
            heat = False
        elif keyPress("K_p"):
            global p
            particles.append(particle(4, 4))
            """


enemy_area = [[0 for y in range(world_size[1] * room_size[1])] for x in range(world_size[0] * room_size[0])]


def pathFinder(start): # Pathfinding algorithm for enemies (Put in separate file?)
    global enemy_area
    kill = 0 # Killswitch if algorithm is unsuccessful
    used_area = [[0 for y in range(world_size[1] * room_size[1])] for x in range(world_size[0] * room_size[0])]
    used_area[start[0]][start[1]] = 1
    active = []
    history = []
    # Generation of first nodes
    for d_x in range(-1, 2):
        for d_y in range(-1, 2):
            if abs(d_x) == abs(d_y):
                continue
            if world.pixels[start[0] + d_x, start[1] + d_y] == world.WALL:
                continue
            if enemy_area[start[0] + d_x][start[1] + d_y]:
                continue
            used_area[start[0] + d_x][start[1] + d_y] = 1
            active.append([[start[0] + d_x, start[1] + d_y],
                           [d_x, d_y],
                           1,
                           abs(start[0] + d_x - mip.x) + abs(start[1] + d_y - mip.y)
                           ])
    active.sort(key=lambda x: x[3])
    # Beginning of pathfinding
    while active:
        kill += 1
        active_x, active_y = active[0][0][0], active[0][0][1]
        active_d = active[0][1]
        active_g, active_h = active[0][2], active[0][3]
        """DEVTOOLS
        if heat:
            history.append([active_x, active_y]) # History for heatmap
        """
        for d_x in range(-1, 2):
            for d_y in range(-1, 2):

                if abs(d_x) == abs(d_y):  # Ignore corners and center
                    continue

                if [active_x + d_x, active_y + d_y] == [mip.x, mip.y]:  # If player is found
                    """DEVTOOLS
                    if heat:
                        hg.heatMap(history)
                    """
                    if enemy_area[start[0] + active_d[0]][start[1] + active_d[1]]:  # Won't move if enemy is in the way
                        return [0, 0]
                    else:
                        return active_d

                if world.pixels[active_x + d_x, active_y + d_y] == world.WALL:
                    continue
                if used_area[active_x + d_x][active_y + d_y]:
                    continue

                for i, a in enumerate(active):  # Create new node in direction if all above conditions were ignored
                    if a[2] + a[3] >= active_g + 1 + active_h:  # Placing node in the suitable spot
                        try:
                            if a[3] >= abs(active_x + d_x - mip.x) + abs(active_y + d_y - mip.y) \
                                            or a[2] + a[3] != active[i + 1][2] + active[i + 1][3]:
                                active = active[:i] + [[[active_x + d_x, active_y + d_y],
                                                        active_d,
                                                        active_g + 1,
                                                        abs(active_x + d_x - mip.x) + abs(active_y + d_y - mip.y)
                                                        ]] + active[i:]
                                used_area[active_x + d_x][active_y + d_y] = 1
                                break
                        except IndexError:
                            pass
                else:
                    active.append([[active_x + d_x, active_y + d_y],
                                   active_d,
                                   active_g + 1,
                                   abs(active_x + d_x - mip.x) + abs(active_y + d_y - mip.y)])
        active = active[1:]
        if kill == 100:
            break
    return [0, 0]


particles = []


class particle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time = time.time()
        self.nof = 5
        self.fps = 10
        self.frame = 0
        self.frames = tiles_all[5][0:5]

    def update(self):
        if int((time.time() - self.time) * self.fps % (self.nof + 1)) == 5:
            particles.remove(self)
        else:
            self.frame = int((time.time() - self.time) * self.fps % self.nof)
            win_x, win_y = self.x - mip.x + win_center, self.y - mip.y + win_center
            win.blit(self.frames[self.frame], (win_x * tile_scale, win_y * tile_scale))

area_time = time.time()

# Enemy
class basicEnemy(object):
    def __init__(self, x, y):
        global enemy_area
        # Traits
        self.hp_og = 3
        self.hp = 3
        self.b_up = False  # Build up

        # Position
        self.x = x
        self.y = y
        self.tag = str(x // room_size[0]) + str(y // room_size[1])
        enemy_area[x][y] = 1

        # Draw
        self.standby_fps = 4
        self.standby_frame = 0
        self.standby_nof = 2
        self.standby = tiles_all[1][0:2]
        self.hb = tiles_all[3][0:2]
        self.hbo = -25 # Healthbar offset
        self.attacked = []
        self.a_area = tiles_all[4][0:2] # Area area
        self.a_attack = tiles_all[5][0:5] # area Attack

    def action(self):
        global enemy_area
        if self.hp <= 0:
            enemy_area[self.x][self.y] = 0
            world.enemies_left[self.tag] -= 1
            if world.enemies_left[self.tag] == 0:
                world.openExits(int(self.tag[0]), int(self.tag[1]))
            world.enemies.remove(self)

        if abs(mip.x - self.x) + abs(mip.y - self.y) == 1 or self.b_up:
            if self.b_up:
                if abs(mip.x - self.x) + abs(mip.y - self.y) == 1:
                    mip.hp -= 1
                self.b_up = False
                for d_x in range(-1, 2):
                    for d_y in range(-1, 2):
                        if abs(d_x) == abs(d_y):
                            continue
                        if world.pixels[self.x + d_x, self.y + d_y] in [world.WALL, world.GATE] \
                                or enemy_area[self.x + d_x][self.y + d_y]:
                            continue
                        particles.append(particle(self.x + d_x, self.y + d_y))
            else:
                self.b_up = True
        else:
            global takenCells
            takenCells = []
            d_x, d_y = pathFinder([self.x, self.y])
            enemy_area[self.x][self.y] = 0
            self.x, self.y = self.x + d_x, self.y + d_y
            enemy_area[self.x][self.y] = 1

    def draw(self, pos_x, pos_y):
        # Enemy
        t = time.time() - mip.attack_time
        if self.attacked and not -1 * t ** 2 + 0.1 * t <= 0:
            d_x = int(self.attacked[0] * 250 * (-1 * t ** 2 + 0.2 * t)) * 2 * scale
            d_y = int(self.attacked[1] * 250 * (-1 * t ** 2 + 0.2 * t)) * 2 * scale
            win.blit(self.standby[self.standby_frame], (d_x + pos_x, d_y + pos_y))
        else:
            self.attacked = []
            self.standby_frame = int((time.time() - mip.standby_time) * self.standby_fps % self.standby_nof)
            win.blit(self.standby[self.standby_frame], (pos_x, pos_y))
        # Healthbar
        hb_size = self.hb[0].get_rect().size[0] * self.hp / self.hp_og
        d_hbo = int((time.time() - mip.standby_time) * 2 % 2)
        win.blit(self.hb[1], (pos_x, pos_y + self.hbo + d_hbo))
        win.blit(self.hb[0], (pos_x, pos_y + self.hbo + d_hbo), pg.Rect(0, 0, hb_size, self.hb[0].get_rect().size[1]))
        # Area
        if self.b_up:
            for d_x in range(-1, 2):
                for d_y in range(-1, 2):
                    if abs(d_x) == abs(d_y):
                        continue
                    if world.pixels[self.x + d_x, self.y + d_y] == world.WALL:
                        continue
                    if enemy_area[self.x + d_x][self.y + d_y]:
                        continue
                    area_frame = int((time.time() - area_time) * 3 % 2)
                    win.blit(self.a_area[area_frame], (pos_x + d_x * tile_scale, pos_y + d_y * tile_scale))


# Input
pressed = {}
def keyPress(k):
    global pressed
    keys = pg.key.get_pressed()

    """\/REMOVE WHEN KEYMAPPING IS FINISHED\/"""
    if k not in pressed:
        pressed[k] = False
    """^"""

    # Update the state of all unpressed keys
    for key in pressed:
        if not eval("keys[pg." + key + "]"):
            pressed[key] = False

    # Check if pressed key was previously pressed
    if eval("keys[pg." + k + "]"):
        if not pressed[k]:
            pressed[k] = True
            return True

    return False

# Buttons

class button(object):
    def __init__(self, imgs, x, y, code):
        global menu, run
        self.imgs = imgs
        self.x = x
        self.y = y
        self.code = code
        self.hover = False
        self.click = False

    def update(self, event):
        if (self.imgs[0]).get_rect(topleft=(self.x, self.y)).collidepoint(pg.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hover:
                    self.click = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.click and self.hover:
                self.click = False
                exec(self.code, globals())

    def draw(self):
        if self.hover:
            if self.click:
                win.blit(self.imgs[2], (self.x, self.y))
            else:
                win.blit(self.imgs[1], (self.x, self.y))
        else:
            win.blit(self.imgs[0], (self.x, self.y))



buttons = [button([pg.image.load("menu_imgs/Start.png"), pg.image.load("menu_imgs/StartHover.png"),
                   pg.image.load("menu_imgs/StartClick.png")],
                  232, 441, "if True : menu, mode, mode_new = False, 'G', True"),
           button([pg.image.load("menu_imgs/Exit.png"), pg.image.load("menu_imgs/ExitHover.png"),
                   pg.image.load("menu_imgs/ExitClick.png")],
                  232, 563, "if True : menu, run = False, False")
           ]


# Grouping
def allControls():
    mip.controls()


def updateWin():
    # Map
    world.draw(mip.x, mip.y)
    # Player / Statistics
    mip.draw()
    # Estetic
    win.blit(frame_final, (0, 0))


    pg.display.update()


# menu_imgs
menu_imgs = [pg.image.load("menu_imgs/Startmenu.png"),
        [pg.image.load("menu_imgs/Start.png"), pg.image.load("menu_imgs/StartHover.png"), pg.image.load("menu_imgs/StartClick.png")],
        [pg.image.load("menu_imgs/Exit.png"), pg.image.load("menu_imgs/ExitHover.png"), pg.image.load("menu_imgs/ExitClick.png")]]

run = True
menu = True

while menu:
    win.blit(menu_imgs[0], (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            menu, run = False, False
        else:
            for b in buttons:
                b.update(event)
    for b in buttons:
        b.draw()


    pg.display.update()
# Startup
def GameInit():
    global mip, world, particles, enemy_area, clock
    if run:
        mip = player(1, 1)
        world = GenerateWorld()
        particles = []
        enemy_area = [[0 for y in range(world_size[1] * room_size[1])] for x in range(world_size[0] * room_size[0])]
        clock = pg.time.Clock()

# Game
def Game():
    global run
    if not mip.hp <= 0:
        allControls()
    updateWin()

    if [mip.x, mip.y] == [world.size[0] - 3, world.size[1] - 3]:
        global mode
        mode = "C"

# GameOver
go_img = pg.image.load("menu_imgs/GameOver.png")
def GameOver():
    global run
    win.blit(go_img, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        else:
            for b in buttons:
                b.update(event)
    for b in buttons:
        b.draw()

    counter_text = counter_font_menu.render(": " + str(mip.counter) + "p :", False, (155, 188, 15))
    counter_rect = counter_text.get_rect()
    counter_rect.center = (win_size // 2, win_size // 2 - 20)
    counter_text_outline = counter_font_menu.render(": " + str(mip.counter) + "p :", False, (15, 56, 15))
    for d_x in range(-1, 2):
        for d_y in range(-1, 2):
            win.blit(counter_text_outline, (counter_rect.x + d_x * 8, counter_rect.y + d_y * 8))
    win.blit(counter_text, counter_rect)

    pg.display.update()

# MazeCompleted
c_img = pg.image.load("menu_imgs/Completed.png")
def Completed():
    global run
    win.blit(c_img, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        else:
            for b in buttons:
                b.update(event)
    for b in buttons:
        b.draw()

    counter_text = counter_font_menu.render(": " + str(mip.counter) + "p :", False, (155, 188, 15))
    counter_rect = counter_text.get_rect()
    counter_rect.center = (win_size // 2, win_size // 2 - 20)
    counter_text_outline = counter_font_menu.render(": " + str(mip.counter) + "p :", False, (15, 56, 15))
    for d_x in range(-1, 2):
        for d_y in range(-1, 2):
            win.blit(counter_text_outline, (counter_rect.x + d_x * 8, counter_rect.y + d_y * 8))
    win.blit(counter_text, counter_rect)

    pg.display.update()

modes = {"G": ["GameInit()", "Game()"],
         "GO": ["()", "GameOver()"],
         "C": ["()", "Completed()"]}
mode = "G"
mode_new = True

while run:
    if mode_new:
        eval(modes[mode][0])
        mode_new = False

    eval(modes[mode][1])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

pg.quit()
