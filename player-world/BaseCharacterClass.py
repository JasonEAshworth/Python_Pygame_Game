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
		self.p_frames_per_state = 8
		self.p_frames = []
		for i in range(9):
			self.p_frames.append([])
		self.p_cur_frame = 0
		self.P_DELAY_FRAME = 80
		self.p_cur_delay = self.P_DELAY_FRAME
		self.frames_per_state = 8
		self.damage_list = []

	def loadFrames(self, character, s_type, anim_type):   # s_type can either be "Class" or "Monster"
		""" Loads all frames from sprite sheet for given character for 96 x 96 frames """
		tmpstr = "SVN Root/Artwork/" + s_type + " Sprites/" + character + anim_type
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

	def update(self, dtime, p_state, vel_mag):
		""" Updates frames of animation for players and enemies """
		self.p_state = p_state
		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME

		elif self.p_state == 1:
			self.p_cur_delay -= dtime * 1000
			while self.p_cur_delay < self.P_DELAY_FRAME:
				self.p_cur_delay += self.P_DELAY_FRAME
				self.p_cur_frame += 1
				if self.p_cur_frame == 8:
					self.p_cur_frame = 0

			tmpwidth = self.p_frames[self.walkdir][self.p_cur_frame].get_width()

			tmpheight = self.p_frames[self.walkdir][self.p_cur_frame].get_height()

			norm_move_vector = math3d.Vector2FromPolar(math.degrees(self.dir))
			self.vel = vel_mag * dtime
			norm_move_vector *= self.vel

			self.pos[0] += norm_move_vector[0]
			self.pos[1] += norm_move_vector[1]

	def getWidth(self):
		h = self.p_frames[self.walkdir][self.p_cur_frame].get_width()
		return h

	def getHeight(self):
		w = self.p_frames[self.walkdir][self.p_cur_frame].get_height()
		return w

	def blit(self, window):
		self.window = window
		if self.walkdir <= 8:
			self.orientation = self.walkdir
		else:
			self.orientation = 5
		self.window.blit(self.p_frames[self.orientation][self.p_cur_frame], self.pos)
		
	def addDamage(self, damage, font):
		""" When character takes damage, pass damage value to this method """
		self.damage_list.append(FloatingText(self.pos,damage,font))


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
		self.p_class = "Mage"
		self.loadFrames(self.p_class, "Class", "Other")

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
		self.p_class = "Warrior"
		self.loadFrames(self.p_class, "Class", "Other")

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
		self.p_class = "Cleric"
		self.loadFrames(self.p_class, "Class", "Other")

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
		self.p_class = "Thief"
		self.loadFrames(self.p_class, "Class", "Other")
        

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
        self.loadFrames(self.p_class, "Monster", "walk")


class FloatingText(object):
	""" Manages and renders the floating damage text above characters """
	def __init__(self, pos, string, font):
		self.pos = pos
		self.pos[0] = self.pos[0] + player.getWidth() / 2
		self.pos[1] = self.pos[1] - player.getHeight()
		self.top = self.pos
		self.str = string
		
		#self.font = pygame.font.Font(None, 20)
		#self.player = player
		self.font = font
	
	

	def render(self, dtime):
		""" Blits and controls the movement of the floating text """
		for font_damage in self.damage_list: 
			#color fade
			if self.player.pos[1] < self.pos[1] - 30 :
				val = 0
			elif self.player.pos[1] < self.pos[1] - 20:
				val = (y/200)*255
			elif self.player.pos[1] < self.pos[1] - 10:
				val = 255-((y-400)/200)*255
			elif self.player.pos[1] < self.pos[1]:
				val = 255
			else:
				val  = 0
            # Blits to screen
			color = (val,val,val)
			tempS = self.font.render(font_damage[currentline], True, color)
			window.blit(tempS, (100, 300))
