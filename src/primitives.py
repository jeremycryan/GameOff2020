##!/usr/bin/env python3

class GameObject:
    def __init__(self, game):
        self.game = game

    def update(self, dt, events):
        raise NotImplementedError()

    def draw(self, surf, offset=(0, 0)):
        raise NotImplementedError()
