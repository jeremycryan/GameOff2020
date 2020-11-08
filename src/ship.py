##!/usr/bin/env python3

import constants as c
from primitives import PhysicsObject

class Ship(PhysicsObject):
    def __init__(self, game, program_string, player, position=(0, 0), angle=90):
        super().__init__(game, position, angle)
        self.program_string = program_string
        self.program = parse_program(program_string)
        self.player = player
        self.age = 0
        self.commandIndex = 0
        self.delay = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        if self.delay > 0:
            self.delay = max(0, self.delay-dt)
        while self.delay <= 0 and self.commandIndex < len(self.program):
            if self.command[i][0] == 'd': # delay
                self.delay += self.command[i][1]
            if self.command[i][0] == 't': # thrust
                # self.acceleration[0] += self.command[i][1]
            if self.command[i][0] == 'r': # rotate
                self.velocity[2] = self.command[i][1]
            self.commandIndex += 1




    def draw(self, surface, offset=(0, 0)):
        pass
        # draw a spaceship using self.pose
    
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
                if number[1:].isnumeric() and \
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
        print(program)
        return program

if __name__ == '__main__':
    Ship.parse_program("Thrust;100 ; d20 r-10")
