import pygame
import sys
import chord_story.decode_notes as dn
from pydub import AudioSegment
from pygame.locals import *
from pygame import mixer
from chord_story.Game import Game
from chord_story.Obstacle import Obstacle
from chord_story.Powerup import Powerup
from chord_story.Player import Player

# initialize display
clock = pygame.time.Clock()
pygame.init()
mixer.init()
pygame.display.set_caption("Chord Story")
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
# used as the surface for rendering, which is scaled
display = pygame.Surface((300, 200))

# initialize game and player
game = Game()
player = Player()


# opens the main menu screen
def main_menu():
    click = False
    menu_open = True

    while menu_open:

        display.fill((255, 255, 255))  # clear screen by filling it with white
        chord = pygame.image.load("assets/mainmenu.png")
        screen.blit(chord, (0, 0))

        mousex, mousey = pygame.mouse.get_pos()

        # create the classic mode button
        classic_button = pygame.Rect(50, 50, 150, 60)

        # render button
        pygame.draw.rect(screen, (156, 17, 21), classic_button)

        highlight = (232, 58, 63)

        if classic_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, classic_button)
            if click:
                # play the game if the button is pressed
                select_difficulty()
                run_game()

        classic_font = pygame.font.Font("freesansbold.ttf", 17)
        classic_text = classic_font.render(
            "CLASSIC MODE", True, (255, 255, 255))
        screen.blit(classic_text, (59, 72))

        click = False

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                menu_open = False
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# sets the difficulty level of the current game
def select_difficulty():
    click = False
    select = True

    while select:
        display.fill((224, 132, 132))  # clear screen by filling it with pink

        pinkbackground = pygame.image.load("assets/pink.png")

        screen.blit(pinkbackground, (0, 0))

        font = pygame.font.Font("freesansbold.ttf", 45)
        text = font.render("CHOOSE THE DIFFICULTY", True, (0, 0, 0))
        text2 = font.render("CHOOSE THE DIFFICULTY", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() / 2, 45))
        text_rect2 = text.get_rect(center=((screen.get_width() / 2) + 2, 47))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)

        mousex, mousey = pygame.mouse.get_pos()

        easy_button = pygame.Rect(screen.get_width() / 2 - 72.5, 100, 145, 60)
        medium_button = pygame.Rect(
            screen.get_width() / 2 - 72.5, 200, 145, 60)
        hard_button = pygame.Rect(screen.get_width() / 2 - 72.5, 300, 145, 60)

        # render buttons
        pygame.draw.rect(screen, (255, 255, 255), easy_button)
        pygame.draw.rect(screen, (255, 255, 255), medium_button)
        pygame.draw.rect(screen, (255, 255, 255), hard_button)

        highlight = (212, 221, 255)

        # harder difficult = smaller interval between notes
        if easy_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, easy_button)
            if click:
                game.difficulty = 0.5
                select = False
        if medium_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, medium_button)
            if click:
                game.difficulty = 0.35
                select = False
        if hard_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, hard_button)
            if click:
                game.difficulty = 0.25
                select = False

        # easy text
        font = pygame.font.Font("freesansbold.ttf", 35)
        text = font.render("EASY", True, (0, 0, 0))
        text2 = font.render("EASY", True, (224, 132, 132))
        screen.blit(text, (247, 116))
        screen.blit(text2, (249, 118))

        # medium text
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("MEDIUM", True, (0, 0, 0))
        text2 = font.render("MEDIUM", True, (224, 132, 132))
        screen.blit(text, (237, 216))
        screen.blit(text2, (239, 218))

        # hard text
        font = pygame.font.Font("freesansbold.ttf", 35)
        text = font.render("HARD", True, (0, 0, 0))
        text2 = font.render("HARD", True, (224, 132, 132))
        screen.blit(text, (247, 316))
        screen.blit(text2, (249, 318))

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# open the pause screen
def paused():
    click = False
    # pause_screen = True
    while game.state == "paused":

        mousex, mousey = pygame.mouse.get_pos()

        pygame.mixer.music.pause()

        # create the buttons used to get back into the game or quit
        continue_button = pygame.Rect(470, 340, 95, 50)
        quit_button = pygame.Rect(40, 340, 95, 50)

        # pause message on the screen
        pause_font = pygame.font.Font("freesansbold.ttf", 80)
        pause_text = pause_font.render("PAUSE", True, (255, 0, 0))
        text_rect = pause_text.get_rect(
            center=(screen.get_width() / 2, screen.get_height() / 2)
        )
        screen.blit(pause_text, text_rect)

        # render buttons
        pygame.draw.rect(screen, (156, 17, 21), continue_button)
        pygame.draw.rect(screen, (156, 17, 21), quit_button)

        highlight = (232, 58, 63)

        # highlight buttons on mouse hover
        if continue_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, continue_button)
            if click:
                game.state = "running"
                pygame.mixer.music.unpause()
                return
        if quit_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight, quit_button)
            if click:
                player.lives = 3
                player.score = 0
                game.obstacles.clear()
                game.powerups.clear()
                game.state = "running"
                main_menu()

        button_font = pygame.font.Font("freesansbold.ttf", 17)
        continue_text = button_font.render("CONTINUE", True, (255, 255, 255))
        quit_text = button_font.render("QUIT", True, (255, 255, 255))
        screen.blit(continue_text, (472, 355))
        screen.blit(quit_text, (65, 355))

        click = False

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                # pause_screen = False
                game.state = "exit"
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# open the restart screen
def restarting():
    click = False

    while game.state == "restarting":
        mousex, mousey = pygame.mouse.get_pos()

        # create the buttons used to get back into the game or quit
        restart_button = pygame.Rect(470, 340, 95, 50)
        quit_button = pygame.Rect(40, 340, 95, 50)

        # render buttons
        pygame.draw.rect(screen, (52, 224, 69), restart_button)
        pygame.draw.rect(screen, (156, 17, 21), quit_button)

        highlight1 = (110, 255, 124)
        highlight2 = (232, 58, 63)

        # highlight buttons on hover
        if restart_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight1, restart_button)
            if click:
                player.lives = 3
                player.score = 0
                game.state = "running"
                game.obstacles.clear()
                game.powerups.clear()
                return
        if quit_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(screen, highlight2, quit_button)
            if click:
                player.lives = 3
                player.score = 0
                game.state = "running"
                game.obstacles.clear()
                game.powerups.clear()
                main_menu()

        button_font = pygame.font.Font("freesansbold.ttf", 17)
        restart_text = button_font.render("RESTART", True, (255, 255, 255))
        quit_text = button_font.render("QUIT", True, (255, 255, 255))
        screen.blit(restart_text, (480, 355))
        screen.blit(quit_text, (65, 355))

        click = False

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                game.state = "exit"
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# check if objects are colliding
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


