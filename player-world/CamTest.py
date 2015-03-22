"""Test Program for Player Class"""
import pygame
import time
"""Import"""
import math
import NewBullet
import CamCharacterClass
import world
import glob
import configparser
import random
import soundDB

area = world.Zone()
pygame.display.init()
pygame.font.init()
window = pygame.display.set_mode((area.winWidth, area.winHeight))

"""Variables"""
done = False
aiming = False
active = False
e_active = False
key_pressed = []
bulletArray = []
soundList = []
clock = pygame.time.Clock()
p_pos = [200,200]
p_vel = [0, 0]
p_vel_mag = 200 / 1000.0
e_vel_mag = 100 / 1000.0
damage = 10
p_state = 0
cameraspeed = 3
ctr = 0
Clock = pygame.time.Clock()

"""Create Player"""


"""Main Game Loop"""
while not done:
	test = CamCharacterClass.Cleric(p_pos, area.cameraPos, p_vel_mag, 1)
	area.CreateEnemy()
	dtime = Clock.tick_busy_loop()

	evtList = pygame.event.get()
	for evt in evtList:
		if evt.type == pygame.QUIT:
			done = True
		elif evt.type == pygame.KEYDOWN:
			key_pressed.append(evt.key)
		elif evt.type == pygame.KEYUP:
			key_pressed.remove(evt.key)
		elif evt.type == pygame.MOUSEBUTTONDOWN:
			pygame.mouse.get_pos()
			mx = evt.pos[0]
			my = evt.pos[1]
			angle = math.atan2(-(my - (p_pos[1] - area.cameraPos[1])), mx - (p_pos[0] - area.cameraPos[0]))
			b_test = NewBullet.bullet(p_pos[0] - area.cameraPos[0], p_pos[1] - area.cameraPos[1], angle, damage)
			test.bullets.append(b_test)
			soundList.append(soundDB.cleric_sounds["0"])
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

	if area.collision(p_pos) == 4:
		test.cur_health = test.cur_health - (test.max_health /100)
		if test.cur_health < 0:
			test.cur_health = 0
	elif area.collision(p_pos) == 3:
		test.vel_mag = .05
	else:
		p_pos = area.collision(p_pos)
		test.vel_mag = p_vel_mag


	#Create Enemies
	for i in area.enemyList:
		e_angle = math.atan2(-(p_pos[1] - i.pos[1]), p_pos[0] - i.pos[0])
		e_test = NewBullet.bullet(i.pos[0] - area.cameraPos[0], i.pos[1] - area.cameraPos[1], e_angle, damage)
		i.bullets.append(e_test)
		e_active = True
		#soundList.append(soundDB.hub_sounds["cow"])
		area.tileCheck(i.pos[1], i.pos[0])
		i.pos[0] = area.collision([i.pos[0], i.pos[1]], True)[0]
		i.pos[1] = area.collision([i.pos[0], i.pos[1]], True)[1]
		area.enemiesPos = [i.pos[0], i.pos[1]]
		i.basicMovement(dtime, 100/1000.0, p_pos[0], p_pos[1], area.cameraPos)
		i.blit(window, dtime)
		if e_active == True:
			for b in i.bullets:
				b.update(dtime)
				if b.remove == True:
					i.bullets.remove(b)
				b.render(window)
        #enemy hit detection
		if i.cur_health <= 0:
			area.enemyList.remove(i)

	#call player class
	test.update(dtime, p_state, area.cameraPos)
	test.blit(window, dtime)
    #player hit detection
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
	for i in soundList:
		i.play()
		soundList.remove(i)


pygame.quit()