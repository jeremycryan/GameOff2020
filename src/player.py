##!/usr/bin/env python3

import random

class Player:
    def __init__(self, game, name, color=None):
        self.name = name
        self.color = color if color is not None else self.random_color()

    @staticmethod
    def random_color():
        a = 90
        b = 128 + random.random() * 128
        c = 192 + random.random() * 64
        rgb = [a, b, c]
        random.shuffle(rgb)
        return tuple(rgb)
