import pyray as pr
import os
#> textures
Wall_texture = None
Vent_texture = None
Point_texture = None
PLayer_texture = None
Enemy_texture = None
Heart_texture = None
Atack_texture = None
Heal_texture = None
bg_menu_texture = None
Imgs = [Wall_texture , Vent_texture , Point_texture, PLayer_texture , Enemy_texture , Heart_texture , Atack_texture , Heal_texture , bg_menu_texture]
#>audio
select_audio = None
data_audio = None
game_over_audio = None
sounds = [select_audio , data_audio , game_over_audio]
#>music
menu_theme = None
game_theme = None
music = [menu_theme , game_theme]

def load_textures():
    global Wall_texture, Vent_texture , Point_texture , PLayer_texture , Enemy_texture , Heart_texture , Atack_texture , Heal_texture , Imgs , bg_menu_texture
    Imgs = [Wall_texture, Vent_texture, Point_texture, PLayer_texture,
            Enemy_texture, Heart_texture, Atack_texture, Heal_texture , bg_menu_texture]
    base_path = os.path.join(os.path.dirname(__file__), "Source")
    Wall_texture = pr.load_texture(os.path.join(base_path, "wall.png"))
    Heart_texture = pr.load_texture(os.path.join(base_path, "Heart.png"))
    PLayer_texture = pr.load_texture(os.path.join(base_path, "Player.png"))
    Vent_texture = pr.load_texture(os.path.join(base_path, "vent.png"))
    Point_texture = pr.load_texture(os.path.join(base_path, "point.png"))
    Enemy_texture = pr.load_texture(os.path.join(base_path, "Enemy.png"))
    Atack_texture = pr.load_texture(os.path.join(base_path, "atack.png"))
    Heal_texture = pr.load_texture(os.path.join(base_path, "Heal.png"))
    bg_menu_texture =  pr.load_texture(os.path.join(base_path, "bg_menu.png"))

def load_sounds():
    global select_audio ,sounds , data_audio, game_over_audio
    sounds = [select_audio , data_audio , game_over_audio]
    base_path = os.path.join(os.path.dirname(__file__), "sounds")
    select_audio = pr.load_sound(os.path.join(base_path, "Blip.wav"))
    data_audio = pr.load_sound(os.path.join(base_path, "data.wav"))
    game_over_audio = pr.load_sound(os.path.join(base_path, "game_over.wav"))
def load_music():
    global menu_theme , music , game_theme
    music = [menu_theme , game_theme]
    base_path = os.path.join(os.path.dirname(__file__), "music")
    menu_theme =pr.load_music_stream(os.path.join(base_path, "Here start your hell!.wav"))
    game_theme = pr.load_music_stream(os.path.join(base_path, "heeeeeeeeeel yeah!.wav"))

def unload():
    global Imgs, sounds , music
    for music in music:
        if music is not None:
            pr.unload_texture(music)
    for texture in Imgs:
        if texture is not None:
            pr.unload_texture(texture)
    for sound in sounds:
        if sound is not None:
            pr.unload_sound(sound)
    print("data unloaded succesfully")