# move the player and ground player on string
def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False,
                       "right": False, "left": False}
    rect.x += movement[0]

    # keep player withing window bounds
    if rect.right > 299:
        rect.right = 299
    if rect.x < 0:
        rect.x = 0

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
    return rect, collision_types


# check if player has hit an obstacle
def obstacle_collision(player_rect, obstacles):
    # if collision, decrement lives
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            # TODO: add damage sound effect
            player.lives = player.lives - 1
            obstacles.remove(obstacle)
        if obstacle.rect.left < -15:
            obstacles.remove(obstacle)
        if player.lives == 0:
            game.state = "dead"


def powerup_collision(player_rect, powerups):
    for powerup in powerups:
        if player_rect.colliderect(powerup):
            if powerup.type == "life":
                # TODO: add 1up sound effect
                player.lives += 1
            if powerup.type == "phaser":
                player.powerup = "phaser"
                # TODO: add powerup sound effect
                player.img = pygame.image.load("assets/player_invincible.png").convert_alpha()
                # player.img.set_colorkey((255, 255, 255))
                pygame.time.set_timer(game.events["PHASERTIMER"], 5000, True)
            powerups.remove(powerup)
        if powerup.rect.left < -15:
            powerups.remove(powerup)


# display the game over screen
def game_over():
    mixer.music.stop()
    # TODO: add dead sound effect
    font = pygame.font.Font("freesansbold.ttf", 80)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


# display the game won screen
def game_won():
    font = pygame.font.Font("freesansbold.ttf", 80)
    text = font.render("YOU WIN", True, (0, 255, 0))
    text_rect = text.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)
    mixer.music.stop()


