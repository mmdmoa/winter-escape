from player import Player
import renderer
from settings import *
from level import Level
import time

pg.mixer.Channel(0).set_volume(0.3)
pg.mixer.Channel(1).set_volume(0.5)
pg.mixer.Channel(2).set_volume(1)
pg.mixer.Channel(3).set_volume(0.3)


class Game:
    def __init__(self):
        pg.init()

        self.WIDTH, self.HEIGHT = 600, 600

        self.death_count = 0
        self.incremented_death_count = False

        self.started_time = False
        self.stopped_time = False
        self.finish_time = 0
        self.start_time = 0

        self.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("winter escape")
        pg.display.set_icon(pg.transform.scale_by(pg.image.load("assets/player.png"), 5))

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

        self.tutorial = renderer.Tutorial()
        self.tutorial_passed = False
        self.show_next_card = False
        self.enter_pressed = False

        self.player = Player(TILE_WIDTH, self.WIDTH, self.HEIGHT)

        self.wind = renderer.Wind()

        self.exited = False

        self.game_is_beaten = False

    def run(self):
        pg.mixer.Channel(0).play(main_song, -1)

        running = True
        while running:
            if self.level.level_n == 17:
                self.game_is_beaten = True
                self.finish_time = time.perf_counter()
                self.overlay.set_alpha(255)
                running = False

            self.dt = self.clock.tick(self.FPS)/1000.0

            keys_pressed = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    self.exited = True

            if self.tutorial_passed:
                if self.can_play:
                    # check anything important
                    self.player.rect = self.level.check_if_player_exited_the_level_if_so_load_the_next_level_except_if_its_the_last_level_show_win_screen_so_he_will_be_proud_and_dont_forget_about_showing_his_terrible_finish_time(self.player.rect)
                    self.player.no_brakes = self.level.no_brakes

                    self.player.collision(self.level.map)
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
            else:
                if keys_pressed[pg.K_RETURN]:
                    if self.tutorial.show and not self.enter_pressed:
                        self.enter_pressed = True
                        self.tutorial.show = False
                        self.tutorial.time_wasted = 0
                        self.tutorial.can_show_next = True
                        self.tutorial.rect.y = 200

                    if not self.enter_pressed and not self.show_next_card and self.tutorial.can_show_next:
                        self.show_next_card = True
                        self.enter_pressed = True

                    elif self.tutorial.can_show_next and self.show_next_card and not self.enter_pressed:
                        self.enter_pressed = True
                        self.tutorial.increment()
                        self.tutorial.show = True
                        self.tutorial.time_wasted = 0
                        self.tutorial.can_show_next = False
                        self.tutorial.rect.y = 650
                else:
                    self.enter_pressed = False

                if self.tutorial.show is True:
                    self.show_next_card = False

                self.tutorial_thing()

                if self.tutorial.n == len(renderer.tutorials)+1:
                    self.tutorial_passed = True

            pg.display.update()

    def game_thing(self, keys_pressed):
        renderer.draw_level(self.level, self.display)

        if self.player.dead is True and self.can_play is False:
            self.overlay_a += 500 * self.dt
            self.overlay.set_alpha(int(self.overlay_a))
            self.overlay.fill(black)

            if self.overlay.get_alpha() >= 255:
                self.player.reset()
                self.level.reset()
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

                self.can_play = True
                self.overlay_a = 0

        else:
            self.player.move(keys_pressed, self.dt)


        self.player.draw(self.display, self.dt)

        self.wind.draw(self.display, self.level.wind_direction)

        self.display.blit(self.overlay, (0, 0))

    def tutorial_thing(self):
        self.display.blit(self.overlay, (0, 0))

        if self.tutorial.show:
            self.tutorial.show_card(self.dt)
        elif self.show_next_card:
            self.tutorial.change_card(self.dt)

        self.tutorial.draw(self.display)

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
        wind_speed = 5*self.dt
        if self.level.wind_direction in ["up", "down", "left", "right"]:
            self.wind.simulate(self.dt, self.level.wind_direction)

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
