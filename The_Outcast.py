# The Outcast | Sharjeel Mustafa
# ------------------------------------------------------------------------

from pygame import *
from math import *
from random import *
import pygame

# Global Variables
# ------------------------------------------------------------------------

# Contains data such as game stage, coins, item types, etc.
# Used for determining other parts of the game and/or as a save string.

# Game_Stage, Level, Platform_mechanics, Player_x, Player_y, back_point, player_health
Game_Data = ['null', 'level_1', False, 0, 0, 'null', 100, 600]

# Classes & Functions
# ----------------------------------------------------------------------------------------------------------------


'''
Short explanation of the class structuring. The code is broken based
on if it a specific area, event, or background structure.
Example, there are two physics classes, one for the "3d" world and the 
other for the "2d" platform. The sound class deals with all the music 
and storage of sound. This class is called on by other classes, as
depending on different game stages different sounds/music is played. 
'''

'''
In this class all sounds are stored per each stage. Depending on the stage a function may activate
the Sound Class and change the music. Any class that switches music calls this class.
'''


class SoundEngine:

    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        self.initialize_music = True
        # pygame.mixer_music.set_volume(0)

    def background_music(self):
        global Game_Data

        if Game_Data[0] == 'null' and self.initialize_music:
            pygame.mixer.music.load('Audio/Music/Music_1.mp3')
            pygame.mixer.music.play(-1)
            self.initialize_music = False

        elif Game_Data[0] == 'play' and self.initialize_music:
            pygame.mixer_music.stop()
            pygame.mixer.music.load('Audio/Music/Music_10.mp3')
            pygame.mixer.music.play(-1)
            self.initialize_music = False

        elif Game_Data[1] == 'boss' and self.initialize_music:
            if Game_Data[7] < 300:
                pygame.mixer_music.stop()
                pygame.mixer.music.load('Audio/Music/Music_9.mp3')
                pygame.mixer.music.play(-1)
                self.initialize_music = False
            else:
                pygame.mixer_music.stop()
                pygame.mixer.music.load('Audio/Music/Music_6.mp3')
                pygame.mixer.music.play(-1)
                self.initialize_music = False

        elif Game_Data[0] == 'castle' and self.initialize_music:
            pygame.mixer_music.stop()
            pygame.mixer.music.load('Audio/Music/Music_7.mp3')
            pygame.mixer.music.play(-1)
            self.initialize_music = False


# ----------------------------------------------------------------------------------------------------------------

'''
In this class all the menus are generated. First all the images are initialized. If the images are of a set than
they are kept together. The game data is acting as a switch between all functions.

'''


