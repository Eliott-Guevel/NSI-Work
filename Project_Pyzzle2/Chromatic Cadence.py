import pygame
from pygame.locals import *

# permet de changer les valeurs par défaut
# fréquence : 44100 et buffer : 512
#pygame.mixer.pre_init(44100,-16,2, 1024)
""" fixer vitesse musique"""
# lancement de pygame
pygame.init()
pygame.mixer.init()

""" fichiers nécessaires
sprites(.png):
red_square
blue_square
red_note
blue_note
title_screen
background_with_tracks

musiques(.ogg):
Louis XIV - God Killed the Queen INSTRUMENTAL
Breakfast (Pause Menu) - Friday Night Funkin' OST
Final Fantasy VII - Victory Fanfare
Sayonara Wild Heart
Crypt of the NecroDancer OST - King Conga Kappa (King Conga)
OMORI OST - 106 GOLDENVENGEANCE
Bossfight - Milky Ways

font(.ttf):
SMW
"""

""" à faire
victory screen
menu d'options (volume musique, taille notes)
sound effects
gestion collisions
au moins 2 niveaux (tuto + ez)
score : combo des notes (100 pts par note réussie, +50 pour combo commençant à 1, cappant à 200)
"""

# logo = pygame.image.load("monimage.png").convert_alpha()
# pygame.display.set_icon(logo)

pygame.display.set_caption("Chromatic Cadence")

# gestion des constantes
# 1920 / 2
width_screen = 960
# 1080 / 2
height_screen = 540

# création de la fenêtre
screen = pygame.display.set_mode((width_screen, height_screen))

# attributs : nom, taille, gras et italique (booléens)
principal_font = pygame.font.SysFont("SMW", 40)

music = pygame.mixer.music.load("Louis XIV - God Killed the Queen INSTRUMENTAL.ogg")
# -1 permet de jouer indéfiniment la musique
pygame.mixer.music.play(-1)

# initialise la gestion du framerate
clock_framerate = pygame.time.Clock()

background = pygame.image.load("title_screen.png").convert_alpha()

def update_music_time_remaining():
    # * 1000 puisque temps en ms
    music_time_passed = str(pygame.mixer.music.get_pos() // 1000)
    # utilise le format RGBA (A = alpha, opacité couleur)
    music_time_remaining = principal_font.render(music_time_passed, True, pygame.Color("white"))
    return music_time_remaining

def music_time():
    music_length = str(int(pygame.mixer.Sound.get_length(music_setup)))
    music_length_text = principal_font.render(music_length, True, pygame.Color("white"))
    return music_length_text

def update_fps():
    fps = str(int(clock_framerate.get_fps()))
    fps_text = principal_font.render(fps, True, pygame.Color("purple"))
    return fps_text

def score_increase():
    #score =
    pass

continue_menu = True
while continue_menu:
    for event in pygame.event.get():
    # appuyer sur la croix ou sur escape quitte le jeu
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            quit()
        # 1er niveau
        if event.type == KEYDOWN:
            if event.key == K_F1:
                continue_menu = False
                level_counter = 0
            # 2ème niveau
            elif event.key == K_F2:
                continue_menu = False
                level_counter = 1

    screen.blit(background, (0,0))
    screen.blit(update_fps(), (400, 0))
    # 60 fps maximum
    clock_framerate.tick(60)
    # actualisation permanente du screen principal
    pygame.display.flip()

background = pygame.image.load("background_with_tracks.png").convert_alpha()
# victory_screen_music = pygame.mixer.music.load("Final Fantasy VII - Victory Fanfare.ogg")

# click = pygame.mixer.Sound(".mp3")

pause_text = principal_font.render('Pause', True, pygame.color.Color('red'))

# tutoriel
if level_counter == 0:
    # 1:31, 92 BPM
    music_setup = pygame.mixer.Sound("Sayonara Wild Heart.ogg")
    music = pygame.mixer.music.load("Sayonara Wild Heart.ogg")

# easy
elif level_counter == 1:
    # 1:53, 120 BPM
    music_setup = pygame.mixer.Sound("Crypt of the NecroDancer OST - Konga Conga Kappa (King Conga).ogg")
    music = pygame.mixer.music.load("Crypt of the NecroDancer OST - Konga Conga Kappa (King Conga).ogg")

        # medium
elif level_counter == 2:
    # 2:29, 140 BPM
    music = pygame.mixer.music.load("OMORI OST - 106 GOLDENVENGEANCE.ogg")

# hard
elif level_counter == 3:
    # 3:07, 184 BPM
    music = pygame.mixer.music.load("Bossfight - Milky Ways.ogg")

# premet de jouer la musique du niveau sélectionné
pygame.mixer.music.play()

pause_canal = pygame.mixer.Channel(0)

running = True
pause = False
state = running

class Player:
    """gère le personnage principal"""
    def __init__(self, character_red, character_blue):
        super().__init__()
        # sprites du personnage principal
        self.character_red = pygame.image.load(character_red).convert_alpha()
        self.character_blue = pygame.image.load(character_blue).convert_alpha()

        self.x = width_screen // 2 - 40
        self.y = height_screen // 2 - 40

        # état par défaut du personnage
        self.default_state = self.character_red

    def change_state(self, state):
        if state == "red":
            self.default_state = self.character_red
        if state == "blue":
            self.default_state = self.character_blue

    def absorb_note(self, state):
        pass

class Note:
    """gère les notes arrivant"""
    def __init__(self, red_note, blue_note):
        # sprites des notes (couleurs en hexadécimal identiques au personnage principal)
        self.red_note = pygame.image.load("red_note.png").convert_alpha()
        self.blue_note = pygame.image.load("blue_note.png").convert_alpha()

# création du personnage principal (40 * 40)
# rouge : FF3C28
# bleu : 0AB9E6
character = Player("red_square.png", "blue_square.png")

note = Note("red_note.png", "blue_note.png")

# boucle principale
while running:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        # click sur un bouton de la souris active cet évènement:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # left mouse button
            if event.button == 1:
                character.change_state("red")
            # right mouse button
            if event.button == 3:
                character.change_state("blue")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                state = pause
            if event.key == pygame.K_s:
                state = running

    if state == running:
        music_count = 0
        # applique le background sur le screen principal
        screen.blit(background, (0, 0))
        # affiche le fps en haut à gauche de l'écran (x, y)
        screen.blit(update_fps(), (400, 0))
        # affiche le temps restant de la musique en haut à droite de l'écran
        screen.blit(music_time(), (550, 0))
        screen.blit(update_music_time_remaining(), (490, 0))
        # character.default_state utilise l'état, et blit = block image transfer
        screen.blit(character.default_state, (character.x, character.y))
        # permet de savoir quand la musique est finie
        #pygame.mixer.music.set_endevent()
        #screen.blit(Note.red_note, (480, 235))
        #screen.blit(Note.blue_note, (5, 235))
        pygame.mixer.music.unpause()
        pause_canal.pause()

    elif state == pause:
        pygame.mixer.music.pause()
        screen.blit(pause_text, (0, 0))
        pause_music = pygame.mixer.Sound("Breakfast (Pause Menu) - Friday Night Funkin' OST.ogg")
        # permet de ne jouer qu'une seule fois la musique
        while music_count < 2:
            music_count += 1
            pause_canal.play(pause_music, -1)

    clock_framerate.tick(60)
    pygame.display.flip()

pygame.quit()
quit()
