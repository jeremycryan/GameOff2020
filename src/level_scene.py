##!/usr/bin/env python3

import math

import pygame
import random

import constants as c
from scene import Scene
from planet import Planet
from moon import Moon
from wormhole import Wormhole
from ship import Ship
from primitives import Pose
from achievement_row import AchievementRow
from nugget import Nugget
from player import Player
from wind_particle import WindParticle

class LevelScene(Scene):
    def __init__(self, *args, lastLevel=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.game.temp_scores = {}
        self.lastLevel = lastLevel
        self.game.players_in_last_round = set()
        self.spawn_level()

        self.home_planet = None
        for item in self.planets:
            if item.home:
                self.home_planet = item
                break

        self.ships = []

        self.surface = pygame.Surface((c.LEVEL_WIDTH, c.LEVEL_HEIGHT))
        self.side_panel = pygame.Surface(c.SIDE_PANEL_SIZE)
        self.achievement_row = AchievementRow(self.game, (0, 0))
        self.achievement_row.pose.y = c.WINDOW_HEIGHT - self.achievement_row.get_height()
        self.alignment = c.LEFT, c.DOWN
        self.offset = self.get_initial_offset()
        self.particles = set()
        self.screenshake_time = 0
        self.screenshake_amp = 0
        self.exploded_planets = 0
        self.age = 0
        self.scene_over = False

        self.shade = pygame.Surface(c.WINDOW_SIZE)
        self.shade.fill(c.BLACK)
        self.shade_alpha = 255
        self.shade.set_colorkey(c.MAGENTA)
        #self.timer_label = self.game.

        self.since_sh = 99

        self.instructions = pygame.image.load(c.IMAGE_PATH + "/instructions.png")

        if self.game.modifications:
            lowered = [mod.lower() for mod in self.game.modifications]
            self.game.alertManager.alert(f"Modifications active: {', '.join(lowered)}")

    def shake(self, amp=15):
        self.screenshake_amp = max(self.screenshake_amp, amp)
        self.screenshake_time = 0

    def round_length(self):
        if c.EXTRA_TIME_MOD in self.game.modifications:
            return 12
        else:
            return 10 # minutes

    def apply_screenshake(self, offset):
        x = offset[0] + self.screenshake_amp * math.cos(self.screenshake_time * 24)
        y = offset[1] + self.screenshake_amp * math.cos(self.screenshake_time * 24)
        return (x, y)

    def apply_own_offset(self, offset):
        return offset[0] + self.offset[0], offset[1] + self.offset[1]

    def update(self, dt, events):
        self.age += dt

        self.since_sh += dt
        self.screenshake_time += dt
        self.screenshake_amp *= 0.001**dt
        self.screenshake_amp = max(0, self.screenshake_amp - 20*dt)

        if c.SOLAR_WIND in self.game.modifications:
            if self.since_sh > 0.75:
                self.game.solar_wind_sound.play()
                self.since_sh = 0
            self.particles.add(WindParticle(self.game))

        if c.EXPLODING_PLANETS in self.game.modifications:
            if self.age > (self.exploded_planets+1)*c.PLANET_EXPLODE_RATE and len(self.planets) > 2:
                self.exploded_planets += 1
                i = random.randint(2, len(self.planets)-1)
                if not isinstance(self.planets[i], Wormhole):
                    self.planets[i].destroy()
                    self.game.current_scene.shake(25)

        for ship in self.ships[::-1]:
            if ship.destroyed:
                self.ships.remove(ship)
        for object_to_update in self.ships + self.planets + [self.achievement_row] + self.nuggets:
            object_to_update.update(dt, events)
        for particle in self.particles:
            particle.update(dt, events)
        self.particles = {item for item in self.particles if not item.dead}

        for message in self.game.stream.queue_flush():
            if message.text.lower() == '!recolor':
                if message.user in self.game.players:
                    self.game.players[message.user].recolor()
                    for ship in self.ships:
                        if ship.player.name == message.user:
                            ship.recolor()
                    self.game.recolor_flag(message.user)
            elif message.text.lower() == '!score':
                board = self.game.scoreboard.get_total_by_player(c.SCORE_EXPIRATION)
                if message.user in board:
                    score = self.game.scoreboard.get_total_by_player(c.SCORE_EXPIRATION)[message.user].score
                    self.game.alertManager.alert("Your score is "+str(score), message.user)
                else:
                    self.game.alertManager.alert("You have not played in the last " + str(c.SCORE_EXPIRATION) + " hours", message.user)
            elif message.text.lower()[:5] == "!vote":
                pass
            elif message.text[0] == '!':
                program, info = Ship.parse_program(message.text)
                if not program:
                    #print("Error: " + info)
                    self.game.alertManager.alert(info, message.user)
                elif not self.scene_over:
                    if message.user not in self.game.players:
                        self.game.players[message.user] = Player(self.game, message.user)
                    self.spawn_ship(message.text, message.user)

        shade_speed = 900
        if self.shade_alpha > 0 and not self.scene_over:
            center = (self.home_planet.pose.x, self.home_planet.pose.y)
            hold_rad = 100
            pause = 0.3
            radius = max(
                max((self.age - pause + 0.1), 0)**2.5 * c.WINDOW_WIDTH,
                min((1 - (1 - self.age/pause)**3)*hold_rad, hold_rad)
            )
            if radius < c.WINDOW_WIDTH * 1.4:
                pygame.draw.circle(self.shade, c.MAGENTA, center, radius)
            else:
                self.shade_alpha = 0
        elif self.shade_alpha < 255 and self.scene_over:
            if not self.shade.get_at((0, 0))[:3] == c.BLACK:
                self.shade.fill(c.BLACK)
            self.shade_alpha = min(255, self.shade_alpha + shade_speed * dt)

        if self.age > self.round_length() * 60:
            self.scene_over = True
        if self.achievement_row.all_scored():
            self.scene_over = True
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.scene_over = True

        if self.scene_over and self.shade_alpha == 255:
            self.is_running = False

    def draw(self, surf, offset=(0, 0)):
        offset_with_shake = self.apply_screenshake(offset)
        #surf.fill(c.BLACK)
        if not c.SOLAR_WIND in self.game.modifications:
            self.surface.fill(c.DARK_GRAY)
        else:
            color = (65 - math.sin(self.age*2)*8, 35, 30)
            self.surface.fill(color)
        self.draw_lines()      # TODO make background more interesting but not so laggy
        for planet in self.planets[:]:
            if planet.destroyed:
                self.planets.remove(planet)
        for planet in self.planets:
            planet.draw_gravity_region(self.surface, offset_with_shake)
        for planet in self.planets:
            planet.draw(self.surface, offset_with_shake)
        for nugget in self.nuggets:
            nugget.draw(self.surface, offset_with_shake)
        for particle in self.particles:
            particle.draw(self.surface, offset_with_shake)
        for ship in self.ships:
            ship.draw(self.surface, offset_with_shake)
        surf.blit(self.surface, self.apply_own_offset(offset))

        self.side_panel.fill(c.BLACK)
        self.achievement_row.draw(self.side_panel)
        self.draw_timer(self.side_panel, c.TIMER_POSITION)
        surf.blit(self.side_panel, (c.LEVEL_WIDTH, 0))
        surf.blit(self.instructions, (c.WINDOW_WIDTH - self.instructions.get_width(),
                                      80))

        if self.shade_alpha > 0:
            self.shade.set_alpha(self.shade_alpha)
            surf.blit(self.shade, (0, 0))

    def draw_lines(self):
        border = 15
        line_period = 40
        line_width = 5
        offset = (self.age * 25) % line_period
        x = - c.WINDOW_HEIGHT - border + offset
        y_low = c.WINDOW_HEIGHT + border
        y_high = - border
        y_height = y_low - y_high
        color = c.DARKER_GRAY
        if c.SOLAR_WIND in self.game.modifications:
            return
        while x < c.WINDOW_WIDTH + border:
            pygame.draw.line(self.surface,
                             c.DARKER_GRAY,
                             (x, y_low),
                             (x+y_height, y_high),
                             width=line_width)
            x += line_period

    def get_initial_offset(self):
        x = 0
        if self.alignment[0] == c.RIGHT:
            x = c.WINDOW_WIDTH - c.LEVEL_WIDTH
        elif self.alignment[0] == c.CENTER:
            x = (c.WINDOW_WIDTH - c.LEVEL_WIDTH)//2
        y = 0
        if self.alignment[1] == c.DOWN:
            y = c.WINDOW_HEIGHT - c.LEVEL_HEIGHT
        elif self.alignment[1] == c.CENTER:
            y = (c.WINDOW_HEIGHT - c.LEVEL_HEIGHT)//2
        return (x, y)

    def spawn_level(self, level=None):
        # if not level:
        #     levels = ["giant", "small", "wormhole", "default"]
        #     weights = [1, 2, 1, 3]
        #     if self.lastLevel in levels and self.lastLevel != "default":
        #         i = levels.index(self.lastLevel)
        #         weights[i] = 0
        #     level = random.choices(levels, weights)[0]
        if c.GIANT_PLANET_MOD in self.game.modifications:
            level = "giant"
        elif c.MANY_WORMHOLES_MOD in self.game.modifications:
            level = "wormhole"
        elif c.SMALL_PLANETS_MOD in self.game.modifications:
            level = "small"
        else:
            level = "default"
        self.level = level
        #print("Level type: " + level)
        self.planets = []
        self.nuggets = []
        self.spawn_home_planet()
        self.spawn_moon()
        if c.NO_PLANETS_MOD in self.game.modifications:
            self.spawn_waypoint(2)
            if random.random() < 0.35:
                self.add_wormhole()
        elif level == "giant":
            self.add_planet(rmin=120, rmax=150, clearance=c.MIN_SPACING+50, border=300)
            self.spawn_waypoint(2)
            if random.random() < 0.35:
                self.add_wormhole()
            self.add_planet(n=7)
        elif level == "small":
            self.spawn_waypoint(2)
            if random.random() < 0.35:
                self.add_wormhole()
            self.add_planet(rmax=50, n=20)
        elif level == "wormhole":
            self.spawn_waypoint(2)
            for i in range(4):
                self.add_wormhole(color=i)
            self.add_planet(n=7)
        else:
            self.spawn_waypoint(2)
            if random.random() < 0.35:
                self.add_wormhole()
            self.add_planet(n=random.randint(7,12))

    def spawn_home_planet(self, home=None, clearance=c.MIN_SPACING+100):
        if not home:
            home = self.get_edge(offset=c.HOME_PLANET_RADIUS//2)
        spawn_angle = self.get_angle(home, (c.LEVEL_WIDTH/2, c.LEVEL_HEIGHT/2))
        spawn_angle += (2 * random.random() - 1) * c.HOME_ANGLE_VARIATION * math.pi/180
        spawn_x = home[0] + int(math.cos(spawn_angle)*(c.HOME_PLANET_RADIUS+c.SHIP_SPAWN_ALTITUDE))
        spawn_y = home[1] - int(math.sin(spawn_angle)*(c.HOME_PLANET_RADIUS+c.SHIP_SPAWN_ALTITUDE))
        self.spawn_angle = math.degrees(spawn_angle)
        self.spawn_pos = (spawn_x, spawn_y)
        self.home_planet = Planet(self.game, home, angle=self.spawn_angle, radius=c.HOME_PLANET_RADIUS, home=True)
        self.home_planet.clearance = clearance
        self.planets.append(self.home_planet)

    def spawn_moon(self, home_clearance=400, clearance=c.MIN_SPACING + 50):
        for i in range(100):
            moon = Pose(self.get_edge(offset=100), 0)
            if moon.distance_to(self.home_planet.pose) > home_clearance:
                break
        self.moon = Moon(self.game, (moon.x, moon.y))
        self.moon.clearance = clearance
        self.planets.append(self.moon)

    def spawn_waypoint(self, n=1, home_clearance=250, moon_clearance=250, waypoint_clearance=400, clearance=c.MIN_SPACING + 50):
        for i in range(n):
            for i in range(100):
                pos = self.get_viable_point(22, clearance, point=self.get_point(border=100))
                if not pos:
                    continue
                waypoint = Pose(pos, 0)
                if waypoint.distance_to(self.home_planet.pose) < home_clearance:
                    continue
                if waypoint.distance_to(self.moon.pose) < moon_clearance:
                    continue
                fail = False
                for waypoint2 in self.nuggets:
                    if waypoint.distance_to(waypoint2.pose) < waypoint_clearance:
                        fail = True
                        break
                if not fail:
                    break
            waypoint = Nugget(self.game, (waypoint.x, waypoint.y), 0)
            waypoint.clearance = clearance
            self.nuggets.append(waypoint)

    def get_point(self, W=c.LEVEL_WIDTH, H=c.LEVEL_HEIGHT, border=0):
        x = int(random.random()*(W-border*2)) + border
        y = int(random.random()*(H-border*2)) + border
        return (x, y)

    def get_edge(self, W=c.LEVEL_WIDTH, H=c.LEVEL_HEIGHT, offset=0):
        perimeter = (W+H-offset*4)*2
        x = int(random.random()*(W-2*offset))
        y = int(random.random()*(H-2*offset))
        edge = int(random.random()*4)
        if edge == 0:
            x = offset
            y = max(offset, y)
            y = min(W - offset, y)
        elif edge == 1:
            x = W - offset
            y = max(offset, y)
            y = min(W - offset, y)
        elif edge == 2:
            y = offset
            x = max(offset, x)
            x = min(H - offset, x)
        elif edge == 3:
            y = H - offset
            x = max(offset, x)
            x = min(H - offset, x)
        return (x, y)

    def get_angle(self, p1, p2):
        return math.atan2(p1[1]-p2[1], p2[0]-p1[0])

    def get_viable_point(self, r, clearance=c.MIN_SPACING, point=None):
        if not point:
            point = self.get_point()
        x, y = point
        pose = Pose((x, y), 0)
        for planet in self.planets + self.nuggets:
            if planet.overlaps(pose, r, clearance):
                return False
        return (x, y)

    def add_planet(self, rmin=c.MIN_PLANET_RADIUS, rmax=c.MAX_PLANET_RADIUS, n=1, clearance=c.MIN_SPACING, border=0, edge=False):
        for i in range(100):
            r = int(random.random()*(rmax-rmin))+rmin
            if edge:
                p = self.get_edge(offset=border)
            else:
                p = self.get_point(border=border)
            pos = self.get_viable_point(r, clearance, point=p)
            if pos:
                p = Planet(self.game, pos, radius=r)
                p.clearance = clearance
                self.planets.append(p)
                n -= 1
                if n <= 0:
                    break
        return True

    def add_wormhole(self, min_travel=300, clearance=c.MIN_SPACING, color=3):
        for i in range(100):
            p = self.get_point(border=100)
            pos1 = self.get_viable_point(20, clearance, point=p)
            if pos1:
                break
        if not pos1:
            return
        for i in range(100):
            p = self.get_point(border=100)
            pos2 = self.get_viable_point(20, clearance, point=p)
            if pos2 and Pose(pos1, 0).distance_to(Pose(pos2, 0)) > min_travel:
                break
        if not pos2:
            return
        w = Wormhole(self.game, pos1, pos2, color=color)
        w.clearance = clearance
        self.planets.append(w)

    def spawn_ship(self, program, name):
        player = self.game.players[name]
        new_ship = Ship(self.game, program, player, self.spawn_pos, self.spawn_angle)
        for existing_ship in self.ships[:]:
            if existing_ship.player == player:
                existing_ship.destroy()
        self.ships.append(new_ship)

        self.game.players_in_last_round.add(player)

    def draw_timer(self, surface, center, offset=(0, 0)):
        duration = self.round_length() * 60
        left = int(duration - self.age)
        minutes = left // 60
        seconds = int(left % 60)
        zero = "0" if seconds < 10 else ""
        text = f"{minutes}:{zero}{seconds}"
        font_dict = self.game.timer_render if minutes else self.game.red_timer_render
        surfaces = [font_dict[digit] for digit in text]
        total_width = sum([surf.get_width() for surf in surfaces])
        max_height = max([surf.get_height() for surf in surfaces])

        x = center[0] + offset[0] - total_width//2
        y = center[1] + offset[1] - max_height//2
        for item in surfaces:
            surface.blit(item, (x, y))
            x += item.get_width()

    def next_scene(self):
        multiplier = self.game.player_multiplier()
        for player_name in self.game.temp_scores:
            self.game.scoreboard.add_score(player_name, self.game.temp_scores[player_name] * multiplier)
        for player in self.game.players_in_last_round:
            self.game.scoreboard.add_score(player.name, c.PARTICIPATION_POINTS * multiplier)
        self.game.modifications = []
        #self.game.alertManager.clear()
        self.game.solar_wind_sound.fadeout(500)
        return self.game.high_score_scene()
