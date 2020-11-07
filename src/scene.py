##!/usr/bin/env python3

import pygame

import primitives as p

class Scene(p.GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = True

    def main(self):
        while self.is_running:
            dt, events = self.game.update_globals()
            self.update(dt, events)
            self.draw(self.game.screen)
            pygame.display.flip()

    def next_scene(self):
        raise NotImplementedError()
