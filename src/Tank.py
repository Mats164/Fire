import time
import os
import sys

from math import sin, cos, radians
import numpy as np
import pygame
from pygame.version import ver

class Player:
    def __init__(self, verticies, colour=(0, 255, 0)) -> None:
        self.verticies = verticies
        self.colour = colour

    def shoot(self):
        pass

    def movement(self, keys):
        if playArea.current_display == 'pause':
            pass
        else:
            if keys[pygame.K_w]:
                self.verticies = self.move()
            elif keys[pygame.K_s]:
                self.verticies = self.move(forward=False)
            elif keys[pygame.K_a]:
                self.verticies = self.rotate(self.verticies, right)
            elif keys[pygame.K_d]:
                self.verticies = self.rotate(self.verticies, left)
        return None

    def move(self, forward=True):
        out = []
        self.direction = (self.verticies[0][0] - self.verticies[1][0],
                          self.verticies[0][1] - self.verticies[1][1])
        for point in self.verticies:
            if forward:
                new_point = (point[0] + self.direction[0], point[1] + self.direction[1])
            else:
                new_point = (point[0] - self.direction[0], point[1] - self.direction[1])
            out.append(new_point)
        return out

    def draw(self):
        pygame.draw.polygon(playArea.main, 
                            self.colour, 
                            upscale_model(self.verticies[2:], 
                            upscale, 
                            center)
                            )
        return None

    def rotate(self, verticies, angle):
        out = []

        dx = verticies[0][0]
        dy = verticies[0][1]
        θ = radians(angle)

        rotN = np.array([
            [cos(θ), -sin(θ), ((-dx)*cos(θ)) + (dy*sin(θ)) + dx],
            [sin(θ), cos(θ), ((-dx*sin(θ)) - (dy*cos(θ)) + dy)],
            [0, 0, 1]
        ])

        for point in verticies:
            vector = np.array([
                [point[0]],
                [point[1]],
                [1]
            ])
            new_point = np.matmul(rotN, vector)
            new_point = [new_point[0, 0], new_point[1, 0]]
            out.append(new_point)
        return out

# class Projectile(Player):
#     def __init__(self, verticies, colour, direction) -> None:
#         self.direction = direction
#         self.move()
#         super().__init__(verticies, colour=colour)

#     def move(self, forward=True):
#         return super().move(forward=forward)

class Display:

    resolution = [1000, 800]

    def __init__(self, initDisplay) -> None:
        self.current_display = initDisplay
        self.main = pygame.display.set_mode(self.resolution)
        self.pause = pygame.display.set_mode(self.resolution)

    def update(self):
        if self.current_display == "main":
            self.main.fill((0, 0, 255))
            tank1.draw()
        elif self.current_display == "pause":
            self.pause.fill((100, 0, 200))
        return None

pygame.init()
pygame.display.set_caption("Tank")

clock = pygame.time.Clock()
fps = 60
right = -1
left = 1
upscale = 10
center = [Display.resolution[i] / 2 for i in range(2)]

verticies = np.array([
    [0, 0],
    [0, 1],
    [-1.5, 2], 
    [1.5, 2], 
    [1.5, 1.5], 
    [2, 1.5], 
    [2, -0.5], 
    [1.5, -0.5], 
    [1.5, -2], 
    [0.5, -2], 
    [0.5, -4.5], 
    [-0.5, -4.5], 
    [-0.5, -2], 
    [-1.5, -2], 
    [-1.5, -0.5], 
    [-2, -0.5], 
    [-2, 1.5], 
    [-1.5, 1.5]
])

tank1 = Player(verticies=verticies)
playArea = Display(initDisplay='main')

def upscale_model(cordinates, upscale, center):
    out = []
    for point in cordinates:
        out.append((point[0]*upscale + center[0], point[1]*upscale + center[1]))
    return out

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    keys = pygame.key.get_pressed()

    tank1.movement(keys=keys)

    if keys[pygame.K_ESCAPE]:
        if playArea.current_display == 'main':
            playArea.current_display = 'pause'
            time.sleep(0.3)
        else:
            playArea.current_display = 'main'
            time.sleep(0.3)

    playArea.update()

    pygame.display.update()
    clock.tick(fps)