class UserInterface(SoundEngine):
    # --------------------------------------------------------------------
    def __init__(self):
        self.gui_images = []

        # Other menu screens
        self.instructions = image.load('Interface/GUI/Instructions.png')
        self.instructions = transform.scale(self.instructions, (1280, 720))
        self.credits = image.load('Interface/GUI/credits.png')
        self.credits = transform.scale(self.credits, (1280, 720))

        self.game_over_image = image.load('Interface/GUI/Game_Over.png')
        self.game_over_image = transform.scale(self.game_over_image, (1280, 720))
        self.you_win_image = image.load('Interface/GUI/You_Win.png')
        self.you_win_image = transform.scale(self.you_win_image, (1280, 720))
        self.story_image = image.load('Interface/GUI/Story.png')
        self.story_image = transform.scale(self.story_image, (1280, 720))
        '''
        The code here adds in little features for the window such as a name and icon works on mac, not sure how well it
        will work on Windows.
        '''
        # Game window
        icon = image.load('Interface/GUI/Icons/Icon_4.png')
        pygame.display.set_caption('The Outcast')
        pygame.display.set_icon(icon)
        '''
        Initialize font for usage
        '''
        # Font
        pygame.font.init()
        game_font = font.SysFont("Times New Roman", 100)

        '''
        At first I was going to generate the menus in game, but that would make the code very bloated so I ended
        up pre making the menus which would be generated on the screen.
        '''
        # Pause set up
        self.pause_text = game_font.render('Paused', True, (0, 0, 0))
        self.pre_pause = 'null'
        # -------------------------------------------------
        for i in range(35):  # Frames in a sequence
            ui_graphics = image.load('Interface/Graphics/Image_' + str(i) + '.png')
            self.gui_images.append(ui_graphics)

        self.gui_images[17] = transform.scale(self.gui_images[17], (200, 100))
        self.gui_images[28] = transform.scale(self.gui_images[28], (500, 300))

    # --------------------------------------------------------------------
    def title_screen(self, screen, mouse_x, mouse_y, mouse_b, sound_class):
        global Game_Data
        '''
        Cycles through all options and when a collision is made it will detect and alter the Game data
        accordingly. This will than move the game forward.
        
        '''
        menu_items = ['play', 'instructions', 'credits']
        menu_background = image.load('Interface/GUI/Title_Screen/Menu.png')
        menu_background = transform.smoothscale(menu_background, (1280, 720))
        title = image.load('Interface/GUI/Title_Screen/Title.png')

        # -------------------------------------------------
        screen.blit(menu_background, (0, 0))
        screen.blit(title, (400, 220))
        title_screen_buttons = []

        # -------------------------------------------------
        for i in range(1, 4):
            subtitle = image.load('Interface/GUI/Title_Screen/Image_' + str(i) + '.png')
            subtitle_pressed = image.load('Interface/GUI/Title_Screen/Image_' + str(i) + '_P.png')

            hit_box = Rect((540, 320 + i * 60, 200, 50))
            option = []
            option.extend([subtitle, subtitle_pressed, hit_box])
            title_screen_buttons.append(option)

        for i in range(3):
            if title_screen_buttons[i][2].collidepoint(mouse_x, mouse_y) and mouse_b[0] == 1:
                Game_Data[0] = menu_items[i]
                if menu_items[i] == 'play':
                    pygame.mixer_music.stop()
                    sound_class.initialize_music = True
                    Game_Data[5] = 'play'

            elif title_screen_buttons[i][2].collidepoint(mouse_x, mouse_y):
                screen.blit(title_screen_buttons[i][1], (580, 380 + i * 60))
                continue

            screen.blit(title_screen_buttons[i][0], (540, 380 + i * 60))

    def player_gui(self):
        '''
        The player health is stored global as many things interact on it. It uses that global variable as
        the Y cord to show the change in it. Same method is used for the boss. If the Y variable falls below a certain
        point it will initiate game over.
        '''

        global Game_Data
        if Game_Data[6] > 1:
            health_bar = pygame.Surface((10, Game_Data[6]))
            health_bar.set_alpha(150)
            health_bar.fill((100, 0, 0))
            Screen.blit(health_bar, (1260, 600))
        else:
            self.game_over()

    # --------------------------------------------------------------------
    '''
    These screens work on the same bases as the title screen.
    '''

    def instruction_screen(self):
        # print('instruction screen')
        Game_Data[5] = 'null'
        Screen.blit(self.instructions, (0, 0))

    def credit_screen(self):
        # print('credit screen')
        Game_Data[5] = 'null'
        Screen.blit(self.credits, (0, 0))

    # --------------------------------------------------------------------
    def pause_screen(self, sound_class):
        global Game_Data

        if Game_Data[0] != 'null':
            if Game_Data[0] != 'freeze':
                self.pre_pause = Game_Data[0]
                Game_Data[0] = 'freeze'
                sound_class.initialize_music = True
                pygame.mixer.music.stop()

                Screen.blit(self.gui_images[28], (390, 210))
                Screen.blit(self.pause_text, (520, 320, 100, 100))

            else:
                Game_Data[0] = self.pre_pause

    '''
    The following screens set up the game data to basically end the game. After the image is displayed the player just
    stops the program from running.
    '''

    def game_over(self):
        global Game_Data
        Game_Data[0] = 'game_over'
        Game_Data[5] = 'close'

    def you_win(self):
        global Game_Data

        Game_Data[0] = 'game_won'
        Game_Data[5] = 'close'

    def story(self):
        Screen.blit(self.story_image, (0, 0))
        Game_Data[5] = 'play'


# ----------------------------------------------------------------------------------------------------------------
'''

This class controls the "open world aspect of the game"
'''


