import pygame
from pygame.locals import K_ESCAPE
import constant
import colours
import math
from monster import Monster
from player import Player

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W = screen.get_width()
SCREEN_H = screen.get_height()
clock = pygame.time.Clock()

running = True
last_time = pygame.time.get_ticks()

# create player at center of screen

def in_circle(player, circle_radius):
    return math.sqrt((player.x - SCREEN_W / 2) ** 2 + (player.y - SCREEN_H / 2) ** 2) < circle_radius

loop_num = 2

while running:
    if loop_num == 0:
        p = Player(SCREEN_W / 2, SCREEN_H / 2, 5, colours.GREEN)
    elif loop_num == 1:
        p = Player(SCREEN_W / 2, SCREEN_H / 2, 5, colours.TEAL)
    else:
        p = Player(SCREEN_W / 2, SCREEN_H / 2, 5, colours.ORANGE)
        
    m = Monster(SCREEN_W / 2, SCREEN_H / 2 + constant.CIRCLE_RADIUS, SCREEN_W / 2, SCREEN_H / 2, 8, colours.RED)

    # reset background
    screen.fill(colours.BLACK)
    pygame.draw.circle(screen, colours.WHITE, (SCREEN_W / 2, SCREEN_H / 2), 5, 5)
    pygame.draw.circle(screen, colours.WHITE, (SCREEN_W / 2, SCREEN_H / 2), constant.CIRCLE_RADIUS, 2)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        time_delta = pygame.time.get_ticks() - last_time
        last_time = pygame.time.get_ticks()

        if loop_num == 0:
            p.move(time_delta, m.x, m.y, "normal")
        elif loop_num == 1:
            p.move(time_delta, m.x, m.y, "skilled")
        else: 
            p.move(time_delta, m.x, m.y, "pro")

        m.move(time_delta, p.x, p.y)

        # draw player and monster
        p.draw(screen)
        m.draw(screen)

        pygame.display.flip()

        clock.tick(constant.FPS)

        if not in_circle(p, constant.CIRCLE_RADIUS):
            loop_num = (loop_num + 1) % 3
            distance_from_monster = math.sqrt((p.x - m.x) ** 2 + (p.y - m.y) ** 2)
            print("Remaining distance: ", distance_from_monster)
            break


pygame.quit()
