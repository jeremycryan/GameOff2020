##!/usr/bin/env python3

import pygame

from primitives import GameObject

class Scene(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = True

    def main(self):
        while self.is_running:
            dt, events = self.game.update_globals()
            self.update(dt, events)
            self.draw(self.game.screen)
            self.game.update_screen()

    def next_scene(self):
        raise NotImplementedError()
