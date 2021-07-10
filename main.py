import os
import random
import pygame
import pygame_menu

songs_path = os.getcwd() + '/songs'

mode = (1280, 720)

pygame.init()
surface = pygame.display.set_mode(mode)
font = pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30)


def random_color():
    return random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)


def wait_key_press(key=None):
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if key is not None:
                    if evt.key == key:
                        return
                else:
                    return


def write_text(text, bg_color=None):
    f = font.render(text, True, (255, 255, 255))
    f_esc = font.render('Pressione qualquer tecla para continuar', True, (255, 255, 255))

    surface.fill(bg_color or random_color())
    surface.blit(f, (int((mode[0] - f.get_width()) / 2),
                     int(mode[1] / 2 - f.get_height())))
    surface.blit(f_esc, (int((mode[0] - f_esc.get_width()) / 2),
                         int(mode[1] / 2 + f_esc.get_height())))
    pygame.display.flip()
    wait_key_press()


def create_main_menu():
    menu = pygame_menu.Menu('Escolha a dificuldade!', mode[0], mode[1],
                            theme=pygame_menu.themes.THEME_BLUE)

    [menu.add.button(level, play_song, level) for level in os.listdir(songs_path)]
    menu.add.button('Sair', pygame_menu.events.EXIT)

    return menu


def display_main_menu():
    create_main_menu().mainloop(surface)


def on_choose_song(playing_song, chosen_song):
    if playing_song == chosen_song:
        write_text('Yoohoo, Você acertou!')
    else:
        write_text('Oh nooo! Errou, tente novamente!')

    pygame.mixer.music.stop()
    display_main_menu()


def create_song_choice_menu(playing_song, folder):
    chosen_songs = [playing_song.replace('.mp3', '')]
    folder_songs = os.listdir(folder)
    total_folder_songs = len(folder_songs)
    folder_songs.remove(playing_song)

    while len(chosen_songs) <= 4 or len(chosen_songs) == total_folder_songs:
        next_song = random.choice(folder_songs)
        folder_songs.remove(next_song)
        chosen_songs.append(next_song.replace('.mp3', ''))

    chosen_songs.sort()

    menu = pygame_menu.Menu('Qual musica está tocando?', mode[0], mode[1],
                            theme=pygame_menu.themes.THEME_BLUE)

    [menu.add.button(song, on_choose_song, playing_song.replace('.mp3', ''), song) for song in chosen_songs]

    return menu


def display_song_choice_menu(playing_song, folder):
    create_song_choice_menu(playing_song, folder).mainloop(surface)


def play_song(folder):
    level_path = f'{songs_path}/{folder}'

    song = random.choice(os.listdir(level_path))
    pygame.mixer.init()
    pygame.mixer.music.load(f'{level_path}/{song}')
    pygame.mixer.music.play()
    display_song_choice_menu(song, level_path)


def start_game():
    display_main_menu()


start_game()
