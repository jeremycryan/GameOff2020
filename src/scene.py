##!/usr/bin/env python3

import pygame

import constants as c
from primitives import GameObject

class Scene(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = True

    def main(self):
        lag = 0
        fps_queue = []
        max_ticks_per_render = 5
        while self.is_running:
            dt, events = self.game.update_globals()
            lag += dt
            ticks_this_render = 0
            while lag > c.TICK_LENGTH:
                lag -= c.TICK_LENGTH
                self.update(c.TICK_LENGTH, events)
                ticks_this_render += 1
                if ticks_this_render >= max_ticks_per_render:
                    lag = 0
                    break
            self.draw(self.game.screen)
            fps_queue.append(1/dt)
            if len(fps_queue) > 20:
                self.game.fps = fps_queue + self.game.fps[:40]
                fps_queue = []
            self.game.update_screen()

    def next_scene(self):
        raise NotImplementedError()
