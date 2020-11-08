##!/usr/bin/env python3

from planet import Planet

class Moon(Planet):
    def __init__(self, game, position):
        super.__init__(position, 0, radius=50)

    def is_moon(self):
        return True
