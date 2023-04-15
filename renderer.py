from settings import *
from math import sin, pi
from font import *


def convert_images():
    global floor, no_brakes_floor, wind, wall, texts, tutorials, enter
    floor = floor.convert()
    no_brakes_floor = no_brakes_floor.convert()

    wall = wall.convert()

    wind = [i.convert_alpha() for i in wind]

    texts = [i.convert_alpha() for i in texts]

    tutorials = [i.convert_alpha() for i in tutorials]

    enter = enter.convert_alpha()


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

    if level.level_n == 2:
        surf.blit(texts[0], (TILE_WIDTH//2, 7.5*TILE_WIDTH))
    elif level.level_n == 10:
        surf.blit(texts[1], (120, 50))
        surf.blit(texts[2], (250, 490))
    elif level.level_n == 16:
        surf.blit(texts[3], (130, 130))


def show_that_final_thingy(surf, death_count, time_spent):
    """
    shows finish time and death count
    """
    time_spent = round(time_spent, 2)
    time_spent = get_time_str(time_spent)

    if death_count > 99999:  # bro, you are fire... i mean ice
        death_count = 99999

    tablet1 = that_final_thingy.subsurface(0, 0, 63, 16)
    tablet2 = that_final_thingy.subsurface(0, 16, 63, 16)

    result1 = get_numbers_on_a_special_tablet_so_it_looks_cool_sorry_for_the_bad_name(death_count)
    result2 = get_numbers_on_a_special_tablet_so_it_looks_cool_sorry_for_the_bad_name(time_spent)

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

    def simulate(self, dt, direction):
        if not pg.mixer.Channel(2).get_busy():
            pg.mixer.Channel(2).play(self.sound)

        self.frame += self.FPS*dt
        if self.frame > 7:
            self.frame -= 7

        self.image = pg.transform.scale(wind[int(self.frame)], (600, 600))
        if direction == "up":
            self.image = pg.transform.rotate(self.image, -90)
        elif direction == "down":
            self.image = pg.transform.rotate(self.image, 90)
        elif direction == "right":
            self.image = pg.transform.rotate(self.image, 180)

    def draw(self, surf, direction):
        if direction in ["up", "down", "left", "right"]:
            surf.blit(self.image, (0, 0))


class Tutorial:
    def __init__(self):
        self.n = 1
        self.image = tutorials[self.n-1]

        self.rect = self.image.get_rect()
        self.rect.centerx = 300
        self.rect.top = 650

        self.show = True
        self.can_show_next = False

        self.time_wasted = 0

        self.enter = enter
        self.enter_a = 255
        self.a = pi / 2

    def draw(self, surf):
        surf.blit(self.image, self.rect)

        self.enter.set_alpha(int(self.enter_a*abs(sin(self.a))))
        self.a += 0.06
        surf.blit(self.enter, (450, 500))

    def show_card(self, dt):
        if self.show:
            self.rect.y = 650 - 450 * sin((pi - pi*self.time_wasted/2))
            self.time_wasted += dt

            if self.time_wasted >= 1:
                self.time_wasted = 0
                self.show = False
                self.can_show_next = True

    def change_card(self, dt):
        if self.can_show_next:
            self.rect.y = 650 - 450 * sin((pi + self.time_wasted*pi)/2)
            self.time_wasted += dt

            if self.time_wasted >= 1:
                self.time_wasted = 0
                self.show = True
                self.can_show_next = False

                self.increment()

    def increment(self):
        self.n += 1
        if self.n < len(tutorials) + 1:
            self.image = tutorials[self.n - 1]
