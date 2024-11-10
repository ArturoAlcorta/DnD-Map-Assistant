"""
Proyecto DND

Autor: Arturo Alcorta
Fecha de comienzo: 28/12/2023
"""
#!/usr/bin/python
import pygame, os, sys
import random
import pandas as pd
from math import sqrt
from pygame.locals import *

# Variables

split = 2 # Number of pixels between each square
char_selec = 0
mapa_actual = 0
act_map = 0
enemies = []
enemy_create = 0
change = 0
measure_dist = 0
pos_0 = (0,0)
pos_1 = (0,0)
close_game = 0

#####################################################################################

# CLASS DEFINITION

#####################################################################################

class Character(): # SuperClass for players and enemies
    def __init__(self, x, y, speed, path):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(path)
        self.rect = None

    def change_position(self, x, y):
        dist = sqrt((self.x - x)**2 + (self.y - y)**2)
        if (dist <= self.speed/5) or (self.speed == 0):
            self.x = x
            self.y = y

    def draw():
        for character in characters:
            character.image = pygame.transform.smoothscale(character.image, (mapa_actual.sz_box, mapa_actual.sz_box))
            character.rect = character.image.get_rect()
            character.rect.left = character.x * (mapa_actual.sz_box + split) + mapa_actual.margin[0]
            character.rect.top = character.y * (mapa_actual.sz_box + split) + mapa_actual.margin[1]
            surface.blit(character.image, character.rect)

    def reset_pos():
        global characters
        characters = [character for character in characters if not isinstance(character, Enemy)]
        for i, character in enumerate(characters):
            character.x = 0
            character.y = i

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Player(Character):
    def __init__(self, character, x, y, path):
        # Inicializar la superclase Character
        self.name = character[0]
        self.clase = character[1]
        path = path + self.clase + '.png'
        speed = character[2]
        super().__init__(x, y, speed, path)
    
class Enemy(Character):
    def __init__(self, x, y, path):
        # Inicializar la superclase Character
        super().__init__(x, y, 0, path)

    def kill(enemy):
        global characters, char_selec
        if isinstance(enemy,Enemy):
            characters.remove(enemy)
            char_selec = 0

    def create():
        global enemy_create, char_selec, measure_dist, close_game
        enemy_create = not enemy_create
        char_selec = 0
        measure_dist = 0
        close_game = 0

