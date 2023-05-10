import pygame as pg

pg.mixer.init()
# don't ask why i put all of the images in this file

decorations_updated = False

TILE_WIDTH = 30

black = (29, 28, 26)

wall = pg.image.load("assets/images/wall.png")

floor = pg.transform.scale(pg.image.load("assets/images/floor.png"), (600, 600))
no_brakes_floor = pg.transform.scale(pg.image.load("assets/images/no_brakes_floor.png"), (600, 600))

wind = [pg.image.load("assets/images/wind1.png"),
        pg.image.load("assets/images/wind2.png"),
        pg.image.load("assets/images/wind3.png"),
        pg.image.load("assets/images/wind4.png"),
        pg.image.load("assets/images/wind5.png"),
        pg.image.load("assets/images/wind6.png"),
        pg.image.load("assets/images/wind7.png")]

that_final_thingy = pg.image.load("assets/images/final_thing.png")
font = pg.image.load("assets/images/font.png")

blank_surface = pg.Surface((0, 0))


ice_breaks_sound = pg.mixer.Sound("assets/music/ice_break.wav")
main_song = pg.mixer.Sound("assets/music/epic_song.mp3")
wind_sound = pg.mixer.Sound("assets/music/kinda windy here.mp3")
