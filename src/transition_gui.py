##!/usr/bin/env python3

import math
import random

import pygame

from primitives import GameObject, Pose
from planet import Planet
import constants as c

class AlertBox(GameObject):

    def __init__(self, game, position, header, message, side_surface=None):
        super().__init__(game)
        self.age = 0
        self.pose = Pose(position, 0)
        self.header = header
        self.message = message
        self.side_surface = side_surface
        self.generate_colors()
        self.load_surfs()
        self.max_width = self.top_surf.get_width() - c.ALERT_SIDE_PADDING * 2
        if self.side_surface is not None:
            self.max_width -= self.side_surface.get_width() + c.ALERT_SIDE_PADDING
        self.header_surf = self.get_header_surface()
        self.message_surface = self.get_message_surface()

    def generate_colors(self):
        self.header_color = (255, 200, 200)
        self.body_color = (190, 160, 160)

    def get_header_surface(self):
        render = self.game.alert_header_font.render(self.header, 1, self.header_color)
        background = pygame.transform.scale(self.middle_surf,
                                            (self.middle_surf.get_width(),
                                            render.get_height() + 8)).convert()
        x = background.get_width()//2 - render.get_width()//2
        if self.side_surface is not None:
            x += (self.side_surface.get_width() + c.ALERT_SIDE_PADDING)//2
        background.blit(render, (x, 0))
        return background

    def get_message_surface(self):
        message_surfaces = []
        message_lines = self.message.split("\n")
        for line in message_lines:
            message_words = line.split()
            this_line = []
            this_width = 0
            for word in message_words:
                surface = self.game.alert_body_font.render(word, 1, self.body_color)
                if this_width + surface.get_width() > self.max_width:
                    message_surfaces.append(this_line)
                    this_line = []
                    this_width = 0
                this_line.append(surface)
                this_width += surface.get_width() + c.ALERT_BODY_SPACE
            message_surfaces.append(this_line)

        total_height = c.ALERT_LINE_SPACING*(len(message_surfaces))
        if self.side_surface is not None and total_height < self.side_surface.get_height() - self.header_surf.get_height():
            total_height = self.side_surface.get_height() - self.header_surf.get_height()
        background = pygame.transform.scale(self.middle_surf,
                                            (self.middle_surf.get_width(),
                                            total_height)).convert()
        y = 0
        for line in message_surfaces:
            line_width = sum([item.get_width() + c.ALERT_BODY_SPACE for item in line]) - c.ALERT_BODY_SPACE
            x = background.get_width()//2 - line_width//2
            if self.side_surface is not None:
                x += self.side_surface.get_width()//2 + c.ALERT_SIDE_PADDING//2
            for word in line:
                background.blit(word, (x, y))
                x += word.get_width() + c.ALERT_BODY_SPACE
            y += c.ALERT_LINE_SPACING

        return background

    def load_surfs(self):
        self.top_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_top.png")
        self.middle_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_middle.png")
        self.bottom_surf = pygame.image.load(c.IMAGE_PATH + "/red_alert_box_bottom.png")

    def draw(self, surface, offset=(0, 0)):
        surfaces = [self.top_surf, self.header_surf, self.message_surface, self.bottom_surf]
        x = self.pose.x - self.top_surf.get_width()//2 + offset[0]
        y = self.pose.y - sum([item.get_height() for item in surfaces])//2 + offset[1] + 4 * math.sin(self.age * 2)
        y0 = y
        for piece in surfaces:
            surface.blit(piece, (x, y))
            y += piece.get_height()

        if self.side_surface is not None:
            surface.blit(self.side_surface,
                (x + c.ALERT_SIDE_PADDING,
                y0 + self.top_surf.get_height()
                + self.header_surf.get_height()//2
                + self.message_surface.get_height()//2
                - self.side_surface.get_height()//2))

    def update(self, dt, events):
        self.age += dt

class GreenAlertBox(AlertBox):
    def generate_colors(self):
        self.header_color = (200, 230, 205)
        self.body_color = (150, 180, 160)

    def load_surfs(self):
        self.top_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_top.png")
        self.middle_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_middle.png")
        self.bottom_surf = pygame.image.load(c.IMAGE_PATH + "/green_alert_box_bottom.png")

class PlayerMultiplierAlertBox(AlertBox):
    def __init__(self, game, position, header, message):
        self.background_color = (68, 35, 48)
        self.game = game
        self.generate_colors()
        side_surface = self.generate_multiplier_surface()
        super().__init__(game, position, header, message, side_surface=side_surface)
        self.age += 2

    def generate_multiplier_surface(self):
        text = f"x{self.game.player_multiplier()}"
        render = self.game.alert_large_font.render(text, 1, self.header_color)
        surface = pygame.Surface((render.get_width(), 70))
        surface.fill(self.background_color)
        surface.blit(render,
            (surface.get_width()//2 - render.get_width()//2,
            surface.get_height()//2 - render.get_height()//2))
        return surface

class VotingObject(GameObject):
    def __init__(self, game, parent, position, strings):
        super().__init__(game)
        self.parent = parent
        self.pose = Pose(position, 0)
        self.option_keys = c.OPTION_A, c.OPTION_B
        self.option_strings = {self.option_keys[i]: strings[i] for i in range(len(self.option_keys))}
        self.votes = {option:set() for option in self.option_keys}
        self.planet_dict = {option:Planet(self.game, (0, 0), radius=75, surf_det_size=50+i) for i, option in enumerate(self.option_keys)}
        self.color_dict = {c.OPTION_A:(255, 225, 200), c.OPTION_B:(200, 210, 255)}
        self.label_dict = {option_key:self.get_label_surf(option_key) for option_key in self.option_keys}
        self.cover = pygame.Surface((150, 150))
        self.cover.fill(c.WHITE)
        pygame.draw.circle(self.cover, c.BLACK, (self.cover.get_width()//2, self.cover.get_height()//2), self.cover.get_width()//2)
        self.cover.set_colorkey(c.WHITE)
        self.cover.set_alpha(80)
        self.not_picked_cover = self.cover.copy()
        self.not_picked_cover.set_alpha(128)
        self.picked = None
        self.since_vote = {option:999 for option in self.option_keys}
        self.vfam = pygame.image.load(c.IMAGE_PATH + "/vote_for_a_modifier.png")

    def vote(self, player_name, option):
        option = option.upper()
        if option not in self.option_keys:
            return 0
        for vote_option in self.votes:
            cur_votes = self.votes[vote_option]
            if player_name in cur_votes:
                cur_votes.remove(player_name)
        self.votes[option].add(player_name)
        self.since_vote[option] = 0
        for option in self.label_dict:
            self.label_dict[option] = self.get_label_surf(option)
        return 1

    def get_label_surf(self, option):
        text = f"!vote {option}"
        color = self.color_dict[option]
        render = self.game.alert_header_font.render(text, 1, color)
        count_text = str(len(self.votes[option]))
        count_render = self.game.alert_body_font.render(count_text, 1, color)
        background = pygame.image.load(c.IMAGE_PATH + "/vote_label_background.png").convert()
        tint = pygame.Surface((background.get_width(), background.get_height()))
        tint.fill(color)
        tint.set_alpha(10)
        background.blit(tint, (0, 0), special_flags=pygame.BLEND_MULT)
        background.set_colorkey(background.get_at((0, 0)))
        background.blit(render,
            (background.get_width()//2 - render.get_width()//2,
            background.get_height()//2 - render.get_height()))
        background.blit(count_render,
            (background.get_width()//2 - count_render.get_width()//2,
            background.get_height()//2))
        return background

    def determine_winner(self):
        option_a_score = len(self.votes[c.OPTION_A])
        option_b_score = len(self.votes[c.OPTION_B])
        if option_a_score > option_b_score:
            self.picked = c.OPTION_A
        elif option_a_score < option_b_score:
            self.picked = c.OPTION_B
        else:
            self.picked = random.choice([c.OPTION_A, c.OPTION_B])

        modification = self.option_strings[self.picked]
        self.game.modifications.append(modification)
        if modification is c.SOLAR_WIND:
            self.game.solar_wind_direction = random.choice([c.UP, c.DOWN, c.LEFT, c.RIGHT])

    def draw_option(self, option_key, surface, offset=(0, 0)):
        planet = self.planet_dict[option_key]
        x = offset[0]
        y = offset[1]
        planet.pose.x = x
        planet.pose.y = y
        planet.align_graphic_pose()
        planet.draw(surface)
        surface.blit(self.cover, (x - self.cover.get_width()//2, y - self.cover.get_height()//2))
        texts = [self.game.voting_planet_font.render(text, 0, c.BLACK) for text in self.option_strings[option_key].split()]
        backs = [pygame.Surface((text.get_width(), text.get_height())) for text in texts]
        for back in backs:
            back.fill(c.MAGENTA)
        for i, text in enumerate(texts):
            texts[i] = backs[i]
            texts[i].blit(text, (0, 0))
            texts[i].set_colorkey(c.MAGENTA)
            texts[i].set_alpha(90)
        white_texts = [self.game.voting_planet_font.render(text, 1, c.WHITE) for text in self.option_strings[option_key].split()]
        total_height = sum([text.get_height() for text in texts])

        y -= total_height//2
        for white, black in zip(white_texts, texts):
            for offset in c.TEXT_BLIT_OFFSETS:
                surface.blit(black, (x - black.get_width()//2 + offset[0], y + offset[1]))
            surface.blit(white, (x - white.get_width()//2, y - 1))
            y += black.get_height()

        if self.picked is not None and self.picked is not option_key:
            surface.blit(self.not_picked_cover, (planet.pose.x - self.cover.get_width()//2, planet.pose.y - self.cover.get_height()//2))

        #if self.picked is None:
        y = planet.pose.y
        label = self.label_dict[option_key]
        label_scale = min(1, self.since_vote[option_key]*1.5 + 0.7)
        if self.picked is not None and self.picked != option_key:
            label_scale = max(0, 1 + self.time_left()*3)
        if label_scale != 0:
            label = pygame.transform.scale(label,
                                            (int(label.get_width() * label_scale),
                                            int(label.get_height() * label_scale)))
            surface.blit(label, (x - label.get_width()//2, y + 95 - label.get_height()//2))

    def time_left(self):
        return self.parent.countdown.duration - 5

    def draw(self, surface, offset):
        x = self.pose.x + offset[0]
        y = self.pose.y + offset[1]
        dist_apart = 200
        self.draw_option(self.option_keys[0], surface, offset=(x-dist_apart//2, y))
        self.draw_option(self.option_keys[1], surface, offset=(x+dist_apart//2, y))
        surface.blit(self.vfam, (x - self.vfam.get_width()//2, y - c.WINDOW_HEIGHT*0.17))

    def update(self, dt, events):
        for key in self.planet_dict:
            self.planet_dict[key].update(dt, events)
        for option in self.since_vote:
            self.since_vote[option] += dt
        if self.time_left() <= 0 and self.picked is None:
            self.determine_winner()

class Countdown(GameObject):
    def __init__(self, game, position):
        super().__init__(game)
        self.duration = 50.999  # seconds
        self.pose = Pose(position, 0)
        self.color = (100, 110, 135)

    def update(self, dt, events):
        self.duration -= dt

    def over(self):
        return self.duration < 0

    def to_string(self):
        if self.over():
            return "0"
        else:
            return f"{int(self.duration)}"

    def draw(self, surface, offset=(0, 0)):
        text_surf = self.game.scoreboard_font.render("Next round in ", 1, self.color)
        surf = self.game.small_timer_font.render(self.to_string(), 1, self.color)
        width = text_surf.get_width() + surf.get_width()
        x = self.pose.x + offset[0] - width//2
        y = self.pose.y + offset[1]
        scale = 0.6 + abs(math.sin(self.duration * math.pi)) * 0.4
        scale = 1 - (1 - scale)**1.5
        if self.duration < 0:
            scale = max(0, 0.7 + self.duration)
        scaled_surf = pygame.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
        surface.blit(scaled_surf,
            (x + text_surf.get_width() + surf.get_width()//2 - scaled_surf.get_width()//2,
            y - scaled_surf.get_height()//2))
        surface.blit(text_surf, (x, y - text_surf.get_height()//2))

class TransitionGui(GameObject):

    def __init__(self, game):
        super().__init__(game)
        self.age = 0
        self.width = c.WINDOW_WIDTH - c.SCORE_TABLE_WIDTH
        self.height = c.WINDOW_HEIGHT
        self.pose = Pose((c.SCORE_TABLE_WIDTH + self.width//2, c.WINDOW_HEIGHT//2), 0)
        self.objects = []
        self.background = pygame.image.load(c.IMAGE_PATH + "/trans_gui_back.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.add_tip_box()
        self.add_player_mult_box()
        self.objects.append(Countdown(self.game, (0, c.WINDOW_HEIGHT*0.44)))
        self.countdown = self.objects[-1]
        mod_options = random.sample(c.MODIFICATIONS, 2)
        self.voting = VotingObject(self.game, self, (0, 0), mod_options)
        self.objects.append(self.voting)

    def countdown_over(self):
        return self.countdown.over()

    def add_tip_box(self):
        position = 0, c.WINDOW_HEIGHT*0.30
        header = "Helpful hint"
        body = random.choice(c.HINTS)
        #ss = pygame.image.load(c.IMAGE_PATH + "/bang.png")
        self.objects.append(GreenAlertBox(self.game, position, header, body))

    def add_player_mult_box(self):
        position = 0, -c.WINDOW_HEIGHT * 0.35
        header = "Player party multiplier"
        if self.game.player_multiplier() == 0:
            choices = c.MULT_0_MESSAGES
        else:
            choices = c.MULT_MESSAGES
        body = random.choice(choices).replace("{num}", str(self.game.number_of_players_last_round()))
        self.objects.append(PlayerMultiplierAlertBox(self.game, position, header, body))

    def vote(self, player, option):
        if self.voting.picked is None:
            self.game.vote_sound.play()
            return self.voting.vote(player, option)

    def update(self, dt, events):
        self.age += dt
        for item in self.objects:
            item.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        xoff = offset[0] + self.pose.x
        yoff = offset[1] + self.pose.y
        surface.blit(self.background, (xoff - self.width//2, yoff - self.height//2))
        for item in self.objects:
            item.draw(surface, (xoff, yoff))
