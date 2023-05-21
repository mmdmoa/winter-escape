import pygame.transform

from settings import *
from font import *


def convert_images():
    global floor, no_brakes_floor, wind, wall, enter  # , moving
    floor = floor.convert()
    no_brakes_floor = no_brakes_floor.convert()

    wall = wall.convert()

    wind = [i.convert_alpha() for i in wind]

    # moving = [i.convert_alpha() for i in moving]
    # for i, x in enumerate(moving):
    #     x.set_alpha(0)
    #     moving[i] = x


def get_wall_image(level_map, row_i, column_i):
    surroundings = [
        (level_map[row_i-1][column_i] == "f") if row_i > 0 else False,  # something higher
        (level_map[row_i+1][column_i] == "f") if row_i < 19 else False,  # something lower
        (level_map[row_i][column_i - 1] == "f") if column_i > 0 else False,  # something to the left
        (level_map[row_i][column_i + 1] == "f") if column_i < 19 else False  # something to the right
    ]

    # cringe
    if surroundings == [False, False, False, False]:
        return wall.subsurface(pg.Rect((3 * 16, 0 * 16, 16, 16)))
    elif surroundings == [True, False, False, False]:
        return wall.subsurface(pg.Rect((6 * 16, 2 * 16, 16, 16)))
    elif surroundings == [False, True, False, False]:
        return wall.subsurface(pg.Rect((6 * 16, 0 * 16, 16, 16)))
    elif surroundings == [False, False, True, False]:
        return wall.subsurface(pg.Rect((5 * 16, 2 * 16, 16, 16)))
    elif surroundings == [False, False, False, True]:
        return wall.subsurface(pg.Rect((3 * 16, 2 * 16, 16, 16)))
    elif surroundings == [True, True, False, False]:
        return wall.subsurface(pg.Rect((6 * 16, 1 * 16, 16, 16)))
    elif surroundings == [True, False, True, False]:
        return wall.subsurface(pg.Rect((2 * 16, 2 * 16, 16, 16)))
    elif surroundings == [True, False, False, True]:
        return wall.subsurface(pg.Rect((0 * 16, 2 * 16, 16, 16)))
    elif surroundings == [False, True, True, False]:
        return wall.subsurface(pg.Rect((2 * 16, 0 * 16, 16, 16)))
    elif surroundings == [False, True, False, True]:
        return wall.subsurface(pg.Rect((0 * 16, 0 * 16, 16, 16)))
    elif surroundings == [False, False, True, True]:
        return wall.subsurface(pg.Rect((4 * 16, 2 * 16, 16, 16)))
    elif surroundings == [True, True, True, False]:
        return wall.subsurface(pg.Rect((2 * 16, 1 * 16, 16, 16)))
    elif surroundings == [True, True, False, True]:
        return wall.subsurface(pg.Rect((0 * 16, 1 * 16, 16, 16)))
    elif surroundings == [True, False, True, True]:
        return wall.subsurface(pg.Rect((1 * 16, 2 * 16, 16, 16)))
    elif surroundings == [False, True, True, True]:
        return wall.subsurface(pg.Rect((1 * 16, 0 * 16, 16, 16)))
    elif surroundings == [True, True, True, True]:
        return wall.subsurface(pg.Rect((1 * 16, 1 * 16, 16, 16)))


def draw_level(level, surf):
    if level.no_brakes is False:
        surf.blit(floor, (0, 0))
        pass
    else:
        surf.blit(no_brakes_floor, (0, 0))

    for row_counter, row in enumerate(level.map):
        for cell_counter, cell in enumerate(row):
            if cell == "f":
                img = get_wall_image(level.map, row_counter, cell_counter)
                img = pg.transform.scale(img, (TILE_WIDTH, TILE_WIDTH))
            else:
                img = blank_surface
            surf.blit(img, (cell_counter * TILE_WIDTH, row_counter * TILE_WIDTH))

    surf.blit(level.decorations_surface, (0, 0))
    surf.blit(pygame.transform.scale2x(level.marks), (0, 0))


def show_that_final_thingy(surf, death_count, time_spent):
    """
    shows finish time and death count
    """
    time_spent = round(time_spent, 2)
    time_spent = get_time_str(time_spent)

    if death_count > 99999:  # bro, you are fire... i mean ice
        death_count = 99999  # JUST HOW, EXPLAIN TO ME

    tablet1 = that_final_thingy.subsurface(0, 0, 63, 16)
    tablet2 = that_final_thingy.subsurface(0, 16, 63, 16)

    result1 = gnoa(death_count)
    result2 = gnoa(time_spent)

    result_tablet = pg.Surface(((result1.get_width() if (result1.get_width() > result2.get_width()) else result2.get_width()) + 63 + 5, 35), pg.SRCALPHA)

    result_tablet.blit(tablet1, (0, 0))
    result_tablet.blit(tablet2, (0, 19))

    result_tablet.blit(result1, (68, 0))
    result_tablet.blit(result2, (68, 19))

    surf.blit(pg.transform.scale_by(result_tablet, 4), (10, 100))


class Wind:
    def __init__(self):
        self.frame = 0
        self.FPS = 4
        self.image = None
        self.sound = wind_sound

    def simulate(self, dt, direction, strength):
        if not pg.mixer.Channel(2).get_busy():
            pg.mixer.Channel(2).play(self.sound)

        self.frame += self.FPS*dt
        if self.frame > 7:
            self.frame -= 7

        self.image = pg.transform.scale(wind[int(self.frame) if (0 <= int(self.frame) <= len(wind)) else 0], (600, 600))
        if direction == "up":
            self.image = pg.transform.rotate(self.image, -90)
        elif direction == "down":
            self.image = pg.transform.rotate(self.image, 90)
        elif direction == "right":
            self.image = pg.transform.rotate(self.image, 180)

        self.image.set_alpha(strength * 26)

    def draw(self, surf, direction):
        if direction in ["up", "down", "left", "right"]:
            try:
                surf.blit(self.image, (0, 0))
            except TypeError:
                pass
