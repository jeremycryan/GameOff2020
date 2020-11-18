##!/usr/bin/env python3

import pygame
import constants as c
from primitives import PhysicsObject, Pose
from player import Player
from exhaust_particle import ExhaustParticle
from explosion import Explosion
from death_particle import DeathParticle

class Ship(PhysicsObject):
    def __init__(self, game, program_string, player, position=(0, 0), angle=90):
        super().__init__(game, position, angle)
        self.program_string = program_string
        self.program = self.parse_program(program_string)
        self.player = player
        self.age = 0
        self.thrust = Pose((0,0), 0)
        self.commandIndex = 0
        self.delay = 0
        self.destroyed = False
        self.surface = self.get_surface()
        self.since_exhaust = 0
        self.radius = 10
        self.label = self.game.player_label_font.render(self.player.name,
                                                        0,
                                                        self.player.color)
        self.label_back = pygame.Surface((self.label.get_width() + 10,
                                          self.label.get_height() + 10))
        self.label_back.fill(c.BLACK)
        self.label_back.set_alpha(100)
        self.label_offset = Pose((0, -35), 0)
        self.label_pose = self.pose - self.label_offset

        self.scale = 0
        self.target_scale = 1

        self.nuggets = set()

    def get_surface(self):
        surface = pygame.image.load(c.IMAGE_PATH + "/ship.png").convert()
        color_surf = pygame.Surface((surface.get_width(), surface.get_height()))
        color_surf.fill(self.player.color)
        surface.blit(color_surf, (0, 0), special_flags=pygame.BLEND_MULT)
        surface.set_colorkey(surface.get_at((surface.get_width()-1, surface.get_height()-1)))
        return surface

    def destroy(self):
        self.destroyed = True
        self.game.current_scene.particles.add(Explosion(self.game, self))
        for i in range(8):
            self.game.current_scene.particles.add(DeathParticle(self.game, self))
        self.game.current_scene.shake(20)

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        self.since_exhaust += dt
        exhaust_period = 0.05
        if self.since_exhaust > exhaust_period:
            self.since_exhaust -= exhaust_period
            self.game.current_scene.particles.add(ExhaustParticle(self.game, self))
        if self.delay > 0:
            self.delay = max(0, self.delay-dt)
        self.runCommands(dt)
        self.acceleration.clear()
        self.acceleration.add_pose(self.thrust, 1, frame=self.pose)
        for planet in self.game.current_scene.planets:
            self.acceleration.add_pose(planet.get_acceleration(self))
        for nugget in self.game.current_scene.nuggets:
            nugget.test_collision(self)

        ds = self.target_scale - self.scale
        if ds < 0.01:
            self.scale = self.target_scale
        self.scale += ds * dt * 8

        if self.pose.y < 120:
            self.label_offset = Pose((0, 35), 0)
        if self.pose.y > 150:
            self.label_offset = Pose((0, -35), 0)
        dl = self.pose - (self.label_pose - self.label_offset)
        self.label_pose += dl * dt * 12

        if self.pose.x < 0 or self.pose.x > c.LEVEL_WIDTH or \
            self.pose.y < 0 or self.pose.y > c.LEVEL_HEIGHT:
            self.destroy()

    def runCommands(self, dt):
        while self.delay <= 0 and self.commandIndex < len(self.program):
            command = self.program[self.commandIndex]
            if command[0] == 'd': # delay
                self.delay += command[1]/1000
            if command[0] == 't': # thrust
                self.thrust = Pose((command[1]*c.THRUST, 0), 0)
            if command[0] == 'r': # rotate
                self.velocity.set_angle(command[1])
            self.commandIndex += 1

    def draw(self, surface, offset=(0, 0)):
        if self.destroyed:
            return

        if self.label_pose.x < self.label_back.get_width()//2 + 10:
            self.label_pose.x = self.label_back.get_width()//2 + 10
        if self.label_pose.x > c.LEVEL_WIDTH - self.label_back.get_width()//2 - 10:
            self.label_pose.x = c.LEVEL_WIDTH - self.label_back.get_width()//2 - 10

        x = self.label_pose.x + offset[0] - self.label_back.get_width()//2
        y = self.label_pose.y + offset[1] - self.label_back.get_height()//2
        surface.blit(self.label_back, (x, y))

        x = self.label_pose.x + offset[0] - self.label.get_width()//2
        y = self.label_pose.y + offset[1] - self.label.get_height()//2
        surface.blit(self.label, (x, y))

        if self.scale == 0:
            return

        ship_surf = pygame.transform.scale(self.surface,
                                           (int(self.surface.get_width() * self.scale),
                                           int(self.surface.get_height() * self.scale)))
        ship_surf = pygame.transform.rotate(ship_surf, self.pose.angle)
        x = self.pose.x + offset[0] - ship_surf.get_width()//2
        y = self.pose.y + offset[1] - ship_surf.get_height()//2
        surface.blit(ship_surf, (x, y))

    @staticmethod
    def parse_program(program_string):
        program_string = program_string.lower().strip() + 'A'
        program = []
        arguments = []
        key = ''
        number = ''
        isNumber = False
        for char in program_string:
            if char == '.':
                print("Decimals not permitted")
                return []
            elif char.isnumeric() or char == '-':
                isNumber = True
                number += char
            elif char.isalnum():
                # terminate previous number
                if (len(number) == 1 or number[1:].isnumeric()) and \
                (number[0].isdigit() or number[0] == '-'):
                    arguments.append(int(number))
                    number = ''
                elif number != '':
                    print("Invalid number")
                    return []
                # terminate previous command
                if isNumber or char == 'A':
                    if key in c.COMMANDS.values():
                        command = key
                    elif key in c.COMMANDS:
                        command = c.COMMANDS[key]
                    else:
                        print("Invalid command")
                        return []
                    if len(arguments) != len(c.COMMANDS_MIN[command]):
                        print("Invalid number of arguments")
                        return []
                    for i, arg in enumerate(arguments):
                        if arg < c.COMMANDS_MIN[command][i]:
                            print("Argument was smaller than minimum value")
                            return []
                        if arg > c.COMMANDS_MAX[command][i]:
                            print("Argument was greater than maximum value")
                            return []
                    program.append((command, *arguments))
                    key = ''
                    arguments = []
                    isNumber = False
                key += char
            elif char in " ,;":
                isNumber = True
                if number[1:].isnumeric() and \
                (number[0].isdigit() or number[0] == '-'):
                    arguments.append(int(number))
                    number = ''
            else:
                print("Invalid character")
                return []
        return program

if __name__ == '__main__':
    Ship.parse_program("t100 r9 d1000 t1")
