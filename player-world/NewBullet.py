"""Bullet Class"""
import math
import pygame

class bullet(object):
	def __init__(self, bulletX, bulletY, angle, damage):
		self.remove = False
		self.x = bulletX
		self.y = bulletY
		self.damage = damage
		self.vel = 600/1000
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

		if self.distTraveled >= 150:
			self.remove = True

