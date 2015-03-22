import pygame
import random
import math
import math3d
class Player(object):
	fontObj = None

	def __init__(self, uname, cType):
		self.uname = uname
		self.horizMovement = "None"
		self.vertMovement = "None"
		self.walkdir = 1		# 8 Cardinal Directions, starting
						 # at 1 for North and going clockwise
		pos = [768, 640]
		self.posX = pos[0]
		self.posY = pos[1]
		self.p_vel = [0, 0]
		self.exp = 0
		self.dir = 0
		self.p_state = 0
		self.bullets = []
		self.level= int(self.exp)//100

		if self.level<1:
			self.level = 1
		if self.level>50:
			self.level = 50

		self.death_frames = []
		self.cur_health = 100
		self.max_health = 100
		self.p_frames = []
		self.p_cur_frame = 0
		self.P_DELAY_FRAME = .2
		self.p_cur_delay = self.P_DELAY_FRAME
		self.frames_per_state = 8
		self.damage_list = []


		self.Pclass = cType
		self.Pname = uname
		if self.Pclass == "Mage":
			self.attack = 12
			self.defense = 3
			self.speed = 100
			self.Range = 8
			self.health = self.defense * 20
			self.bulletSpeed = (self.Range / self.speed) * 1000
			self.colorKey = (105,74,46)
			self.size = 96
			self.loadFrames(self.Pclass, "Class", "Other", self.size)

		elif self.Pclass == "Warrior":
			self.attack = 9
			self.defense = 12
			self.speed = 80
			self.Range = 4
			self.health = self.defense * 10
			self.bulletSpeed = (self.Range / self.speed) * 1000
			self.colorKey = (106,76,48)
			self.size = 96
			self.loadFrames(self.Pclass, "Class", "Other", self.size)
		elif self.Pclass == "Cleric":
			self.attack = 3
			self.defense = 8
			self.speed = 100
			self.Range = 12
			self.bulletSpeed = (self.Range / self.speed) * 1000
			self.health = self.defense * 10
			self.colorKey = (106,73,48)
			self.size = 96
			self.loadFrames(self.Pclass, "Class", "Other", self.size)
		elif self.Pclass == "Thief":
			self.attack = 7
			self.defense = 8
			self.speed = 150
			self.Range = 3
			self.health = self.defense * 10
			self.bulletSpeed = (self.Range / self.speed) * 1000
			self.colorKey = (106,76,48)
			self.size = 96
			self.loadFrames(self.Pclass, "Class", "Other", self.size)
