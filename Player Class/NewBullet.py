#
#
#
#
#
# New Bullet
#
#-------------------------------------------------------------------------------
import math
import pygame

class Bullet(object):

	def __init__(self, x, y, damage, angle, speed_mag, distance):
		self.x = x
		self.y = y
		self.damage = damage
		self.maxDistance = distance	  # Max distance
		self.speed = (speed_mag * math.cos(angle), -speed_mag*math.sin(angle))
		self.active = True
		self.speed_mag = speed_mag
		self.distance = 0.0

	def update(self, dtime):
##		self.mx = mx
##		self.my = my
##
##		self.speed[0] = self.mxv - self.p_pos[0]
##		self.speed[1] = self.myv - self.p_pos[1]
##
##		mag = (self.speedx ** 2 + self.speedy ** 2) ** 0.5
##		if mag == 0:
##			self.speedx = 0
##			self.speedy = 0
##		else:
##			self.speedx /= mag
##			self.speedy /= mag

##		self.speedx *= self.speed_mag
##		self.speedy *= self.speed_mag
		self.distance += self.speed_mag * dtime
		self.x += self.speed[0] * dtime
		self.y += self.speed[1] * dtime
		if self.distance > self.maxDistance:
			self.active = False


	def render(self, window):
		pygame.draw.circle(window, (10, 100, 200), (int(self.x), int(self.y)), 10)









