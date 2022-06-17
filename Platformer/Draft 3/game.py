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
lives = 3

status = 0  # 0 = Start, 1 = Play, 2 = End

# CREATE MAP
platform_width = int(HEIGHT / TILE_SIZE) * 2
platform_height = int(WIDTH / TILE_SIZE) - 8

pos = random.randint(3, platform_width - 4)


def create_platform():
    global platform, platform_width, platform_height

    def create_row(y):
        global platform, pos

        x = 0
        x2 = -1
        reset = True
        while reset:
            x = random.randint(3, platform_width - 4)
            x2 = x - 3
            if pos not in [x, x - 1, x - 2, x - 3] and x2 > 0:
                reset = False

        platform[y][x2: x] = 0, 0, 0

        if y == 2:
            x4 = random.randint(3, platform_width - 1)
            while x4 in [x, x - 1, x - 2, x - 3]:
                x4 = random.randint(3, platform_width - 4)
            platform[y - 1][x4] = 5
        else:
            for i in range(random.randint(1, 6)):
                x4 = random.randint(3, platform_width - 1)
                while x4 in [x, x - 1, x - 2, x - 3]:
                    x4 = random.randint(3, platform_width - 4)
                platform[y - 1][x4] = random.choice([6, 6, 6, 6, 0, 0, 0, 3, 3, 7])

        x3 = random.randint(3, platform_width - 1)
        while x3 in [x, x - 1, x - 2, x - 3]:
            x3 = random.randint(3, platform_width - 4)

        if y != 2:
            platform[y - 2][x3] = 2
            platform[y - 1][x3] = 4

        pos = x3

    platform = []

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

    for y in range(11, 1, -3):
        create_row(y)

    platform[platform_height - 2][0: (platform_width - 1)] = [1]*platform_width
    platform[platform_height - 1][0: (platform_width - 1)] = [8]*platform_width



create_platform()


solid_ground = [1, 2, 4, 8]

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
    global score, lives
    global reset
    global status

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
            and platform[player_y + 2][player_x] not in [0, 8]:  # If player attempting to climb ladder,
        d_y += 1  # let him do so.

    if keyboard.right:  # If right key
        if player_x < platform_width - 2:  # and player isn't going to bash into the wall,
            d_x += 1  # move player to the right.

    if keyboard.left:  # If left key
        if player_x > 0:  # and player isn't going to bash into the wall,
            d_x -= 1  # move player to the left.

    if keyboard.space and platform[player_y][player_x] == 3:  # If space and player standing on coin,
        platform[player_y][player_x] = 0  # let player take coin,
        score += 1  # score a point,
        sounds.combine.play()  # and run a sound effect.

    if keyboard.space and platform[player_y][player_x] == 7:  # If space and player standing on heart,
        platform[player_y][player_x] = 0  # let player take heart,
        lives += 1
        score += 1  # score a point,
        sounds.pickup.play()  # and run a sound effect.

    if platform[player_y][player_x] == 6:  # If player standing on spike,
        sounds.ouch.play()  # run a sound effect,
        lives -= 1  # remove a live
        if score > 0:  # and remove a point if possible.
            score -= 1

    if platform[player_y][player_x] == 5:  # If space and player standing on portal,
        create_platform()  # portal away!
        sounds.doors.play()
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

    if lives <= 0:
        clock.unschedule(update_player)
        status = 2
        clock.schedule_interval(start, 0.01)


    pass


image = {1: images.block,
            3: images.coin,
            4: images.ladder,
            5: images.portal,
            6: images.spike,
            7: images.heart,
            8: images.block2,
            9: images.virus}


def draw():
    global status

    if status == 0:
        screen.fill(BLACK)

        draw_image(images.app, 1050, 600)
        show_text("press space to play", 760, 605, WHITE, 35)


    elif status == 1:
        screen.fill(BLUE)

        show_text(" X " + str(score), 1550, 20, YELLOW, 75)
        draw_image(image[3], 1550, 90)

        show_text(" X " + str(lives), 400, 20, RED, 75)
        draw_image(image[7], 400, 90)


        for y in range(0, platform_height):
            for x in range(0, platform_width):
                if platform[y][x] in image:
                    draw_image(image[platform[y][x]], x*TILE_SIZE, y*TILE_SIZE)

            if player_y == y:
                draw_player()

    elif status == 2:
        screen.fill(BLACK)
        show_text("GAME OVER", 600, 125, RED, 120)
        show_text("  try again? \npress space", 790, 200, WHITE, 40)

        show_text(" X " + str(score), 835, 500, YELLOW, 75)
        draw_image(image[3], 835, 550)

        show_text(" X " + str(lives), 835, 400, RED, 75)
        draw_image(image[7], 835, 450)

        show_text(" +__________ ", 685, 525, WHITE, 80)

        show_text(" X " + str(score*10 + lives*5), 835, 650, YELLOW, 75)
        draw_image(image[3], 835, 700)





def start():
    global status, platform
    global score, lives, player_x, player_y

    if keyboard.space and status in [0, 2]:
        status = 1

        score = 0
        lives = 3
        player_x = 0
        player_y = 10

        clock.schedule_interval(update_player, 0.075)
        clock.unschedule(start)
        create_platform()



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

clock.schedule_interval(start, 0.01)


pgzrun.go()