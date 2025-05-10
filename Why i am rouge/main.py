#---------------------------------> importing
from time import sleep , time
import pyray as pr
import Scripts.world as wr
import Scripts.DATA as DT
import Scripts.SceneManager as SM
import Scripts.Loader as Load
from numpy import sin , cos
import sys

#--------------------------------->bools
#>window
Wx = 900
Wy = 900
Wn = b"Why am I rogue?"
Wfps = 25

#>menu states
IsInMainMenu = True
IsInIntro = False
IsDead = False
IsInPause = False

#>music states
IsMenuMusicPlaying = False
IsGameMusicPlaying = False

#>timer
Timer = None
elapsed_time = None

#--------------------------------->functions
def force_generate_lvl():
    wr.regenerate_world()
    print("generating lvl")

def restart():
    global IsDead , IsInMainMenu , IsInPause , Timer , elapsed_time , IsGameMusicPlaying
    DT.Phealt = 10
    DT.Pscore = 0
    DT.Cscene = 1
    Timer = None
    elapsed_time = 0
    SM.completed = False
    force_generate_lvl()
    IsDead = False
    IsInMainMenu = True
    IsInPause = False
    IsGameMusicPlaying = False

def exit():
    pr.stop_music_stream(Load.game_theme)
    Load.unload()
    pr.close_audio_device()
    pr.close_window()
    sys.exit(0)



#--------------------------------->UI
def draw_debug_ui():
    global Wx , Wy
    if pr.is_key_down(pr.KeyboardKey.KEY_TAB):
        pr.draw_rectangle(5, 10, 400, 200, pr.fade(pr.BLACK, 0.9))
        pr.draw_text("###DEBUG MODE###", 10, 20, 30, pr.WHITE)
        pr.draw_text("FPS : " + str(pr.get_fps()) + f"/ {Wfps}", 10, 50, 20, pr.WHITE)
        pr.draw_text(f"player pos : {wr.find_player()} " , 170 , 50, 20, pr.WHITE)
        pr.draw_text("Level : " + str(DT.Cscene) + f"/ {SM.MAX_SCENE}", 10, 70, 20, pr.WHITE)
    if pr.is_key_down(pr.KeyboardKey.KEY_SEVEN):
        wr.debug = True
    else:
        wr.debug = False
