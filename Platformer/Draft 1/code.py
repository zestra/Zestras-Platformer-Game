import pygame, pgzero, pgzrun


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

# top_left_x = WIDTH / 2
# top_left_y = HEIGHT / 2

top_left_x = 90
top_left_y = 0

TILE_SIZE = 90

# CREATE MAP

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

platform[1][7] = 3
platform[2][8: 11] = 0, 0, 0
platform[4][7] = 2

platform[4][9] = 3
platform[5][10: 13] = 0, 0, 0
platform[7][9] = 2

platform[7][7] = 3
platform[8][3: 6] = 0, 0, 0
platform[10][7] = 2


player_y = 10
player_x = 1

player_images = [images.walk, images.left_climb, images.right_climb]
player_image = 0


falling = False


def show_map():
    for y in range(0, platform_height):
        for x in range(0, platform_width):
            print(platform[y][x], end=" ")
        print()


show_map()


def player_update():
    global player_x, player_y
    global player_image
    global platform
    global falling

    if keyboard.right and platform[player_y + 1][player_x] == 1:
        if player_x < platform_width - 2:
            player_x += 1
        else:
            player_x = platform_width - 2

        player_image = 0

    if keyboard.left and platform[player_y + 1][player_x] == 1:
        if player_x > 0:
            player_x -= 1
        else:
            player_x = 0

        player_image = 0

    if (keyboard.up and platform[player_y][player_x] == 2)\
            or (keyboard.up and platform[player_y + 1][player_x] == 2)\
            or (keyboard.up and platform[player_y + 2][player_x] == 2):
        player_y -= 1

        if player_image == 2:
            player_image = 1
        else:
            player_image = 2

    elif keyboard.up and falling == False:
        player_y -= 1

        if player_x < platform_width - 3:
            if keyboard.right:
                player_x += 3

        if player_x > 2:
            if keyboard.left:
                player_x -= 3

    if (keyboard.down and platform[player_y][player_x] == 2) \
            or (keyboard.down and platform[player_y + 1][player_x] == 2)\
            or (keyboard.down and platform[player_y + 2][player_x] == 2)\
            or (keyboard.down and platform[player_y + 3][player_x] == 2):
        player_y += 1

        if player_image == 2:
            player_image = 1
        else:
            player_image = 2

    if (platform[player_y + 1][player_x] == 0) \
        and (platform[player_y + 2][player_x] != 2 \
        and platform[player_y + 3][player_x] != 2):
        player_y += 1
        falling = True
    else:
        falling = False

    if keyboard.c and platform[player_y][player_x] == 3:
        platform[player_y][player_x] = 0
        sounds.hi.play()


def draw():
    screen.fill(BLUE)


    for y in range(0, platform_height):
        for x in range(0, platform_width):
            if platform[y][x] == 1:
                draw_image(images.block2, x*TILE_SIZE, y*TILE_SIZE)
            elif platform[y][x] == 2:
                draw_image(images.ladder3, x*TILE_SIZE, y*TILE_SIZE)
            elif platform[y][x] == 3:
                draw_image(images.coin, x * TILE_SIZE, y * TILE_SIZE)

        if player_y == y:
            draw_player()


def draw_player():
    draw_image(player_images[player_image], player_x * TILE_SIZE, player_y * TILE_SIZE)


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

clock.schedule_interval(player_update, 0.075)
pgzrun.go()