""" Basic Character Class for players and enemies """
import math
import math3d
import random
import pygame

class BaseCharClass(object):
	def __init__(self, pos, vel_mag, exp = 0, name = "Herp", p_class = "Derp"):
		""" Position and movement """
		self.pos = pos
		self.vel_mag = vel_mag
		self.walkdir = 1  # 8 Cardinal Directions, starting
						  # at 1 for North and going clockwise
		self.dir = 0	  # Direction in radians
		self.p_state = 0

		""" Attributes """
		self.exp = exp
		self.level = self.exp // 100
		if self.level < 1:
			self.level = 1
		if self.level > 50:
			self.level = 50
		self.cur_health = 100
		self.p_frames = []
		self.death_frames = []
		self.p_cur_frame = 0
		self.P_DELAY_FRAME = 80
		self.p_cur_delay = self.P_DELAY_FRAME
		self.damage_list = []
		self.textcolor = (255, 0, 0)
		self.dead = False

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
			# Walking animation load			
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

	def update(self, dtime, p_state, vel_mag):
		""" Updates frames of animation for players and enemies """
		self.p_state = p_state
		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME

		elif self.p_state == 1:
			self.p_cur_delay -= dtime * 1000
			if self.p_cur_delay < self.P_DELAY_FRAME:
				self.p_cur_delay += self.P_DELAY_FRAME
				self.p_cur_frame += 1
				if self.p_cur_frame == self.walkspritesheetsize:
					self.p_cur_frame = 0
                  
			norm_move_vector = math3d.Vector2FromPolar(math.degrees(self.dir))
			self.vel = vel_mag * dtime
			norm_move_vector *= self.vel
            
			self.pos[0] += norm_move_vector[0]
			self.pos[1] += norm_move_vector[1]
				
		if p_state == 2:
			if self.character == "cow":
				self.dead = True
			else:
				self.p_cur_delay -= dtime * 500
				if self.p_cur_delay < self.P_DELAY_FRAME:
					self.p_cur_delay += self.P_DELAY_FRAME
					self.p_cur_frame += 1
					if self.p_cur_frame == self.deathspritesheetsize -1:
						self.dead = True		

	def getWidth(self):
		""" gets width of sprite """
		h = self.p_frames[self.walkdir][self.p_cur_frame].get_width()
		return h

	def getHeight(self):
		""" get height of sprite """
		w = self.p_frames[self.walkdir][self.p_cur_frame].get_height()
		return w

	def blit(self, window):
		""" blits the character to the screen """
		if not self.dead:
			self.window = window
			if self.walkdir <= 8:
				self.orientation = self.walkdir
			else:
				self.orientation = 5
			if self.p_state != 2:
			  self.window.blit(self.p_frames[self.orientation][self.p_cur_frame], self.pos)
			else:
			  self.window.blit(self.death_frames[self.orientation][self.p_cur_frame], self.pos)
		
	def addtext(self, damage):
		""" When character takes damage, pass damage value to this method """
		self.hwidth = self.getWidth() / 2
		textoffset = 0
		if len(self.damage_list) > 10:    # Sets a limit on quantity of damage values
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

""" Classes for player characters """
class Mage(playerClass):
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

class Warrior(playerClass):
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

class Cleric(playerClass):
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

class Thief(playerClass):
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
        

class enemyClass(BaseCharClass):
	def __init__(self, pos, vel_mag, exp):
		BaseCharClass.__init__(self, pos, vel_mag, exp)

		self.walkdir = random.randint(1, 11)
		self.dirtimer = random.randint(1500, 2500) # enemy walks for x ms
		self.dirtimer /= 1000.0	 # converts timer to sec
		self.dir = 0
		self.expGain = self.level * 5
		self.spawn = pos

	def basicMovement(self, dtime, vel_mag, movelimit):
		""" Basic enemy "wandering": walks around and stops randomly """
		if self.p_state != 2:
			self.p_state = 1
			# Timer manager for time spent walking in direction / stopping
			if self.dirtimer > 0:
				self.dirtimer -= dtime
			if self.dirtimer <= 0:
				# Changes direction and timer to different values
				# If walkdir generates same number twice in a row, reroll
				tmpcheck = self.walkdir
				self.walkdir = random.randint(1, 11)
				if tmpcheck == self.walkdir:
					self.walkdir = random.randint(1, 11)
					if self.walkdir <= 8:
						self.p_state = 1
				# Resets timer for walk direction
				self.dirtimer = random.randint(1500, 2500) # enemy walks for x ms
				self.dirtimer /= 1000.0
	
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

""" Enemies """
class Wolf(Thief, enemyClass):
    def __init__(self, pos, vel_mag, exp):
        Thief.__init__(self, pos, vel_mag, exp)
        enemyClass.__init__(self, pos, vel_mag, exp)    
        self.pos = pos
        self.vel_mag = vel_mag
        self.exp = exp
        self.colorKey = (111,79,51)
        self.size = 96
        self.p_class = "wolf"
        self.loadFrames(self.p_class, "Monster", "Move", self.size)
        
class Cow(Warrior, enemyClass):
    def __init__(self, pos, vel_mag, exp):
        Warrior.__init__(self, pos, vel_mag, exp)
        enemyClass.__init__(self, pos, vel_mag, exp)    
        self.pos = pos
        self.vel_mag = vel_mag
        self.exp = exp
        self.colorKey = (111,79,51)
        self.size = 96
        self.p_class = "cow"
        self.loadFrames(self.p_class, "Monster", "walk", self.size)
