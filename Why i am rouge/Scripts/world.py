from random import randint

import pyray as pr
import random
import Scripts.DATA as DATA
import Scripts.Loader as Load

cell_size = 35
debug = True
screen_width = 800
screen_height = 600
map_width = int(screen_width // cell_size * 1.2)
map_height = int(screen_height // cell_size * 0.9)

generation_step = 0
generation_complete = False
enemy_attack_timer = 0
enemy_attack_delay = 1000



Map = []
enemies = []
last_direction = "down"

Room_spawn = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 1, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
]
Room_end = [
    [2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 5, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
]

Room_1 = [
    [2, 2, 2, 3, 3, 3, 2, 2],
    [3, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
]

Room_2 = [
    [2, 2, 2, 3, 3, 3, 2, 2],
    [3, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 2, 2, 2, 0, 0, 3],
    [3, 0, 2, 2, 2, 0, 0, 3],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
]

rooms = [Room_1, Room_2]

def initialize_map():
    global Map
    Map = [[0 for _ in range(map_width)] for _ in range(map_height)]
    for y in range(map_height):
        for x in range(map_width):
            if x == 0 or x == map_width - 1 or y == 0 or y == map_height - 1:
                Map[y][x] = 2

def spawn_items(amount=10):
    count = 0
    while count < amount:
        x = random.randint(1, map_width - 2)
        y = random.randint(1, map_height - 2)
        if Map[y][x] == 0:
            Map[y][x] = 4
            count += 1
def spawn_Heal(amount=5):
    count = 0
    while count < amount:
        x = random.randint(1, map_width - 2)
        y = random.randint(1, map_height - 2)
        if Map[y][x] == 0:
            Map[y][x] = 7
            count += 1


def spawn_enemies(amount=5):
    global enemies
    enemies.clear()
    count = 0
    while count < amount:
        x = random.randint(1, map_width - 2)
        y = random.randint(1, map_height - 2)


        if Map[y][x] == 0 and not is_in_player_room(x, y):
            Map[y][x] = 6
            enemies.append((x, y))
            count += 1


def is_in_player_room(x, y):
    room_width = len(Room_spawn[0])
    room_height = len(Room_spawn)

    room_x_start = spawn_col * room_width + 1
    room_y_start = spawn_row * room_height + 1
    room_x_end = room_x_start + room_width
    room_y_end = room_y_start + room_height

    return room_x_start <= x < room_x_end and room_y_start <= y < room_y_end


def can_enemy_see_player(ex, ey):
    px, py = find_player()
    if ex == px:
        step = 1 if py > ey else -1
        for y in range(ey + step, py, step):
            if Map[y][ex] in (2, 3): return False
        return True
    elif ey == py:
        step = 1 if px > ex else -1
        for x in range(ex + step, px, step):
            if Map[ey][x] in (2, 3): return False
        return True
    return False


def update_enemies():
    global enemies, enemy_attack_timer
    px, py = find_player()
    new_enemies = []


    enemy_attack_timer += 1


    enemy_damage_multiplier = 1

    for ex, ey in enemies:
        if can_enemy_see_player(ex, ey):
            dx = 1 if px > ex else -1 if px < ex else 0
            dy = 1 if py > ey else -1 if py < ey else 0
            new_x, new_y = ex + dx, ey + dy

            if enemy_attack_timer >= enemy_attack_delay:

                if Map[new_y][new_x] == 1:
                    DATA.Phealt = max(0, DATA.Phealt - 1 * enemy_damage_multiplier)
                    enemy_attack_timer = 0

            if 0 <= new_x < map_width and 0 <= new_y < map_height:
                if Map[new_y][new_x] == 1:
                    DATA.Phealt = max(0, DATA.Phealt - 1 * enemy_damage_multiplier)
                    enemy_attack_timer = 0
                elif Map[new_y][new_x] == 0:
                    Map[ey][ex] = 0
                    Map[new_y][new_x] = 6
                    new_enemies.append((new_x, new_y))
                    continue
        new_enemies.append((ex, ey))
    enemies = new_enemies


def attack_player():
    global enemies
    x, y = find_player()
    if x is None or y is None:
        return

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            tx, ty = x + dx, y + dy
            if 0 <= tx < map_width and 0 <= ty < map_height:
                if Map[ty][tx] == 6:
                    Map[ty][tx] = 0
                    if (tx, ty) in enemies:
                        enemies.remove((tx, ty))
                    DATA.Pscore += randint(1, 5)

                    scale = cell_size / Load.Atack_texture.height if Load.Atack_texture.height != 0 else 1
                    pr.draw_texture_ex(
                        Load.Atack_texture,
                        pr.Vector2(tx * cell_size, ty * cell_size),
                        0,
                        scale,
                        pr.WHITE
                    )


def place_room(room, x, y):
    for row in range(len(room)):
        for col in range(len(room[0])):
            if 0 <= y + row < map_height and 0 <= x + col < map_width:
                Map[y + row][x + col] = room[row][col]

def can_place_room(room, x, y):
    for row in range(len(room)):
        for col in range(len(room[0])):
            map_y = y + row
            map_x = x + col
            if 0 <= map_y < map_height and 0 <= map_x < map_width:
                if Map[map_y][map_x] not in (0, 4): return False
            else:
                return False
    return True

def generate_rooms():
    global Map, generation_step, generation_complete
    if generation_complete: return False
    room_height = len(Room_1)
    room_width = len(Room_1[0])
    grid_cols = (map_width - 2) // room_width
    grid_rows = (map_height - 2) // room_height
    if generation_step == 0:
        initialize_map()
        global spawn_col, spawn_row, end_col, end_row
        spawn_col = random.randint(0, grid_cols - 1)
        spawn_row = random.randint(0, grid_rows - 1)
        while True:
            end_col = random.randint(0, grid_cols - 1)
            end_row = random.randint(0, grid_rows - 1)
            if (end_col, end_row) != (spawn_col, spawn_row): break
        generation_step += 1
        return True
    row = (generation_step - 1) // grid_cols
    col = (generation_step - 1) % grid_cols
    if row >= grid_rows:
        generation_complete = True
        return False
    x = 1 + col * room_width
    y = 1 + row * room_height
    if row == spawn_row and col == spawn_col:
        if can_place_room(Room_spawn, x, y): place_room(Room_spawn, x, y)
    elif row == end_row and col == end_col:
        if can_place_room(Room_end, x, y): place_room(Room_end, x, y)
    else:
        room = random.choice(rooms)
        if can_place_room(room, x, y): place_room(room, x, y)
    generation_step += 1
    return True

def draw():
    for y in range(map_height):
        for x in range(map_width):
            tile = Map[y][x]
            pos_x = x * cell_size
            pos_y = y * cell_size
            if tile == 2:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.Wall_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 4:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.Point_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 5:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.Vent_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 1:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.PLayer_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 6:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.Enemy_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 7:
                scale = cell_size / Load.Wall_texture.height if Load.Wall_texture.height != 0 else 1
                pr.draw_texture_ex(Load.Heal_texture, pr.Vector2(pos_x, pos_y), 0, scale, pr.WHITE)
            elif tile == 0:
                pr.draw_rectangle(pos_x, pos_y, cell_size, cell_size, pr.BLACK)
            if debug:
                pr.draw_rectangle_lines(pos_x, pos_y, cell_size, cell_size, pr.DARKGRAY)

def regenerate_world():
    global generation_step, generation_complete
    generation_step = 0
    generation_complete = False
    initialize_map()
    while generate_rooms(): pass
    spawn_items(randint(2, 10 * DATA.Cscene))
    spawn_Heal(randint(1 , 20 ) // DATA.Phealt)
    spawn_enemies(randint(3, 5 + DATA.Cscene))

def find_player():
    for y in range(map_height):
        for x in range(map_width):
            if Map[y][x] == 1: return x, y
    return None, None

def move_left():
    global last_direction
    last_direction = "left"
    x, y = find_player()
    if x is not None and x > 0 and Map[y][x - 1] != 2:
        if Map[y][x - 1] == 4:
            DATA.Pscore += randint(1, 3)
            pr.play_sound(Load.data_audio)
        if Map[y][x - 1] == 7:
            DATA.Phealt += randint(1, 3)
        elif Map[y][x - 1] == 5: DATA.on_player_reach_end()
        Map[y][x] = 0
        Map[y][x - 1] = 1

def move_right():
    global last_direction
    last_direction = "right"
    x, y = find_player()
    if x is not None and x < map_width - 1 and Map[y][x + 1] != 2:
        if Map[y][x + 1] == 4:
            DATA.Pscore += randint(1, 3)
            pr.play_sound(Load.data_audio)
        elif Map[y][x + 1] == 7:
            DATA.Phealt += randint(1, 3)
        elif Map[y][x + 1] == 5: DATA.on_player_reach_end()
        Map[y][x] = 0
        Map[y][x + 1] = 1

def move_up():
    global last_direction
    last_direction = "up"
    x, y = find_player()
    if y is not None and y > 0 and Map[y - 1][x] != 2:
        if Map[y - 1][x] == 4:
            DATA.Pscore += randint(1, 3)
            pr.play_sound(Load.data_audio)
        elif Map[y - 1][x] == 7:
            DATA.Phealt += randint(1, 3)
        elif Map[y - 1][x] == 5: DATA.on_player_reach_end()
        Map[y][x] = 0
        Map[y - 1][x] = 1

def move_down():
    global last_direction
    last_direction = "down"
    x, y = find_player()
    if y is not None and y < map_height - 1 and Map[y + 1][x] != 2:
        if Map[y + 1][x] == 4:
            DATA.Pscore += randint(1, 3)
            pr.play_sound(Load.data_audio)
        elif Map[y + 1][x] == 7:
            DATA.Phealt += randint(1, 3)
        elif Map[y + 1][x] == 5: DATA.on_player_reach_end()
        Map[y][x] = 0
        Map[y + 1][x] = 1