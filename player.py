import pygame as pg
from settings import moving


class Player:
    def __init__(self, TILE_WIDTH, width, height):
        self.width, self.height = width, height  # dimensions of the screen
        self.TILE_WIDTH = TILE_WIDTH

        self.spawn = (75, 495)  # spawn bruh
        self.rect = pg.FRect(self.spawn, (self.TILE_WIDTH, self.TILE_WIDTH))
        self.velocity = pg.Vector2(0, 0)

        self.rotation = 90
        self.rotation_speed = 0
        self.max_rotation_speed = 10

        self.brakes_sound = pg.mixer.Sound("music/brakes.wav")
        self.no_brakes = False

        self.image = pg.transform.scale(pg.transform.rotate(pg.image.load("assets/player.png"), -90), (TILE_WIDTH, TILE_WIDTH))

        self.cracks = [pg.transform.scale(pg.transform.rotate(pg.image.load("assets/player1.png"), -90), (3*TILE_WIDTH, 3*TILE_WIDTH)),
                       pg.transform.scale(pg.transform.rotate(pg.image.load("assets/player2.png"), -90), (3*TILE_WIDTH, 3*TILE_WIDTH)),
                       pg.transform.scale(pg.transform.rotate(pg.image.load("assets/player3.png"), -90), (3*TILE_WIDTH, 3*TILE_WIDTH)),
                       pg.transform.scale(pg.transform.rotate(pg.image.load("assets/player4.png"), -90), (3*TILE_WIDTH, 3*TILE_WIDTH))]

        self.FPS = 10
        self.frame = 0

        self.moving = moving
        self.mFPS = 10
        self.mframe = 0
        self.mimage = self.moving[int(self.mframe)]

        self.dead = False

    def move(self, keys_pressed, dt):
        a = 10*dt

        # basic movement
        if keys_pressed[pg.K_w] or keys_pressed[pg.K_UP]:
            self.velocity.y -= a
            # make it rotate to look up
            if 90 < self.rotation <= 270:
                self.rotation_speed -= (1.01 if self.rotation_speed > -self.max_rotation_speed else 0)
            else:
                self.rotation_speed += (1.01 if self.rotation_speed < self.max_rotation_speed else 0)

        if keys_pressed[pg.K_s] or keys_pressed[pg.K_DOWN]:
            self.velocity.y += a
            # make it rotate to look down
            self.rotation += -1 if keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT] else (1 if keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT] else 0)
            if 90 < self.rotation < 270:
                self.rotation_speed += (1 if self.rotation_speed < self.max_rotation_speed else 0)
            else:
                self.rotation_speed -= (1 if self.rotation_speed > -self.max_rotation_speed else 0)

        if keys_pressed[pg.K_d] or keys_pressed[pg.K_RIGHT]:
            self.velocity.x += a
            # make it rotate to look right
            if 180 < self.rotation <= 360 or self.rotation == 0:
                self.rotation_speed += (1.01 if self.rotation_speed < self.max_rotation_speed else 0)
            else:
                self.rotation_speed -= (1 if self.rotation_speed > -self.max_rotation_speed else 0)

        if keys_pressed[pg.K_a] or keys_pressed[pg.K_LEFT]:
            self.velocity.x -= a
            # make it rotate to look left
            if 180 <= self.rotation < 360:
                self.rotation_speed -= (1 if self.rotation_speed > -self.max_rotation_speed else 0)
            else:
                self.rotation_speed += (1 if self.rotation_speed < self.max_rotation_speed else 0)


        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y

        # keep player in the map
        if not (0 <= self.rect.left < self.width-self.TILE_WIDTH):
            self.rect.left = max(min(self.rect.left, self.width-self.TILE_WIDTH), 0)
            self.velocity.x = 0

        if not (0 <= self.rect.top < self.height-self.TILE_WIDTH):
            self.rect.top = max(min(self.rect.top, self.height-self.TILE_WIDTH), 0)
            self.velocity.y = 0

        # BRAKES
        if keys_pressed[pg.K_SPACE] and self.no_brakes is False:
            if not pg.mixer.Channel(3).get_busy() and self.velocity.length() > 2:
                pg.mixer.Channel(3).play(self.brakes_sound)
            self.velocity -= self.velocity/20

            if self.velocity.length() < a//2:
                self.velocity = pg.Vector2(0, 0)

            self.rotation_speed -= self.rotation_speed/20

        self.rotation += self.rotation_speed

        # so it doesnt overflow. needed, otherwise its gonna be hard to find the way, player should rotate towards a specified direction
        if self.rotation >= 360:
            self.rotation = 360 - self.rotation
        elif self.rotation < 0:
            self.rotation += 360

    def collision(self, level_map):
        for row_counter, row in enumerate(level_map):
            for cell_counter, cell in enumerate(row):
                if cell not in [" ", "E", "e", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                    cell_rect = pg.Rect(cell_counter*self.TILE_WIDTH, row_counter*self.TILE_WIDTH, self.TILE_WIDTH, self.TILE_WIDTH)
                    if self.rect.colliderect(cell_rect):
                        self.dead = True

    def draw(self, surf, dt):
        if self.dead:
            self.frame += self.FPS*dt
            placeholder = self.cracks[int(self.frame)]

            if self.frame >= 3:
                self.frame = 0
        else:
            placeholder = self.image
            self.frame = 0

        self.mframe += dt * self.mFPS
        if self.mframe > 8:
            self.mframe -= 8
        try:
            self.mimage = self.moving[int(self.mframe)]
        except IndexError:
            print(self.mframe)
            self.mframe -= 8
            self.mimage = self.moving[int(self.mframe)]

        if self.velocity.length() > 2:
            temp_image = pg.transform.rotate(self.mimage, self.velocity.angle_to(pg.Vector2(1, 0))+180)
            temp_rect = temp_image.get_rect()
            temp_rect.center = self.rect.center
            surf.blit(temp_image, temp_rect)

        placeholder = pg.transform.rotate(placeholder, self.rotation)

        placeholder_rect = placeholder.get_rect()
        placeholder_rect.center = self.rect.center

        surf.blit(placeholder, placeholder_rect)
        # pg.draw.rect(surf, (255, 0, 0), self.rect, 2)

    def reset(self):
        self.rect.topleft = self.spawn
        self.velocity = pg.Vector2(0, 0)
        self.rotation_speed = 0
        self.rotation = 90
        self.dead = False
