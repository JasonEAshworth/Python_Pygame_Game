import configparser
import glob
import pygame
import player
import random

class TileDbase(object):
	""" Database of all the tiles used in the .map files pulled from all .con files"""
	def __init__(self,path):
		self.dBase = {}
		config = configparser.ConfigParser()
		fList=[]
		fList.append(glob.glob(path+"master.con"))
		for name in fList:
			config.read(name)
			for section in config.sections():
				desc = dict(config.items(section))
				self.dBase[section] = desc
	def collide(self, tileCode):
		# checks to see if particular tile blocks movment
		if self.dBase[tileCode].get('block'):
			return 1
		elif self.dBase[tileCode].get('warp'):
			return 2
		elif self.dBase[tileCode].get('damage'):
			return 3
		elif self.dBase[tileCode].get('slow'):
			return 4
		else:
			return False

class OverlayDbase(object):
	""" Data base of all the overlay images """
	def __init__(self,path):
		self.dBase = {}
		config = configparser.ConfigParser()
		fList=[]
		fList.append(glob.glob(path+"overlay*"))
		for name in fList:
			config.read(name)
			for section in config.sections():
				desc = dict(config.items(section))
				self.dBase[section] = desc


class Zone(object):
	""" Initialization of various world variables."""
	def __init__(self, TileDBptr = ".\\" , TileImgFname = 'tilesetDay', OLayDBptr = ".\\", mapName = "level1.map"):
		self.winHeight = 704
		self.winWidth = 980
		self.TileDBptr = TileDbase(TileDBptr)
		#self.OLayDBptr = OverlayDbase(OLayDBptr)
		self.tileSize = 64
		self.tCheck = [0,0,0,0,0,0,0,0,0]
		self.playerPos = [self.winWidth/2, self.winHeight/2]
		self.enemyList = []
		self.eList = []
		self.totalNumEnemies = 0
		self.enemySpawn = []
		self.enemiesPos = [self.winWidth/2,self.winHeight/2]
		self.cameraPos = [0,0]
		self.cameraSpeed = .2
		self.mapName = mapName
		self.TileImgFname = TileImgFname
		self.tlist = []
		self.olist = []
		self.wlist = []
		self.startPos = []
		self.TileKeys= []
		self.OlayKeys = []
		self.world = self.loadMap(self.mapName)
		self.imgList =[]
