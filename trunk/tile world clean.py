import pygame
import configparser
import glob
class TileDbase(object):
	def __init__(self,path):
		self.dBase = {}
		config = configparser.ConfigParser()
		fList=[]
		fList.append(glob.glob(path+"*.con"))
		for name in fList:
			config.read(name)
			for section in config.sections():
				desc = dict(config.items(section))
				self.dBase[section] = desc
	def collide(self, tileCode):
		if(self.dBase[tileCode]['block'] == 'True'):
			return True
		else:
			return False

class OverlayDbase(object):
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


def load_tile_table(filename='dc-dngn'):
		image = pygame.image.load(filename+".png").convert_alpha()  # change to .png
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, int(image_width/tileSize)):
			line = []
			tile_table.append(line)
			for tile_y in range(0, int(image_height/tileSize)):
				rect = (tile_x*tileSize, tile_y*tileSize,tileSize, tileSize)
				line.append(image.subsurface(rect))
		return tile_table

def DrawingCode(LevelMap):
	# 1. Figure out which tile the camera is in and how much we're "into" that tile
	tileX = int(cameraPos[0]) // tileSize
	tileY = int(cameraPos[1]) // tileSize
	offsetX = int(cameraPos[0]) % tileSize
	offsetY = int(cameraPos[1]) % tileSize
	# 2. Figure out how many tiles we need to draw
	drawX = winWidth // tileSize + 2
	drawY = winHeight // tileSize + 2
	# 3. Draw that section of the TileKeys
##	if world[1]*tileSize < winHeight:
##		y = int(winHeight/2 - world[3]/2)
##	else:
	y = -offsetY
	tiles = load_tile_table()
	for row in range(tileY, tileY + drawY):
##		if world[0]*tileSize < winWidth:
##			x = int(winWidth/2 - world[2]/2)
##		else:
		x = -offsetX
		for col in range(tileX, tileX + drawX):
			if col < world[0] and row < world[1]:
				tileCode = tlist[row][col]
				tile = db.dBase[tileCode]['tile'].split(',')
				tile = int(tile[0]),int(tile[1])
				tileImg = tiles[tile[0]][tile[1]]
				screen.blit(tileImg, (x,y))
			x += tileSize
		y += tileSize


def MapChanger(mapConf,LevelMap):
	playerPos[0] = 50
	playerPos[1] = 50

	mapConf.read(LevelMap)
	TileKeys = mapConf.get("level","map").split("\n")
	for line in TileKeys:
		temp_row = []
		for i in range(0,len(line),3):
			temp_row.append(line[i:i+3])
		tlist.append(temp_row)
	# Calculate the size of the world in tiles and pixels
	world_tileWidth = len(TileKeys[0])/3
	world_tileHeight = len(TileKeys)
	world_pixelWidth = world_tileWidth * tileSize
	world_pixelHeight = world_tileHeight * tileSize
	return [world_tileWidth, world_tileHeight, world_pixelWidth, world_pixelHeight]
	# Create the (giant) background surface


