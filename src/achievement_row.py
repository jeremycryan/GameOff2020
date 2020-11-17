##!/usr/bin/env python3

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
                                                  surface.get_height()))
            self.points = points
            self.description = description

        def update(self, dt, events):
            pass

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
