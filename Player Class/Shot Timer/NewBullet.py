# Rock G Bolton + Cameron Schuette
#
#
#
#
# New Bullet
#
#-------------------------------------------------------------------------------
import math
import pygame

class bullet(object):
	def __init__(self, bulletX, bulletY, angle, damage):
		self.remove = False
		self.x = bulletX
		self.y = bulletY
		self.damage = damage
		self.vel = 1
		self.vx = self.vel * math.cos(-angle)
		self.vy = self.vel * math.sin(-angle)
		self.dir = angle
		self.distTraveled = 0.0

	def render(self, surface):
		pygame.draw.circle(surface, (210,210,0), (int(self.x), int(self.y)), 15)

	def update(self, dtime):
		self.x += self.vx * dtime
		self.y += self.vy * dtime
		self.distTraveled += math.sqrt((self.vx * dtime)**2 + (self.vy * dtime)**2)

		if self.distTraveled >= 300:
			self.remove = True

		else:
			self.remove = False
			'''for i in barriers:
				if self.x >= i.x and self.x <= i.x + i.width and self.y >= i.y and self.y <= i.y + i.length and self.z <= i.height:
					self.remove = True'''
