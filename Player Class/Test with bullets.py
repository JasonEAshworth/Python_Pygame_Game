#Test Program player class
import pygame
import time
import math
import math3d
import NewBullet
import BaseCharacterClass

pygame.display.init()
window = pygame.display.set_mode((800, 600))
done = False
key_pressed = []

bulletArray = []
clock = pygame.time.Clock()
p_pos = [100, 100]
e_pos = [400, 300]
e_spawn = e_pos
e_limit = [50, 50]
p_vel_mag = 200.0
e_vel_mag = 50.0
initial_pos = [p_pos[0],p_pos[1]]
damage = 10
speed = [0, 0]
speed_mag = 500.0
distance = 275
e = BaseCharacterClass.enemyClass(e_pos, e_vel_mag, 1)

p_state = 0
test = BaseCharacterClass.Mage(p_pos, p_vel_mag, 1)
h = test.getHeight()
w = test.getWidth()
halfh = test.getHeight() / 2
halfw = test.getWidth() / 2
bul_pos = [p_pos[0] + halfw, p_pos[1] + halfh]
active = False

while not done:
	dtime = clock.tick() / 1000.0
	evtList = pygame.event.get()
	for evt in evtList:
		if evt.type == pygame.QUIT:
			done = True
		elif evt.type == pygame.KEYDOWN:
			key_pressed.append(evt.key)
		elif evt.type == pygame.KEYUP:
			key_pressed.remove(evt.key)
		elif evt.type == pygame.MOUSEBUTTONDOWN:
			a = test.aimAngle()
			b_test = NewBullet.Bullet(p_pos[0] + halfw, p_pos[1] + halfh, damage, a, speed_mag, distance)
			bulletArray.append(b_test)
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

	e.vel = e.vel_mag * dtime

	#t = BaseCharacterClass.FloatingText(p_pos, test)
	#t.setDamageValue(5)
	#t.render(dtime)

	#print(e.walkdir, e.dir, e.pos)

	if e.pos[0] <= 0:
		e.pos[0] = 0
	if e.pos[0] >= 800:
		e.pos[0] = 800
	if e.pos[1] <= 0:
		e.pos[1] = 0
	if e.pos[1] >= 600:
		e.pos[1] = 600

	pygame.draw.circle(window, (255, 0, 0), (int(e.pos[0]), int(e.pos[1])), 25)

	#call player class
	window.fill((0, 0, 0))
	test.update(dtime, p_state, p_vel_mag)
	test.move()
	test.blit(window)
	e.basicMovement(dtime, p_vel_mag, e_limit)
	pygame.draw.circle(window, (255, 0, 0), (int(e.pos[0]), int(e.pos[1])), 25)
	p_state = 0


	#draw bullet\
	if active == True:
		for b in bulletArray:
			b.update(dtime)

		for b in bulletArray:
			if b.active == True:
				b.render(window)

	#print(p_pos, bul_pos)


	pygame.display.flip()


#print("angle" + str(test.angle))
#test.assignStats("Fighter")
#print("Name " + test.name)
#print("class " + test.p_class)
#print("current health " + str(test.cur_health))
#print("max health " + str(test.max_health))
#print("attack " + str(test.atk))
#print("defense " + str(test.dfn))
#print("speed " + str(test.spd))
#print("range " + str(test.rng))

pygame.quit()