# Cameron Schuette + Rock G Bolton
""" Basic Character Class for players and enemies """
import math
import random
import pygame
import NewBullet
import math3d

class BaseCharClass(object):
	def __init__(self, pos, vel, vel_mag):
		""" Position and movement """
		self.pos = pos
		self.vel = vel
		self.vel_mag = vel_mag
		self.bullets = []

		""" Attributes """
		self.cur_health = 100
		self.max_health = 100
		self.cur_mana = 100
		self.max_mana = 100
		self.p_frames = [[], [], [], []]
		self.p_cur_frame = 0
		self.P_DELAY_FRAME = 80
		self.p_cur_delay = self.P_DELAY_FRAME
		self.p_frames_per_state = 8

	def normalize(self, v):
		""" Normalizes a vector """
		tmplen = (v[0] ** 2 + v[1] ** 2) ** 0.5
		if tmplen: # (is not zero)
			v[0] /= tmplen
			v[1] /= tmplen

			return v

	def move(self, dtime, cameraPos): # IN PROCESS OF CHANGING TO VECTOR-BASED MOVEMENT
		""" Uses velocity and magnitude to move player/enemy """
		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME

		self.pos[0] += (self.vel[0] * self.vel_mag * dtime)
		self.pos[1] += (self.vel[1] * self.vel_mag * dtime)

	def update(self, dtime, p_offset, p_state, cameraPos):
		""" Updates frames of animation for players and enemies """
		self.p_offset = p_offset
		self.p_state = p_state
		if self.p_state == 0:
			self.p_cur_frame = 0
			self.p_cur_delay = self.P_DELAY_FRAME

		if self.p_state == 1:
			self.p_cur_delay -= dtime
			while self.p_cur_delay < self.P_DELAY_FRAME:
				self.p_cur_delay += self.P_DELAY_FRAME
				self.p_cur_frame += 1
				if self.p_cur_frame == len(self.p_frames[0]):
					self.p_cur_frame = 0

		self.move(dtime, cameraPos)
		self.tmpwidth = self.p_frames[self.p_offset][self.p_cur_frame].get_width()
		self.tmpheight = self.p_frames[self.p_offset][self.p_cur_frame].get_height()

		self.vel[0] = 0
		self.vel[1] = 0

	def hit_detect(self, bx, by, b_rad, px, py, tmpwidth, tmpheight):
		""" Hit detection for circular hitboxes """
		cx = bx
		cy = by

		x1 = px
		y1 = py
		x2 = px + tmpwidth
		y2 = py + tmpheight

		if cx < x1:
			cx = x1
		elif cx > x2:
			cx = x2

		if cy < y1:
			cy = y1
		elif cy > y2:
			cy = y2

		dist = ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5

		if dist <= b_rad:
			return True

		return False

	def blit(self, window, cameraPos):
		self.window = window
		self.temppos = [(self.pos[0] - self.tmpwidth // 2) - cameraPos[0], (self.pos[1] - self.tmpheight // 2) - cameraPos[1]]
		self.window.blit(self.p_frames[self.p_offset][self.p_cur_frame], self.temppos)
		"""makes and renders and health bar above the player"""
		width = 50
		height = 10
		border_color = (255, 255, 255)
		border_width = 1
		x = self.temppos[0] + 25
		y = self.temppos[1]
		ax = self.temppos[0] + 25
		ay = self.temppos[1] + 4

		rect = (x, y, width, height)
		mrect = (ax, ay, width, height)
		pygame.draw.rect(self.window, border_color, rect, border_width)

		if self.cur_health:
			x = rect[0] + border_width
			y = rect[1] + border_width
			width = (rect[2] - border_width * 2)
			width *= (self.cur_health / self.max_health)
			height = rect[3] - border_width * 2

			rect = (x, y, width, height/2)
			pygame.draw.rect(self.window, (255, 0, 0), rect)

		if self.cur_mana:
			ax = mrect[0] + border_width
			ay = mrect[1] + border_width
			awidth = (rect[2] + border_width * 2)
			awidth *= (self.cur_mana / self.max_mana)
			aheight = rect[3] + border_width * 2

			mrect = (ax, ay, width, height/2)
			pygame.draw.rect(self.window, (0, 0, 255), mrect)

class Mage(BaseCharClass):
	def __init__(self, pos, vel, vel_mag):
		BaseCharClass.__init__(self, pos, vel, vel_mag)
		self.GCD == 1500   # Global cooldown time
		self.cur_mana = 100
		self.max_mana = 100
		self.atk = 12
		self.dfn = 3
		self.spd = 7
		self.rng = 8
		self.colorKey = (105,74,46)
		self.p_class = 'Mage'
		tmpstr = self.p_class + " Sprites/walking "
		for i in range(0, 8):
			tmpimg = pygame.image.load(tmpstr + "n000" + str(i) + ".bmp").convert()
			tmpimg.set_colorkey(self.colorKey)
			self.p_frames[0].append(tmpimg)

			tmpimg = pygame.image.load(tmpstr + "e000" + str(i) + ".bmp").convert()
			tmpimg.set_colorkey(self.colorKey)
			self.p_frames[1].append(tmpimg)

			tmpimg = pygame.image.load(tmpstr + "s000" + str(i) + ".bmp").convert()
			tmpimg.set_colorkey(self.colorKey)
			self.p_frames[2].append(tmpimg)

			tmpimg = pygame.image.load(tmpstr + "w000" + str(i) + ".bmp").convert()
			tmpimg.set_colorkey(self.colorKey)
			self.p_frames[3].append(tmpimg)

		del tmpstr

class Fighter(BaseCharClass):
    def __init__(self, pos, vel, vel_mag):
        BaseCharClass.__init__(self, pos, vel, vel_mag)
        self.GCD == 800
        self.cur_mana = 100
        self.max_mana = 100
        self.atk = 9
        self.dfn = 12
        self.spd = 5
        self.rng = 4
        self.colorKey = (106,76,48)
        self.p_class = 'Fighter'
        tmpstr = self.p_class + " Sprites/walking "
        for i in range(0, 8):
        	tmpimg = pygame.image.load(tmpstr + "n000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[0].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "e000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[1].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "s000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[2].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "w000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[3].append(tmpimg)

        del tmpstr

class Cleric(BaseCharClass):
    def __init__(self, pos, vel, vel_mag):
        BaseCharClass.__init__(self, pos, vel, vel_mag)
        self.GCD = 700
        self.cur_mana = 100
        self.max_mana = 100
        self.atk = 3
        self.dfn = 8
        self.spd = 7
        self.rng = 12
        self.colorKey = (105,74,46)
        self.p_class = 'Cleric'
        tmpstr = self.p_class + " Sprites/walking "
        for i in range(0, 8):
        	tmpimg = pygame.image.load(tmpstr + "n000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[0].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "e000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[1].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "s000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[2].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "w000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[3].append(tmpimg)

        del tmpstr

class Thief(BaseCharClass):
    def __init__(self, pos, vel, vel_mag):
        BaseCharClass.__init__(self, pos, vel, vel_mag)
        self.GCD == 500
        self.cur_mana = 100
        self.max_mana = 100
        self.atk = 7
        self.dfn = 8
        self.spd = 12
        self.rng = 3
        self.colorKey = (106,76,48)
        self.p_class = 'Thief'
        tmpstr = self.p_class + " Sprites/walking "
        for i in range(0, 8):
        	tmpimg = pygame.image.load(tmpstr + "n000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[0].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "e000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[1].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "s000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[2].append(tmpimg)

        	tmpimg = pygame.image.load(tmpstr + "w000" + str(i) + ".bmp").convert()
        	tmpimg.set_colorkey(self.colorKey)
        	self.p_frames[3].append(tmpimg)

        del tmpstr

class playerClass(BaseCharClass):
	def __init__(self, pos, vel, vel_mag, p_class):
		BaseCharClass.__init__(self, pos, vel, vel_mag, p_class)
		self.fired = False

	def aimAngle(self, mx, my):
		""" Calculates the angle of aim from character to mouse (radians) """
		x = mx - self.pos[0]
		y = my - self.pos[1]

		self.angle = math.atan2(-y, x)

	def fire(self):
		""" Controls firing """
		if fired:
			bulX = self.p_pos[0]
			bulY = self.p_pos[1]

			normalize(vect)
			#print(vect)

			self.fired = False

# Rock G Bolton + Nick Linton
# Basic enemy class that moves in a random direction until within X of player
    # Once within X, enemy chases player

class enemyClass(object):
	def __init__(self, pos, health):
		self.x = pos[0]
		self.y = pos[1]
		self.z = 2
		self.vel = 100/1000
		self.vx = 0
		self.vy = 0
		self.angle = 0
		self.health = health
		self.dead = False
		self.bullets = []
		self.ROF = 1000
		self.shotTimer = 0
		self.distFromPlayer = 3000
		self.allowedToFire = True
		self.aiming = False
		self.attackTimer = 2000
		self.moveTimer = 1500
		self.dir = 0
		self.walkdir = random.randint(1, 11)
		self.lol= 100

		randomDir = random.randint(0,1)
		randomDir = math.radians(randomDir)
		self.vx = math.asin(randomDir)
		self.vy = math.acos(randomDir)

	def draw(self, surface, dtime, barriers, cameraPos):
		tmppos = [(self.x) - cameraPos[0], (self.y) - cameraPos[1]]
		if self.dead == False:
			pygame.draw.circle(surface, (255,0,0), (int(tmppos[0]), int(tmppos[1])), 15)
		if self.dead == True:
			pygame.draw.circle(surface, (0,0,255), (int(tmppos[0]), int(tmppos[1])), 15)
		for i in self.bullets:
			i.update(dtime)
			i.render(surface)
			if i.remove == True:
				self.bullets.remove(i)

	def checkIfHit(self, cameraPos, bullets = []):
		newBullets = bullets
		for i in newBullets:
			dist = math.sqrt(((i.x + cameraPos[0]) - self.x)**2 + ((i.y + cameraPos[1]) - self.y)**2) # sqare root of (bullets x - camera position x - enemy position x)**2 + ((bullets y - camera position y - enemy position y)**2
			#print(dist)
			if dist <= 15:
				self.health -= i.damage
				newBullets.remove(i)

		#checks for enemy death
		if self.health <=0:
			self.dead = True

		return newBullets

	def move(self, playerX, playerY, dtime, cameraPos):
		tempX = self.x - playerX
		tempY = self.y - playerY
		dist = math.sqrt(tempX**2 + tempY**2)

		if dist < 500 and dist >= 40:
			if tempX != 0 and tempY != 0:
				self.angle = -math.atan2(tempY,tempX)
			self.vx = self.vel * math.cos(-self.angle) * dtime
			self.vy = self.vel * math.sin(-self.angle) * dtime
			self.x -= self.vx
			self.y -= self.vy
			self.aiming = False


		else:
			if self.moveTimer > 0:
				self.moveTimer -= dtime
			if self.moveTimer <= 0:
                # Changes direction and timer to different values
                # If walkdir generates same number twice in a row, reroll
				tmpcheck = self.walkdir
				self.walkdir = random.randint(1, 8)
				if tmpcheck == self.walkdir:
					self.walkdir = random.randint(1, 8)
				# Resets timer for walk direction
				self.moveTimer = random.randint(1500, 2500) # enemy walks for x ms
		if dist < 300:
			self.aiming = True
			self.shoot(dtime, cameraPos)

			# if random direction # exceeds 8, enemy stops for durtimer sec
			if self.walkdir > 8:
				self.vel = 0

			# Moves the enemy (WILL USE UPDATE METHOD WHEN ENEMIES HAVE SPRITES)
			self.EnemyMove()
			m = math3d.Vector2FromPolar(math.degrees(self.dir), self.vel)
			self.x += m[0]
			self.y += m[1]

		return [self.x, self.y]



	def shoot(self, dtime, cameraPos):
		if self.allowedToFire:
			fireDir = (self.angle + math.pi)
			if not self.aiming:
				firDir += math.radians(random.randint(-20,20))
			aBullet = NewBullet.bullet(self.x - cameraPos[0], self.y - cameraPos[1], fireDir, 10)
			self.bullets.append(aBullet)
			self.shotTimer = 0
			self.allowedToFire = False
		else:
			self.shotTimer += dtime
			if self.shotTimer>= self.ROF:
				self.allowedToFire = True

		#print (self.bullets)

	def playerHitCheck(self, cameraPos, player):
		Ppos = player.pos
		for i in self.bullets:
			dist = math.sqrt(((i.x + cameraPos[0]) - Ppos[0])**2 + ((i.y + cameraPos[1]) - Ppos[1])**2) # sqare root of (bullets x - camera position x - enemy position x)**2 + ((bullets y - camera position y - enemy position y)**2
			#print(dist)
			if dist <= 15:
				player.cur_health -= i.damage
				if player.cur_health < 0:
					player.cur_health = 0
				self.bullets.remove(i)

	def EnemyMove(self):
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