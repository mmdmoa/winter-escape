import pygame as pg

pg.mixer.init()
# don't ask why i put all of the images in this file

TILE_WIDTH = 30

black = (29, 28, 26)

wall = pg.image.load("assets/wall.png")

floor = pg.transform.scale(pg.image.load("assets/floor.png"), (600, 600))
no_brakes_floor = pg.transform.scale(pg.image.load("assets/no_brakes_floor.png"), (600, 600))

wind = [pg.image.load("assets/wind1.png"),
        pg.image.load("assets/wind2.png"),
        pg.image.load("assets/wind3.png"),
        pg.image.load("assets/wind4.png"),
        pg.image.load("assets/wind5.png"),
        pg.image.load("assets/wind6.png"),
        pg.image.load("assets/wind7.png")]

texts = [pg.image.load("assets/text1.png"),
         pg.image.load("assets/text2.png"),
         pg.image.load("assets/text3.png"),
         pg.image.load("assets/text4.png")]
texts = [pg.transform.scale_by(i, 4) for i in texts]

tutorials = [pg.image.load("assets/tutorial1.png"),
             pg.image.load("assets/tutorial2.png"),
             pg.image.load("assets/tutorial3.png"),
             pg.image.load("assets/tutorial4.png"),
             pg.image.load("assets/tutorial5.png"),
             pg.image.load("assets/tutorial6.png")]
tutorials = [pg.transform.scale_by(i, 4) for i in tutorials]

blank_surface = pg.Surface((0, 0))

enter = pg.transform.scale_by(pg.image.load("assets/enter.png"), 4)

that_final_thingy = pg.image.load("assets/final_thing.png")
font = pg.image.load("assets/font.png")

moving = [pg.image.load("assets/moving1.png"),
          pg.image.load("assets/moving2.png"),
          pg.image.load("assets/moving3.png"),
          pg.image.load("assets/moving4.png"),
          pg.image.load("assets/moving5.png"),
          pg.image.load("assets/moving6.png"),
          pg.image.load("assets/moving7.png"),
          pg.image.load("assets/moving8.png")
          ]
moving = [pg.transform.scale_by(i, 2) for i in moving]

ice_breaks_sound = pg.mixer.Sound("music/ice_break.wav")
main_song = pg.mixer.Sound("music/epic_song.wav")
wind_sound = pg.mixer.Sound("music/windy_kinda_here.wav")
