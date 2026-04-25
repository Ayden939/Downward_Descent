import pygame
import sys
from character import Character
from enemy import Skeleton, Goblin, Phantom
from database import log
import database
import random
from equipment import Sword, Shield
from loot import loot_drop

# Game objects
hero = Character("Lady Samantha Rostnovak", 1)
floor = 1
retreat = False
enemy = random.choice([Skeleton(), Goblin(), Phantom()])

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 40)


while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    fpsClock.tick(fps)


database.con.close()