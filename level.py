from level_loader import load_level
import pygame as pg


class Level:
    def __init__(self, tile_width):
        self.level_n = 1

        self.tile_width = tile_width

        self.level = load_level(self.level_n)
        self.map = self.level["map"]

        self.entrance = self.level["entrance"]
        self.exit = self.level["exit"]
        self.checkpoint = self.level["checkpoint"]
        self.load_entrance_and_exit()

        self.wind_direction = self.level["wind direction"]
        self.no_brakes = self.level["no brakes"]

        self.decorations = self.level["decorations"]
        self.decorations_surface = pg.Surface((600, 600), pg.SRCALPHA)
        self.hittable_decorations = []  # list of object you can still hit
        self.load_decorations()

        self.marks = pg.Surface((300, 300), pg.SRCALPHA)
        self.marks.set_alpha(127)

    def check_if_player_exited_the_level_if_so_load_the_next_level_except_if_its_the_last_level_show_win_screen_so_he_will_be_proud_and_dont_forget_about_showing_his_terrible_finish_time(self, player_rect):
        if player_rect.colliderect(self.exit):
            map_exit = self.exit

            self.level_n += 1
            self.load_new()
            self.load_entrance_and_exit()  # entrance and exit of the next level

            # teleport payer, so that it looks like he is exiting the previous level
            if map_exit.left < player_rect.centerx < map_exit.right:  # entered from the top
                if player_rect.top < map_exit.top:
                    player_rect.topleft = [self.entrance.left + player_rect.left - map_exit.left, self.entrance.top]
                else:
                    player_rect.bottomleft = [self.entrance.left + player_rect.left - map_exit.left, self.entrance.bottom]
            else:  # entered from the side
                if player_rect.left < map_exit.left:
                    player_rect.topleft = [self.entrance.left, self.entrance.top + player_rect.top - map_exit.top]
                else:
                    player_rect.topright = [self.entrance.right, self.entrance.top + player_rect.top - map_exit.top]

        return player_rect

    def load_entrance_and_exit(self):
        self.entrance = pg.Rect(self.level["entrance"][0][0] * self.tile_width,
                                self.level["entrance"][0][1] * self.tile_width,
                                self.level["entrance"][1][0] * self.tile_width,
                                self.level["entrance"][1][1] * self.tile_width)

        self.exit = pg.Rect(self.level["exit"][0][0] * self.tile_width,
                            self.level["exit"][0][1] * self.tile_width,
                            self.level["exit"][1][0] * self.tile_width,
                            self.level["exit"][1][1] * self.tile_width)

    def load_decorations(self):
        self.decorations_surface = pg.Surface((600, 600), pg.SRCALPHA)
        for decoration in self.decorations.values():
            d_image = pg.image.load(decoration["image-path"])  # d stands for decoration
            d_image.convert_alpha()

            d_image = pg.transform.rotate(d_image, decoration["rotation"])
            d_image = pg.transform.scale(d_image, decoration["rect"][2:])

            self.decorations_surface.blit(d_image, decoration["rect"])
            # pg.draw.rect(self.decorations_surface, (255, 0, 0), decoration["rect"], 5)
            # pg.draw.rect(self.decorations_surface, (0, 255, 0), decoration["hit_rect"], 3)

            if decoration["can-die"]:
                self.hittable_decorations.append(decoration["hit_rect"])

    def load_new(self):
        self.level = load_level(self.level_n)
        self.map = self.level["map"]

        self.entrance = self.level["entrance"]
        self.exit = self.level["exit"]
        self.load_entrance_and_exit()

        self.wind_direction = self.level["wind direction"]
        self.no_brakes = self.level["no brakes"]

        self.checkpoint = self.level["checkpoint"]

        self.decorations = self.level["decorations"]
        self.hittable_decorations = []
        self.load_decorations()

        self.marks = pg.Surface((600, 600), pg.SRCALPHA)
        self.marks.set_alpha(127)
