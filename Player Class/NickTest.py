#Test Program player class
import pygame
import time
import math
import math3d
import NewBullet
import BaseCharacterClass
#import soundDB

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
courierFont = pygame.font.SysFont("Courier New", 20)

window = pygame.display.set_mode((800, 600))
done = False
key_pressed = []

bulletArray = []
clock = pygame.time.Clock()
p_pos = [100, 100]
e_pos = [400, 300]
e2_pos = [200, 200]
e_spawn = e_pos
e_limit = [50, 50]
p_vel_mag = 200.0
e_vel_mag = 50.0
initial_pos = [p_pos[0],p_pos[1]]
damage = 10
speed = [0, 0]
speed_mag = 500.0
distance = 275
e = BaseCharacterClass.Wolf(e_pos, e_vel_mag, 1)
e2 = BaseCharacterClass.Cow(e2_pos, e_vel_mag, 1)
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
			soundDB.mage_sounds["0"].play()

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

	if pygame.K_a in key_pressed:
		test.addtext(5)

	if pygame.K_s in key_pressed:
		e.p_state = 2

	if pygame.K_d in key_pressed:
		e2.p_state = 2

##	if pygame.K_1 in key_pressed:
##		soundDB.mage_sounds["1"].play()
##
##	if pygame.K_2 in key_pressed:
##		soundDB.mage_sounds["2"].play()
##
##	if pygame.K_3 in key_pressed:
##		soundDB.mage_sounds["3"].play()
##
##	if pygame.K_4 in key_pressed:
##		soundDB.mage_sounds["4"].play()
##
##	if pygame.K_5 in key_pressed:
##		soundDB.mage_sounds["5"].play()
##

	#print(e.walkdir, e.dir, e.pos)

	if test.dead:
		p_state = 2

	if e.pos[0] <= 0:
		e.pos[0] = 0
	if e.pos[0] >= 800:
		e.pos[0] = 800
	if e.pos[1] <= 0:
		e.pos[1] = 0
	if e.pos[1] >= 600:
		e.pos[1] = 600

	if e2.pos[0] <= 0:
		e2.pos[0] = 0
	if e2.pos[0] >= 800:
		e2.pos[0] = 800
	if e2.pos[1] <= 0:
		e2.pos[1] = 0
	if e2.pos[1] >= 600:
		e2.pos[1] = 600


	#call player class
	window.fill((0,0,0))
	e.basicMovement(dtime, e_vel_mag, e_limit)
	e.blit(window)
	e2.basicMovement(dtime, e_vel_mag, e_limit)
	e2.blit(window)
	test.update(dtime, p_state, p_vel_mag)
	test.move()
	test.blit(window)
	test.updatetext(dtime)
	test.rendertext(courierFont, window)
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