class WorldMechanics(SoundEngine):
    # Variables all functions in the class can use.
    # --------------------------------------------------------------------
    def __init__(self, speed):

        self.overlay = image.load('World/Overlay.png')
        self.overlay = transform.scale(self.overlay, (1280, 720))

        self.player_collide_data = [[660, 420, 0, -10], [660, 428, 0, +10], [640, 424, -10, 0], [680, 424, +10, 0]]
        self.player_island_interaction = ''

        self.island = image.load('World/Island/Island.png')
        self.island = transform.scale(self.island, (5120, 2880))

        self.mask = image.load('World/Island/Island_Mask.png')
        self.mask = transform.scale(self.mask, (5120, 2880))

        self.castle_objects = []

        # -------------------------------------------------
        for i in range(1, 3):
            castle_object = image.load('World/Castle/Objects/Object_' + str(i) + '.png')
            self.castle_objects.append(castle_object)

        '''
        It uses the overall game clock to determine time ex 20 ticks = 1s, 20 ticks meaning it ran 20 times.
        If player timed out he will respawn
        '''
        # -------------------------------------------------
        self.collision_timeout = 0  # Number relates to 'ticks/frames'.
        self.world_x = 0
        self.world_y = -300
        self.speed = speed

    # --------------------------------------------------------------------
    def move_world(self, speed, screen):
        if keys[K_UP]:
            self.world_y += self.speed

        elif keys[K_DOWN]:
            self.world_y -= self.speed

        if keys[K_LEFT]:
            self.world_x += self.speed

        elif keys[K_RIGHT]:
            self.world_x -= self.speed

        # This keeps the moving speed at a diagonal similar to that of walking vertical/horizontal.
        if (keys[K_LEFT] and keys[K_DOWN]) or (keys[K_RIGHT] and keys[K_UP]) or (keys[K_RIGHT] and keys[K_DOWN]) or (
                keys[K_LEFT] and keys[K_UP]):
            self.speed = round(sqrt(((speed ** 2) / 2)))

        else:
            self.speed = speed

        # Displays world relative to the player.
        # -------------------------------------------------
        screen.fill((101, 181, 193))
        screen.blit(self.island, (self.world_x, self.world_y))
        screen.blit(self.overlay, (0, 0))

    # --------------------------------------------------------------------
    def world_boundaries(self):
        # Code to check specific points to see if a collision occurred.
        for collide_point in range(4):
            collide_x = self.player_collide_data[collide_point][0] - self.world_x
            collide_y = self.player_collide_data[collide_point][1] - self.world_y

            if self.mask.get_at((collide_x, collide_y)) == (255, 0, 0, 255):
                self.world_x += self.player_collide_data[collide_point][2]
                self.world_y += self.player_collide_data[collide_point][3]

        # Code to reset player if he goes out of bounds.
        if self.mask.get_at((660 - self.world_x, 420 - self.world_y)) == (255, 0, 0, 255):
            self.collision_timeout += 1
            if self.collision_timeout > 10:  # Timeout occurs when .5s/10ticks has passed.
                self.collision_timeout, self.world_x, self.world_y = 0, 0, -300

    # Several 'methods'/functions are kept inside classes despite not using the class.
    # This is done as a means of organization and to keep code that targets similar things together
    # --------------------------------------------------------------------
    def generate_interaction(self, interaction_type, sound_class):
        '''
        Acts as a switch
        '''
        if interaction_type == 'story':
            Game_Data[0] = 'story'
        if interaction_type == 'castle':
            Castle_.level_generater()
            sound_class.initialize_music = True

    # --------------------------------------------------------------------
    def island_interaction(self):

        '''

        Determines what mask colors mean what and than acts accordingly
        '''
        island_interaction_data = [[(0, 255, 0, 255), 'story'], [(255, 255, 0, 255), 'castle']]
        # -------------------------------------------------
        for collide_point in range(4):
            collide_x = self.player_collide_data[collide_point][0] - self.world_x
            collide_y = self.player_collide_data[collide_point][1] - self.world_y

            for interaction in range(len(island_interaction_data)):
                if self.mask.get_at((collide_x, collide_y)) == island_interaction_data[interaction][0]:
                    World_Mechanics.generate_interaction(island_interaction_data[interaction][1], Sound_Engine)
                    self.world_y += self.player_collide_data[collide_point][3]
                    break


