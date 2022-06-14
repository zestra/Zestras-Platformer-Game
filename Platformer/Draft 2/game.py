import pygame, pgzero, pgzrun
import math, random

BLACK = (0, 0, 0)
BLUE = (0, 155, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (128, 0, 0)

DARK_BLUE = (0, 100, 200)
BRIGHT_BLUE = (100, 255, 355)
PALE_BLUE = (0, 35, 135)

DARK_GREY = (50, 50, 50)
DARKER_GREY = (10, 10, 10)

WIDTH = 1920
HEIGHT = 1050

top_left_x = 90
top_left_y = 0

TILE_SIZE = 90

# PLAYER

player_image = random.choice([images.red, images.green, images.blue])
player_x = 0
player_y = 10
score = 0

# CREATE MAP
ladder_pos = 0


def create_platform():
    global platform, platform_width, platform_height

    def create_row(y):
        global platform, ladder_pos

        x = 0
        x2 = -100
        while 0 > x2 \
                and (ladder_pos + 1) not in range(x2 - 1, x + 1) \
                and 0 < ladder_pos:
            x = random.randint(3, platform_width - 4)
            x2 = x - 3

        if y != 1:
            platform[y][x + 1] = 3
        else:
            platform[y][x + 1] = 5

        platform[y + 1][x2: x] = 0, 0, 0

        if x + 1 < platform_width:
            platform[y + 2][x + 1] = 2
            platform[y + 3][x + 1] = 4
        else:
            platform[y + 2][x] = 2
            platform[y + 3][x] = 4

        ladder_pos = x + 1

    platform = []

    platform_width = int(HEIGHT / TILE_SIZE) * 2
    platform_height = int(WIDTH / TILE_SIZE) - 8

    for y in range(0, platform_height, 3):
        platform.append([])
        for x in range(0, platform_width):
            platform[len(platform) - 1].append(0)

        platform.append([])
        for x in range(0, platform_width):
            platform[len(platform) - 1].append(0)

        platform.append([])
        for x in range(0, platform_width):
            platform[len(platform) - 1].append(1)

    ladder_pos = 0
    for y in range(1, 11, 3):
        create_row(y)

    platform[platform_height - 2][0: (platform_width - 1)] = [1]*platform_width

    # platform[1][7] = 3
    # platform[2][y3: x3] = 0, 0, 0
    # platform[3][7] = 2
    # platform[4][7] = 4
    #
    # platform[4][9] = 3
    # platform[5][10: 13] = 0, 0, 0
    # platform[6][9] = 2
    # platform[7][9] = 4
    #
    # platform[7][7] = 3
    # platform[8][3: 6] = 0, 0, 0
    # platform[9][7] = 2
    # platform[10][7] = 4


create_platform()


solid_ground = [1, 2, 4]

falling = False
reset = False


def show_map():
    for y in range(0, platform_height):
        for x in range(0, platform_width):
            print(platform[y][x], end=" ")
        print()


show_map()


def update_player():
    global falling
    global player_x, player_y
    global platform
    global score
    global reset

    d_y = 0
    d_x = 0

    if platform[player_y + 1][player_x] in solid_ground:  # If the player is standing on solid ground,
        falling = False  # he shall not fall.
    else:
        falling = True  # Otherwise, he will fall.

    if falling:  # If player is falling,
        d_y += 1  # simulate it!

    if keyboard.up \
        and (platform[player_y][player_x] in [2, 4]
             or platform[player_y + 1][player_x] in [2, 4]):  # If player attempting to climb ladder,
        d_y -= 1  # let him do so.
    elif keyboard.up \
            and keyboard.rshift\
            and platform[player_y - 1][player_x] not in solid_ground\
            and platform[player_y + 1][player_x] in solid_ground:  # Otherwise, if player attempting to jump,
        d_y -= 1  # simulate it!

        # Additional Commands to Edit Jump! >>>
        if keyboard.space and platform[player_y - 2][player_x] not in solid_ground:
            d_y -= 2
        if keyboard.left:
            d_x -= 2
        if keyboard.right:
            d_x += 2

    if keyboard.down \
            and platform[player_y + 1][player_x] in [1, 2, 4] \
            and platform[player_y + 2][player_x] != 0:  # If player attempting to climb ladder,
        d_y += 1  # let him do so.

    if keyboard.right:  # If right key
        if player_x < platform_width - 2:  # and player isn't going to bash into the wall,
            d_x += 1  # move player to the right.

    if keyboard.left:  # If left key
        if player_x > 0:  # and player isn't going to bash into the wall,
            d_x -= 1  # move player to the left.

    if keyboard.space and platform[player_y][player_x] == 3:  # If space and player standing on coin,
        platform[player_y][player_x] = 0  # let player take coin,
        score += 1  # and score a point.

    if platform[player_y][player_x] == 5:  # If space and player standing on portal,
        create_platform()  # portal away!
        reset = True

    if reset:
        clock.unschedule(update_player)
        player_x = 0
        player_y = 10
        clock.schedule_interval(update_player, 0.075)
        reset = False

    else:
        player_y += d_y
        player_x += d_x
        reset = False

    pass


def draw():
    screen.fill(BLUE)

    show_text("SCORE: " + str(score), 1550, 20, WHITE, 75)


    for y in range(0, platform_height):
        for x in range(0, platform_width):
            if platform[y][x] == 1:
                draw_image(images.block, x*TILE_SIZE, y*TILE_SIZE)
            elif platform[y][x] == 3:
                draw_image(images.coin, x * TILE_SIZE, y * TILE_SIZE)
            elif platform[y][x] == 4:
                draw_image(images.ladder, x*TILE_SIZE, y*TILE_SIZE)
            elif platform[y][x] == 5:
                draw_image(images.portal, x*TILE_SIZE, y*TILE_SIZE)

        if player_y == y:
            draw_player()


def draw_player():
    draw_image(player_image, player_x*TILE_SIZE, player_y*TILE_SIZE)


def draw_image(image, x, y):
    screen.blit(image,
                (top_left_x + x - image.get_width(),
                 top_left_y + y - image.get_height()))


def draw_rect(x, y,
              width, height,
              colour=BLACK,
              outline=None):
    if outline is not None:
        BOX2 = Rect((top_left_x + x - int(width / 2) - 2, top_left_y + y - int(height / 2) - 2),
                    (width + 4, height + 4)
                    )
        screen.draw.rect(BOX2, outline)

    if colour is not None:
        BOX = Rect((top_left_x + x - int(width / 2), top_left_y + y - int(height / 2)),
                   (width, height)
                   )
        screen.draw.filled_rect(BOX, colour)


def show_text(text_to_show, x, y,
              colour=WHITE,
              size=75):
    screen.draw.text(text_to_show,
                     (top_left_x + x, top_left_y + y),
                     fontsize=size, color=colour)

clock.schedule_interval(update_player, 0.075)
pgzrun.go()