##		for o in self.olist:
##			imgCode = o[0]
##			imgName = str(self.TileDBptr.dBase[imgCode]['name'])
##			imgName = imgName[:-4]
##			#img = pygame.image.load(str(self.OLayDBptr.dBase[imgName]['name']))
##			self.imgList.append(img)


	def load_tile_table(self,TileImgFname):
		""" Loads an image file and 'splits' it up into tiles. These tiels are added
			to a list and stored for blitting to the screen for later use. """
		fList=[]
		fList.append(glob.glob("tileset*"))
		#for name in fList:
			#for x in range(len(name)):
		image = pygame.image.load(TileImgFname+".png").convert_alpha()
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, int(image_width/self.tileSize)):
			line = []
			tile_table.append(line)
			for tile_y in range(0, int(image_height/self.tileSize)):
				rect = (tile_x* self.tileSize, tile_y*self.tileSize,self.tileSize, self.tileSize)
				line.append(image.subsurface(rect))
		return tile_table


	def loadMap(self,fname):
		mapConf = configparser.ConfigParser()
		mapConf.read(fname)
		self.TileKeys = mapConf.get("level","map").split("\n")
		for line in self.TileKeys:
			temp_row = []
			for i in range(0,len(line),3):
				temp_row.append(line[i:i+3])
			self.tlist.append(temp_row)
		# List of Overlay 'keys' pulled from .map file
		OlayKeys = mapConf.get("level","overlay").split("\n")
		for o in OlayKeys:
			olay = o.split(":")
			self.olist.append(olay)
		mapWarps = mapConf.get("level","warps").split("\n")
		for w in mapWarps:
			warp =w.split(":")
			self.wlist.append( warp)
		Pos = mapConf.get("level","pos").split("\n")
		for p in Pos:
			tmp = p.split(':')
			self.startPos = tmp
		enemy=[]
		self.totalNumEnemies = 0
		self.eList = []
		self.enemyList = []
		enemySpawn = []
		tmpSpawn = []
		enemies = mapConf.get("level","enemies").split("\n")
		spawn = mapConf.get("level","enemySpawn").split("\n")
		# pull enemies from the .map file
		item = 0
		while item < 4:
			spawntmp = spawn[item].split(':')
			enemySpawn.append((int(spawntmp[0]),int(spawntmp[1])))
			item +=1
		for e in enemies:
			etmp = e.split(':')
			self.totalNumEnemies += int(etmp[0])
			enemy.append(etmp)
		e = 0
		while e < self.totalNumEnemies:
			self.enemySpawn.append(enemySpawn[random.randint(0,3)])
			e += 1
		self.eList = enemy

		# Calculate the size of the world in tiles and pixels
		self.world_tileWidth = len(self.TileKeys[0])/3
		self.world_tileHeight = len(self.TileKeys)
		self.world_pixelWidth = self.world_tileWidth * self.tileSize
		self.world_pixelHeight = self.world_tileHeight * self.tileSize
		return [self.world_tileWidth, self.world_tileHeight, self.world_pixelWidth, self.world_pixelHeight]
		# may not need this

	def setCameraPos(self,x,y):
		pass
	def getTile(self,x,y):
		print(self.tlist[int(y // self.tileSize)][int(x // self.tileSize)])

	def render(self,surf):

		tiles = self.load_tile_table(self.TileImgFname)
		tileX = int(self.cameraPos[0]) // self.tileSize
		tileY = int(self.cameraPos[1]) // self.tileSize
		offsetX = int(self.cameraPos[0]) % self.tileSize
		offsetY = int(self.cameraPos[1]) % self.tileSize
		# 2. Figure out how many tiles we need to draw
		drawX = self.winWidth // self.tileSize + 2
		drawY = self.winHeight // self.tileSize + 2
		# 3. Draw that section of the TileKeys
		if self.world[3] < self.winHeight:
			y = int(self.winHeight/2 - self.world[3]/2)
		else:
			y = -offsetY

		for row in range(tileY, tileY + drawY):
			if self.world[2] < self.winWidth:
				x = int(self.winWidth/2 - self.world[2]/2)
			else:
				x = -offsetX
			for col in range(tileX, tileX + drawX):
				if col < self.world[0] and row < self.world[1]:
					tileCode = self.tlist[row][col]
					tile = self.TileDBptr.dBase[tileCode]['tile'].split(',')
					tile = int(tile[0]),int(tile[1])
					tileImg = tiles[tile[0]][tile[1]]
					surf.blit(tileImg, (x,y))
				x += self.tileSize
			y += self.tileSize

	def OverLayRender(self,surf):

		for x in range(len(self.olist)):
			pos = int(self.olist[x][1]),int(self.olist[x][2])
			surf.blit(self.imgList[x],(pos[0]*self.tileSize-self.cameraPos[0],pos[1]*self.tileSize-self.cameraPos[1]))


	def tileCheck(self, playerY, playerX):
		self.getTile(playerX, playerY)
		if self.world[3] < self.winHeight:
			playerY = playerY - (self.winHeight/2-self.world[3]/2)
		else:
			playerY = int(playerY)
		if self.world[2] < self.winWidth:
		   playerX = playerX - (self.winWidth/2-self.world[2]/2)
		else:
			playerX = int(playerX)

		self.tCheck[0] = (self.tlist[int((playerY // self.tileSize) - 1)][int(playerX // self.tileSize)])  #up
		self.tCheck[2] = (self.tlist[int(playerY // self.tileSize)][int((playerX // self.tileSize) - 1)])  #left
		self.tCheck[1] = (self.tlist[int(playerY // self.tileSize) + 1][int(playerX // self.tileSize)])  #down
		self.tCheck[3] = (self.tlist[int(playerY // self.tileSize)][int(playerX // self.tileSize) + 1])  #right
		self.tCheck[4] = (self.tlist[int((playerY // self.tileSize) + 1)][int((playerX // self.tileSize) - 1)]) #down-left
		self.tCheck[5] = (self.tlist[int((playerY // self.tileSize) + 1)][int((playerX // self.tileSize) + 1)]) #down-right
		self.tCheck[6] = (self.tlist[int((playerY // self.tileSize) - 1)][int((playerX // self.tileSize) -1)]) #up-left
		self.tCheck[7] = (self.tlist[int((playerY // self.tileSize) - 1)][int((playerX // self.tileSize) + 1)]) #up-right
		self.tCheck[8] = (self.tlist[int((playerY // self.tileSize))][int((playerX // self.tileSize))]) # on

	def collision(self, objectPos, enemy = False):
		#print("dink")
		tmpPos = objectPos[0]//self.tileSize,objectPos[1] // self.tileSize
		playerX = int(objectPos[0])
		playerY = int(objectPos[1])
		playerRad = 5
		tX = (int(playerX) // self.tileSize) * self.tileSize
		tY = (int(playerY) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[8]) #collision check on
		if (collide == 2) and (enemy == False):



			for i in range(len(self.wlist)):
				if int(self.wlist[i][0]) == tmpPos[0] and  int(self.wlist[i][1]) == tmpPos[1]:

					level = self.wlist[i][2]
					self.playerPos[0] = int(self.startPos[0])
					self.playerPos[1] = int(self.startPos[1])
					self.wlist = []
					self.tlist = []
					self.world = self.loadMap(level)

					break
		if collide == 3:
			return 3
		if collide == 4:
			return 4

		collide = self.TileDBptr.collide(self.tCheck[2]) #collision check left
		tX -= self.tileSize
		if collide == 1 and ((playerX - playerRad - 3) <= tX + self.tileSize):
			objectPos[0] = tX + self.tileSize + playerRad + 3
		tX = (int(playerX) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[3]) #collision check right
		tX += self.tileSize
		if collide == 1 and ((playerX + playerRad + 3) >= tX):
			objectPos[0] = tX - playerRad - 3
		tX = (int(playerX) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[0]) # colission check up
		if collide  == 1 and ((playerY - playerRad - 3) <= tY):
			objectPos[1] = tY + playerRad + 3
		tY = (int(playerY) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[1]) # colission check down
		tY += self.tileSize
		if collide  == 1 and ((playerY + playerRad +3) >= tY):
			objectPos[1] = tY - playerRad - 3
		tY = (int(playerY) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[4]) #colission check down-left
		tX -= self.tileSize
		tY += self.tileSize
		if collide  == 1 and ((playerX - playerRad) <= tX + self.tileSize -6) and ((playerY + playerRad - 6) >= tY):
			pygame.event.pump()
			pressedList = pygame.key.get_pressed()
			if pressedList[pygame.K_DOWN]:
				objectPos[0]= tX + 6 + self.tileSize
				objectPos[1]= tY - 6
			if pressedList[pygame.K_LEFT]:
				objectPos[0]= tX - 6 + self.tileSize
				objectPos[1]= tY - 6
		tX = (int(playerX) // self.tileSize) * self.tileSize
		tY = (int(playerY) // self.tileSize) * self.tileSize


		collide = self.TileDBptr.collide(self.tCheck[5]) #colission check down-right
		tX += self.tileSize
		tY += self.tileSize
		if collide  == 1 and ((playerX + playerRad) >= tX + 6) and ((playerY + playerRad -6) >= tY):
			pygame.event.pump()
			pressedList = pygame.key.get_pressed()
			if pressedList[pygame.K_DOWN]:
				objectPos[0] = tX - 6
				objectPos[1] = tY - 6
			if pressedList[pygame.K_RIGHT]:
				objectPos[0] = tX + 3
				objectPos[1] = tY - 6
		tX = (int(playerX) // self.tileSize) * self.tileSize
		tY = (int(playerY) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[6]) #collision check up-left
		if collide  == 1 and ((playerX - playerRad) <= tX - 6) and ((playerY - playerRad + 6) <= tY):
			pygame.event.pump()
			pressedList = pygame.key.get_pressed()
			if pressedList[pygame.K_UP]:
				objectPos[0] = tX + 6
				objectPos[1] = tY + 6
			if pressedList[pygame.K_LEFT]:
				objectPos[0] = tX - 3
				objectPos[1] = tY + 6
		tX = (int(playerX) // self.tileSize) * self.tileSize
		tY = (int(playerY) // self.tileSize) * self.tileSize

		collide = self.TileDBptr.collide(self.tCheck[7]) #collision check up-right
		tX += self.tileSize
		if collide  == 1 and ((playerX + playerRad) >= tX + 6) and ((playerY - playerRad +6) <= tY):
			pygame.event.pump()
			pressedList = pygame.key.get_pressed()
			if pressedList[pygame.K_UP]:
				objectPos[0] = tX - 6
				objectPos[1] = tY - 6
			if pressedList[pygame.K_RIGHT]:
				objectPos[0] = tX + 3
				objectPos[1] = tY + 6
		tX = (int(playerX) // self.tileSize) * self.tileSize
		tY = (int(playerY) // self.tileSize) * self.tileSize
		return objectPos

	def CreateEnemy(self):
		n = 0
		for i in self.enemyList:
			n +=1
		if n < self.totalNumEnemies:
			z = 0
			p = 0
			for i in self.eList:
				while z < int(self.eList[p][0]):
					if self.eList[p][1] == 'Cow':
						health = 10
						enemy = CamCharacterClass.Cow([self.enemySpawn[z][0],self.enemySpawn[z][1]], self.cameraPos, 100/1000.0, health)
						self.enemyList.append(enemy)
					elif self.eList[p][1] == 'Wolf':
						health = 50
						enemy = CamCharacterClass.Wolf([self.enemySpawn[z][0],self.enemySpawn[z][1]], self.cameraPos, 100/1000.0, health)
						self.enemyList.append(enemy)
					z += 1
				p += 1
				z = 0
		p = 0

