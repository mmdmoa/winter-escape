from player import Player
import renderer
from settings import *
from level import Level
import time
from font import *


music_channel = 0
player_sfx_channel = 1
wind_sfx_channel = 2
i_forgor_channel = 3

pg.mixer.Channel(music_channel).set_volume(0.3)  # main song volume
pg.mixer.Channel(player_sfx_channel).set_volume(0.2)  # player death sound + player movement sound
pg.mixer.Channel(wind_sfx_channel).set_volume(0.0)  # wind sound volume
pg.mixer.Channel(i_forgor_channel).set_volume(0.3)


class Game:
    def __init__(self):
        pg.init()

        self.WIDTH, self.HEIGHT = 600, 600

        self.death_count = 0
        self.incremented_death_count = False

        self.record_rime = True

        self.started_time = False
        self.stopped_time = False
        self.finish_time = 0
        self.start_time = 0

        self.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("winter escape")
        pg.display.set_icon(pg.transform.scale_by(pg.image.load("assets/images/player.png"), 5))

        self.overlay = pg.Surface((self.WIDTH, self.HEIGHT), pg.SRCALPHA)
        self.overlay.fill(black)
        self.overlay_a = 255
        self.can_play = False

        self.player_dead_sound_played = False

        renderer.convert_images()

        self.clock = pg.time.Clock()
        self.FPS = 60
        self.dt = 0

        self.level = Level(TILE_WIDTH)


        self.player = Player(TILE_WIDTH, self.WIDTH, self.HEIGHT, self.level.checkpoint)

        self.wind = renderer.Wind()
        self.max_wind_strength = 10

        self.exited = False

        self.game_is_beaten = False

    def run(self):
        pg.mixer.Channel(0).play(main_song, -1)

        running = True
        while running:
            if self.level.level_n == 16:
                self.overlay.fill((250, 248, 246))
                self.overlay.set_alpha(((self.player.rect.x-30)/2.11764705882) if ((self.player.rect.x-30)/2.11764705882) > 0 else 0)
            if self.level.level_n == 17:
                self.game_is_beaten = True
                self.record_rime = False
                self.overlay.set_alpha(255)
                running = False

            if self.record_rime:
                self.finish_time = time.perf_counter()

            self.dt = self.clock.tick(self.FPS)/1000.0

            keys_pressed = pg.key.get_pressed()

            if pg.mouse.get_pressed()[0]:
                print(pg.mouse.get_pos())

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    self.exited = True

            if self.can_play:
                # check anything important
                self.player.rect = self.level.check_if_player_exited_the_level_if_so_load_the_next_level_except_if_its_the_last_level_show_win_screen_so_he_will_be_proud_and_dont_forget_about_showing_his_terrible_finish_time(self.player.rect)
                self.player.no_brakes = self.level.no_brakes

                self.player.collision(self.level.map, self.level.hittable_decorations)
                if self.player.dead:
                    self.can_play = False

                    if self.incremented_death_count is False:
                        self.death_count += 1
                        self.incremented_death_count = True

                    if self.player_dead_sound_played is False:
                        pg.mixer.Channel(1).play(ice_breaks_sound)
                        self.player_dead_sound_played = True

                self.simulate_wind()

            # rendering/updating
            self.game_thing(keys_pressed)

            pg.display.update()

    def game_thing(self, keys_pressed):
        renderer.draw_level(self.level, self.display)

        if self.player.dead is True and self.can_play is False:
            self.overlay_a += 500 * self.dt
            self.overlay.set_alpha(int(self.overlay_a))
            self.overlay.fill(black)

            if self.overlay.get_alpha() >= 255:
                self.player.reset(self.level.checkpoint)
                self.incremented_death_count = False
                self.player_dead_sound_played = False
                self.overlay_a = 255


        elif self.player.dead is False and self.can_play is False:
            self.overlay_a -= 500*self.dt
            self.overlay.set_alpha(int(self.overlay_a))
            self.overlay.fill(black)

            if self.overlay.get_alpha() <= 0:
                if self.started_time is False:
                    self.start_time = time.perf_counter()
                    self.started_time = True

                self.can_play = True
                self.overlay_a = 0

        else:
            self.player.move(keys_pressed, self.dt)

            if self.player.leaving_marks:
                self.level.marks.set_at((int(self.player.rect.centerx//2), int(self.player.rect.centery//2)), (255, 255, 255))

        self.player.draw(self.display, self.dt)

        self.wind.draw(self.display, self.level.wind_direction)

        self.display.blit(pg.transform.scale_by(get_numbers_on_a_special_tablet_so_it_looks_cool_sorry_for_the_bad_name(get_time_str(self.finish_time-self.start_time)), 3), (0, 0))
        self.display.blit(pg.transform.scale_by(get_numbers_on_a_special_tablet_so_it_looks_cool_sorry_for_the_bad_name(self.death_count), 3), (0, 50))

        self.display.blit(self.overlay, (0, 0))


    def win_screen(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            self.display.blit(self.overlay, (0, 0))

            renderer.show_that_final_thingy(self.display, self.death_count, self.finish_time-self.start_time)

            pg.display.update()

    def simulate_wind(self):
        wind_strength = self.max_wind_strength - (17 - self.level.level_n)
        wind_strength = 0 if wind_strength < 0 else wind_strength

        pg.mixer.Channel(wind_sfx_channel).set_volume(0.3*(wind_strength/10))

        wind_speed = wind_strength*self.dt
        if self.level.wind_direction in ["up", "down", "left", "right"]:
            self.wind.simulate(self.dt, self.level.wind_direction, wind_strength)

            if self.level.wind_direction == "up":
                self.player.velocity.y -= wind_speed
            elif self.level.wind_direction == "down":
                self.player.velocity.y += wind_speed
            elif self.level.wind_direction == "left":
                self.player.velocity.x -= wind_speed
            elif self.level.wind_direction == "right":
                self.player.velocity.x += wind_speed


game = Game()
game.run()
if not game.exited:
    game.win_screen()
