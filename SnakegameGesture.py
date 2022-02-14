# Importing Libraries
import pygame
import random
import cv2
import mediapipe as mp

# Starting pygame
pygame.init()

# Colour Codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
hybrid = (23, 234, 223)
BGCOLOR = (0, 0, 0)

# Setting Window width, height, fps and level
WINDOWWIDTH = 1080
WINDOWHEIGHT = 720
FPS = 60
LEVEL = 10

# Importing background images and resizing
starting_bg = pygame.image.load("4.jpg")
starting_bg = pygame.transform.scale(starting_bg, (WINDOWWIDTH, WINDOWHEIGHT))
ending_bg = pygame.image.load("7.jpg")
ending_bg = pygame.transform.scale(ending_bg, (WINDOWWIDTH, WINDOWHEIGHT))

# Importing game sounds
APPLE_EAT_SOUND = pygame.mixer.Sound(r"sounds/appleEatSound.wav")
GAME_OVER = pygame.mixer.Sound(r"sounds/gameover.wav")
pygame.mixer.music.load(r"sounds/bgmusic.mid")

# Making Window and setting font and clock
Snake_Window = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption("Snake_game")
pygame.display.update()
CLOCK = pygame.time.Clock()


def write(text, font, size, color, x, y):
    title_font = pygame.font.Font(font, size)
    titleText = title_font.render(text, True, color)
    Snake_Window.blit(titleText, (x, y))


def create_body(window, color, Snake_list, Snake_Size):
    for x, y in Snake_list:
        pygame.draw.rect(window, color, [x, y, Snake_Size, Snake_Size], border_radius=15)


def starting(window, bg):
    pygame.mixer.music.play(-1, 0.0)
    window.blit(bg, (0, 0))
    write("Name ", 'freesansbold.ttf', 30, DARKGREEN, 100, 500)


def ending(window, bg, score):
    pygame.mixer.music.stop()
    window.blit(bg, (0, 0))
    write("Game Over", 'freesansbold.ttf', 100, GREEN, WINDOWWIDTH / 2 - 270, 330)
    write(f"Total Score: %s" % score, 'freesansbold.ttf', 40, GREEN, WINDOWWIDTH / 2 - 130, 250)


def grid(color, width, height):
    for x in range(0, width, 30):
        pygame.draw.line(Snake_Window, color, (x, 0), (x, height))
    for y in range(0, height, 30):
        pygame.draw.line(Snake_Window, color, (0, y), (width, y))


