##!/usr/bin/env python3

import sys

import pygame

import constants as c
from error_logging import error_logging
from start_scene import StartScene
from twitch_chat_stream import Stream
from level_scene import LevelScene
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(c.WINDOW_SIZE, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.stream = Stream(channel="TwitchPlaysPokemon")
        self.players = {name:Player(self, name) for name in ["Paul", "Jeremy"]}
        self.current_scene = LevelScene(self)
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
        return dt, events

    def close(self):
        """ Close the game. """
        pygame.quit()
        sys.exit()

    def update_screen(self):
        """ Update the pygame display.

            This can also be used as a hook to add game-wide
            display objects, like an FPS monitor.
        """
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
