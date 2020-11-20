##!/usr/bin/env python3

import sys

import pygame

import constants as c
from error_logging import error_logging
from start_scene import StartScene
from twitch_chat_stream import Stream
from level_scene import LevelScene
from player import Player
from score_manager import ScoreManager

class Game:
    def __init__(self):
        pygame.init()
        if c.FULLSCREEN:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(c.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.stream = Stream(channel="plasmastarfish")
        self.scoreboard = ScoreManager.from_file("test_scores.pkl")
        self.players = {name:Player(self, name) for name in ["PlasmaStarfish", "superduperpacman42"]}
        self.player_label_font = pygame.font.Font(c.FONT_PATH + "/pixel_caps.ttf", 12)
        self.timer_font = pygame.font.Font(c.FONT_PATH + "/a_goblin_appears.ttf", 40)
        self.timer_render = {digit:self.timer_font.render(digit, 0, c.WHITE) for digit in "1234567890:-"}
        self.red_timer_render = {digit:self.timer_font.render(digit, 0, (255, 80, 80)) for digit in "1234567890:-"}
        self.small_font = pygame.font.Font(c.FONT_PATH + "/a_goblin_appears.ttf", 10)
        self.very_small_font = pygame.font.Font(c.FONT_PATH + "/a_goblin_appears.ttf", 7)
        self.current_scene = LevelScene(self)
        self.fps = [0]
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
        pygame.display.flip()

    def main(self):
        while True:
            self.current_scene.main()
            self.current_scene = self.current_scene.next_scene()
            if self.current_scene is None:
                self.close()

if __name__ == '__main__':
    with error_logging(c.LOG_PATH):
        Game()
