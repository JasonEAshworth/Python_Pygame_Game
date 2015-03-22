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

pygame.init()
pygame.display.init()
pygame.font.init()
window = pygame.display.set_mode((area.winWidth, area.winHeight))

#variables
done = False
aiming = False
active = False
timeCheck = False
canShoot = False
key_pressed = []
bulletArray = []
clock = pygame.time.Clock()
p_pos = [area.winWidth/2, area.winHeight/2 + 100]
e_pos = [area.winWidth/2, area.winHeight/2 + 100]
p_vel = [0, 0]
p_vel_mag = 200 / 1000.0
damage = 10
bul_pos = [p_pos[0],p_pos[1]]
p_offset = 0
p_state = 0
cameraspeed = 3
timetest = 0
timer = 0

#create classes
test = CamCharacterClass.Cleric(p_pos, p_vel, p_vel_mag)
enemy = CamCharacterClass.enemyClass(e_pos,100)
enemy2 = CamCharacterClass.enemyClass((600,400), 100)

while not done:


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
			if timeCheck == True:
				test.bullets.append(b_test)
				active = True


	for key in key_pressed:
		if key == pygame.K_LEFT:
			test.vel[0] = -1
			p_offset = 3
			p_state = 1




		elif key == pygame.K_RIGHT:
			test.vel[0] = 1
			p_offset = 1
			p_state = 1



		elif key == pygame.K_UP:
			test.vel[1] = -1
			p_offset = 0
			p_state = 1



		elif key == pygame.K_DOWN:
			test.vel[1] = 1
			p_offset = 2
			p_state = 1




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
	minustime = dtime + 1
	actualtime = minustime - dtime

	if timeCheck == False:
	   timer += actualtime
	   print(timeCheck)

	print(dtime, minustime, actualtime, timer)

	if timer > 10:
		timeCheck = True
		print(timeCheck)
		#print(timer)


	if timetest <3:
	   timetest = time.clock()
	   #print (timetest)
	if timetest > 3:
		timetest = 0
		#timetest = time.clock() - time.clock()
		#print(timetest)


	#print (timeCheck)


	#area.playerPos = p_pos

	#update Variables



	window.fill((0, 0, 0))
	area.render(window)


	area.tileCheck(area.playerPos[1],area.playerPos[0])
	p_pos = area.collision(p_pos)
	area.tileCheck(enemy.y,enemy.x)
	enemy.x = area.collision([enemy.x, enemy.y], True)[0]
	enemy.y= area.collision([enemy.x, enemy.y], True)[1]
	area.enemiesPos = [enemy.x, enemy.y]

	area.tileCheck(enemy2.y,enemy2.x)
	enemy2.x = area.collision([enemy2.x, enemy2.y], True)[0]
	enemy2.y= area.collision([enemy2.x, enemy2.y], True)[1]

	#enemy #1
	enemy.move(p_pos[0], p_pos[1], dtime, area.cameraPos)
	enemy.draw(window, dtime, None, area.cameraPos)
	enemy.checkIfHit(area.cameraPos, test.bullets)
	enemy.playerHitCheck(area.cameraPos, test)
	#enemy #2
	enemy2.move(p_pos[0], p_pos[1], dtime, area.cameraPos)
	enemy2.draw(window, dtime, None, area.cameraPos)
	enemy2.checkIfHit(area.cameraPos,test.bullets)
	enemy2.playerHitCheck(area.cameraPos, test)
	#call player class
	test.update(dtime, p_offset, p_state, area.cameraPos)
	test.blit(window, area.cameraPos)
	p_state = 0

	#draw bullet\
	if active == True and timeCheck == True:
		canShoot = True
		active = False
		timeCheck = False
		timer = 0

	if canShoot == True:
		for b in test.bullets:
			b.update(dtime)
			if b.remove == True:
				test.bullets.remove(b)
			b.render(window)
		#canShoot = False
#            if xtime > cdtime:
#                bTime = True

	#print(area.playerPos)
	area.playerPos	= p_pos
	pygame.display.flip()
	#print(active)
	#print(dtime)


pygame.quit()