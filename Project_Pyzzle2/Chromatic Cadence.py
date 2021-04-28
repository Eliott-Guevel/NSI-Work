import pygame
pygame.init()

""" fichiers nécessaires
sprites(.png):
red_character
blue_character
red_note
blue_note
title_screen
background_with_tracks
background

musiques(.ogg):
Louis XIV - God Killed the Queen INSTRUMENTAL
Breakfast (Pause Menu) - Friday Night Funkin' OST
Final Fantasy VII - Victory Fanfare
Sayonara Wild Heart

son(.wav):
fail_sound

font(.ttf):
SMW """

pygame.display.set_caption("Chromatic Cadence")

# gestion des constantes
# 1920 / 2
width_screen = 960
# 1080 / 2
height_screen = 540
# attributs : nom, taille, gras et italique (booléens)
principal_font = pygame.font.SysFont("SMW", 40)

# création de la fenêtre
screen = pygame.display.set_mode((width_screen, height_screen))

logo = pygame.image.load("red_note.png").convert_alpha()
pygame.display.set_icon(logo)

#pygame.mixer.music.set_volume(0)

music = pygame.mixer.music.load("Louis XIV - God Killed the Queen INSTRUMENTAL.ogg")
# -1 permet de jouer indéfiniment la musique
pygame.mixer.music.play(-1)

# initialise la gestion du framerate
clock_framerate = pygame.time.Clock()

background = pygame.image.load("title_screen.png").convert_alpha()

max_combo_text = principal_font.render("MAX", True, pygame.color.Color("green"))

fail_sound = pygame.mixer.Sound("fail_sound.wav")

def update_fps():
    fps = str(int(clock_framerate.get_fps()))
    fps_text = principal_font.render(fps, True, pygame.Color("purple"))
    return fps_text

def music_time():
    music_length = str(int(pygame.mixer.Sound.get_length(music_setup)))
    music_length_text = principal_font.render(music_length, True, pygame.Color("white"))
    return music_length_text