# update the lives displayed on screen
def update_lives():
    lives_display = pygame.Rect(20, 370, 55, 25)

    pygame.draw.rect(screen, (255, 255, 255), lives_display)

    lives_font = pygame.font.Font("freesansbold.ttf", 12)
    player_lives_str = str(player.lives)
    lives_text = lives_font.render(
        "LIVES: " + player_lives_str, True, (0, 0, 0))
    screen.blit(lives_text, (22, 375))


# update the score displayed on screen
def update_score():
    score_display = pygame.Rect(80, 370, 100, 25)

    pygame.draw.rect(screen, (255, 255, 255), score_display)

    score_font = pygame.font.Font("freesansbold.ttf", 12)
    score_str = str(player.score)
    score_text = score_font.render("SCORE: " + score_str, True, (0, 0, 0))
    screen.blit(score_text, (82, 375))


def draw_strings():
    tile_rects = []

    # draw strings
    pygame.draw.line(display, (255, 255, 255), (0, 29), (400, 29), 2)  # line 0
    tile_rects.append(pygame.Rect(0, 29, 400, 2))
    pygame.draw.line(display, (255, 255, 255), (0, 59), (400, 59), 2)  # line 1
    tile_rects.append(pygame.Rect(0, 59, 400, 2))
    pygame.draw.line(display, (255, 255, 255), (0, 89), (400, 89), 2)  # line 2
    tile_rects.append(pygame.Rect(0, 89, 400, 2))
    pygame.draw.line(display, (255, 255, 255), (0, 119), (400, 119), 2)  # line 3
    tile_rects.append(pygame.Rect(0, 119, 400, 2))
    pygame.draw.line(display, (255, 255, 255), (0, 149), (400, 149), 2)  # line 4
    tile_rects.append(pygame.Rect(0, 149, 400, 2))
    pygame.draw.line(display, (255, 255, 255), (0, 179), (400, 179), 2)  # line 5
    tile_rects.append(pygame.Rect(0, 179, 400, 2))

    return tile_rects