# ----------------------------------------------------------------------------------------------------------------


class Castle:
    # --------------------------------------------------------------------
    def __init__(self):
        global Game_Data

        self.lever_switched = False
        self.level_progress = 0
        self.level = 2

        '''Inital castle values'''

        # -------------------------------------------------
        self.levels, self.level_masks = [], []
        for level in range(1, 6):
            level_state, mask_state = [], []
            for level_status in range(1, 3):
                # -------------------------------------------------
                level_image = image.load('World/Castle/Levels/Level_' + str(level) + '_' + str(level_status) + '.png')
                level_mask = image.load('World/Castle/Masks/Mask_' + str(level) + '_' + str(level_status) + '.png')
                level_mask = transform.scale(level_mask, (1280, 720))
                level_image = transform.scale(level_image, (1280, 720))
                # -------------------------------------------------
                mask_state.append(level_mask)
                level_state.append(level_image)

            self.level_masks.append(mask_state)
            self.levels.append(level_state)

    # --------------------------------------------------------------------
    def level_generater(self):
        global Game_Data
        Game_Data[0] = 'castle'
        '''starts the function group in the main loop'''

    # --------------------------------------------------------------------
    def generate_level(self):
        global Game_Data

        # -------------------------------------------------
        if self.lever_switched:
            self.level_progress += 1
            self.lever_switched = False

        Screen.blit(self.levels[self.level][self.level_progress], (0, 0))

        # -------------------------------------------------
        '''Control specific level functions, the last level has its own code group'''
        if self.level == 2:
            Player_Mechanics.arrow_mechanics()

        if self.level == 3:
            Player_Mechanics.lava_mechanics()

        if self.level == 4:
            Game_Data[1] = 'boss'


# ----------------------------------------------------------------------------------------------------------------


