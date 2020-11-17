##!/usr/bin/env python3

import random

import pygame

from primitives import GameObject, Pose
import constants as c

class AchievementRow(GameObject):

    class AchievementPanel(GameObject):
        def __init__(self,
                    game,
                    container,
                    surface,
                    points,
                    description):
            super().__init__(game)
            self.container = container
            self.surface = pygame.transform.scale(surface,
                                                  (c.ACHIEVEMENT_WIDTH,
                                                  surface.get_height())).convert()
            self.points = points
            self.description = description
            self.achieved = False

        def update(self, dt, events):
            pass

        def achieve(self, player):
            base_color = self.surface.get_at((0, 0))
            cover_surf = pygame.Surface((self.surface.get_width() - c.ACHIEVEMENT_POINTS_WIDTH, self.surface.get_height() - 3))
            cover_surf.fill(base_color)
            self.surface.blit(cover_surf, (c.ACHIEVEMENT_POINTS_WIDTH, 0))

            veil_surf = pygame.Surface((c.ACHIEVEMENT_WIDTH, self.surface.get_height()-3))
            veil_surf.fill(c.BLACK)
            veil_surf.set_alpha(150)
            self.surface.blit(veil_surf, (0, 0))

            font = self.game.small_font if len(player.name) < 15 else self.game.very_small_font
            font_render = font.render(player.name[:23].upper(), 0, player.color)
            y = self.surface.get_height()//2 - font_render.get_height()//2
            x = (c.ACHIEVEMENT_WIDTH - c.ACHIEVEMENT_POINTS_WIDTH)//2 + c.ACHIEVEMENT_POINTS_WIDTH - font_render.get_width()//2

            self.game.scoreboard.add_score(player.name, self.points)

            self.surface.blit(font_render, (x, y))


        def draw(self, surface, offset=(0, 0)):
            shake_offset = self.game.current_scene.apply_screenshake((0, 0))
            x = self.container.pose.x + offset[0]
            y = self.container.pose.y + offset[1]
            surface.blit(self.surface, (x, y))


    def __init__(self, game, top_left_position=(0, 0)):
        super().__init__(game)
        self.pose = Pose(top_left_position, 0)
        self.achievements = self.default_achievements()
        self.label = pygame.image.load(c.IMAGE_PATH + "/achievement_box_header.png")
        self.label = pygame.transform.scale(self.label, (c.ACHIEVEMENT_LABEL_WIDTH, self.label.get_height()))
        self.body = pygame.image.load(c.IMAGE_PATH + "/achievement_box_body.png")
        self.body = pygame.transform.scale(self.body,
            (c.ACHIEVEMENT_LABEL_WIDTH,
            sum([item.surface.get_height() for item in self.achievements]) + 5 * (len(self.achievements) - 1) + 8))
        random.choice(self.achievements).achieve(self.game.players["PlasmaStarfish"])

    def default_achievements(self):
        achievements = [
            AchievementRow.AchievementPanel(self.game,
                self,
                pygame.image.load(c.IMAGE_PATH + "/achievement_1.png"),
                1000,
                "land on moon"),
            AchievementRow.AchievementPanel(self.game,
                self,
                pygame.image.load(c.IMAGE_PATH + "/achievement_2.png"),
                1000,
                "1 thing and land on moon"),
            AchievementRow.AchievementPanel(self.game,
                self,
                pygame.image.load(c.IMAGE_PATH + "/achievement_3.png"),
                1000,
                "2 things and land on moon")
        ]
        return achievements


    def update(self, dt, events):
        for item in self.achievements:
            item.update(dt, events)

    def draw_box(self, surface, offset=(0, 0)):
        x = self.pose.x + offset[0]
        y = self.pose.y + offset[1]
        surface.blit(self.label, (x, y))
        y += self.label.get_height()
        surface.blit(self.body, (x, y))
        return y - self.pose.y

    def draw(self, surface, offset=(0, 0)):
        x = self.pose.x + c.SIDE_PANEL_WIDTH//2 - c.ACHIEVEMENT_WIDTH//2
        y = self.draw_box(surface, offset)
        #surface.blit(self.label, (x, y))
        for item in self.achievements:
            item.draw(surface, (x, y))
            y += item.surface.get_height() + 5