def draw_load_ui():
    pr.draw_text("Loading...", 10, 20, 40, pr.WHITE)
    pr.draw_text(f"step :{wr.generation_step} / completed : {wr.generation_complete} ", 10, 60, 20, pr.WHITE)
    pr.draw_text("please wait...", Wx // 2, Wy // 2, 40, pr.WHITE)
import random

def draw_player_ui():
    global Wy
    pr.draw_text("#INFO#", 10, Wy // 2 + 120 , 40, pr.WHITE)
    pr.draw_text(f"DATA was stolen GB : {DT.Pscore}", 10, Wy // 2 + 160, 20, pr.WHITE)
    pr.draw_text("SPACE to destroy defenders", 10 + 500, Wy // 2 + 160, 20, pr.WHITE)
    pr.draw_text("P to PAUSE", 10 + 500, Wy // 2 + 190, 20, pr.WHITE)
    pr.draw_text(f"current security LEVEL at server no. : {DT.Cscene}", 10, Wy // 2 + 190, 20, pr.WHITE)
    pr.draw_text(f"restart will cost 20 GB of DATA press 7", 10, Wy // 2 + 220, 20, pr.WHITE)

    max_health = max(1, 10)

    for i in range(int(DT.Phealt) + 1):
        shake_strength = max(0, (5 - (DT.Phealt / max_health) * 5))
        offset_x = random.randint(int(-shake_strength), int(shake_strength))
        offset_y = random.randint(int(-shake_strength), int(shake_strength))
        pos_x = 10 + i * (Load.Heart_texture.width - 10) + offset_x
        pos_y = Wy - 200 + offset_y
        pr.draw_texture_ex(Load.Heart_texture, pr.Vector2(pos_x, pos_y), 0, 1, pr.WHITE)


#--------------------------------->main
#>init window
pr.init_window(Wx, Wy, Wn)
pr.init_audio_device()
pr.set_target_fps(Wfps)
Load.load_textures()
Load.load_sounds()
Load.load_music()
wr.initialize_map()


#>game cycle
while not pr.window_should_close():
    pr.clear_background(pr.BLACK)

    # > controls
    if not IsInMainMenu and not IsDead and not IsInPause:
        if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
            wr.attack_player()

        if pr.is_key_down(pr.KeyboardKey.KEY_W):
            wr.move_up()
        if pr.is_key_down(pr.KeyboardKey.KEY_S):
            wr.move_down()
        if pr.is_key_down(pr.KeyboardKey.KEY_A):
            wr.move_left()
        if pr.is_key_down(pr.KeyboardKey.KEY_D):
            wr.move_right()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_P):
            IsInPause = not IsInPause

        # >debug controls
        if pr.is_key_down(pr.KeyboardKey.KEY_SEVEN):
            force_generate_lvl()
            DT.Pscore -= 20
            sleep(1)
        if pr.is_key_down(pr.KeyboardKey.KEY_EIGHT):
            wr.debug = True
        else:
            wr.debug = False
        if pr.is_key_down(pr.KeyboardKey.KEY_NINE):
            DT.Phealt += 10
        if pr.is_key_down(pr.KeyboardKey.KEY_SIX):
            DT.Pscore += 10




    pr.begin_drawing()

    # > menu draw
    if IsInMainMenu:
        if not IsInIntro:
            if IsInMainMenu:
                pr.update_music_stream(Load.menu_theme)

                if not IsInIntro:
                    if not IsMenuMusicPlaying:
                        pr.play_music_stream(Load.menu_theme)
                        IsMenuMusicPlaying = True

            bg_color = pr.Color(255, 255, 255, 90)
            texture = Load.bg_menu_texture
            scale_x = Wx / texture.width
            scale_y = Wy / texture.height
            pr.draw_texture_ex(texture, pr.Vector2(0, 0), 0.0, scale_x, bg_color)
            pr.draw_text("originally developed by : Porko (Y. K.)", 10, 20, 20, pr.WHITE)
            t = pr.get_time()
            red_value = int(127 + 127 * sin(t))
            color = pr.Color(red_value, 225, 225, 255)
            shake_x = int(3 * sin(t * 2))
            shake_y = int(3 * cos(t * 3))

            title_text = "WHY I AM ROUGE?"
            title_font_size = 60
            title_y = Wy // 2
            title_height = title_font_size

            pr.draw_text(title_text, 10 + shake_x, title_y, title_font_size, color)

            spacing = 10
            pr.draw_text("[SPACE] to start the game", 10, title_y + title_height + spacing, 40, pr.WHITE)
            pr.draw_text("[ESC] to exit the game", 10, title_y + title_height + spacing + 50, 40, pr.RED)

            if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
                pr.play_sound(Load.select_audio)
                pr.stop_music_stream(Load.menu_theme)
                IsMenuMusicPlaying = False
                IsInIntro = True

        else:
            pr.draw_text("Year 2035", 10, Wy // 2, 40, pr.WHITE)
            pr.draw_text("You are a Ukrainian hacker who hacks a", 12, Wy // 2 + 40, 40, pr.WHITE)
            pr.draw_text("Russian server with national secrets.", 12, Wy // 2 + 80, 40, pr.WHITE)
            pr.draw_text("[Press W to continue]", 10, Wy // 2 + 120, 20, pr.WHITE)

            if pr.is_key_down(pr.KeyboardKey.KEY_W):
                IsInMainMenu = False
                IsInIntro = False

        if pr.is_key_down(pr.KeyboardKey.KEY_ESCAPE):
            exit()

    elif IsDead:
        t = pr.get_time()
        red_value = int(127 + 127 * sin(t))
        color = pr.Color(red_value, 0, 0, 255)
        shake_x = int(3 * sin(t * 10))
        shake_y = int(3 * cos(t * 8))
        pr.draw_text("GAME OVER", Wx // 2 + shake_x, Wy // 2 + shake_y, 60, color)
        pr.draw_text("You were found.", Wx // 2, Wy // 2 + 90, 40, pr.WHITE)
        pr.draw_text("Statistics", 10, Wy // 2 + 120, 40, pr.WHITE)
        pr.draw_text(f"Score : {DT.Pscore}", 10, Wy // 2 + 160, 20, pr.WHITE)
        pr.draw_text(f"Level : {DT.Cscene}", 10, Wy // 2 + 190, 20, pr.WHITE)
        pr.draw_text("Press [W] to restart", 10, Wy // 2 + 230, 20, pr.WHITE)

        if pr.is_key_down(pr.KeyboardKey.KEY_W):
            pr.play_sound(Load.game_over_audio)
            restart()


    else:
        SM.handle()
        if SM.completed == True:
            t = pr.get_time()
            r = int(200 + 55 * sin(t * 2))
            g = int(200 + 55 * sin(t * 2 + 1))
            color = pr.Color(r, g, 0, 255)

            shake_x = int(3 * sin(t * 8))
            shake_y = int(3 * cos(t * 6))
            pr.draw_text("you are victorious", Wx // 2 + shake_x - 190, Wy // 2 + shake_y, 60, color)

            pr.draw_text("Good work!", Wx // 2, Wy // 2 + 90, 40, pr.WHITE)
            pr.draw_text("Statistics", 10, Wy // 2 + 120, 40, pr.WHITE)
            pr.draw_text(f"Score : {DT.Pscore}", 10, Wy // 2 + 160, 20, pr.WHITE)
            pr.draw_text(f"Level : {DT.Cscene}", 10, Wy // 2 + 190, 20, pr.WHITE)
            pr.draw_text(f"time : {elapsed_time}", 10, Wy // 2 + 230, 20, pr.WHITE)
            pr.draw_text("press [space] to continue", 10, Wy // 2 + 250, 20, pr.WHITE)

            if pr.is_key_down(pr.KeyboardKey.KEY_SPACE):
                restart()

        if DT.Phealt <= 0:
            IsDead = True
        if wr.generation_complete and not IsInPause and not SM.completed:
            if Timer == None:
                Timer = time()
            elapsed_time = time() - Timer
            wr.draw()
            wr.update_enemies()
            draw_debug_ui()
            draw_player_ui()
            if not IsGameMusicPlaying:
                pr.stop_music_stream(Load.menu_theme)
                pr.play_music_stream(Load.game_theme)
                IsGameMusicPlaying = True
            pr.update_music_stream(Load.game_theme)
        elif IsInPause and not SM.completed:
            pr.draw_text("###PAUSE MENU###", 10, 20, 40, pr.WHITE)
            pr.draw_text("press [P] to return", 10, 65, 20, pr.WHITE)
            pr.draw_text("press [R] to restart game", 10, 90, 20, pr.WHITE)
            pr.draw_text("press [E] to exit", 10, 120, 20, pr.RED)
            if pr.is_key_down(pr.KeyboardKey.KEY_R):
                restart()
            if pr.is_key_down(pr.KeyboardKey.KEY_E):
                exit()


        else:
            if not SM.completed:
                draw_load_ui()


    pr.end_drawing()

exit()