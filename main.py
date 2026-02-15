# Snek
#
# A "Snake" game
# Controls are cursor/arrow keys
# Collect the yellow dots
# Press Space to restart
import asyncio
import pygame

from collections import deque
from random import randrange

pygame.init()
boxsize=10
game_font = pygame.font.SysFont("Arial", 24)

field_width  = 64
field_height = 64
window = pygame.display.set_mode((field_width  * boxsize,\
                                  field_height * boxsize))
clock = pygame.time.Clock()
keys= {pygame.K_RIGHT:0, pygame.K_DOWN:1,
       pygame.K_LEFT :2, pygame.K_UP  :3}
d_keys=[False]*4
dir=[(1,0),(0,1),(-1,0),(0,-1)]

async def main():
    to_start = False
    while True:
        playing=True
        points=0
        level=1
        snake=deque([(field_width/2,field_height/2)])
        d=None
        grow=10
        fruit=[]
        for _ in range(20):
            while True:
                n=(randrange(field_width), randrange(field_height))
                if not (n in fruit):
                    fruit.append(n)
                    break
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                kd=False
                if (kd:= event.type == pygame.KEYDOWN) or event.type == pygame.KEYUP:
                    if event.key in keys:
                        d_keys[keys[event.key]]=kd

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:
                        to_start = True

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_SPACE:
                        to_start = False
            if playing:
                s=snake[-1]
                if True in d_keys:
                    d=d_keys.index(True)
                if d!=None:
                    x=s[0]+dir[d][0]
                    y=s[1]+dir[d][1]
                    if x<0:
                        x+=field_width
                    elif x>=field_width:
                        x-=field_width
                    if y<0:
                        y+=field_height
                    elif y>=field_height:
                        y-=field_height
                    if (x,y) in fruit:
                        fruit.remove((x,y))
                        points+=1
                        grow+=8+level*2
                    if (x,y) in snake:
                        playing=False
                    snake.append((x,y))
                    if grow:
                        grow-=1
                    else:
                        snake.popleft()
                if len(fruit) <=5:
                    level+=1
                    fruit=[]
                    for _ in range(18+level*2):
                        while True:
                            n=(randrange(field_width), randrange(field_height))
                            if not (n in fruit):
                                fruit.append(n)
                                break
                    snake=deque([(field_width/2,field_height/2)])
                    d=None
                    grow=10        
            elif to_start:
                break

        #    if to_left:
        #        hx -= 1
        #    if to_right:
        #        hx += 1
        #    if to_up:
        #        hy -= 1
        #    if to_down:
        #        hy += 1
            window.fill((0,0,0))
            for f in fruit:
                x=f[0]*boxsize
                y=f[1]*boxsize
                pygame.draw.rect(window,(255,255,0),(x,y,boxsize,boxsize))
            for s in list(snake)[0:-1]:
                x=s[0]*boxsize
                y=s[1]*boxsize
                pygame.draw.rect(window,(255,0,0),(x,y,boxsize,boxsize))
            for s in list(snake)[-1:]:
                x=s[0]*boxsize
                y=s[1]*boxsize
                pygame.draw.rect(window,(0,255,0),(x,y,boxsize,boxsize))
                
            game_text = game_font.render("Points: " + str(points), True, (255, 255, 255))
            window.blit(game_text, (400, 10))
            if not playing:
                game_text = game_font.render("Game Over", True, (255, 255, 255))
                window.blit(game_text, (320-game_text.get_width()//2, 100))
                game_text = game_font.render("Press Space to Start", True, (255, 255, 255))
                window.blit(game_text, (320-game_text.get_width()//2, 350))

            pygame.display.flip()
            await asyncio.sleep(0) 

            clock.tick(20)
            
asyncio.run(main())