def Game_loop():
    # Game bool
    starting_screen = True
    game_exit = False
    game_over = False

    # loop variables
    Snake_head_x = random.randint(2, 34) * 30
    Snake_head_y = random.randint(2, 23) * 30
    Score = 0
    Food_x = random.randint(2, 34) * 30
    Food_y = random.randint(2, 23) * 30
    Speed_x = 0
    Speed_y = 0
    Snake_Size = 30
    Snake_list = []
    Snake_length = 1

    # Starting camera input
    cam = cv2.VideoCapture(0)
    mp_hand = mp.solutions.hands
    mpHands = mp_hand.Hands()

    # Creating input text box
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    input_rect = pygame.Rect(200, 500, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive

    # Start button
    start_rect = pygame.Rect(100, 600, 140, 32)
    exit_rect1 = pygame.Rect(250, 600, 140, 32)
    playagain_rect = pygame.Rect(350, 500, 140, 32)
    exit_rect2 = pygame.Rect(550, 500, 140, 32)

    # Game loop
    while not game_exit:

        if starting_screen:

            # Starting screen
            starting(Snake_Window, starting_bg)
            pygame.display.update()

            # Checking for keyboard inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        color = color_active
                    else:
                        color = color_passive
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        starting_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rect1.collidepoint(event.pos):
                        game_exit = True

                if event.type == pygame.KEYDOWN:

                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]

                    # Unicode standard is used for string
                    # formation
                    else:
                        user_text += event.unicode

            # draw rectangle and argument passed which should be on screen
            pygame.draw.rect(Snake_Window, color, input_rect)
            pygame.draw.rect(Snake_Window, color, start_rect)
            pygame.draw.rect(Snake_Window, color, exit_rect1)

            text_surface1 = base_font.render(user_text, True, (255, 255, 255))
            text_surface2 = base_font.render("Start Game !", True, (255, 255, 255))
            text_surface3 = base_font.render("       Exit", True, (255, 255, 255))

            # render at position stated in arguments
            Snake_Window.blit(text_surface1, (input_rect.x + 5, input_rect.y + 5))
            Snake_Window.blit(text_surface2, (start_rect.x, start_rect.y))
            Snake_Window.blit(text_surface3, (exit_rect1.x, exit_rect1.y))

            # set width of textfield so that text cannot get outside of user's text input
            input_rect.w = max(100, text_surface1.get_width() + 10)

            # display.flip() will update only a portion of the screen to updated
            pygame.display.flip()

        elif game_over:

            # Game over screen
            ending(Snake_Window, ending_bg, Score)
            pygame.display.update()

            # Checking for keyboard inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playagain_rect.collidepoint(event.pos):
                        Game_loop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rect2.collidepoint(event.pos):
                        game_exit = True

            pygame.draw.rect(Snake_Window, GREEN, playagain_rect)
            pygame.draw.rect(Snake_Window, GREEN, exit_rect2)

            text_surface4 = base_font.render("Play Again !", True, (255, 255, 255))
            text_surface5 = base_font.render("Exit", True, (255, 255, 255))

            # render at position stated in arguments
            Snake_Window.blit(text_surface4, (playagain_rect.x, playagain_rect.y))
            Snake_Window.blit(text_surface5, (exit_rect2.x, exit_rect2.y))

            pygame.display.update()

        else:
            with open("highscore.txt", mode="r") as file:
                hi_score = int(file.readlines()[1])
            if Score > hi_score:
                hi_score = Score
                with open("highscore.txt", mode="w") as file:
                    file.write(user_text + "\n")
                    file.write(str(Score) + "\n")

            if Score <= 20:
                LEVEL = 10
                snake_head = pygame.image.load("3.jpg")
            elif Score <= 40:
                LEVEL = 15
                snake_head = pygame.image.load("0.jpg")
            elif Score <= 60:
                LEVEL = 20
                snake_head = pygame.image.load("1.jpg")
            elif Score <= 80:
                LEVEL = 30
                snake_head = pygame.image.load("2.jpg")
            else:
                LEVEL = 40
                snake_head = pygame.image.load("5.jpg")

            snake_head = pygame.transform.scale(snake_head, (30, 30))

            # Processing input from camera
            success, image = cam.read()
            img = cv2.flip(image, 1)
            image = cv2.resize(img, (600, 600))
            output = mpHands.process(image)

            # Detecting hands
            if output.multi_hand_landmarks:
                for landmarks in output.multi_hand_landmarks:

                    # Checking for id 8 in landmarks of one hand
                    for id_, pos in enumerate(landmarks.landmark):
                        height, width, z = image.shape
                        pos_x, pos_y = int(width * pos.x), int(height * pos.y)

                        # Drawing circles for reference
                        if id_ == 8:
                            cv2.circle(image, (300, 300), 500, DARKGREEN, cv2.FILLED)
                            cv2.circle(image, (300, 300), 30, RED, cv2.FILLED)
                            cv2.circle(image, (pos_x, pos_y), 25, hybrid, cv2.FILLED)

                            # Checking for Gesture inputs
                            if pos_x > 350 > pos_y > 250 and Speed_x != -LEVEL and Snake_head_y % 30 == 0:
                                Speed_x = LEVEL
                                Speed_y = 0
                            if pos_x < 250 < pos_y < 350 and Speed_x != LEVEL and Snake_head_y % 30 == 0:
                                Speed_x = -LEVEL
                                Speed_y = 0
                            if pos_y < 250 < pos_x < 350 and Speed_y != LEVEL and Snake_head_x % 30 == 0:
                                Speed_y = -LEVEL
                                Speed_x = 0
                            if pos_y > 350 > pos_x > 250 and Speed_y != -LEVEL and Snake_head_x % 30 == 0:
                                Speed_y = LEVEL
                                Speed_x = 0

            # Checking for keyboard inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and Speed_x != LEVEL:
                        Speed_x = -LEVEL
                        Speed_y = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d and Speed_x != -LEVEL:
                        Speed_x = LEVEL
                        Speed_y = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and Speed_y != -LEVEL:
                        Speed_x = 0
                        Speed_y = LEVEL
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and Speed_y != LEVEL:
                        Speed_x = 0
                        Speed_y = -LEVEL

            # Checking food and head collision
            if abs(Snake_head_x - Food_x) < 30 and abs(Snake_head_y - Food_y) < 30:
                APPLE_EAT_SOUND.play()
                Food_x = random.randint(2, 35) * 30
                Food_y = random.randint(2, 23) * 30
                Score += 5
                Snake_length += 5

            # Updating Snake head wrt speed
            Snake_head_x += Speed_x
            Snake_head_y += Speed_y

            # Background screen
            Snake_Window.fill(BLACK)
            write('Score: ' + str(Score), 'freesansbold.ttf', 20, RED, 90, 60)
            write('High-Score: ' + str(hi_score), 'freesansbold.ttf', 20, RED, 690, 60)
            body = [Snake_head_x, Snake_head_y]
            Snake_list.append(body)

            # Detecting collision with wall
            if Snake_head_x < 0 or Snake_head_x > 1080 or Snake_head_y < 0 or Snake_head_y > 720:
                GAME_OVER.play()
                game_over = True

            # Updating snake list
            if Snake_length < len(Snake_list):
                del Snake_list[0]

            # Checking for self collision
            if body in Snake_list[:-1]:
                GAME_OVER.play()
                game_over = True

            # Drawing grid
            grid(DARKGRAY, WINDOWWIDTH, WINDOWHEIGHT)

            # Creating snake body
            create_body(Snake_Window, YELLOW, Snake_list, Snake_Size)

            # Creating food
            pygame.draw.rect(Snake_Window, GREEN, [Food_x, Food_y, Snake_Size, Snake_Size], border_radius=15)

            # Creating snake head
            pygame.draw.rect(Snake_Window, YELLOW, [Snake_head_x, Snake_head_y, Snake_Size, Snake_Size],
                             border_radius=15)

            # Drawing snake on screen
            Snake_Window.blit(snake_head, (Snake_head_x, Snake_head_y))
            pygame.display.update()

            # Initializing cv2 screen
            cv2.imshow("Snake_game Controller", image)
            cv2.waitKey(1)
            CLOCK.tick(FPS)

        pygame.display.update()
        CLOCK.tick(FPS)


# Running game loop
Game_loop()
