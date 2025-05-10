import Scripts.world as wr
import Scripts.DATA as dt
import random
completed = False

MAX_SCENE = random.randint(5, 10)

called_scenes = set()

def handle():
    if dt.Cscene <= MAX_SCENE and dt.Cscene not in called_scenes:
        wr.regenerate_world()
        called_scenes.add(dt.Cscene)

def next_scene():
    global completed
    if dt.Cscene < MAX_SCENE:
        dt.Cscene += 1
    else:
        completed = True

