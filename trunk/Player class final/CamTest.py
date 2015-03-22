# Test Program player class
# Rock G Bolton + Cameron Schuette
import pygame
import time
import math
import NewBullet
import CamCharacterClass
import world
import glob
import configparser
import random


area = world.Zone()

pygame.display.init()
pygame.font.init()
window = pygame.display.set_mode((area.winWidth, area.winHeight))
area.CreateEnemy()


#variables
done = False
aiming = False
active = False
key_pressed = []
bulletArray = []
clock = pygame.time.Clock()
p_pos = [area.winWidth/2, area.winHeight/2 + 100]
p_vel = [0, 0]
p_vel_mag = 200 / 1000.0
e_vel_mag = 100 / 1000.0
damage = 10
bul_pos = [p_pos[0],p_pos[1]]
p_state = 0
cameraspeed = 3

#create classes
test = CamCharacterClass.Cleric(p_pos, p_vel_mag, 1)

while not done:
	area.CreateEnemy()

	evtList = pygame.event.get()
	for evt in evtList:
		if evt.type == pygame.QUIT:
			done = True
		elif evt.type == pygame.KEYDOWN:
			key_pressed.append(evt.key)
		elif evt.type == pygame.KEYUP:
			key_pressed.remove(evt.key)
		elif evt.type == pygame.MOUSEMOTION:
			pygame.mouse.get_pos()
			mx = evt.pos[0]
			my = evt.pos[1]
		elif evt.type == pygame.MOUSEBUTTONDOWN:
			pygame.mouse.get_pos()
			mx = evt.pos[0]
			my = evt.pos[1]
			angle = math.atan2(-(my - (p_pos[1] - area.cameraPos[1])), mx - (p_pos[0] - area.cameraPos[0]))
			b_test = NewBullet.bullet(p_pos[0] - area.cameraPos[0], p_pos[1] - area.cameraPos[1], angle, damage)
			test.bullets.append(b_test)
			active = True

	if pygame.K_UP in key_pressed and pygame.K_RIGHT in key_pressed:
	   test.walkdir = 2
	   p_state = 1

	elif pygame.K_DOWN in key_pressed and pygame.K_RIGHT in key_pressed:
	   test.walkdir = 4
	   p_state = 1

	elif pygame.K_DOWN in key_pressed and pygame.K_LEFT in key_pressed:
	   test.walkdir = 6
	   p_state = 1

	elif pygame.K_UP in key_pressed and pygame.K_LEFT in key_pressed:
	   test.walkdir = 8
	   p_state = 1

	elif pygame.K_UP in key_pressed:
	   test.walkdir = 1
	   p_state = 1

	elif pygame.K_RIGHT in key_pressed:
	   test.walkdir = 3
	   p_state = 1

	elif pygame.K_DOWN in key_pressed:
	   test.walkdir = 5
	   p_state = 1

	elif pygame.K_LEFT in key_pressed:
	   test.walkdir = 7
	   p_state = 1

	elif pygame.K_ESCAPE in key_pressed:
		done = True

	area.cameraPos[0] = p_pos[0] - area.winWidth/2
	area.cameraPos[1] = p_pos[1] - area.winHeight/2

	# New requirements for alternate scrolling:
	if area.cameraPos[0] < 0:								  area.cameraPos[0] = 0
	if area.cameraPos[0] >= area.world[2] - area.winWidth - 1:   area.cameraPos[0] = area.world[2] - area.winWidth - 1
	if area.cameraPos[1] < 0:								  area.cameraPos[1] = 0
	if area.cameraPos[1] >= area.world[3] - area.winHeight - 1: area.cameraPos[1] = area.world[3] - area.winHeight - 1
	if area.cameraPos[0] < 0: area.cameraPos[0] = 0 ##
	if area.cameraPos[1] < 0: area.cameraPos[1] = 0 ## fixes small map problems temporarily


	dtime = clock.tick_busy_loop()

	window.fill((0, 0, 0))
	area.render(window)

	area.tileCheck(area.playerPos[1],area.playerPos[0])
	p_pos = area.collision(p_pos)

	#Create Enemies
	for i in area.enemyList:
		area.tileCheck(i.pos[1], i.pos[0])
		i.pos[0] = area.collision([i.pos[0], i.pos[1]], True)[0]
		i.pos[1] = area.collision([i.pos[0], i.pos[1]], True)[1]
		area.enemiesPos = [i.pos[0], i.pos[1]]
		i.basicMovement(dtime, 100/1000.0)
		i.blit(window, area.cameraPos)

    #call player class
	test.update(dtime, p_state, area.cameraPos)
	test.blit(window, area.cameraPos)
	p_state = 0

	#draw bullet\
	if active == True:
		for b in test.bullets:
			b.update(dtime)
			if b.remove == True:
				test.bullets.remove(b)
			b.render(window)

	area.playerPos	= p_pos
	pygame.display.flip()


pygame.quit()