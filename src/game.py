##!/usr/bin/env python3

import sys
import string
import random

import pygame

import constants as c
from error_logging import error_logging
from start_scene import StartScene
from twitch_chat_stream import Stream
from level_scene import LevelScene
from player import Player
from score_manager import ScoreManager
from high_score_scene import HighScoreScene
from high_score_table import HighScoreTable
from alert_manager import AlertManager

class Game:
    def __init__(self):
        pygame.init()
        if c.FULLSCREEN:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.players_in_last_round = set()
        self.stream = Stream(channel="plasmastarfish")
        self.scoreboard = ScoreManager.from_file("test_scores.pkl")
        self.temp_scores = {}
        # if not len(self.scoreboard.scores):
        #     self.scoreboard.add_score("N4tticus", 5000)
        #     self.scoreboard.add_score("ZebulahCrimson", 3500)
        #     self.scoreboard.add_score("superduperpacman42", 2500)
        self.last_snapshot = None
        self.players = {name:Player(self, name) for name in ["superduperpacman42"]}
        self.player_label_font = pygame.font.Font(c.FONT_PATH + "/pixel_caps.ttf", 12)
        self.timer_font = pygame.font.Font(c.FONT_PATH + "/asap-bold.otf", 55)
        self.small_timer_font = pygame.font.Font(c.FONT_PATH + "/asap-bold.otf", 40)
        self.timer_render = {digit:self.timer_font.render(digit, 1, c.WHITE) for digit in "1234567890:-"}
        self.red_timer_render = {digit:self.timer_font.render(digit, 1, (255, 80, 80)) for digit in "1234567890:-"}
        self.small_font = pygame.font.Font(c.FONT_PATH + "/a_goblin_appears.ttf", 10)
        self.small_font_render = {char:self.small_font.render(char, 0, c.WHITE) for char in string.printable}
        self.very_small_font = pygame.font.Font(c.FONT_PATH + "/a_goblin_appears.ttf", 7)
        self.scoreboard_font = pygame.font.Font(c.FONT_PATH + "/asap.otf", 25)
        self.small_scoreboard_font = pygame.font.Font(c.FONT_PATH + "/asap.otf", 16)
        self.scoreboard_title_font = pygame.font.Font(c.FONT_PATH + "/eras_demi_bold.ttf", 40)
        self.scoreboard_description_font = pygame.font.Font(c.FONT_PATH + "/eras_demi.ttf", 25)
        self.alert_body_font = pygame.font.Font(c.FONT_PATH + "/asap-italic.otf", 15)
        self.alert_header_font = pygame.font.Font(c.FONT_PATH + "/asap-bold.otf", 18)
        self.scoreboard_font.bold = False
        self.alert_large_font = pygame.font.Font(c.FONT_PATH + "/eras_demi.ttf", 50)
        self.other_alert_font = pygame.font.Font(c.FONT_PATH + "/asap.otf", 14)
        self.current_scene = HighScoreScene(self)
        self.fps = [0]
        self.alertManager = AlertManager(self)
        self.main()

    def update_globals(self):
        """ Update global events, like checking for game close.
            Returns a tuple (dt, events), where dt is the float amount of
            seconds since the last update_globals call and events is a list
            of PyGame events that have occurred since the last call.
        """
        dt = self.clock.tick(c.MAX_FPS)
        dt /= 1000 # ms to seconds
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.close()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.current_scene.lastLevel = self.current_scene.level
                self.current_scene.spawn_level()
                self.current_scene.ships = []
                self.current_scene.spawn_ship("t100", "superduperpacman42")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                message = random.choice(c.JOKE_MESSAGES)
                self.alertManager.alert(message)
        self.alertManager.update(dt)
        return dt, events

    def close(self):
        """ Close the game. """
        try:
            self.scoreboard.save_if_changes()
        except NameError:
            pass
        pygame.quit()
        sys.exit()

    def update_screen(self):
        """ Update the pygame display.

            This can also be used as a hook to add game-wide
            display objects, like an FPS monitor.
        """
        fps_text = f"FPS: {int(sum(self.fps)/len(self.fps))}"
        self.screen.blit(self.small_font.render(fps_text, 0, c.BLACK), (10, 10))
        self.screen.blit(self.small_font.render(fps_text, 0, c.WHITE), (8, 9))
        self.alertManager.draw(self.screen)
        pygame.display.flip()

    def main(self):
        while True:
            self.current_scene.main()
            self.current_scene = self.current_scene.next_scene()
            if self.current_scene is None:
                self.close()

    def high_score_scene(self):
        return HighScoreScene(self)

    def number_of_players_last_round(self):
        return len(self.players_in_last_round)

    def player_multiplier(self):
        if self.number_of_players_last_round() < 3:
            return 0
        elif self.number_of_players_last_round() < 10:
            return 1
        elif self.number_of_players_last_round() < 30:
            return 2
        else:
            return 3

if __name__ == '__main__':
    with error_logging(c.LOG_PATH):
        Game()