class EnemyMechanics(SoundEngine):
    def __init__(self):

        global Game_Data
        self.enemies = []
        self.enemy_masks = []
        self.boss = []

        # -------------------------------------------------
        for i in range(0, 2):
            enemy = image.load('World/Enemy/Enemy_' + str(i) + '.png')
            enemy_mask = image.load('World/Enemy/Mask_' + str(i) + '.png')
            self.enemy_masks.append(enemy_mask)
            self.enemies.append(enemy)

        # -------------------------------------------------
        self.enemies[0] = transform.smoothscale(self.enemies[0], (140, 400))
        self.enemy_masks[0] = transform.smoothscale(self.enemy_masks[0], (140, 400))

        self.lava_monsters = [[160, 520, 520, True], [430, 820, 820, True], [720, 620, 620, True]]

        # Boss
        # -------------------------------------------------
        self.boss_data = [False]
        self.boss_fight = False
        self.boss_y = 700
        self.frame = 0
        self.Once = True

        # Rock
        self.rock_mask = image.load('World/Castle/Objects/Mask_2.png')
        self.rock = image.load('World/Castle/Objects/Object_2.png')
        self.rock_data = []
        self.rock_mask_data = []

        pygame.font.init()
        game_font = font.SysFont("Times New Roman", 35)
        self.boss_text = game_font.render('BOSS BATTLE', True, (200, 200, 200))

        # Arrow
        # -------------------------------------------------
        self.enemies[1] = transform.smoothscale(self.enemies[1], (10, 60))
        self.enemies[1] = transform.rotate(self.enemies[1], 90)

        self.arrow_x = 1200

        self.arrow_object_t = []
        self.arrow_object_b = []

        '''
        the above stores all sorts of data, some of the data was used in earlier version of the game but not any more.
        '''

    # --------------------------------------------------------------------

    '''
    This starts up all the boss data.
    
    '''

    def init_boss_battle(self, sound_class):
        if not self.boss_fight:
            # -------------------------------------------------
            Game_Data[1] = "boss"
            sound_class.initialize_music = True

            # -------------------------------------------------
            for i in range(1, 11):
                boss_frame = image.load('World/Enemy/Boss/Boss_' + str(i) + '.png')
                boss_frame = transform.scale(boss_frame, (500, 360))
                self.boss.append(boss_frame)
            self.boss_fight = True
        else:
            pass

    '''
    
    Uses global data to find player and shoot rocks at him. Collide rect is used for all damage collsion
    '''

    def boss_attack(self):
        rock_x, rock_y = Game_Data[3], 0
        package = []

        package.extend([rock_x, rock_y])
        self.rock_data.append(package)

    def animate_boss(self):
        Screen.blit(self.boss[self.frame], (392, self.boss_y))

        if self.boss_y > 330:
            self.boss_y -= 4
        else:
            self.boss_data[0] = True

        if self.frame > 8:
            self.frame = 0
        else:
            self.frame += 1

    # --------------------------------------------------------------------
    def boss_battle(self, sound_class):

        # Same as player health
        # Boss Bar
        boss_bar = pygame.Surface((Game_Data[7], 10))
        boss_bar.set_alpha(150)
        boss_bar.fill((100, 0, 0))

        Screen.blit(self.boss_text, (550, 20))
        Screen.blit(boss_bar, (340, 50))

        player_hit_box = Rect(Game_Data[3], Game_Data[4], 35, 62)

        if randint(1, 30) < 2 and self.boss_data[0]:
            self.boss_attack()

        if Game_Data[7] < 10:
            User_Interface.you_win()

        elif Game_Data[7] < 300 and self.Once:
            sound_class.initialize_music = True
            self.Once = False

        for i in range(len(self.rock_data)):
            if self.rock_data[i][1] < 660:
                Screen.blit(self.rock, (self.rock_data[i][0], self.rock_data[i][1]))
                self.rock_data[i][1] += 16
                hit_box = Rect(self.rock_data[i][0], self.rock_data[i][1], 30, 30)

                if hit_box.colliderect(player_hit_box):
                    if Game_Data[6] > 0:
                        Game_Data[6] -= 10

        # The above checks to see player damage and boss damage

    # --------------------------------------------------------------------
    def lava_monster(self):

        player_hit_box = Rect(Game_Data[3], Game_Data[4], 35, 62)

        for i in range(0, 3):
            Screen.blit(self.enemies[0], (self.lava_monsters[i][0], self.lava_monsters[i][1]))

            # -------------------------------------------------
            if self.lava_monsters[i][1] < 260:
                self.lava_monsters[i][3] = False

            elif self.lava_monsters[i][1] > self.lava_monsters[i][2]:
                self.lava_monsters[i][3] = True

            # -------------------------------------------------
            if self.lava_monsters[i][3]:
                self.lava_monsters[i][1] -= 4
            else:
                self.lava_monsters[i][1] += 4

            lava_monster_hit_box = Rect(self.lava_monsters[i][0], self.lava_monsters[i][1], 140, 400)

            if player_hit_box.colliderect(lava_monster_hit_box):

                if Game_Data[6] > 0:
                    Game_Data[6] -= 5

    # --------------------------------------------------------------------
    def arrows(self):
        player_hit_box = Rect(Game_Data[3], Game_Data[4], 35, 62)

        if randint(0, 50) < 2:
            # print("arrow shot")
            arrows_package_t = []
            arrows_package_b = []
            arrows_package_t.extend([self.enemies[1], self.arrow_x, 50, +1])
            arrows_package_b.extend([self.enemies[1], self.arrow_x, 250, +1])
            self.arrow_object_t.append(arrows_package_t)
            self.arrow_object_b.append(arrows_package_b)

        for i in range(len(self.arrow_object_t)):
            if self.arrow_object_t[i][1] > 280:
                Screen.blit(self.arrow_object_t[i][0], (self.arrow_object_t[i][1], self.arrow_object_t[i][2]))
                arrow_hit_box_t = Rect(self.arrow_object_t[i][1], self.arrow_object_t[i][2], 60, 10)
                if player_hit_box.colliderect(arrow_hit_box_t):
                    if Game_Data[6] > 0:
                        Game_Data[6] -= 5

            if self.arrow_object_b[i][1] > 450:
                Screen.blit(self.arrow_object_b[i][0], (self.arrow_object_b[i][1], self.arrow_object_b[i][2]))
                arrow_hit_box_b = Rect(self.arrow_object_b[i][1], self.arrow_object_b[i][2], 60, 10)
                if player_hit_box.colliderect(arrow_hit_box_b):
                    if Game_Data[6] > 0:
                        Game_Data[6] -= 5

            self.arrow_object_t[i][1] -= 20
            self.arrow_object_t[i][3] += 0.2
            self.arrow_object_t[i][2] += self.arrow_object_t[i][3]
            self.arrow_object_b[i][1] -= 20
            self.arrow_object_b[i][3] += 0.2
            self.arrow_object_b[i][2] += self.arrow_object_b[i][3]