##		self.color = [random.randint(100,255), random.randint(100,255), random.randint(100,255)]

		# Shadow values.  Used to detect if we need to transmit data to a client/server
		self.olddir = None
		self.oldposX = None
		self.oldposY = None
		self.oldp_state = None


		# Create the font
		if Player.fontObj == None and pygame.font.get_init():
			Player.fontObj = pygame.font.SysFont("Courier New", 12)



	def __str__(self):
		return "[Player." + self.uname + ".(" + str(self.posX) + "," + \
						   str(self.posY) + ").(" + str(self.dir) + ")"

	def render(self, window, cameraPos):
		self.window = window
		self.tmpwidth = self.p_frames[self.walkdir][self.p_cur_frame].get_width()
		self.tmpheight = self.p_frames[self.walkdir][self.p_cur_frame].get_height()
		self.temppos = [(self.posX - self.tmpwidth // 2) - cameraPos[0], (self.posY - self.tmpheight // 2) - cameraPos[1]]
		self.window.blit(self.p_frames[self.walkdir][self.p_cur_frame], self.temppos)
		"""makes and renders and health bar above the Player"""
		width = 50
		height = 10
		border_color = (255, 255, 255)
		border_width = 1
		x = self.temppos[0] + 25
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


	def setMove(self, horiz=None, vert=None):
		if horiz:
			self.horizMovement = horiz
		if vert:
			self.vertMovement = vert
	# CHANGES OCCURE HERE !!!!!#!@#^!@#
	def update(self, dT):
		if self.p_state == 1:
			self.p_mag = 250

			if self.horizMovement == "Left":
				self.p_vel[0] = -1
			elif self.horizMovement == "Right":
				self.p_vel[0] = 1
			if self.vertMovement == "Up":
				self.p_vel[1] = -1
			elif self.vertMovement == "Down":
				self.p_vel[1] = 1

			templen = (self.p_vel[0] ** 2 + self.p_vel[1] ** 2) ** .5

			if templen:
				self.p_state = 1
				self.p_vel[0] /= templen
				self.p_vel[1] /= templen
				self.p_vel[0] *= self.p_mag
				self.p_vel[1] *= self.p_mag

			else: self.p_state = 0

			self.posX += self.p_vel[0] * dT
			self.posY += self.p_vel[1] * dT

		# If Diagonals are Messed Up Delete Me!!
##		if self.vertMovement == "Up" and self.horizMovement == "Right":
##			self.posX += self.p_mag * dT
##			self.posY -= self.p_mag * dT
##		elif self.vertMovement == "Up" and self.horizMovement == "Left":
##			self.posX -= self.p_mag * dT
##			self.posY -= self.p_mag * dT
##		if self.vertMovement == "Down" and self.horizMovement == "Right":
##			self.posX += self.p_mag * dT
##			self.posY += self.p_mag * dT
##		elif self.vertMovement == "Down" and self.horizMovement == "Left":
##			self.posX -= self.p_mag * dT
##			self.posY += self.p_mag * dT


		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME
			self.p_vel[0]= 0
			self.p_vel[1] = 0

		elif self.p_state == 1:
			self.p_cur_delay -= dT
			while self.p_cur_delay < self.P_DELAY_FRAME:
				self.p_cur_delay += self.P_DELAY_FRAME
				self.p_cur_frame += 1
				if self.p_cur_frame == 8:
					self.p_cur_frame = 0


	def serialize(self, level, updateOldValues=True):
		""" If level==0, only serialize those things that need to be sent from client to server (or vice-versa) during normal updates
			If level==1, only serialize those things that have changed.
			If level==2, serialize everything.
			If level==3, serialize those things that need to go in the account database (on the server)
			In either case, if updateOldValues is true, update the "shadow" copies of attributes. """
		if level not in [0, 1, 2, 3]:
			raise ValueError("Level must be 0-3")

		s = ""

		if level == 0:
			if self.olddir == None or self.dir != self.olddir:   s += ":direction=" + str(self.dir)
			if self.oldp_state == None or self.p_state != self.oldp_state:					   s += ":PState=" + str(self.p_state)
			s += ":Pname=" + str(self.Pname)
			s += ":Pclass=" + str(self.Pclass)
			if len(s) > 0:
				s = s[1:]

		if level == 2:
			print(self.exp)
			s = "uname=" + self.uname + ":x=" + str(int(self.posX)) + ":y=" + str(int(self.posY)) + ":PState=" + str(self.p_state)
			s += ":direction=" + str(self.dir) + ":Pname=" + str(self.Pname) + ":Pclass=" + str(self.Pclass)


		if level == 3:
			s = "uname=" + self.uname + ":x=" + str(int(self.posX)) + ":y=" + str(int(self.posY))
			s += ":Pname=" + str(self.Pname) + ":Pclass=" + str(self.Pclass)


		if updateOldValues:
			self.olddir = self.dir
			self.oldUname = self.uname
			self.oldposX = self.posX
			self.oldposY = self.posY
			self.oldp_state = self.p_state

		return s

	def deserialize(self, s):
		#print("De-serializing '" + s + "'")
		#if s.count(":") == 0:
		#   return	# Nothing to de-serialize!
		elem = s.split(":")
		print(elem)
		for e in elem:
			if not e.find("=") or e == "":
				continue
			print(e)
			key, value = e.split("=")
			if key == "PState":
				self.p_state = int(value)
			elif key == "x":
				self.posX = float(value)
			elif key == "y":
				self.posY = float(value)
			elif key == "Pname":
				self.Pname = value
			elif key == "Pclass":
				self.Pclass= value
			elif key == "uname":
				pass
			elif key == "direction":
				self.dir = value
##			elif key == "c0":
##				self.color[0] = int(value)
##			elif key == "c1":
##				self.color[1] = int(value)
##			elif key == "c2":
##				self.color[2] = int(value)
			else:
				raise ValueError("Undefined deserialize key ('" + key + "')")

	def loadFrames(self, character, c_type, anim_type, size):   # c_type can either be "Class" or "Monster"
		""" Loads all frames from sprite sheet for given character for size x size frames """
		tmpstr = "../Artwork/" + c_type + " Sprites/" + character + anim_type
		self.walkSurf = pygame.image.load(tmpstr + ".png").convert()
		self.p_frames = []
		self.size = size
		self.character = character
		self.walkspritesheetsize = self.walkSurf.get_width() // self.size
		for i in range(0, self.walkspritesheetsize + 1):
			self.p_frames.append([])
		for j in range(0, self.walkspritesheetsize):
			# Walking animation load`
			# j is the frame number
			for i in range(1, 9):
				# i represents self.walkdir
				if i == 1:	 # North
					y = 6 * self.size
				elif i == 2:   # NE
					y = 5 * self.size
				elif i == 3:	# E
					y = 7 * self.size
				elif i == 4:	# SE
					y = 2 * self.size
				elif i == 5:	# S
					y = 3 * self.size
				elif i == 6:	# SW
					y = 1 * self.size
				elif i == 7:	# W
					y = 0 * self.size
				elif i == 8:	# NW
					y = 4 * self.size
				self.walkSurf.set_colorkey(self.colorKey)
				rect = (j * self.size, y, self.size, self.size)
				tempS = pygame.Surface((size, size)).convert_alpha()
				tempS.fill((0, 0, 0, 0))
				tempS.blit(self.walkSurf, (0,0), rect)
				self.p_frames[i].append(tempS)

		# Death animation load
		for i in range(0, self.walkspritesheetsize + 1):
			 if character == "cow":   # exception for cow sprites
				 return
			 self.death_frames.append([])
		tmpstr = "../Artwork/" + c_type + " Sprites/" + character + "Death"
		self.walkSurf = pygame.image.load(tmpstr + ".png").convert()
		self.deathspritesheetsize = self.walkSurf.get_width() // self.size
		for j in range(self.deathspritesheetsize-1,-1,-1):
			# j is the frame number
			for i in range(1, 9):
				# i represents self.walkdir
				if i == 1:	 # North
					y = 6 * self.size
				elif i == 2:   # NE
					y = 5 * self.size
				elif i == 3:	# E
					y = 7 * self.size
				elif i == 4:	# SE
					y = 2 * self.size
				elif i == 5:	# S
					y = 3 * self.size
				elif i == 6:	# SW
					y = 1 * self.size
				elif i == 7:	# W
					y = 0 * self.size
				elif i == 8:	# NW
					y = 4 * self.size
				self.walkSurf.set_colorkey(self.colorKey)
				rect = (j * self.size, y, self.size, self.size)
				tempS = pygame.Surface((size, size)).convert_alpha()
				tempS.fill((0, 0, 0, 0))
				tempS.blit(self.walkSurf, (0,0), rect)
				self.death_frames[i].append(tempS)

		del tmpstr





class PlayerClass(Player):
	def __init__(self, pos, vel_mag, exp):
		Player.__init__(self, pos, vel_mag, self.dir, exp)
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
class Mage(PlayerClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, exp)
		self.attack = 12
		self.defense = 3
		self.speed = 7
		self.Range = 8
		self.health = self.defense * 20
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (105,74,46)
		self.size = 96
		self.p_class = "Mage"
		self.loadFrames(self.p_class, "Class", "Other", self.size)

class Warrior(PlayerClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, exp)
		self.attack = 9
		self.defense = 12
		self.speed = 5
		self.Range = 4
		self.health = self.defense * 10
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (106,76,48)
		self.size = 96
		self.p_class = "Warrior"
		self.loadFrames(self.p_class, "Class", "Other", self.size)

class Cleric(PlayerClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, exp)
		self.attack = 3
		self.defense = 8
		self.speed = 7
		self.Range = 12
		self.bulletSpeed = (self.Range / speed) * 1000
		self.health = self.defense * 10
		self.colorKey = (105,74,46)
		self.size = 96
		self.p_class = "Cleric"
		self.loadFrames(self.p_class, "Class", "Other", self.size)

class Thief(PlayerClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, exp)
		self.attack = 7
		self.defense = 8
		self.speed = 12
		self.Range = 3
		self.health = self.defense * 10
		self.bulletSpeed = (self.Range / self.speed) * 1000
		self.colorKey = (106,76,48)
		self.size = 96
		self.p_class = "Thief"
		self.loadFrames(self.p_class, "Class", "Other", self.size)



"""Enemy Class"""
class enemyClass(Player):
	def __init__(self, pos, vel_mag, exp):
		Player.__init__(self, pos, vel_mag, exp)
		self.dirtimer = 9000
		#self.dirtimer = random.randint(1500, 2500) # enemy walks for x ms
		#self.dirtimer /= 1000.0	 # converts timer to sec
		self.dir = 1
		self.expGain = self.level * 5
		self.spawn = pos

	def basicMovement(self, dtime, vel_mag):
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
		self.update(dtime, self.p_state, self.vel_mag)

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

"""Enemies"""
class Wolf(Thief, enemyClass):
	def __init__(self, pos, vel_mag, exp):
		Thief.__init__(self, pos, vel_mag, exp)
		enemyClass.__init__(self, pos, vel_mag, exp)
		self.pos = pos
		self.vel_mag = vel_mag
		self.exp = exp
		self.colorKey = (111,79,51)
		self.p_class = "wolf"
		self.loadFrames(self.p_class, "Monster", "Move")

class Cow(Warrior, enemyClass):
	def __init__(self, pos, vel_mag, exp):
		Warrior.__init__(self, pos, vel_mag, exp)
		enemyClass.__init__(self, pos, vel_mag, exp)
		self.pos = pos
		self.vel_mag = vel_mag
		self.exp = exp
		self.colorKey = (111,79,51)
		self.p_class = "cow"
		self.loadFrames(self.p_class, "Monster", "Walk")