class Map:
    def __init__(self, path, cols, rows):
        self.path = path
        self.cols = cols
        self.rows = rows
        if rows > cols:
            self.sz_box = (max_map_height - (rows-1)*5)//rows 
            self.margin = [(max_map_width - (cols * (self.sz_box + split) - split)) // 2, (max_map_height - (rows * (self.sz_box + split) - split)) // 2]
        elif cols > rows:
            self.sz_box = (max_map_width - (cols-1)*5)//cols
            self.margin = [(max_map_width - (cols * (self.sz_box + split) - split)) // 2, (max_map_height - (rows * (self.sz_box + split) - split)) // 2]
        elif cols == rows:
            if max_map_width > max_map_height:
                self.sz_box = (max_map_height - (rows-1)*5)//rows 
                self.margin = [(max_map_width - (cols * (self.sz_box + split) - split)) // 2, (max_map_height - (rows * (self.sz_box + split) - split)) // 2]
            elif max_map_height > max_map_width:
                self.sz_box = (max_map_width - (cols-1)*5)//cols
                self.margin = [(max_map_width - (cols * (self.sz_box + split) - split)) // 2, (max_map_height - (rows * (self.sz_box + split) - split)) // 2]
        

    def load(map):
        map_load = pygame.image.load(map.path)
        map_load = pygame.transform.smoothscale(map_load, (map.sz_box * map.cols, map.sz_box * map.rows))
        width, height = map_load.get_size()

        for i in range(map.cols):
            for j in range(map.rows):
                if map.rows > map.cols:
                    x, y = i*width//map.cols, j*height//map.rows
                    fragment_surface = map_load.subsurface(pygame.Rect(x, y, map.sz_box, map.sz_box))
                    Posx, Posy = i  * (width//map.cols + split) + map.margin[0], j * (height//map.rows + split) + map.margin[1]

                else:
                    x, y = i*width//map.cols, j*height//map.rows
                    fragment_surface = map_load.subsurface(pygame.Rect(x, y, map.sz_box, map.sz_box))
                    Posx, Posy = i * (width//map.cols + split) + map.margin[0], j * (height//map.rows + split) + map.margin[1]

                surface.blit(fragment_surface, (Posx, Posy))

    def next_map():
        global act_map
        global max_map
        if act_map != max_map:
            act_map += 1
            Character.reset_pos()

    def prev_map():
        global act_map
        if act_map != 0:
            act_map -= 1
            Character.reset_pos()

class Button:
    def __init__(self, x, y, function, path, size):
        self.function = function
        self.path = path
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw():
        for button in buttons:
            surface.blit(button.image, button.rect)
            pygame.draw.rect(surface, (255, 255, 255), button.rect, 5)

    def is_clicked(self,pos):
        return self.rect.collidepoint(pos)
    

#####################################################################################

# FUNCTION DEFINITION

#####################################################################################

def measure_var():
    global measure_dist, pos_0, pos_1
    global enemy_create, char_selec, measure_dist, close_game
    measure_dist = not measure_dist
    pos_0 = (0,0)
    pos_1 = (0,0)
    enemy_create = 0
    char_selec = 0
    close_game = 0

def start_game():
    global mapa_actual
    players = []
    maps = []
    Pos_inicial = 0

    map_path = '.\Maps'
    for i, path in enumerate(os.listdir(map_path)):
        if os.path.isfile(os.path.join(map_path, path)):
            path_map = os.path.join(map_path, path)
            dim = input(f'Que dimensiones tiene el mapa {i + 1}? (columnas , filas)')
            map = Map(path_map, int(dim.split()[0]), int(dim.split()[1]))
            maps.append(map)

    mapa_actual = maps[0]

    characters = pd.read_csv('.\Characters\characters.csv',header=None).values
    for char in characters:
        player = Player(char, Pos_inicial, 0, './Utilities/token_')
        players.append(player)
        Pos_inicial = + 1

    return players, maps


def draw_ui():
    Map.load(mapa_actual)
    Button.draw()
    Character.draw()
    write_data(surface)

def def_buttons():
    # Definimos los botones de flechas
    buttons = []
    button_path = './Utilities/'

    path = os.path.join(button_path,'prev_arrow.png')
    button = Button(max_map_width + max_ui_width/4, max_map_height*9/10, lambda: Map.prev_map(), path, (max_ui_width*0.49, max_ui_width*0.49))
    buttons.append(button)

    path = os.path.join(button_path,'post_arrow.png')
    button = Button( max_map_width + max_ui_width*3/4, max_map_height*9/10, lambda: Map.next_map(), path, (max_ui_width*0.49, max_ui_width*0.49))
    buttons.append(button)
    
    # Create enemy
    path = os.path.join(button_path,'enemy_token.png')
    button = Button(max_map_width + max_ui_width/4, max_map_height*5/10, lambda: Enemy.create(), path, (max_ui_width*0.49, max_ui_width*0.49))
    buttons.append(button)

    # Kill Enemy
    path = os.path.join(button_path,'kill_enemy.png')
    kill = Button(max_map_width + max_ui_width*3/4,  max_map_height*5/10, lambda: Enemy.kill(char_selec), path, (max_ui_width*0.49, max_ui_width*0.49))
    buttons.append(kill)

    # Measure Distance
    path = os.path.join(button_path,'ruler-removebg-preview.png')
    measure = Button(max_map_width + max_ui_width/2, max_map_height*6.6/10, lambda: measure_var(), path, (max_ui_width*0.99, max_map_height*0.1))
    buttons.append(measure)

    return buttons

def write_data(surface):
    if char_selec and isinstance(char_selec, Player):
        # Renderizamos el nombre en el hueco de las caracteristicas
        Name = char_selec.name
        Name = title.render(Name, 1, (255,255,255))
        Name_pos = Name.get_rect(centerx = max_map_width+max_ui_width/2 , top = max_map_height*0.1)
        surface.blit(Name, Name_pos)

        # Ahora renderizamos el resto de datos
        Data = "Class:........{0}\nSpeed:........{1}"
        info = Data.format(char_selec.clase, char_selec.speed)
        # Calcula la altura de cada línea
        line_height = font.get_linesize()
        # Inicializa la posición vertical
        vertical_position = max_map_height*0.2
        # Divide la información en líneas
        lines = info.split('\n')
        for line in lines:
            Data_line = font.render(line, 1, (255,255,255))
            Data_pos = Data_line.get_rect(centerx = max_map_width+max_ui_width/2, top = vertical_position)
            surface.blit(Data_line, Data_pos)
            vertical_position += line_height

        
        x = char_selec.x * (mapa_actual.sz_box + split) + mapa_actual.margin[0] + mapa_actual.sz_box//2
        y = char_selec.y * (mapa_actual.sz_box + split) + mapa_actual.margin[1] + mapa_actual.sz_box//2
        rad = char_selec.speed//5*(mapa_actual.sz_box + split) + mapa_actual.sz_box//2
        pygame.draw.circle(surface, (255,0,0), (x,y), rad, 5)

    elif char_selec and isinstance(char_selec, Enemy):
        Name = 'Enemy'
        Name = title.render(Name, 1, (255,255,255))
        Name_pos = Name.get_rect(centerx = max_map_width+max_ui_width/2 , top = max_map_height*0.1)
        surface.blit(Name, Name_pos)

    elif measure_dist:
        Name = 'Distance\nMeasurement'
        line_height = title.get_linesize()
        # Inicializa la posición vertical
        vertical_position = max_map_height*0.1
        # Divide la información en líneas
        lines = Name.split('\n')
        for line in lines:
            Data_line = title.render(line, 1, (255,255,255))
            Data_pos = Data_line.get_rect(centerx = max_map_width+max_ui_width/2, top = vertical_position)
            surface.blit(Data_line, Data_pos)
            vertical_position += line_height + 0.01*max_map_height


        Data = "Point 1:........{0}\nPoint 2:........{1}\nDistance:......{2}ft"
        dist = sqrt(((pos_0[0] - pos_1[0])**2 + (pos_0[1] - pos_1[1])**2))*5
        info = Data.format(pos_0, pos_1, dist)
        # Calcula la altura de cada línea
        line_height = font.get_linesize()
        # Inicializa la posición vertical
        vertical_position = max_map_height*0.25
        # Divide la información en líneas
        lines = info.split('\n')
        for line in lines:
            Data_line = font.render(line, 1, (255,255,255))
            Data_pos = Data_line.get_rect(centerx = max_map_width+max_ui_width/2, top = vertical_position)
            surface.blit(Data_line, Data_pos)
            vertical_position += line_height

        temp_0 = (pos_0[0]* (mapa_actual.sz_box + split) + mapa_actual.margin[0] + mapa_actual.sz_box//2, pos_0[1] * (mapa_actual.sz_box + split) + mapa_actual.margin[1] + mapa_actual.sz_box//2)
        temp_1 = (pos_1[0]* (mapa_actual.sz_box + split) + mapa_actual.margin[0] + mapa_actual.sz_box//2, pos_1[1] * (mapa_actual.sz_box + split) + mapa_actual.margin[1] + mapa_actual.sz_box//2)
        pygame.draw.line(surface, (0,0,255), temp_0, temp_1, 5)

    elif  enemy_create:
        Name = 'Creating\nEnemy'
        line_height = title.get_linesize()
        # Inicializa la posición vertical
        vertical_position = max_map_height*0.1
        # Divide la información en líneas
        lines = Name.split('\n')
        for line in lines:
            Data_line = title.render(line, 1, (255,255,255))
            Data_pos = Data_line.get_rect(centerx = max_map_width+max_ui_width/2, top = vertical_position)
            surface.blit(Data_line, Data_pos)
            vertical_position += line_height + 0.01*max_map_height

    elif close_game:
        Name = 'Close\nGame?'
        line_height = title.get_linesize()
        # Inicializa la posición vertical
        vertical_position = max_map_height*0.1
        # Divide la información en líneas
        lines = Name.split('\n')
        for line in lines:
            Data_line = title.render(line, 1, (255,0,0))
            Data_pos = Data_line.get_rect(centerx = max_map_width+max_ui_width/2, top = vertical_position)
            surface.blit(Data_line, Data_pos)
            vertical_position += line_height + 0.01*max_map_height
    

#####################################################################################

# MAIN GAME LOOP

#####################################################################################

pygame.init() # Initialize video module
fpsClock = pygame.time.Clock()

# Get screen dimensions and set app dimensions
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
max_map_width = screen_width*3/4
max_map_height = screen_height
max_ui_width = screen_width - max_map_width

if screen_height == 2160:
    title = pygame.font.Font(None,160)
    title.set_underline(True)
    title.set_bold(True)
    font = pygame.font.Font(None,96)
elif screen_height < 2160 and screen_height > 1080:
    title = pygame.font.Font(None,128)
    title.set_underline(True)
    title.set_bold(True)
    font = pygame.font.Font(None,64)
elif screen_height <= 1080:
    title = pygame.font.Font(None,96)
    title.set_underline(True)
    title.set_bold(True)
    font = pygame.font.Font(None,48)

quitGame = False
isPlaying = False
buttons = def_buttons()
characters, maps = start_game()
max_map = len(maps) - 1
mapa_actual = maps[act_map]
surface = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("DnD Map Assistant") # Window name
icon = pygame.image.load("Map_assistant_icon.png")  # Asegúrate de que el archivo icono.ico esté en la misma carpeta
pygame.display.set_icon(icon)

while not quitGame:
    surface.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame = True  # Cambia el valor de quitGame para salir del bucle
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left Mouse Click. Main Actions
            pos = pygame.mouse.get_pos()
            x, y = pos
            x = (x - mapa_actual.margin[0]) // (mapa_actual.sz_box + split)
            y = (y - mapa_actual.margin[1]) // (mapa_actual.sz_box + split)

            for button in buttons:
                if button.is_clicked(pos):
                    button.function()
                    change = 1

            if not measure_dist:
                for character in characters:
                    if character.is_clicked(pos):
                        char_selec = character
                        close_game = 0
                        enemy_create = 0
                        change = 1

                if change == 0:

                    if (enemy_create != 0):
                        new_enemy = Enemy(x, y, './Utilities/enemy_token.png')
                        characters.append(new_enemy)
                        enemy_create = 0

                    elif (char_selec != 0):
                        Character.change_position(char_selec, x, y)
                        char_selec = 0
            else:
                if change == 0:
                    if pos_0 == (0,0): pos_0=(x,y)
                    elif pos_0 != (0,0) and pos_1 == (0,0): pos_1 = (x,y)
                    elif pos_0 != (0,0) and pos_1 != (0,0): pos_0=(x,y); pos_1 = (0,0)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right Mouse Click. Reset all variables
            enemy_create = 0
            char_selec = 0
            measure_dist = 0
            close_game = 0

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m: # Detectar si se ha presionado la tecla M
            pygame.display.iconify()  # Minimizar la ventana

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not close_game:
                close_game = 1
                enemy_create = 0
                char_selec = 0
                measure_dist = 0
            else:
                quitGame = True  # Close the window

    
    # Aquí iría la lógica del juego, como la actualización de la posición de los jugadores y la redibujado de la pantalla
    change = 0
    mapa_actual = maps[act_map]
    draw_ui()

    pygame.display.flip()
    fpsClock.tick(30)  # Ajusta la velocidad del bucle