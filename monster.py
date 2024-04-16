import pygame
import math
import constant

class Monster(pygame.sprite.Sprite):

    def __init__(self, x, y, center_x, center_y, radius, colour):
        super().__init__()
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.surf = pygame.Surface(
            (self.radius * 2, self.radius * 2), flags=pygame.SRCALPHA)
        self.rect = self.surf.get_rect(
            topleft=(x - self.radius, y - self.radius))
        self.colour = colour

    def move(self, time_delta, player_x, player_y):
        # find projection of player onto circle
        player_angle = math.atan2(player_y - self.center_y, player_x - self.center_x)

        # find current angle
        current_angle = math.atan2(self.y - self.center_y, self.x - self.center_x)

        # move monster along circle in direction of player
        # check if need to move
        if player_angle > current_angle or player_angle < 0 and current_angle > 0:
            current_angle += constant.MONSTER_SPEED * constant.SPEED_MULT * time_delta / 1000 / constant.CIRCLE_RADIUS
            if current_angle >= math.pi:
                current_angle -= 2 * math.pi

            self.x = self.center_x + constant.CIRCLE_RADIUS * math.cos(current_angle)
            self.y = self.center_y + constant.CIRCLE_RADIUS * math.sin(current_angle)

            self.rect.x = self.x - self.radius
            self.rect.y = self.y - self.radius

    def draw(self, screen):
        self.surf.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.circle(self.surf, self.colour,
                           (self.radius, self.radius), self.radius)
        screen.blit(self.surf, self.rect)