# ----------------------------------------------------------------------------------------------------------------


class PlayerMechanics(Castle):
    # --------------------------------------------------------------------
    def __init__(self):

        # -------------------------------------------------
        # Player frame, motion type and graphics data
        self.shadow = image.load('Player/Player_Walking/Player_Shadow.png')
        self.shadow = transform.scale(self.shadow, (40, 30))
        self.image = []
        self.frame, self.motion_type = 0, 0

        #  2 for loops, one for all the frames in a sequence,
        #  the second one for all the motion types. - This is for walking
        for walk_cycle in range(1, 9):  # All motion types
            movement_package = []
            for frames in range(1, 9):  # Frames in a sequence
                frame_image = image.load(
                    'Player/Player_Walking/Player_Walking_' + str(walk_cycle) + '/Player_F' + str(frames) + ".png")
                movement_package.append(frame_image)
            self.image.append(movement_package)

        player_shooting_right = image.load('Player/Player_Shooting/Player_Shooting.png')
        player_shooting_left = transform.flip(player_shooting_right, 1, 0)
        player_shooting = [player_shooting_right, player_shooting_left]
        self.image.append(player_shooting)

        # -------------------------------------------------
        # Player position, velocity, and gravity data
        # x, y, vx, vy, g (grounded), HP
        self.player = [10, 622, 0, 0, False, False, 100]
        self.collision_timeout = 0
        self.player_collide_data = [[0, 5, 12], [34, 5, -12], [17, -4, 0], [0, 62, 'null'], [34, 62, 'null']]

        # -------------------------------------------------
        self.castle_objects = []
        for i in range(1, 3):
            castle_object = image.load('World/Castle/Objects/Object_' + str(i) + '.png')
            self.castle_objects.append(castle_object)
        self.castle_objects[0] = transform.scale(self.castle_objects[0], (750, 292))

        # Cross Bow
        # -------------------------------------------------
        self.bullets = []
        self.direction = 0
        self.shoot, self.shot = False, False

    # --------------------------------------------------------------------
    def animate_world_player(self, world):
        if key.get_pressed():

            if keys[K_RIGHT] and keys[K_UP]:
                self.motion_type = 1

            elif keys[K_RIGHT] and keys[K_DOWN]:
                self.motion_type = 3

            elif keys[K_LEFT] and keys[K_UP]:
                self.motion_type = 7

            elif keys[K_LEFT] and keys[K_DOWN]:
                self.motion_type = 5

            elif keys[K_LEFT]:
                self.motion_type = 6

            elif keys[K_RIGHT]:
                self.motion_type = 2

            elif keys[K_UP]:
                self.motion_type = 0

            elif keys[K_DOWN]:
                self.motion_type = 4
            else:
                self.frame = 0

            # Frame Cycle
            # ---------------------------------------------
            if self.frame == 7:
                self.frame = 0
            else:
                self.frame += 1

        # -------------------------------------------------

        world.blit(self.shadow, (640, 400))
        world.blit(self.image[self.motion_type][self.frame], (640, 360))

    # --------------------------------------------------------------------
    def animate_platform_player(self):
        x, y, vx, vy, g, c = 0, 1, 2, 3, 4, 5

        if key.get_pressed():

            if keys[K_UP] and self.player[g]:
                self.player[g] = False
                self.frame = 0
                self.player[vy] = -36

            elif keys[K_LEFT]:
                self.motion_type = 6
                self.player[vx] = -15
                self.direction = 1

            elif keys[K_RIGHT]:
                self.motion_type = 2
                self.player[vx] = 15
                self.direction = 0

            elif keys[K_c] and not self.shot:
                self.shot, self.shoot = True, True
                self.motion_type = 8
                self.frame = self.direction

                if self.direction == 0:
                    bullet_vx = 20
                    shift_x = 35
                else:
                    bullet_vx = -20
                    shift_x = -10

                bullet_package = []
                bullet_package.extend([self.player[x] + shift_x, self.player[y] + 38, 10, 2, bullet_vx])
                self.bullets.append(bullet_package)

            elif not self.shoot:
                self.player[vx] = 0
                self.frame = 0

            else:
                self.player[vx] = 0

                if not keys[K_c]:
                    self.shot = False

            # Frame Cycle
            # ---------------------------------------------
            if not self.shoot:
                if self.frame == 7:
                    self.frame = 0
                else:
                    self.frame += 1

        # -------------------------------------------------
        self.player[x] += self.player[vx]
        self.player[y] += self.player[vy]

        # -------------------------------------------------

        Screen.blit(self.image[self.motion_type][self.frame], (self.player[x], self.player[y]))

    # --------------------------------------------------------------------
    def platform_physics(self, castle):
        global Game_Data
        self.levels = castle.levels
        self.level_masks = castle.level_masks

        level_p = castle.level_progress  # level_p (Level Progression)
        level = castle.level

        x, y, vx, vy, g, c = 0, 1, 2, 3, 4, 5
        start_position = [[10, 622], [10, 200], [10, 292], [10, 466]]

        collide = [(255, 0, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255), (255, 0, 0, 255), (255, 155, 0, 255),
                   (0, 0, 0, 255)]

        # Generate and check hit box
        # -------------------------------------------------
        # Vertical

        # print(self.player[x], self.player[y])
        # If player falls out of bounds
        if self.player[y] + 64 > 700:
            # User_Interface.game_over()
            pass

        else:

            for height in range(55):
                if 720 > self.player[y] + 2 > 0 and 0 < self.player[x] and self.player[x] + 35 < 1280:
                    for j in range(2):
                        point_x = self.player[x] + self.player_collide_data[j][0]
                        point_y = self.player[y] + self.player_collide_data[j][1] + height

                        if self.level_masks[level][level_p].get_at((point_x, point_y)) == collide[0]:
                            self.player[x] = self.player[x] + self.player_collide_data[j][2]

                            self.collision_timeout += 1
                            #print('active')
                            if self.collision_timeout > 50:  # Timeout occurs when 1.25s/5ticks has passed.
                                self.player[x], self.player[y] = start_position[level]
                                self.collision_timeout = 0

                        if self.level_masks[level][level_p].get_at((point_x, point_y)) == collide[1] and level_p == 0:
                            castle.lever_switched = True

                        elif self.level_masks[level][level_p].get_at((point_x, point_y)) == collide[2] and level_p == 1:
                            castle.level += 1
                            castle.level_progress = 0
                            self.player[x], self.player[y] = start_position[level]
                            self.player[vx], self.player[vy] = 0, 0

                        if self.level_masks[level][level_p].get_at((point_x, point_y)) == collide[5]:
                            Game_Data[6] -= 5
            # -------------------------------------------------
            # Horizontal
            for i in range(35):
                # Check head collision
                if 720 > self.player[y] - 4 > 0 and 0 < self.player[x] and self.player[x] + 35 < 1280:
                    top_point_x = self.player[x] + i
                    top_point_y = self.player[y] + self.player_collide_data[2][1]

                    if self.level_masks[level][level_p].get_at((top_point_x, top_point_y)) == collide[3]:
                        self.player[vy] = 0
                        self.player[g] = False

                # Check feet collision
                if 720 > self.player[y] + 62 > 0 and 0 < self.player[x] and self.player[x] + 35 < 1280:
                    # print(level, level_p)
                    for j in range(3, 5):
                        if self.player[vy] > 0:
                            path_point = self.player[vy]
                        else:
                            path_point = 0

                        bottom_point_x = self.player[x] + self.player_collide_data[j][0]
                        bottom_point_y = self.player[y] + self.player_collide_data[j][1] + path_point

                        if self.level_masks[level][level_p].get_at((bottom_point_x, bottom_point_y)) == collide[4]:
                            self.player_collide_data[j][2] = True
                        else:
                            self.player_collide_data[j][2] = False

                # Determine if player is grounded
                if self.player_collide_data[3][2] or self.player_collide_data[4][2]:
                    self.player[g] = True
                    self.player[vy] = 0
                else:
                    self.player[g] = False

            # Gravity
            # -------------------------------------------------
            if not self.player[g]:
                if self.player[vy] < 13:
                    self.player[vy] += 3

            # Boss Battle Stage
            # -------------------------------------------------
            if level_p == 4:
                if self.player[x] > 1250:
                    self.player[x] -= 10
                elif self.player[x] < 30:
                    self.player[x] += 10

            Game_Data[3], Game_Data[4] = self.player[x], self.player[y]

    # --------------------------------------------------------------------
    def lava_mechanics(self):
        Enemy_Mechanics.lava_monster()
        Screen.blit(self.castle_objects[0], (155, 620))

    # --------------------------------------------------------------------
    def arrow_mechanics(self):
        Enemy_Mechanics.arrows()

    def bullet_mechanics(self):
        boss_hit_box = Rect(590, 490, 100, 180)

        for i in range(len(self.bullets)):

            if 0 < self.bullets[i][0] < 1280:
                draw.rect(Screen, (100, 100, 100),
                          (self.bullets[i][0], self.bullets[i][1], self.bullets[i][2], self.bullets[i][3]))
                self.bullets[i][0] += self.bullets[i][4]

                if boss_hit_box.colliderect(
                        (self.bullets[i][0], self.bullets[i][1], self.bullets[i][2], self.bullets[i][3])):
                    Game_Data[7] -= 1
            else:
                pass


