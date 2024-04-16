import pygame
import math
import constant

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, colour):
        super().__init__()
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.radius = radius
        self.rotation_r = -1
        self.done_rotating = False
        self.surf = pygame.Surface(
            (self.radius * 2, self.radius * 2), flags=pygame.SRCALPHA)
        self.rect = self.surf.get_rect(
            topleft=(x - self.radius, y - self.radius))
        self.colour = colour

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.done_rotating = False
        self.rotation_r = -1

    def move(self, time_delta, monster_x, monster_y, mode="normal"):
        r = math.sqrt((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2)
        inner_radius = constant.CIRCLE_RADIUS * constant.PLAYER_SPEED / constant.MONSTER_SPEED

        vx = 0
        vy = 0
        if mode == "normal":
            vy = self._normal_move()
        
        elif mode == "skilled":
            if r + 1 < inner_radius: 
                vy = self._normal_move()
            else:
                if not self.monster_is_opposite(monster_x, monster_y) and not self.done_rotating:
                    # perform inner rotation away from monster
                    vx = 0
                    vy = 0
                    self.rotation_r = r
                    self._inner_rotation(time_delta)
                else:
                    # move towards edge
                    self.done_rotating = True
                    current_angle = math.atan2(self.y - self.start_y, self.x - self.start_x)
                    vx = math.cos(current_angle) * constant.PLAYER_SPEED * constant.SPEED_MULT
                    vy = math.sin(current_angle) * constant.PLAYER_SPEED * constant.SPEED_MULT

        else:
            if r + 1 < inner_radius: 
                vy = self._normal_move()
            else:
                if not self.monster_is_opposite(monster_x, monster_y) and not self.done_rotating:
                    # perform inner rotation away from monster
                    vx = 0
                    vy = 0
                    self.rotation_r = r
                    self._inner_rotation(time_delta)
                else:
                    # move towards edge with changing angle TODO: FIX THIS
                    self.done_rotating = True
                    if r < self.rotation_r + 3:
                        optimal_angle = math.asin(constant.PLAYER_SPEED * constant.CIRCLE_RADIUS / (self.rotation_r + 3) / constant.MONSTER_SPEED)
                    else:
                        optimal_angle = math.asin(constant.PLAYER_SPEED * constant.CIRCLE_RADIUS / r / constant.MONSTER_SPEED)
                    
                    current_angle = math.atan2(self.y - self.start_y, self.x - self.start_x)
                    
                    vrad = math.cos(optimal_angle) * constant.PLAYER_SPEED * constant.SPEED_MULT
                    vtan = math.sin(optimal_angle) * constant.PLAYER_SPEED * constant.SPEED_MULT

                    vx = vrad * math.cos(current_angle) - vtan * math.sin(current_angle)
                    vy = vrad * math.sin(current_angle) + vtan * math.cos(current_angle)

        if abs(vx) > constant.PLAYER_SPEED * constant.SPEED_MULT:
            vx_size = constant.PLAYER_SPEED * constant.SPEED_MULT
            if (vx < 0):
                vx = -vx_size
            else:
                vx = vx_size

        vy_size = math.sqrt((constant.PLAYER_SPEED * constant.SPEED_MULT) ** 2 - vx ** 2)

        if vy < 0:
            vy = -vy_size
        elif vy > 0:
            vy = vy_size
         
        self.x += vx * time_delta / 1000
        self.y += vy * time_delta / 1000
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius

    def draw(self, screen):
        self.surf.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.circle(self.surf, self.colour,
                           (self.radius, self.radius), self.radius)
        screen.blit(self.surf, self.rect)

    def _normal_move(self):
        return -(constant.PLAYER_SPEED * constant.SPEED_MULT)
    
    def monster_is_opposite(self, monster_x, monster_y):
        monster_angle = math.atan2(monster_y - self.start_y, monster_x - self.start_x) + math.pi
        current_angle = math.atan2(self.y - self.start_y, self.x - self.start_x) + math.pi

        dist_1 = monster_angle - current_angle
        if dist_1 < 0:
            dist_1 += 2 * math.pi
        dist_2 = current_angle - monster_angle
        if dist_2 < 0:
            dist_2 += 2 * math.pi

        return dist_1 + 0.04 >= math.pi and dist_2  + 0.04 >= math.pi
    
    def _inner_rotation(self, time_delta):
        current_angle = math.atan2(self.y - self.start_y, self.x - self.start_x)

        # speed this up cuz it would take forever normally
        current_angle += constant.INNER_ROTATION_MULT * constant.PLAYER_SPEED * constant.SPEED_MULT * time_delta / 1000 / self.rotation_r
        if current_angle >= math.pi:
            current_angle -= 2 * math.pi

        self.x = self.start_x + self.rotation_r * math.cos(current_angle)
        self.y = self.start_y + self.rotation_r * math.sin(current_angle)
