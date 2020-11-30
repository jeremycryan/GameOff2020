##!/usr/bin/env python3

import pygame

import constants as c
from scene import Scene
from level_scene import LevelScene
from high_score_table import HighScoreTable
from transition_gui import TransitionGui

class HighScoreScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for player in self.game.players:
            if player not in [item.name for item in self.game.scoreboard.scores]:
                self.game.scoreboard.add_score(player, 0)

        self.board_offset = -c.WINDOW_HEIGHT
        self.table = HighScoreTable(self.game)
        self.table_all = HighScoreTable(self.game, hours_to_display=10**9)
        self.table.pose.x = c.WINDOW_WIDTH * 0.3
        self.table_all.pose.x = self.table.pose.x
        self.age = 0
        self.shade = pygame.Surface(c.WINDOW_SIZE)
        self.shade.fill(c.BLACK)
        self.shade_alpha = 255
        self.scene_over = False
        self.side_gui = TransitionGui(self.game)
        pygame.mixer.music.set_volume(0.25)

    def next_scene(self):
        pygame.mixer.music.set_volume(1.0)
        return LevelScene(self.game)

    def update(self, dt, events):
        self.age += dt

        if self.age > 25 and self.board_offset < 0:
            speed = 4
            d = abs(self.board_offset)
            self.board_offset += min(d * dt * speed, c.WINDOW_HEIGHT*dt*2)
            if self.board_offset > 0:
                self.board_offset = 0

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.scene_over = True
        if self.side_gui.countdown_over():
            self.scene_over = True
        self.table.update(dt, events)
        self.table_all.update(dt, events)
        self.side_gui.update(dt, events)

        for message in self.game.stream.queue_flush():
            if message.text.lower() == '!recolor':
                if message.user in self.game.players:
                    self.game.players[message.user].recolor()
                    self.game.recolor_flag(message.user)
            elif message.text.lower() == '!score':
                board = self.game.scoreboard.get_total_by_player(c.SCORE_EXPIRATION)
                if message.user in board:
                    score = self.game.scoreboard.get_total_by_player(c.SCORE_EXPIRATION)[message.user].score
                    self.game.alertManager.alert("Your score is "+str(score), message.user)
                else:
                    self.game.alertManager.alert("You have not played in the last " + str(c.SCORE_EXPIRATION) + " hours", message.user)
            elif message.text.lower()[:5] == "!vote":
                split = message.text.lower().split()
                if len(split) != 2:
                    self.game.alertManager.alert("Invalid number of arguments for !vote", message.user)
                    continue
                player_name = message.user
                argument = split[1]
                self.game.current_scene.side_gui.vote(player_name, argument)

        speed = 800
        if self.scene_over:
            self.shade_alpha += speed*dt
        else:
            self.shade_alpha -= speed*dt
        self.shade_alpha = max(0, min(255, self.shade_alpha))

        if self.scene_over and self.shade_alpha == 255:
            self.is_running = False

    def draw(self, surface, offset=(0, 0)):
        surface.fill(c.BLACK)
        surface.blit(self.table.background_surface, (0, 0))
        self.table.draw(surface, (offset[0], offset[1] + self.board_offset + c.WINDOW_HEIGHT))
        self.table_all.draw(surface, (offset[0], offset[1] + self.board_offset))
        self.side_gui.draw(surface, offset)

        if self.shade_alpha > 0:
            self.shade.set_alpha(self.shade_alpha)
            surface.blit(self.shade, (0, 0))