# Setup & Initialize
# ------------------------------------------------------------------------

Screen = display.set_mode((1280, 720))

Enemy_Mechanics = EnemyMechanics()

Sound_Engine = SoundEngine()

User_Interface = UserInterface()

World_Mechanics = WorldMechanics(10)

Player_Mechanics = PlayerMechanics()

Castle_ = Castle()

clock = pygame.time.Clock()

# Initialize Game Loop
# ------------------------------------------------------------------------
running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        keys = key.get_pressed()
        if keys[K_p]:
            User_Interface.pause_screen(Sound_Engine)
        if keys[K_ESCAPE]:
            Game_Data[0] = Game_Data[5]

    # Data Input
    # --------------------------------------------------------------------
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    # Unbound Functions
    # --------------------------------------------------------------------
    Sound_Engine.background_music()

    # Bound Functions
    # --------------------------------------------------------------------
    if Game_Data[0] == 'null':
        User_Interface.title_screen(Screen, mx, my, mb, Sound_Engine)

    # Title Screen Input
    # --------------------------------------------
    elif Game_Data[0] == 'play':
        Sound_Engine.background_music()
        World_Mechanics.move_world(10, Screen)
        Player_Mechanics.animate_world_player(Screen)
        World_Mechanics.world_boundaries()
        World_Mechanics.island_interaction()

    elif Game_Data[0] == 'instructions':
        User_Interface.instruction_screen()

    elif Game_Data[0] == 'credits':
        User_Interface.credit_screen()

    # Main World Input
    # --------------------------------------------
    elif Game_Data[0] == 'shop':
        running = False

    elif Game_Data[0] == 'story':
        User_Interface.story()

    elif Game_Data[0] == 'castle':
        Player_Mechanics.platform_physics(Castle_)
        Castle_.generate_level()
        Player_Mechanics.animate_platform_player()
        Player_Mechanics.bullet_mechanics()
        User_Interface.player_gui()

        if Game_Data[1] == 'boss':
            Enemy_Mechanics.init_boss_battle(Sound_Engine)
            Enemy_Mechanics.animate_boss()
            Enemy_Mechanics.boss_battle(Sound_Engine)

    # Events
    # --------------------------------------------
    if Game_Data[0] == 'close':
        running = False

    elif Game_Data[0] == "game_over":
        Screen.blit(User_Interface.game_over_image, (0, 0))
        # print('Active Game Over screen')
        # User_Interface.game_over()

        '''
        Castle_.lever_switched = False
        Castle_.level_progress = 0
        Castle_.level = 0
        Player_Mechanics.player = [10, 622, 0, 0, False, False, 100]
        '''

    elif Game_Data[0] == "game_won":
        Screen.blit(User_Interface.you_win_image, (0, 0))

    # --------------------------------------------
    clock.tick(20)  # Game frame rate
    # ------------------------------------------------------------------------
    display.flip()
quit()