def update_music_time_remaining():
    # * 1000 puisque temps en ms
    music_time_passed = str(pygame.mixer.music.get_pos() // 1000)
    music_time_remaining = principal_font.render(music_time_passed, True, pygame.Color("white"))
    return music_time_remaining

class Player(pygame.sprite.Sprite):
        """gère le personnage principal"""
        def __init__(self, game, red_character, blue_character):
            super().__init__()
            self.game = game
            # sprites du personnage principal
            self.red_character = pygame.image.load(red_character).convert_alpha()
            self.blue_character = pygame.image.load(blue_character).convert_alpha()

            # état par défaut du personnage
            self.image = self.red_character
            self.player_color = "red"

            self.rect = self.red_character.get_rect()
            # width_screen // 2 - 40
            self.rect.x = 440
            # height_screen // 2 - 40
            self.rect.y = 230

        def change_state(self):
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left mouse button
                if event.button == 1:
                    self.image = self.red_character
                    self.player_color = "red"
                # right mouse button
                if event.button == 3:
                    self.image = self.blue_character
                    self.player_color = "blue"

class Game():
    def __init__(self):
        super().__init__()
        self.all_players = pygame.sprite.Group()
        # création du personnage principal (40 * 40)
        # rouge : FF3C28
        # bleu : 0AB9E6
        self.player = Player(self, "red_character.png", "blue_character.png")
        self.all_players.add(self.player)
        self.all_notes = pygame.sprite.Group()
        self.counter = 0
        self.time_elapsed = 0
        self.time_elapsed_2 = 0
        self.difference = 0
        self.other_combo = 0
        self.other_score = 0

    def spawn_red_right_note(self):
        red_right_note = Note(self, "red_note.png", "right")
        self.all_notes.add(red_right_note)

    def spawn_blue_right_note(self):
        blue_right_note = Note(self, "blue_note.png", "right")
        self.all_notes.add(blue_right_note)

    def spawn_red_left_note(self):
        red_left_note = Note(self, "red_note.png", "left")
        self.all_notes.add(red_left_note)

    def spawn_blue_left_note(self):
        blue_left_note = Note(self, "blue_note.png", "left")
        self.all_notes.add(blue_left_note)

    def spawn_red_up_note(self):
        red_up_note = Note(self, "red_note.png", "up")
        self.all_notes.add(red_up_note)

    def spawn_blue_up_note(self):
        blue_up_note = Note(self, "blue_note.png", "up")
        self.all_notes.add(blue_up_note)

    def spawn_red_down_note(self):
        red_down_note = Note(self, "red_note.png", "down")
        self.all_notes.add(red_down_note)

    def spawn_blue_down_note(self):
        blue_down_note = Note(self, "blue_note.png", "down")
        self.all_notes.add(blue_down_note)

    def time(self):
        # en s, et musique n'est pas égale exactement à 98s donc int()
        self.entire_music_time = int(pygame.mixer.Sound.get_length(music_setup))
        # en ms
        self.music_elapsed = round(pygame.mixer.music.get_pos() / 1000, 2)
        self.difference = self.entire_music_time - self.music_elapsed
        #print(self.entire_music_time)
        #print(self.music_elapsed)
        print(self.difference)

    def tutorial(self):
        # level design
        self.counter += 1
        if self.counter < 2:
            self.spawn_red_right_note()
        # décompte, puisqu'on part de la longueur de la musique
        if self.difference == 97 or self.difference == 97.01:
            self.spawn_blue_right_note()
        if self.difference == 96 or self.difference == 96.01:
            self.spawn_red_left_note()
        if self.difference == 95 or self.difference == 95.01:
            self.spawn_blue_left_note()
        if self.difference == 94 or self.difference == 94.01:
            self.spawn_red_right_note()
        if self.difference == 93 or self.difference == 93.01:
            self.spawn_blue_left_note()
        if self.difference == 92 or self.difference == 92.01:
            self.spawn_red_left_note()
            self.spawn_red_right_note()
        if self.difference == 91 or self.difference == 91.01:
            self.spawn_blue_up_note()
        if self.difference == 90 or self.difference == 90.01:
            self.spawn_red_down_note()
        if self.difference == 88 or self.difference == 88.01:
            self.spawn_blue_right_note()
            self.spawn_blue_up_note()
        if self.difference == 87 or self.difference == 87.01:
            self.spawn_red_left_note()
            self.spawn_red_down_note()

    def check_collision(self, sprite, Group):
        return pygame.sprite.spritecollide(sprite, Group, False, pygame.sprite.collide_mask)

    def update(self, screen):
        # character.default_state utilise l'état, et blit = block image transfer
        screen.blit(self.player.image, self.player.rect)

        for Note in self.all_notes:
            Note.forward_right()
            Note.forward_left()
            Note.forward_up()
            Note.forward_down()

        #print(self.all_notes)
        self.all_notes.draw(screen)

        if self.other_combo == 3:
            screen.blit(max_combo_text, (150, 0))

    def combo_increase(self):
        self.combo = str(self.other_combo)
        self.combo_text = principal_font.render(self.combo, True, pygame.Color("green"))
        return self.combo_text

    def score_increase(self):
        self.score = str(self.other_score)
        self.score_text = principal_font.render(self.score, True, pygame.Color("orange"))
        return self.score_text

game = Game()

# création notes (espace total : 33 * 33, mais non espace totalement utilisé)
class Note(pygame.sprite.Sprite):
    def __init__(self, game, note, direction):
        super().__init__()
        self.game = game
        self.player = Player
        self.note_color = ""
        self.direction = ""
        self.image = pygame.image.load(note)
        # if self.image ne fonctionne pas
        if note == "red_note.png":
            self.note_color = "red"
        if note == "blue_note.png":
            self.note_color = "blue"
        self.rect = self.image.get_rect()
        self.velocity = 4
        self.slower_velocity = 2
        self.direction = direction
        if self.direction == "right":
            self.rect.x = 960
            self.rect.y = 235
        if self.direction == "left":
            self.rect.x = -70
            self.rect.y = 235
        if self.direction == "up":
            self.rect.x = 440
            self.rect.y = -30
        if self.direction == "down":
            self.rect.x = 440
            self.rect.y = 550

    def forward(self):
        #print(self.note_color)
        if self.game.check_collision(self, self.game.all_players):
            if self.game.player.player_color == self.note_color:
                # soit un multiplicateur de score maxé à 3
                if game.other_combo < 3:
                    game.other_combo += 1
                game.other_score += 1 * game.other_combo
            else:
                fail_sound.play()
                game.other_score -= 1
                game.other_combo = 0
            self.kill()

    def forward_right(self):
        if self.direction == "right":
            if not self.game.check_collision(self, self.game.all_players):
                self.rect.x -= self.velocity
            else:
                self.forward()

    def forward_left(self):
        if self.direction == "left":
            if not self.game.check_collision(self, self.game.all_players):
                self.rect.x += self.velocity
            else:
                self.forward()

    def forward_up(self):
        if self.direction == "up":
            if not self.game.check_collision(self, self.game.all_players):
                self.rect.y += self.slower_velocity
            else:
                self.forward()

    def forward_down(self):
        if self.direction == "down":
            if not self.game.check_collision(self, self.game.all_players):
                self.rect.y -= self.slower_velocity
            else:
                self.forward()

continue_menu = True

while continue_menu:
    for event in pygame.event.get():
    # appuyer sur la croix ou sur escape quitte le jeu
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        # 1er niveau
        if event.type == pygame.KEYDOWN:
            # pour certains pc sous windows 10, appuyer sur fn + f(x)
            if event.key == pygame.K_F1:
                continue_menu = False
                level_counter = 0
                # 1:31, 92 BPM
                music_setup = pygame.mixer.Sound("Sayonara Wild Heart.ogg")
                music = pygame.mixer.music.load("Sayonara Wild Heart.ogg")
                # score maximal pour ce niveau, montré lors du victory screen
                max_score = 100

    screen.blit(background, (0,0))
    screen.blit(update_fps(), (400, 0))
    # 60 fps maximum
    clock_framerate.tick(60)
    # actualisation permanente du screen
    pygame.display.flip()

background = pygame.image.load("background_with_tracks.png").convert_alpha()

pause_text = principal_font.render("Pause", True, pygame.color.Color("red"))

def maximum_score():
    # permet d'obtenir le bon format pour pouvoir blit
    other_max_score = str(max_score)
    max_score_text = principal_font.render(other_max_score, True, pygame.Color("yellow"))
    return max_score_text

victory_letter = ""

def victory_screen_letter():
    # <= 20 % du score maximal du niveau
    if game.other_score <= 0.2 * max_score:
        victory_letter = "E"
    if game.other_score > 0.2 * max_score and game.score <= 0.4 * max_score:
        victory_letter = "D"
    if game.other_score > 0.4 * max_score and game.score <= 0.6 * max_score:
        victory_letter = "C"
    if game.other_score > 0.6 * max_score and game.score <= 0.8 * max_score:
        victory_letter = "B"
    if game.other_score > 0.8 * max_score and game.score <= 0.95 * max_score:
        victory_letter = "A"
    if game.other_score > 0.95 * max_score:
        victory_letter = "S"
    victory_letter_text = principal_font.render(victory_letter, True, pygame.Color("white"))
    return victory_letter_text

# permet de jouer la musique du niveau sélectionné
pygame.mixer.music.play()

pause_canal = pygame.mixer.Channel(0)

# permet de savoir quand la musique est finie
music_end = pygame.USEREVENT + 2
pygame.mixer.music.set_endevent(music_end)

running = True
pause_state = running
pause_counter = 0

victory_screen_text = principal_font.render("Vous avez fini cette map", True, pygame.color.Color("red"))

time_elapsed = pygame.time.get_ticks()

# boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_counter += 1
                if pause_counter % 2 == 0:
                    pause_state = True
                if pause_counter % 2 == 1:
                    # enlève l'état pause
                    pause_state = False
        elif event.type == music_end:
            running = False
            victory_screen = True

    if pause_state == True:
        # utilisé pour lancer la pause music
        music_count = 0
        # applique le background sur le screen principal
        screen.blit(background, (0, 0))
        game.time()
        if level_counter == 0:
            game.tutorial()
        game.update(screen)
        game.player.change_state()
        # affiche le fps en haut à gauche de l'écran (x, y)
        screen.blit(update_fps(), (400, 0))
        # affiche le temps restant de la musique en haut à droite de l'écran
        screen.blit(music_time(), (550, 0))
        screen.blit(update_music_time_remaining(), (490, 0))
        # affiche le combo
        screen.blit(game.combo_increase(), (125, 0))
        # affiche le score
        screen.blit(game.score_increase(), (225, 0))

        pygame.mixer.music.unpause()
        pause_canal.pause()

    elif pause_state == False:
        pygame.mixer.music.pause()
        screen.blit(pause_text, (0, 0))
        pause_music = pygame.mixer.Sound("Breakfast (Pause Menu) - Friday Night Funkin' OST.ogg")
        # permet de ne jouer qu'une seule fois la musique
        while music_count < 2:
            music_count += 1
            pause_canal.play(pause_music, -1)

    clock_framerate.tick(60)
    pygame.display.flip()

victory_screen_music = pygame.mixer.music.load("Final Fantasy VII - Victory Fanfare.ogg")
pygame.mixer.music.play(-1)

background = pygame.image.load("background.png")

while victory_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()

    screen.blit(background, (0,0))
    screen.blit(game.combo_increase(), (125, 0))
    screen.blit(game.score_increase(), (225, 0))
    screen.blit(maximum_score(), (300,0))
    screen.blit(victory_screen_letter(), (650, 270))
    screen.blit(update_fps(), (400, 0))
    # affiche ce texte au milieu, puisque y = 540 / 2 = 270
    screen.blit(victory_screen_text, (300, 270))

    clock_framerate.tick(60)
    pygame.display.flip()
