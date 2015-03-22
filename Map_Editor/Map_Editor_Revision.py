class Map(object):
	"""Master class for loading, saving, and creating a map for the map editor"""

	def __init__(self):
		self.tlist = []
		self.mapName = None
		self.map_tileWidth = None
		self.map_tileHeight = None
		self.map_pixelWidth = None
		self.map_pixelHeight = None
		self.tileCode = None
		self.palletteSelected = None
		self.cameraPos = [0,0]
		self.tileSize = 64
		self.keys = None
		self.pallette_tileHeight = None
		self.pallette_tileWidth = 266 // self.tileSize
		self.palletteX = 2
		self.palletteY = 2
		self.tileX = 0
		self.tileY = 0
		#need more variables!!

	def startup(self):
		decision = input("Do you want to 'Create' a map or 'Load' a map?")
		if decision.lower() != "create" and decision.lower() != "load":
			self.startup()
		elif decision.lower() == "create":
			self.createMap()
		elif decision.lower() == "load":
			self.loadMap()

	def isInt(self, choice):
		try:
			int(choice)
			return True
		except ValueError:
			return False


	def loadMap(self):
		self.tlist = []
		mapList = glob.glob(".\Maps\*.map")
		prompt = ""
		for i in range(len(mapList)):
			prompt += str(i) + " : " + mapList[i] + "\n"

		choice = input(prompt + "\n Choose Wisely!")
		if self.isInt(choice):
			if int(choice) <= len(mapList)-1 and int(choice) >=0:
				choice = int(choice)
			else:
				self.loadMap()
		else:
			self.loadMap()

		#Get the height and width and generate the tlist from the .map file.
		mapConf =  configparser.ConfigParser()
		mapConf.read(mapList[choice])

		TileKeys = mapConf.get("level","map").split("\n")
		for line in TileKeys:
			temp_row = []
			for i in range(0,len(line),3):
				temp_row.append(line[i:i+3])
			self.tlist.append(temp_row)
		# Calculate the size of the world in tiles and pixels
		self.map_tileWidth = len(TileKeys[0])/3
		self.map_tileHeight = len(TileKeys)
		self.map_pixelWidth = self.map_tileWidth * self.tileSize
		self.map_pixelHeight = self.map_tileHeight * self.tileSize



	def saveMap(self):

		"""Done by Aaron"""

		FileName = input("What do you want to name the .map file?")
		if str(FileName[-4:]) != ".map":
			FileName += ".map"
		saved = open('./Maps/'+FileName, 'w')
		newtlist = "[level]\ntileset = tiles32x32.bmp\nmap = "
		for character in str(self.tlist):
		   if character == "'" or character == "[" or character == "," or character == " ":
		  			pass
		   elif character == "]":
			  	character = "\n\t  "
			  	newtlist += character
		   else:
		   		newtlist += character
		saved.write(str(newtlist))

		#save the tlist to a .map file with the name passed in

	def masterHitDetection(self, mouseX, mouseY):

		"""#Create 2 hit boxes one overtop of the map surface, and one over top of
		the pallette surface. (Done) If map surface, call mapTileDetection (passing in X and
		Y) and getting the information to change the tlist.  If pallette hit, detect
		which tile is hit, store the key, and set the green square 'selected' trigger.
		(I don't know what that is yet)"""

		palletteRect = pygame.Rect(1315,30, 266, 704)
		gameSurfRect = pygame.Rect(10,30, 1280, 704)

		if palletteRect.collidepoint(mouseX, mouseY):
			self.palletteHitDetection(mouseX, mouseY)

		elif gameSurfRect.collidepoint(mouseX, mouseY):

			if self.palletteSelected == None:
				pass
			else:
				self.mapTileDetection(mouseX, mouseY)

		else:
			pass

	def palletteSelection(self):
		try:
			self.palletteSelected = self.pList[self.tileY -1][self.tileX -1]
			return True
		except IndexError:
			return False

	def palletteHitDetection(self, mouseX, mouseY):

		hitX = mouseX -1315
		self.hitY = mouseY -30 - self.palletteY -(mouseY // self.tileSize ) * 2
		# TrueDiv "//" it by self.tileSize
		self.tileX = (hitX // self.tileSize)+1
		self.tileY = (self.hitY // self.tileSize)+1
		self.drawSelected()
		if self.palletteSelection():
			self.palletteSelected = self.pList[self.tileY -1][self.tileX -1]
		else:
			pass

	def drawSelected(self):
		pygame.draw.rect(palletteSurf, (0,255,0), ((self.tileX-1)*self.tileSize+((self.tileX - 1)*2),\
						 (self.tileY-1)*self.tileSize+((self.tileY - 1)*2) +self.palletteY-2, 68,68))

	def createMap(self):
		mapList = []
		self.mapName = input("What do you want to name the .map file?")
		if str(self.mapName[-4:]) != ".map":
			self.mapName += ".map"
			#error detection for .map and non-.map names entered.
		self.map_tileHeight = int(input("How many TILES high is the map?"))
		self.map_tileWidth = int(input("How many TILES wide is the map?"))
		counter = 1
		for i in range(int(self.map_tileHeight)):
			tempList = []
			for j in range(int(self.map_tileWidth)):
				tempList.append('a00')
			mapList.append(tempList)
		self.tlist = mapList

	def buildPallette(self, palletteSelected = None):

		#Arron on this

		#creates the palletteList for the right hand side.
		#depending on which button is selected
		#Default to display ALL the tiles.

		self.tiles = self.loadTileTable()
		self.keys = list(db.dBase.keys())
		self.keys.sort()


	def displayPallette(self):

		self.pList=[]
		x = self.palletteX
		y = self.palletteY
		for row in range(1):

			for tileCode in self.keys:
				tile = db.dBase[tileCode]['tile'].split(',')
				tile = int(tile[1]),int(tile[0])
				tileImg = self.tiles[tile[1]][tile[0]]
				palletteSurf.blit(tileImg, (x,y))
				x += self.tileSize + 2
				if x > self.tileSize * 4:
					y += self.tileSize + 2
					x = 2
		for x in range(0, len(self.keys),4):
			tmp = self.keys[x:x + 4]
			self.pList.append(tmp)

	def displayGrid(self, zoomChange = None, startx=-50, starty=-50, endx = 0, endy= 10000):

		#Displays the Grid overlay on the actual surface

		startx = int(-self.cameraPos[0] % self.tileSize)
		starty = int(-self.cameraPos[1] % self.tileSize)
		for i in range(int((1280 / self.tileSize) +1)):
				#Change hard coded numbers to
			#Vertical Lines
			pygame.draw.line(gameSurf, (255,255,255), (startx,starty-self.tileSize  ),(startx, 704 + starty) , 1)
			startx += self.tileSize

		startx = (self.cameraPos[0] % self.tileSize)

		for i in range(int((704 / self.tileSize) + 1)):
			#Horizontal Lines
			pygame.draw.line(gameSurf, (255,255,255), (startx - self.tileSize, starty ),(1280+startx,starty) , 1)
			starty += self.tileSize

	def displayMap(self, tlist= None, zoomChange= None):
		self.map_pixelWidth = self.map_tileWidth * self.tileSize
		self.map_pixelHeight = self.map_tileHeight * self.tileSize
		if self.cameraPos[0] < 0:
			self.cameraPos[0] = 0
		if self.cameraPos[0] >= self.map_pixelWidth - mapWinWidth - 1:
			self.cameraPos[0] = self.map_pixelWidth - mapWinWidth - 1
		if self.cameraPos[1] < 0:
			self.cameraPos[1] = 0
		if self.cameraPos[1] >= self.map_pixelHeight - mapWinHeight - 1:
			self.cameraPos[1] = self.map_pixelHeight - mapWinHeight - 1
		# Alternate drawing code...
		# 1. Figure out which tile the camera is in and how much we're "into" that tile
		tileX = int(self.cameraPos[0]) // self.tileSize
		tileY = int(self.cameraPos[1]) // self.tileSize
		offsetX = int(self.cameraPos[0]) % self.tileSize
		offsetY = int(self.cameraPos[1]) % self.tileSize
		# 2. Figure out how many tiles we need to draw
		drawX = mapWinWidth // self.tileSize + 2
		drawY = mapWinHeight // self.tileSize + 2
		# 3. Draw that section of the TileKeys
		y = -offsetY
		tiles = self.loadTileTable()
		for row in range(tileY, tileY + drawY):
			x = -offsetX
			for col in range(tileX, tileX + drawX):
				if col < self.map_tileWidth and row < self.map_tileHeight:
					tileCode = self.tlist[row][col]
					tile = db.dBase[tileCode]['tile'].split(',')
					tile = int(tile[0]),int(tile[1])
					tileImg = tiles[tile[0]][tile[1]]
					gameSurf.blit(tileImg, (x,y))
				x += self.tileSize
			y += self.tileSize

	def mapTileDetection(self, mX, mY):

		#Does the detection for which tile the user clicked on, and changes that tlist value
		#according to the tile code from the pallette.
		hitX = mX + self.cameraPos[0] -10
		hitY = mY + self.cameraPos[1] -30
		# TrueDiv "//" it by tilesize
		tileX = int(hitX // self.tileSize)
		tileY = int(hitY // self.tileSize)
		#That will give the tile position in the tlist
		#Changes that tilecode, IF something is selected on the pallette
		self.tlist[tileY][tileX] = self.palletteSelected

		"""un-comment these 2 lnes so that you can find the tile number, and the
           location on the map of that specific tile."""

		print(tileY, tileX)
		#print(self.palletteSelected)

	def loadTileTable(self, filename='tilesetDay'):
		#Loads and creates the tile table
		image = pygame.image.load(filename+".png").convert_alpha()
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, int(image_width/64)):
			line = []
			tile_table.append(line)
			for tile_y in range(0, int(image_height/64)):
				rect = (tile_x*64, tile_y*64,64, 64)
				line.append(image.subsurface(rect))
		return tile_table

class TileDbase(object):
	#creates the database for the surfaces (tiles)
	def __init__(self,path):
		self.dBase = {}
		config = configparser.ConfigParser()
		fList=[]
		fList.append(glob.glob("Master.con"))
		for name in fList:
			config.read(name)
			for section in config.sections():
				desc = dict(config.items(section))
				self.dBase[section] = desc

class events(object):
	"""This handles all the clicking and what not."""
	def getPressed():
		#pygame.event.pump()
		global eList
		global pressedList
		pressedList = pygame.key.get_pressed()
		eList = pygame.event.get()

	def checkKeys():
		global done
		if pressedList[pygame.K_ESCAPE]:
			done = True
		if pressedList[pygame.K_LEFT]:
			gameSurf.fill((0,0,0))
			map.cameraPos[0] -= cameraSpeed

		if pressedList[pygame.K_RIGHT]:
			gameSurf.fill((0,0,0))
			map.cameraPos[0] += cameraSpeed

		if pressedList[pygame.K_UP]:
			gameSurf.fill((0,0,0))
			map.cameraPos[1] -= cameraSpeed

		if pressedList[pygame.K_DOWN]:
			gameSurf.fill((0,0,0))
			map.cameraPos[1] += cameraSpeed
		if pressedList[pygame.K_l]:
			map.loadMap()

	def checkMouse():
		global done
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
				posX = e.pos[0]
				posY = e.pos[1]
				map.masterHitDetection(posX, posY)

			elif  e.type == pygame.MOUSEBUTTONDOWN and e.button == 5:
				map.palletteY -= 30
				if map.palletteY < -2240:
					map.palletteY = -2240
				map.drawSelected()

			elif  e.type == pygame.MOUSEBUTTONDOWN and e.button == 4:
				map.palletteY += 30
				if map.palletteY > 2:
					   map.palletteY = 2
				map.drawSelected()

			if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
				#Calls the function to save the game map as a .map file (using the key values
				#created in the Dictionary of the loaded images.
				map.saveMap()
			if e.type == pygame.QUIT:
				done = True



				"""The Menu/GUI stuff here is lowest priority, command line input
					is acceptable for now, if we have time to work on it."""

class menus(object):
	"""For all the GUI stuff here"""
	def __init__(self):
		pass

	def palletteMenu(self):
		pass

	def displayButtons(self):
		pass

	def buttonHitDetect(self):
		pass


"""Global Variables here!!"""
#Global Variables here!!
import pygame
import random   		#For later maybe
import time				#For later maybe
import glob	 			#For getting the .map files
import configparser
import numbers


eList = None
mapWinWidth = 1280
mapWinHeight = 704
cameraSpeed = 10
pygame.display.set_caption("Map Editor version 2.0")
screen=pygame.display.set_mode((1600,750))
gameSurf= pygame.Surface((mapWinWidth,mapWinHeight))
palletteSurf = pygame.Surface((266, 704))
pygame.display.init()
pygame.font.init()
done = False
db = TileDbase(".\\")

"""Begin Main program loop here!!"""
#Begin Main program loop here!!

map = Map()
map.startup()
map.buildPallette()

while done == False:
	screen.fill((128,0,0))
	#Creates the game map Surface
	screen.blit(gameSurf, (10,30))
	#Creates the Pallettte Surface
	screen.blit(palletteSurf, (1315,30))
	palletteSurf.fill((255,20,147))
	map.drawSelected()
	map.displayPallette()
	#menus.displayButtons()
	events.getPressed()
	events.checkKeys()
	events.checkMouse()
	map.displayMap()
	map.displayGrid()
   	#Flip to see the back buffer
	pygame.display.flip()
#Shutting Down
pygame.font.quit()
pygame.display.quit()