# main game function with loop
def run_game():
    game.state = "running"

    # initialize movement
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    # clear the board
    game.obstacles.clear()
    game.powerups.clear()

    # process the audio file
    decode = dn.decode(game.difficulty)

    # if mp3 selected, convert to a temporary wav for pygame mixer compatibility
    if decode[1].endswith(".mp3"):
        sound = AudioSegment.from_mp3(decode[1])
        sound.export(decode[1][:-4] + ".wav", format="wav")

    # load the notes and music
    notes = decode[0]
    mixer.music.load(decode[1][:-4] + ".wav")
    noteKeys = list(notes.keys())

    # deleted the temporary wav file
    if decode[1].endswith(".mp3"):
        os.remove(decode[1][:-4] + ".wav")

    # get the first note/obstacle
    noteTime = noteKeys[0]
    stringNo = notes[noteTime]

    # start the timers for game events and spawning
    pygame.time.set_timer(game.events["NEWOBSTACLE"], int(noteTime * 1000), True)
    pygame.time.set_timer(game.events["SCOREUP"], 1000)
    pygame.time.set_timer(game.events["SPAWNLIFE"], 6000, True)
    pygame.time.set_timer(game.events["SPAWNPHASER"], 10000, True)

    # start the music
    keyIndex = 0
    mixer.music.play()

    player.img.set_colorkey((255, 255, 255))

    background_rect = game.background.get_rect()

    while game.state == "running":
        display.fill((255, 255, 255))  # clear screen by filling it with white

        # scrolling background
        display.blit(game.background, background_rect)  # left image
        display.blit(
            game.background, background_rect.move(background_rect.width, 0)
        )  # right image
        if game.state == "running":
            background_rect.move_ip(-1, 0)
        if background_rect.right == 0:
            background_rect.x = 0

        # draw the guitar strings to screen
        tile_rects = draw_strings()

        # move obstacles and other objects across screen
        for obstacle in game.obstacles:
            if game.state == "running":
                obstacle.rect.x -= 2
            pygame.draw.rect(display, (255, 255, 255), obstacle.rect)

        for powerup in game.powerups:
            if game.state == "running":
                powerup.rect.x -= 2
            pygame.draw.rect(display, powerup.color, powerup.rect)

        player_movement = [0, 0]

        # move player
        if game.state == "running":
            if moving_right == True:
                player_movement[0] += 2
            if moving_left == True:
                player_movement[0] -= 2
            player_movement[1] += vertical_momentum
            vertical_momentum += 0.2
            if vertical_momentum > 3:
                vertical_momentum = 3

        # check for collisions and grounding
        player.rect, collisions = move(player.rect, player_movement, tile_rects)

        # death if collision with obstacle
        # player passes through and ignores obstacles if possessing phaser ability
        if player.powerup != "phaser":
            obstacle_collision(player.rect, game.obstacles)

        powerup_collision(player.rect, game.powerups)

        for event in pygame.event.get():  # event loop

            # quit on x clicked
            if event.type == QUIT:
                game.state == "exit"
                play_game = False
                pygame.quit()
                sys.exit()

            if game.state == "running":
                # move player
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        game.state = "paused"
                        paused()
                    if event.key == K_RIGHT:
                        moving_right = True
                    if event.key == K_LEFT:
                        moving_left = True
                    if event.key == K_UP:
                        if air_timer < 6:
                            vertical_momentum = -3
                    if event.key == K_DOWN:
                        if air_timer < 6:
                            vertical_momentum = 3
                        player.rect.y += 12
                        if player.rect.y > 166:
                            player.rect.y = 166

                # stop moving on release
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        moving_right = False
                    if event.key == K_LEFT:
                        moving_left = False

                # spawn a new obstacle
                if event.type == game.events["NEWOBSTACLE"]:
                    obstacle = Obstacle(stringNo)
                    game.obstacles.append(obstacle)

                    keyIndex = keyIndex + 1

                    # if end of song, win
                    if keyIndex > len(noteKeys) - 1:
                        game.state = "won"
                        break

                    noteTime = noteKeys[keyIndex]

                    noteDiffTime = noteKeys[keyIndex] - noteKeys[keyIndex - 1]
                    stringNo = notes[noteTime]

                    # set the timer to spawn the next obstacle
                    pygame.time.set_timer(game.events["NEWOBSTACLE"], int(noteDiffTime * 1000), True)

                # increase the score every second; higher difficulty = greater increment
                if event.type == game.events["SCOREUP"]:
                    player.score += (1 - game.difficulty) * 20

                # spawn a life every minute
                if event.type == game.events["SPAWNLIFE"]:
                    life = Powerup("life", (0, 128, 0))
                    game.powerups.append(life)
                    pygame.time.set_timer(game.events["SPAWNLIFE"], 6000, True)

                # spawn a phaser powerup
                if event.type == game.events["SPAWNPHASER"]:
                    phaser = Powerup("phaser", (0, 255, 255))
                    game.powerups.append(phaser)
                    pygame.time.set_timer(game.events["SPAWNPHASER"], 10000, True)

                # phaser powerup lasts for 5s
                if event.type == game.events["PHASERTIMER"] and player.powerup == "phaser":
                    player.powerup = None
                    player.img = pygame.image.load("assets/player.png").convert()
                    player.img.set_colorkey((255, 255, 255))

        display.blit(player.img, (player.rect.x, player.rect.y))

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))

        # display the lives and score
        update_lives()
        update_score()

        # dead - game over screen; restart level or quit
        if game.state == "dead":
            game_over()
            game.state = "restarting"
            restarting()

            noteTime = noteKeys[0]
            stringNo = notes[noteTime]

            pygame.time.set_timer(game.events["NEWOBSTACLE"], int(noteTime * 1000), True)

            keyIndex = 0
            mixer.music.play()

        # win - show game win screen; start new level or quit
        if game.state == "won":
            game_won()
            game.state = "restarting"
            restarting()
            # game.state == "running"
            game.obstacles.clear()
            game.powerups.clear()

            noteTime = noteKeys[0]
            stringNo = notes[noteTime]

            pygame.time.set_timer(game.events["NEWOBSTACLE"], int(noteTime * 1000), True)

            keyIndex = 0
            mixer.music.play()

        pygame.display.update()
        clock.tick(120)