def tileCheck(playerY, playerX):
	playerY = int(playerY)
	playerX = int(playerX)


	tCheck[0] = (tlist[(playerY // tileSize) - 1][(playerX // tileSize)])  #up
	tCheck[2] = (tlist[(playerY // tileSize)][(playerX // tileSize) - 1])  #left
	tCheck[1] = (tlist[(playerY // tileSize) + 1][(playerX // tileSize)])  #down
	tCheck[3] = (tlist[(playerY // tileSize)][(playerX // tileSize) + 1])  #right
	tCheck[4] = (tlist[(playerY // tileSize) + 1][(playerX // tileSize) - 1]) #down-left
	tCheck[5] = (tlist[(playerY // tileSize) + 1][(playerX // tileSize) + 1]) #down-right
	tCheck[6] = (tlist[(playerY // tileSize) - 1][(playerX // tileSize) -1]) #up-left
	tCheck[7] = (tlist[(playerY // tileSize) - 1][(playerX // tileSize) + 1]) #up-right


def collision():
	playerX = int(playerPos[0])
	playerY = int(playerPos[1])
	playerRad = 10
	tX = (int(playerX) // tileSize) * tileSize
	tY = (int(playerY) // tileSize) * tileSize

	collide = db.collide(tCheck[2]) #collision check left
	tX -= tileSize
	if collide & ((playerX - playerRad - 3) <= tX + tileSize):
		playerPos[0]= tX + tileSize + playerRad + 3
	tX = (int(playerX) // tileSize) * tileSize

	collide = db.collide(tCheck[3]) #collision check right
	tX += tileSize
	if collide & ((playerX + playerRad + 3) >= tX):
		playerPos[0] = tX - playerRad - 3
	tX = (int(playerX) // tileSize) * tileSize

	collide = db.collide(tCheck[0]) # colission check up
	if collide & ((playerY - playerRad - 3) <= tY):
		playerPos[1] = tY + playerRad + 3
	tY = (int(playerY) // tileSize) * tileSize

	collide = db.collide(tCheck[1]) # colission check down
	tY += tileSize
	if collide & ((playerY + playerRad +3) >= tY):
		playerPos[1] = tY - playerRad - 3
	tY = (int(playerY) // tileSize) * tileSize

	collide = db.collide(tCheck[4]) #colission check down-left
	tX -= tileSize
	tY += tileSize
	if collide & ((playerX - playerRad) <= tX + tileSize -7) & ((playerY + playerRad - 7) >= tY):
		playerPos[0]= tX - 3 + tileSize
		playerPos[1]= tY - 3
	tX = (int(playerX) // tileSize) * tileSize
	tY = (int(playerY) // tileSize) * tileSize


	collide = db.collide(tCheck[5]) #colission check down-right
	tX += tileSize
	tY += tileSize
	if collide & ((playerX + playerRad) >= tX + 7) & ((playerY + playerRad -7) >= tY):
		playerPos[0]= tX + 3
		playerPos[1]= tY - 3
	tX = (int(playerX) // tileSize) * tileSize
	tY = (int(playerY) // tileSize) * tileSize

	collide = db.collide(tCheck[6]) #collision check up-left
	if collide & ((playerX - playerRad) <= tX - 7) & ((playerY - playerRad + 7) <= tY):
		playerPos[0]= tX - 3
		playerPos[1]= tY + 3
	tX = (int(playerX) // tileSize) * tileSize
	tY = (int(playerY) // tileSize) * tileSize

	collide = db.collide(tCheck[7]) #collision check up-right
	tX += tileSize
	if collide & ((playerX + playerRad) >= tX + 7) & ((playerY - playerRad +7) <= tY):
		playerPos[0]= tX + 3
		playerPos[1]= tY + 3
	tX = (int(playerX) // tileSize) * tileSize
	tY = (int(playerY) // tileSize) * tileSize

def OverlayDraw(x,y):
	for name in odb.dBase:

		path = db.dBase[name]['name']
		pos = db.dBase[name]['pos'].split(',')
		pos = int(pos[0])+x,int(pos[1])+y
		img = pygame.image.load(path).convert_alpha()
		screen.blit(img, pos)

###############
# world / pygame inits
###############
winWidth = 1280
winHeight = 704
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((winWidth,winHeight))
done = False
playerPos = [winWidth/2, winHeight/2]
db = TileDbase(".\\")
odb = OverlayDbase(".\\")
# Set the tile size
tileSize = 32
cameraPos = [0,0]
cameraSpeed = 8
# Collision detection list
tCheck = [0,0,0,0,0,0,0,0]




###############
# testing
#troll = pygame.image.load('files_troll_2.png')


###############
# map loading
###############
tlist = []
TileKeys = []
mapConf = configparser.ConfigParser()

LevelMap = "level.map"
world = MapChanger(mapConf,LevelMap)#chris  Wren's flash drive file


while not done:

	# Erase the old screen
	screen.fill((0,0,0))
	#screen.blit(troll,(200,200))


	# Update variables
	cameraPos[0] = playerPos[0] - winWidth/2
	cameraPos[1] = playerPos[1] - winHeight/2
	# New requirements for alternate scrolling:
	if cameraPos[0] < 0:								  cameraPos[0] = 0
	if cameraPos[0] >= world[2] - winWidth - 1:   cameraPos[0] = world[2] - winWidth - 1
	if cameraPos[1] < 0:								  cameraPos[1] = 0
	if cameraPos[1] >= world[3] - winHeight - 1: cameraPos[1] = world[3] - winHeight - 1
	if cameraPos[0] < 0: cameraPos[0] = 0 ##
	if cameraPos[1] < 0: cameraPos[1] = 0 ## fixes small map problems temporarily


	#screen.blit(troll,(-cameraPos[0], -cameraPos[1])) # PLACES IMAGES "PERM" on map
	# -cameraPos[0] + X and -cameraPos[1] + Y : x & y represent the x and y pos of the uper left corner
	# of the image in respect to its position in the world (by pixel)

	# Draw the level
	DrawingCode(LevelMap)

	# Check each tile around player for collision checks
	tileCheck(playerPos[1],playerPos[0])

	#Collision detection
	collision()

	# Get user input
	pygame.event.pump()
	pressedList = pygame.key.get_pressed()
	if pressedList[pygame.K_ESCAPE]:
		done = True
	if pressedList[pygame.K_LEFT]:
		playerPos[0] -= cameraSpeed
	if pressedList[pygame.K_RIGHT]:
		playerPos[0] += cameraSpeed
	if pressedList[pygame.K_UP]:
		playerPos[1] -= cameraSpeed
	if pressedList[pygame.K_DOWN]:
		playerPos[1] += cameraSpeed
	if pressedList[pygame.K_1]:
		tlist = []
		LevelMap = "level1.map"
##		playerPos[0] = 50
##		playerPos[1] = 50
		world = MapChanger(mapConf,LevelMap)
	if pressedList[pygame.K_2]:
		tlist = []
		LevelMap = "level2.map"
		world = MapChanger(mapConf,LevelMap)
	if pressedList[pygame.K_0]:
		tlist = []
		LevelMap = "level.map"
		world = MapChanger(mapConf,LevelMap)


	pygame.draw.circle(screen, (128,128,128), (int(playerPos[0] - cameraPos[0]), int(playerPos[1] - cameraPos[1])), 10, 0)
	OverlayDraw(-cameraPos[0],-cameraPos[1])

	pygame.display.flip()

pygame.font.quit()
pygame.display.quit()