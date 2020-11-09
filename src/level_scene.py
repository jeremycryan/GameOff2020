##!/usr/bin/env python3

import constants as c
from scene import Scene
from planet import Planet
from ship import Ship
from primitives import Pose

class LevelScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.planets = [Planet(self.game, (200, 200), 0),
                        Planet(self.game, (500, 500), 0, 50, 100)]
        self.ships = [Ship(self.game, "r0 t100 d200 t0", self.game.players["Paul"], (500, 200), 180)]

    def update(self, dt, events):
        for object_to_update in self.ships + self.planets:
            object_to_update.update(dt, events)

    def draw(self, surf, offset=(0, 0)):
        surf.fill(c.BLACK)
        for planet in self.planets:
            planet.draw(surf, offset)
        for ship in self.ships:
            ship.draw(surf, offset)
