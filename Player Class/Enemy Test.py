import pygame
import math
import math3d
import BaseCharacterClass

pygame.init()

window = pygame.display.set_mode((1200, 800))
done = False
clock = pygame.time.Clock()
e = BaseCharacterClass.enemyClass([600, 400], 0, .1)

while not done:
	evtList = pygame.event.get()
	for evt in evtList:
		if evt.type == pygame.QUIT:
			done = True
	
	dtime = clock.tick()
	
	e.vel = e.vel_mag * dtime
	e.basicMovement(dtime)
	
	print(e.walkdir, e.dir, e.pos)
	
	m = math3d.Vector2FromPolar(math.degrees(-e.dir), e.vel)
	
	e.pos[0] += m[0]
	e.pos[1] += m[1]
	
	if e.pos[0] <= 0:
		e.pos[0] = 0
	if e.pos[0] >= 1200:
		e.pos[0] = 1200
	if e.pos[1] <= 0:
		e.pos[1] = 0
	if e.pos[1] >= 800:
		e.pos[1] = 800
	
	window.fill((0, 0, 0))
	
	pygame.draw.circle(window, (255, 0, 0), (int(e.pos[0]), int(e.pos[1])), 25)
	
	pygame.display.flip()

pygame.quit()