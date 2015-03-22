# Cameron Schuette + Rock G Bolton
""" Basic Character Class for players and enemies """
import math
import random
import pygame
import NewBullet
import math3d
import world

area = world.Zone()
pygame.font.init()

class BaseCharClass(object):
	def __init__(self, pos, cameraPos, vel_mag, exp = 0):
		""" Position and movement """
		self.pos = pos
		self.vel_mag = vel_mag
		self.walkdir = 1  # 8 Cardinal Directions, starting
						  # at 1 for North and going clockwise
		self.dir = 0	  # Direction in radians
		self.p_state = 0
		self.bullets = []
		self.courierFont = pygame.font.SysFont("Courier New", 20)

		""" Attributes """
		self.exp = exp
		self.level = self.exp // 100
		if self.level < 1:
			self.level = 1
		if self.level > 50:
			self.level = 50
		self.cur_health = 100
		self.max_health = 100
		self.p_frames_per_state = 8
		self.p_frames = []
		for i in range(9):
			self.p_frames.append([])
		self.p_cur_frame = 0
		self.P_DELAY_FRAME = 80
		self.p_cur_delay = self.P_DELAY_FRAME
		self.frames_per_state = 8
		self.damage_list = []
		self.textcolor = (255, 0, 0)
		self.tmpwidth = self.p_frames[self.walkdir][self.p_cur_frame].get_width()
		self.tmpheight = self.p_frames[self.walkdir][self.p_cur_frame].get_height()
		self.temppos = [(self.pos[0] - self.tmpwidth // 2) - cameraPos[0], (self.pos[1] - self.tmpheight // 2) - cameraPos[1]]

	def loadFrames(self, character, s_type, anim_type):   # s_type can either be "Class" or "Monster"
		""" Loads all frames from sprite sheet for given character for 96 x 96 frames """
		tmpstr = character + anim_type
		self.walkSurf = pygame.image.load(tmpstr + ".png").convert()
		self.p_frames = []
		for i in range(9):
			self.p_frames.append([])
		for j in range(0, 8):
			# j is the frame number
			for i in range(1, 9):
				# i represents self.walkdir
				if i == 1:	 # North
					y = 6 * 96
				elif i == 2:   # NE
					y = 5 * 96
				elif i == 3:	# E
					y = 7 * 96
				elif i == 4:	# SE
					y = 2 * 96
				elif i == 5:	# S
					y = 3 * 96
				elif i == 6:	# SW
					y = 1 * 96
				elif i == 7:	# W
					y = 0 * 96
				elif i == 8:	# NW
					y = 4 * 96
				self.walkSurf.set_colorkey(self.colorKey)
				rect = (j * 96, y, 96, 96)
				tempS = pygame.Surface((96,96)).convert_alpha()
				tempS.fill((0, 0, 0, 0))
				tempS.blit(self.walkSurf, (0,0), rect)
				self.p_frames[i].append(tempS)

		del tmpstr

	def move(self):
		""" Creates a directional vector for character movement """
		# Takes the direction and converts it to an angle in radians
		# 8 Cardinal Directions, starting at 1 for North and going clockwise
		if self.walkdir == 1:
			self.dir = math.pi / 2
		if self.walkdir == 2:
			self.dir = math.pi / 4
		if self.walkdir == 3:
			self.dir = 0
		if self.walkdir == 4:
			self.dir = 7 * math.pi / 4
		if self.walkdir == 5:
			self.dir = 3 * math.pi / 2
		if self.walkdir == 6:
			self.dir = 5 * math.pi / 4
		if self.walkdir == 7:
			self.dir = math.pi
		if self.walkdir == 8:
			self.dir = 3 * math.pi / 4
		self.dir = -self.dir


	def update(self, dtime, p_state, cameraPos):
		""" Updates frames of animation for players and enemies """
		self.p_state = p_state
		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME

		elif self.p_state == 1:
			self.p_cur_delay -= dtime
			while self.p_cur_delay < self.P_DELAY_FRAME:
				self.p_cur_delay += self.P_DELAY_FRAME
				self.p_cur_frame += 1
				if self.p_cur_frame == 8:
					self.p_cur_frame = 0

			norm_move_vector = math3d.Vector2FromPolar(math.degrees(self.dir))
			self.vel = self.vel_mag * dtime
			norm_move_vector *= self.vel

			self.pos[0] += norm_move_vector[0]
			self.pos[1] += norm_move_vector[1]

		self.move()

	def getWidth(self):
		""" gets width of sprite """
		h = self.p_frames[self.walkdir][self.p_cur_frame].get_width()
		return h

	def getHeight(self):
		""" get height of sprite """
		w = self.p_frames[self.walkdir][self.p_cur_frame].get_height()
		return w

	def blit(self, window, dtime):
		self.window = window
		self.window.blit(self.p_frames[self.walkdir][self.p_cur_frame], self.temppos)
		"""makes and renders and health bar above the player"""
		width = 50
		height = 10
		border_color = (255, 255, 255)
		border_width = 1
		x = self.temppos[0] +25
		y = self.temppos[1]

		rect = (x, y, width, height)

		pygame.draw.rect(self.window, border_color, rect, border_width)

		if self.cur_health:
			x = rect[0] + border_width
			y = rect[1] + border_width
			width = (rect[2] - border_width * 2)
			width *= (self.cur_health / self.max_health)
			height = rect[3] - border_width * 2

			rect = (x, y, width, height)
			pygame.draw.rect(self.window, (255, 0, 0), rect)

		self.updatetext(dtime)
		self.rendertext(self.courierFont, self.window)

	def playerHit(enemyList):
		for i in self.bullets:
			for k in enemyList:
				dist = (i.pos[0] - k.pos[0]) ** 2 + (i.pos[1] - k.pos[1]) **2
				dist **= .5
				if dist < 30:
					k.cur_health -= i.damage
				else:
					pass

	def addtext(self, damage):
		""" When character takes damage, pass damage value to this method """
		self.hwidth = self.getWidth() / 2
		textoffset = 0
		if len(self.damage_list) > 10:	# Sets a limit on quantity of damage values
			del self.damage_list[10]
		self.damage_list.append([str(damage), self.textcolor, textoffset]) # fdamage[0] is value, fdamage[1] is textcolor, fdamage[2] is textoffset

	def updatetext(self, dtime):
		""" controls the movement and fadout of text """
		for font_damage in self.damage_list:
			# float upwards
			font_damage[2] += 65 * dtime
			#color fade
			#if font_damage[2] != 0:
			#	red = 255 // font_damage[2]
				#font_damage[1] = (red, 0, 0)
			if font_damage[2] >= 50:
				del self.damage_list[0]

	def rendertext(self, font, window):
		""" Blits floating text """
		for font_damage in self.damage_list:
			pos = self.pos[:]
			pos[0] += self.hwidth
			pos[1] -= font_damage[2]
			tempS = font.render(font_damage[0], False, font_damage[1])
			window.blit(tempS, pos)

class playerClass(BaseCharClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, self.dir, exp)
		self.fired = False

	def aimAngle(self):
		""" Calculates the angle of aim from character to mouse (radians) """
		mx, my = pygame.mouse.get_pos()
		x = mx - (self.pos[0] + self.getWidth() / 2)
		y = my - (self.pos[1] + self.getHeight() / 2)
		angle = math.atan2(-y, x)
		return angle

	def fire(self):
		""" Controls firing """
		if fired:
			bulX = self.p_pos[0]
			bulY = self.p_pos[1]

			normalize(vect)
			print(vect)

			self.fired = False

""" Classes for player characters """
class Mage(playerClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.attack = 12
		self.defense = 3
		self.speed = 7
		self.Range = 8
		self.gcd = 1100
		self.health = self.defense * 20
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (105,74,46)
		self.p_class = "Mage"
		self.loadFrames(self.p_class, "Class", "Other")

class Warrior(playerClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.attack = 9
		self.defense = 12
		self.speed = 5
		self.Range = 4
		self.gcd = 800
		self.health = self.defense * 10
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (106,76,48)
		self.p_class = "Warrior"
		self.loadFrames(self.p_class, "Class", "Other")

class Cleric(playerClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.attack = 3
		self.defense = 8
		self.speed = 7
		self.Range = 12
		self.gcd = 1700
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.health = self.defense * 10
		self.colorKey = (106,73,48)
		self.p_class = "Cleric"
		self.loadFrames(self.p_class, "Class", "Other")

class Thief(playerClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.attack = 7
		self.defense = 8
		self.speed = 12
		self.Range = 3
		self.gcd = 500
		self.health = self.defense * 10
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (106,76,48)
		self.p_class = "Thief"
		self.loadFrames(self.p_class, "Class", "Other")

"""Enemy Class"""
class enemyClass(BaseCharClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.dirtimer = 0
		#self.dirtimer = random.randint(1500, 2500) # enemy walks for x ms
		#self.dirtimer /= 1000.0	 # converts timer to sec
		self.dir = 1
		self.expGain = self.level * 5
		self.spawn = pos
		self.allowedToFire = True
		self.ROF = 1000
		self.shotTimer = 0

	def basicMovement(self, dtime, vel_mag, playerX, playerY, cameraPos):
		""" Basic enemy "wandering": walks around and stops randomly """
		self.p_state = 1
		# Timer manager for time spent walking in direction / stopping
		if self.dirtimer > 0:
			self.dirtimer -= dtime
		if self.dirtimer <= 0:
			# Changes direction and timer to different values
			# If walkdir generates same number twice in a row, reroll
			tmpcheck = self.walkdir
			self.walkdir = random.randint(1, 8)
			if tmpcheck == self.walkdir:
				self.walkdir = random.randint(1, 8)
				if self.walkdir <= 8:
					self.p_state = 1
			# Resets timer for walk direction
			self.dirtimer = random.randint(1500, 2500) # enemy walks for x ms
			#self.dirtimer /= 1000.0

		# if random direction # exceeds 8, enemy stops for durtimer sec
		if self.walkdir > 8:
			self.vel = 0
			self.p_state = 0

		# Moves the enemy
		self.move()
		self.update(dtime, self.p_state, cameraPos)
		#self.shoot(dtime, cameraPos, playerX, playerY)

		#if movelimit:
		#	self.setMovementRange(movelimit[0], movelimit[1])

	def setMovementRange(self, xdist, ydist):
		""" Creates a limit on how far enemy can move from spawn point """
		if self.pos[0] < self.spawn[0] - xdist:
			self.pos[0] = self.spawn[0] - xdist
		if self.pos[0] > self.spawn[0] + xdist:
			self.pos[0] = self.spawn[0] + xdist
		if self.pos[1] < self.spawn[1] - ydist:
			self.pos[1] = self.spawn[1] - ydist
		if self.pos[1] > self.spawn[1] + ydist:
			self.pos[1] = self.spawn[1] + ydist

	def enemyHit(playerList):
		for i in self.bullets:
			for k in playerList:
				dist = (i.pos[0] - k.pos[0]) ** 2 + (i.pos[1] - k.pos[1]) **2
				dist **= .5
				if dist < 30:
					k.cur_health -= i.damage
				else:
					pass

"""Enemies"""
class Wolf(Thief, enemyClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		Thief.__init__(self, pos, cameraPos, vel_mag, exp)
		enemyClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.pos = pos
		self.vel_mag = vel_mag
		self.exp = exp
		self.colorKey = (111,79,51)
		self.p_class = "wolf"
		self.loadFrames(self.p_class, "Monster", "Move")

class Cow(Warrior, enemyClass):
	def __init__(self, pos, cameraPos, vel_mag, exp):
		Warrior.__init__(self, pos, cameraPos, vel_mag, exp)
		enemyClass.__init__(self, pos, cameraPos, vel_mag, exp)
		self.pos = pos
		self.vel_mag = vel_mag
		self.exp = exp
		self.colorKey = (111,79,51)
		self.p_class = "cow"
		self.loadFrames(self.p_class, "Monster", "Walk")
