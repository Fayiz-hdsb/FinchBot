from Finchbot.BirdBrain import Finch
import pygame
pygame.init()
bird = Finch()
from time import sleep

dKeyIsDown:bool = False
aKeyIsDown:bool = False

while True:    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bird.setMotors(100, 100)
            if event.key == pygame.K_d:
                dKeyIsDown = True
            if event.key == pygame.K_a:
                aKeyIsDown = True
            if event.key == pygame.K_s:
                bird.setMotors(-100, -100)
        elif event.type == pygame.KEYUP:
            bird.setMotors(0,0)

            if(event.key == pygame.K_d):
                dKeyIsDown=False
            if(event.key == pygame.K_a):
                aKeyIsDown=False
        
    if dKeyIsDown:
        bird.setTurn('R',30,100)
    if(aKeyIsDown):
        bird.setTurn('L',15,100)