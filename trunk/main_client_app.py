import pygame
import random
import player
import GUIManager
import connection
import time
import math
import NewBullet
import world
import glob
import configparser


def generateRandomString(numChars):
	""" A utility function for generating random passwords or unames """
	s = ""
	for i in range(numChars):
		s += chr(random.choice(tuple(range(65,91)) + tuple(range(97,123))))
	return s




class Application(object):
	""" A collection of all game-related attributes
		and methods.  This class interacts with
		the client (which handles the networking) """
	def __init__(self):
		self.initialize()


###############################################################################
# Initialization and shutdown methods										 #
###############################################################################
	def initialize(self):
		""" Initializes all application-related (mostly pygame) attributes.
			   Does this by calling a bunch of "helper" methods """
		self.initConnection()
		self.initScreen()
		self.initClock()
		self.initFonts()
		self.initGUI()
		self.initGameObjects()


	def initConnection(self):
		self.connection = connection.Connection()

		# These attributes will be initialized when we connect to the server
		self.remoteIP = None	  # IP of the server
		self.remotePort = None  # Port the server is listening on


	def initScreen(self):
		pygame.display.init()
		self.screen = pygame.display.set_mode((1280,704))


	def initClock(self):
		self.clock = pygame.time.Clock()

	def initFonts(self):
		pygame.font.init()

	def initGUI(self):
		# Create self.guiManager
		self.GUIManager = GUIManager.GUIManager("title")
		font = pygame.font.Font("font\BlackCastle.ttf", 20)
		self.GUIManager.setFont(font)
		# All the Gui screens for the game


			#Title Screen
		self.GUIManager.createLabel(0, "title", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createButton(2, "title", (550, 300), pygame.image.load("GUIassets\\Login\\button_login_1.png"), pygame.image.load("GUIassets\\Login\\button_login_2.png"),  pygame.image.load("GUIassets\\Login\\button_login_3.png"), (0,255,0) )
		self.GUIManager.createButton(5, "title", (550, 375), pygame.image.load("GUIassets\\New_User\\button_newUser_1.png"), pygame.image.load("GUIassets\\New_User\\button_newUser_2.png"),  pygame.image.load("GUIassets\\New_User\\button_newUser_3.png"), (0,255,0) )

			#Login Screen
		self.GUIManager.createLabel(0, "login", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "login", (500, 250), "GUIassets\\gui_username.png", (0,255,0) )
		self.GUIManager.createLabel(0, "login", (500, 350), "GUIassets\\gui_password.png", (0,255,0) )
		self.GUIManager.createLabel(0, "login", (500, 450), "GUIassets\\gui_ipaddress.png", (0,255,0) )
		self.GUIManager.createTextEntry(0, "login", (510, 303), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextEntry(0, "login", (510, 403), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextEntry(0, "login", (510, 503), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createButton(16, "login", (560, 550), pygame.image.load("GUIassets\\Login\\button_login_1.png"), pygame.image.load("GUIassets\\Login\\button_login_2.png"),  pygame.image.load("GUIassets\\Login\\button_login_3.png"), (0,255,0) )
		self.GUIManager.createButton(-1, "login", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#Login fail
		self.GUIManager.createLabel(0, "login_failure", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "login_failure", (415, 250), "GUIassets\\gui_login_fail.png", (0,255,0) )
		self.GUIManager.createButton(2, "login_failure", (560, 550), pygame.image.load("GUIassets\\Ok\\button_ok_1.png"), pygame.image.load("GUIassets\\Ok\\button_ok_2.png"),  pygame.image.load("GUIassets\\OK\\button_ok_3.png"), (0,255,0) )
		self.GUIManager.createButton(-1, "login_failure", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#Login busy
		self.GUIManager.createLabel(0, "login_busy", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "login_busy", (415, 200), "GUIassets\\gui_login_busy.png", (0,255,0) )
		self.GUIManager.createButton(2, "login_busy", (560, 550), pygame.image.load("GUIassets\\Ok\\button_ok_1.png"), pygame.image.load("GUIassets\\Ok\\button_ok_2.png"),  pygame.image.load("GUIassets\\OK\\button_ok_3.png"), (0,255,0) )
		self.GUIManager.createButton(-1, "login_busy", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#New_user
		self.GUIManager.createLabel(0, "New_user", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "New_user", (500, 200), "GUIassets\\gui_username.png", (0,255,0) )
		self.GUIManager.createLabel(0, "New_user", (500, 300), "GUIassets\\gui_password.png", (0,255,0) )
		self.GUIManager.createLabel(0, "New_user", (500, 400), "GUIassets\\gui_confirm.png", (0,255,0) )
		self.GUIManager.createLabel(0, "New_user", (500, 500), "GUIassets\\gui_ipaddress.png", (0,255,0) )
		self.GUIManager.createTextEntry(0, "New_user", (510, 253), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextEntry(0, "New_user", (510, 353), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextEntry(0, "New_user", (510, 453), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextEntry(0, "New_user", (510, 553), 225, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createButton(17, "New_user", (560, 600), pygame.image.load("GUIassets\\Create\\button_create_1.png"), pygame.image.load("GUIassets\\Create\\button_create_2.png"),  pygame.image.load("GUIassets\\Create\\button_create_1.png"), (0,255,0) )
		self.GUIManager.createButton(12, "New_user", (200, 200), pygame.image.load("GUIassets\\Mage.png"),					pygame.image.load("GUIassets\\Mage.png"),					 pygame.image.load("GUIassets\\Mage.png"),					(0,255,0) )
		self.GUIManager.createButton(13, "New_user", (200, 500), pygame.image.load("GUIassets\\Cleric.png"),				  pygame.image.load("GUIassets\\Cleric.png"),				   pygame.image.load("GUIassets\\Cleric.png"),				  (0,255,0) )
		self.GUIManager.createButton(14, "New_user", (1000,200), pygame.image.load("GUIassets\\Thief.png"),				   pygame.image.load("GUIassets\\Thief.png"),					pygame.image.load("GUIassets\\Thief.png"),				   (0,255,0) )
		self.GUIManager.createButton(15, "New_user", (1000,500), pygame.image.load("GUIassets\\Warrior.png"),				 pygame.image.load("GUIassets\\Warrior.png"),				  pygame.image.load("GUIassets\\Warrior.png"),				 (0,255,0) )
		self.GUIManager.createButton(-1, "New_user", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#New User fail
		self.GUIManager.createLabel(0, "new_account_failure", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "new_account_failure", (415, 200), "GUIassets\\gui_new_user_fail.png", (0,255,0) )
		self.GUIManager.createButton(5, "new_account_failure", (560, 550), pygame.image.load("GUIassets\\Ok\\button_ok_1.png"), pygame.image.load("GUIassets\\Ok\\button_ok_2.png"),  pygame.image.load("GUIassets\\OK\\button_ok_3.png"), (0,255,0) )
		self.GUIManager.createButton(-1, "new_account_failure", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#New User busy
		self.GUIManager.createLabel(0, "new_account_busy", (0, 0), "GUIassets\\gui_title.png" , (0,255,0))
		self.GUIManager.createLabel(0, "new_account_busy", (415, 200), "GUIassets\\gui_new_user_busy.png", (0,255,0) )
		self.GUIManager.createButton(5, "new_account_busy", (560, 550), pygame.image.load("GUIassets\\Ok\\button_ok_1.png"), pygame.image.load("GUIassets\\Ok\\button_ok_2.png"),  pygame.image.load("GUIassets\\OK\\button_ok_3.png"), (0,255,0) )
		self.GUIManager.createButton(-1, "new_account_busy", (1150, 0), pygame.image.load("GUIassets\\Menu\\button_menu_1.png"), pygame.image.load("GUIassets\\Menu\\button_menu_2.png"),  pygame.image.load("GUIassets\\Menu\\button_menu_3.png"), (0,255,0) )

			#Game
		#self.GUIManager.createLabel(0, "Game", (960, 0), "GUIassets\\gui_inventory.png", (0,255,0) )
		self.GUIManager.createTextEntry(0, "Game", (0, 680), 500, self.GUIManager.font, (0,0,0), (255,255,255))
		self.GUIManager.createTextList(0,"Game",(0,450),500,self.GUIManager.font,50,(255,255,255), (255,255,255))

			#Credits
		self.GUIManager.createLabel(0, "credits", (0, 0), "GUIassets\\gui_title.jpg" , (0,255,0))
		self.GUIManager.createLabel(0, "credits", (200, 315), "GUIassets\\credits.png", (0,255,0) )


	def initGameObjects(self):
		self.gameState = "title"	 # 'title'
									 # 'new_account'
									 # 'new_account_waiting'
									 # 'new_account_failure'
									 # 'new_account_busy'
									 # 'login'
									 # 'login_waiting'
									 # 'login_failure'
									 # 'login_busy'
									 # 'Game'
									 # 'credits'
									 # 'quit'
		self.players = {}	   # A list of all player objects
								#	(including us)
		self.playerID = None # The key of our player within
							 #	self.players
		self.map = world.Zone()
		self.classstr = None


	def shutdown(self):
		self.gameState = "quit"
		self.shutdownConnection()
		pygame.font.quit()
		pygame.display.quit()

	def shutdownConnection(self):
		if self.remoteIP and self.remotePort:
			self.connection.sendMessage("<QUIT>", (self.remoteIP, self.remotePort), True)
		self.connection.kill()





###############################################################################
# Update methods															  #
###############################################################################
	def update(self):
		self.dT = self.clock.tick() / 1000.0

		self.updateGame(self.dT)
		self.updateGUI(self.dT)
		self.updateConnection(self.dT)

	def updateGame(self, dT):
		for idNum in self.players:
			self.map.cameraPos[0] = self.players[idNum].posX  - self.map.winWidth/2
			self.map.cameraPos[1] = self.players[idNum].posY - self.map.winHeight/2
			#self.map.collision((self.players[idNum].posX, self.players[idNum].posY))
			# New requirements for alternate scrolling:
			if self.map.cameraPos[0] < 0:								  self.map.cameraPos[0] = 0
			if self.map.cameraPos[0] >= self.map.world[2] - self.map.winWidth - 1:   self.map.cameraPos[0] = self.map.world[2] - self.map.winWidth - 1
			if self.map.cameraPos[1] < 0:								  self.map.cameraPos[1] = 0
			if self.map.cameraPos[1] >= self.map.world[3] - self.map.winHeight - 1: self.map.cameraPos[1] = self.map.world[3] - self.map.winHeight - 1
			if self.map.cameraPos[0] < 0: self.map.cameraPos[0] = 0 ##
			if self.map.cameraPos[1] < 0: self.map.cameraPos[1] = 0 ## fixes small map problems temporarily
			self.players[idNum].update(dT)
			#print(self.map.getTile(self.players[idNum].posX,self.players[idNum].posY))
			#print(self.players[idNum].posX,self.players[idNum].posY)
			self.map.tileCheck(self.players[idNum].posY, self.players[idNum].posX)
			temp = self.map.collision([self.players[idNum].posX, self.players[idNum].posY])

			if temp == 4:
				self.players[idNum].cur_health -= ( self.players[idNum].max_health/100 )
				if  self.players[idNum].cur_health < 0:
					 self.players[idNum].cur_health = 0
			if temp == 3:
				 self.players[idNum].vel_mag = 0.05
			else:
				 self.players[idNum].vel_mag =  1

	def updateGUI(self, dT):
		self.GUIManager.update(dT)

	def updateConnection(self, dT):
		# Update the client if we've connected to the server
		self.connection.update()

		if self.connection.getActive():
			# Get and handle new messages from the server
			self.handleServerMessages()

			# Check for dead server
			self.connection.checkForDeadConnection(self.remoteIP, self.remotePort)

			# See if the player has changed -- if so, send a message to the server
			if self.playerID in self.players:
				s = self.players[self.playerID].serialize(0)
				#(s)
				if s:
					self.connection.sendMessage("<UPDATE:" + s + ">", (self.remoteIP, self.remotePort), True)



##############################################################################
# Render methods															 #
##############################################################################
	def render(self, surf):
		if self.gameState == "quit":
			return

		surf.fill((125,125,125))   # Temporary!
		self.map.render(surf)
		self.renderGame(surf)
		self.renderGUI(surf)

		pygame.display.flip()

	def renderGame(self, surf):
		for idNum in self.players:
			self.players[idNum].render(surf, self.map.cameraPos)

	def renderGUI(self, surf):
		# Render the gui.  surf is the surface to draw to.
		self.GUIManager.render(surf)


###############################################################################
# Methods for communicating with the server									  #
###############################################################################
	def connectToServer(self, uname, passW, class_string, createAccount, remoteIP, remotePort):



		# Make sure we have a valid uname and password.
		if uname.count("<") or uname.count(">") or uname.count(":") or len(uname) >= 32:
			raise ValueError("uname must not contain '<', '>', or ':' and must be less than 32 characters")
		if passW.count("<") or passW.count(">") or passW.count(":") or len(passW) >= 32:
			raise ValueError("passW name must not contain '<', '>', or ':' and must be less than 32 characters")

		# Save the remote IP/port
		self.remoteIP = remoteIP	  # IP of the server
		self.remotePort = remotePort  # Port the server is listening on

		# Set our state and the initial message to send to the server
		if createAccount:
			initialMessage = "<NEW_ACCOUNT:uname=" + uname + ":pass=" + passW + ":class=" + class_string + ">"
		else:
			initialMessage = "<LOGIN:uname=" + uname + ":pass=" + passW + ">"

		# Connect to the server and send our initial message
		if not self.connection.hasSocket():
		  print("Creating socket.")
		  self.connection.createSocket(random.randint(10000,49999))




		# See if we were given a remoteIP -- if not assume we're looking for a local server
		if remoteIP == "":
			self.remoteIP = self.connection.getLocalIP()
		else:
			self.remoteIP = remoteIP

		print("Connecting to server...remoteIP=" + self.remoteIP + ", remotePort=" + str(self.remotePort))

		# Save our user name, pass, class_string
		self.uname = uname
		self.password = passW
		self.class_string = class_string
		#self.playerID = player_ID

		# Send the initial message to the server
		print("Sending '" + initialMessage + "'")
		self.connection.sendMessage(initialMessage, (self.remoteIP, self.remotePort), True)

		# Start doing dead-server checks
		self.connection.setPingEnable(True)

	def handleServerMessages(self):
		""" Gets and handles new messages from the server. """
		msgList = self.connection.getNewMessages()
		for item in msgList:
			newMsg, remoteAddr = item
			self.connection.logMessage("Processing message '" + newMsg + "'", 5)
			opcode = newMsg.split(":")[0]

			if opcode == "NEW_ACCOUNT_ACK":
				rv = self.__processNewAccountMsg(newMsg)
				if rv != 0:
					self.connectionState = "quit"
			elif opcode == "LOGIN_ACK":
				rv = self.__processLoginMsg(newMsg)
				if rv != 0:
					self.connectionState = "quit"
			elif opcode == "FULL_UPDATE_ACK":
				rv = self.__processFullUpdateMsg(newMsg)
			elif opcode == "HEARTBEAT":
				self.__processHeartbeatMsg(newMsg)
			elif opcode == "PLAYER_JOINED":
				self.__processPlayerJoinedMsg(newMsg)
			elif opcode == "PLAYER_LEFT":
				self.__processPlayerLeftMsg(newMsg)
			elif opcode == "PING":
				self.__processPingMsg(newMsg)
			elif opcode == "PING_ACK":
				pass	# Don't need to do anything -- the connection should have updated it's time-since-last message value.
			elif opcode == "QUIT_ACK":
				self.__processQuitAckMsg(newMsg)
			elif opcode == "CHAT":
				self.__processChatMsg(newMsg)
			else:
				raise ValueError("Unhandled opcode '" + opcode + "'")

	def __processChatMsg(self, msg):
		print("ChatMsg has been sent and recieved")
		"""Handles Chat message from the Server"""
		unameS = msg.split(":")[2].split("=")[1] + ": "
		msgS = msg.split(":")[1].split("=")[1]
		#print(msgS)
		self.GUIManager.elementCategories["Game"][1].addTextdraw(unameS + msgS)


	def __processNewAccountMsg(self, msg):
		""" Process a NEW_ACCOUNT_ACK message """
		# See if the server accepted this uname / password pair
		self.connection.logMessage("handling NEW_ACCOUNT_ACK msg", 1)
		me = msg.split(":")

		if len(me) == 3 and me[1].find("=") > 0 and me[1].find("=") == len(me[1])-2:
			response = me[1].split("=")[1]
			idNum= me[2].split("=")[1]
			self.connection.setID(idNum)
		else:
			self.connection.logMessage("Corrupt NEW_ACCOUNT_ACK message from server.", 1)
			return 3

		self.getNewAccountResponse(response, idNum)

		if response == "T":
			pass
			  #Now, actually attempt to log-in
			self.connection.sendMessage("<LOGIN:uname=" + self.uname + ":pass=" + self.password + ":class=" + self.class_string + ">", (self.remoteIP, self.remotePort), True)
			return 0
		else:
			return 100

	def __processLoginMsg(self, msg):
		""" Process a LOGIN_ACK message """
		# See if the server accepted this uname
		self.connection.logMessage("handling LOGIN_MSG msg", 1)
		me = msg.split(":")
		if len(me) < 2 or me[1].find("=") < 0 or me[1].find("=") != len(me[1])-2:
			self.connection.logMessage("Corrupt LOGIN_ACK message from server.", 1)
			return 3
		response = me[1].split("=")[1]
		if response == "F":
			self.connection.logMessage("Incorrect uname and/or password", 1)
			self.getLoginResponse("F")
			return 100
		elif response == "B":
			self.connection.logMessage("Server is busy -- check again later")
			self.getLoginResponse("B")
			return 101
		if len(me) < 3 or me[2].find("=") != 2 or len(me[2]) <= 3:
			self.connection.logMessage("Corrupt LOGIN_ACK message from server.", 1)
			return 5
		else:
			# Get the ID number.  Set our connection ID# and playerID number to this value
			idNum = int(me[2].split("=")[1])
			serialStr = ""
			for i in range(3, len(me)):
				if i > 3:
					serialStr += ":"
				serialStr += me[i]
			self.getLoginResponse("T", idNum, serialStr)
			self.connection.setID(idNum)

		# Ask the server for a full update
		self.connection.sendMessage("<FULL_UPDATE>", (self.remoteIP, self.remotePort), True)

		return 0

	def __processFullUpdateMsg(self, msg):
		""" Process a full update of everything in the game. """
		self.connection.logMessage("Processing FULL_UPDATE_ACK msg '" + msg + "'", 3)
		# Create and initialize the player and any existing players
		me = msg.split(":")
		serializeStr = ""
		idNum = None
		playerData = {}
		includedPlayers = []
		for i in range(1, len(me)):
			if me[i][:3] == "ID=":
				if serializeStr != "":
					playerData[idNum] = serializeStr
					serializeStr = ""
				#if me[i][] ==
				idNum = int(me[i].split("=")[1])
				includedPlayers.append(idNum)
			else:
				if len(serializeStr) > 0:
					serializeStr += ":"
				serializeStr += me[i]
		if serializeStr != "":
			playerData[idNum] = serializeStr

		self.getFullUpdateResponse(playerData, None)

		return 0


	def __processHeartbeatMsg(self, msg):
		""" Process some kind of data from the server. """
		self.connection.logMessage("Processing HEARTBEAT msg '" + msg + "'", 4)
		me = msg.split(":")
		curPlayerID = None
		curSerialStr = ""
		playerData = {}
		for i in range(1, len(me)):
			if me[i][:3] == "ID=" and len(me[i]) > 3:
				if curPlayerID != None:
					playerData[curPlayerID] = curSerialStr
					curSerialStr = ""
				curPlayerID = int(me[i][3:])
			else:
				if len(curSerialStr) > 0:
					curSerialStr += ":"
				curSerialStr += me[i]
		playerData[curPlayerID] = curSerialStr

		self.getUpdateResponse(playerData, None)

	def __processPlayerJoinedMsg(self, msg):
		""" A new player has joined the game.  This message should include a serialized string for that player. """
		self.connection.logMessage("Processing PLAYER_JOINED msg", 2)
		me = msg.split(":")
		IDnum = None
		serialStr = ""
		for i in range(1, len(me)):
			if me[i][:3] == "ID=":
				if IDnum != None and IDnum != self.connection.getID():
					self.gotPlayerJoinedResponse(IDnum, serialStr)
					serialStr = ""
				IDnum = int(me[i].split("=")[1])
			else:
				if serialStr != "":
					serialStr += ":"
				serialStr += me[i]
		if IDnum != None and IDnum != self.connection.getID():
			self.getPlayerJoinedResponse(IDnum, serialStr)


	def __processPlayerLeftMsg(self, msg):
		""" A player has dropped out.  Remove them from our players list. """
		self.connection.logMessage("Processing PLAYER_LEFT msg", 2)
		me = msg.split(":")
		if len(me) == 2 and len(me[1]) > 3 and me[1].find("=") == 2:
			idNum = int(me[1].split("=")[1])
			self.getPlayerLeftResponse(idNum)
		else:
			self.connection.logMessage("Corrupt PLAYER_LEFT message", 2)


	def __processPingMsg(self, msg):
		self.connection.logMessage("Processing PING msg -- sending to " + self.remoteIP + ":" + str(self.remotePort), 2)
		self.connection.sendMessage("<PING_ACK>", (self.remoteIP, self.remotePort), True)


	def __processQuitAckMsg(self, msg):
		self.connection.logMessage("Processing QUIT_ACK msg", 0)
		self.connection.kill()
		self.connectionState = "quit"

	def getUpdates(self):
		""" This function is called by the client object.  We need to return
			a string indicating if the player has changed state.  If not,
			return an empty string.  If it has, call the serialize method of
			the player (passing a 0) and return the string """
		if self.playerID != None:
			return self.players[self.playerID].serialize(0)
		return ""

	def getNewAccountResponse(self, response, idNum=None, serialStr=""):
		""" Called when we receive a response to our attempt to create a new
			account on the server.  response should be one of:
				T:   The server accepted this.  The new account exists now.
					 The client has also sent a login message as well.
				F:   The server denied the new account (usually b/c uname exists)
				B:   The server is busy right now
 	"""
		if response == "T":
			self.playerID = idNum
			self.players[idNum] = player.Player("herp", "Cleric")
			self.players[idNum].deserialize(serialStr)

			self.gameState = "Game"
			self.GUIManager.currentGroup = self.gameState
			# Turn on 'game' GUI\

		if response == "F":
			self.gameState = "new_account_failure"
			self.GUIManager.currentGroup = self.gameState

		if response == "B":
			self.gameState = "new_account_busy"
			self.GUIManager.currentGroup = self.gameState
		pass

	def getLoginResponse(self, response, idNum=None, serialStr=""):
		""" Called when we receive a response to our attempt to log in
			to the server.  response should be one of:
				T:   The server accepted this.  The new account exists now.
						The client has also sent a full update message as well.
						The idNum parameter indicates our player's ID number.
						serialStr is a string to pass to the player's deserialize
						method.
				F:   The server denied the new account (usually b/c uname
						and passW don't match, or uname doesn't exist)
				B:   The server is busy right now
		"""
		if response == "T":
			self.playerID = idNum
			self.players[idNum] = player.Player("herp", "Cleric")
			self.players[idNum].deserialize(serialStr)
			self.gameState = "Game"
			self.GUIManager.currentGroup = self.gameState
			# Turn on 'game' GUI\

		if response == "F":
			self.gameState = "login_failure"
			self.GUIManager.currentGroup = self.gameState

		if response == "B":
			self.gameState = "login_waiting"
			self.GUIManager.currentGroup = self.gameState



	def getFullUpdateResponse(self, playerDictionary, worldDictionary):
		""" Gets a full update from the server (which should contain the
			state of all other players, the state of the environment, etc.
			playerDictionary has keys for each player's ID# (including our own);
			the value is a string we can pass to deserialize.
			worldDictionary..."""
		includedPlayers = []
		playersToDelete = []

		for idNum in playerDictionary:
			includedPlayers.append(idNum)
			if idNum not in self.players:
				self.players[idNum] = player.Player("???")
				self.players[idNum].deserialize(playerDictionary[idNum])
			elif idNum != self.playerID:
				# This isn't us.  Update our local copy.
				self.players[idNum].deserialize(playerDictionary[idNum])
			else:
				sstr = self.players[idNum].deserialize(playerDictionary[idNum])
				if sstr:
					self.connection.sendMessage("<UPDATE:" + sstr + ">", (self.remoteIP, self.remotePort), True)
		for idNum in self.players:
			if idNum not in includedPlayers:
				playersToDelete.append(idNum)
		for idNum in playersToDelete:
			self.getPlayerLeftResponse(idNum)

	def getUpdateResponse(self, playerDictionary, worldDictionary):
		""" Gets some kind of incremental update from the server.  The
			format is very similar to getFullUpdateResponse, but we don't
			get info on all players / world-data, so only do an update. """
		for idNum in playerDictionary:
			if idNum in self.players:
				self.players[idNum].deserialize(playerDictionary[idNum])


	def getPlayerJoinedResponse(self, ID, serialStr):
		if ID not in self.players:
			self.players[ID] = player.Player("???", "???")
			self.players[ID].deserialize(serialStr)

	def getPlayerLeftResponse(self, ID):
		if ID in self.players:
			del self.players[ID]

	def getQuitResponse(self):
		self.shutdown()






###############################################################################
# Methods for dealing with input											  #
###############################################################################
	def processInput(self):
		if self.gameState == "quit":
			return
		eList = pygame.event.get()
		for e in eList:
			if e.type == pygame.QUIT:
				self.shutdown()
				return
			elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
				self.keyMessage(e.type, e.key, e.mod)
			elif e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
				self.mouseMessage(e.type, e.button, e.pos)
			elif e.type == pygame.MOUSEMOTION:
				self.mouseMessage(e.type, None, e.pos)


	def keyMessage(self, eventType, keyCode, mod):

		if eventType == pygame.KEYDOWN:
			if keyCode == pygame.K_ESCAPE:
				self.shutdown()
				return
			if self.playerID != None and self.playerID in self.players:
				if keyCode == pygame.K_LEFT:
					self.players[self.playerID].setMove(horiz="Left")
					self.players[self.playerID].walkdir =  7
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_RIGHT:
					self.players[self.playerID].setMove(horiz="Right")
					self.players[self.playerID].walkdir =  3
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_UP:
					self.players[self.playerID].setMove(vert="Up")
					self.players[self.playerID].walkdir =  1
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_DOWN:
					self.players[self.playerID].setMove(vert="Down")
					self.players[self.playerID].walkdir =  5
					self.players[self.playerID].p_state = 1
				if keyCode == pygame.K_UP and keyCode == pygame.K_LEFT:
					self.players[self.playerID].setMove(vert="Up")
					self.players[self.playerID].setMove(horiz="Left")
					self.players[self.playerID].walkdir =  8
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_UP and keyCode == pygame.K_RIGHT:
					self.players[self.playerID].setMove(vert="Up")
					self.players[self.playerID].setMove(horiz="Right")
					self.players[self.playerID].walkdir =  2
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_DOWN and keyCode == pygame.K_LEFT:
					self.players[self.playerID].setMove(vert="Down")
					self.players[self.playerID].setMove(horiz="Left")
					self.players[self.playerID].walkdir =  6
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_DOWN and keyCode == pygame.K_RIGHT:
					self.players[self.playerID].setMove(vert="Down")
					self.players[self.playerID].setMove(horiz="Right")
					self.players[self.playerID].walkdir =  4
					self.players[self.playerID].p_state = 1
				elif keyCode == pygame.K_SPACE:
					self.players[self.playerID].active = True
				elif keyCode == pygame.K_RETURN and self.gameState == "Game":
					msg = ("<CHAT:msg=" + str(self.GUIManager.elementCategories["Game"][0].current_str) + ":uname=" + self.uname + ">")
					self.connection.sendMessage(msg, (self.remoteIP, self.remotePort), True)
		elif eventType == pygame.KEYUP:
			if self.playerID != None and self.playerID in self.players:
				if keyCode == pygame.K_LEFT or keyCode == pygame.K_RIGHT:

					self.players[self.playerID].setMove(horiz="-")
					self.players[self.playerID].p_state = 0
					#self.connection.sendMessage("<UPDATE:hmove=->", (self.remoteIP, self.remotePort), True)
				elif keyCode == pygame.K_UP or keyCode == pygame.K_DOWN:

					self.players[self.playerID].setMove(vert="-")
					self.players[self.playerID].p_state = 0
					#self.connection.sendMessage("<UPDATE:vmove=->", (self.remoteIP, self.remotePort), True)
				elif keyCode == pygame.K_SPACE:
					self.players[self.playerID].active = False
		# Notify guiManager of key presses
		self.GUIManager.onKeyEvent(eventType, keyCode, mod)

	def mouseMessage(self, eventType, button, pos):
		hitId = self.GUIManager.onMouse(eventType, button, pos)
		if eventType == pygame.MOUSEBUTTONDOWN:
			# Notify guiManager of mouse presses
			#hitId = None
			#bullet = player.Player.bullet
			#tempStr = "bullet="
			#tempStr += ":x=" + str(bullet[0][0]) + ":y=" + str(bullet[0][1]) + ":Angle=" + str(bullet[1])
			#self.connection.sendMessage("<UPDATE:bullet=" + tempStr + ">")
			if hitId == -1:
				"""To title"""
				self.gameState = "title"
			elif hitId == 1:
				"""To quit"""
				self.gameState = "quit"

			elif hitId == 2:
				"""To go to login in screen"""
				print("Going to login")
				self.gameState = "login"

			elif hitId == 3:
				"""To go to fail screen for username/password/IP"""
				self.gameState = "login_failure"

			elif hitId == 4:
				"""To go to fail screen for busy server"""
				self.gameState = "login_busy"

			elif hitId == 5:
				"""To go to new user screen"""
				self.gameState = "New_user"

			elif hitId == 6:
				"""To go to new user screen for fail in username/password/IP"""
				self.gameState = "new_account_failure"

			elif hitId == 7:
				"""To go to new user screen fail for busy server"""
				self.gameState = "new_account_busy"

			elif hitId == 8:
				"""To go to the game screen"""
				self.gameState = "Game"

			elif hitId == 9:
				"""To quit and a gameover maybe"""
				self.gameState = "game_over"

			elif hitId == 10:
				"""To the credits screen"""
				self.gameState = "credits"

			elif hitId == 11:
				self.gameState = "start_menu"


			elif hitId == 12:
				"""Used to select the class for new user-Mage"""
				self.classstr = "Mage"

			elif hitId == 13:
				"""Used to select the class for new user-Cleric"""
				self.classstr = "Cleric"
				#print(self.classstr)

			elif hitId == 14:
				"""Used to select the class for new user-Thief"""
				self.classstr = "Thief"

			elif hitId == 15:
				"""Used to select the class for new user-Warrior"""
				self.classstr = "Warrior"

			elif hitId == 16:
				"""To pass the login info for the server"""
				print("Calling connectToServer")
				self.connectToServer(self.GUIManager.elementCategories["login"][4].current_str, self.GUIManager.elementCategories["login"][5].current_str, self.classstr, False, self.GUIManager.elementCategories["login"][6].current_str, 50000)

			elif hitId == 17:
				"""Checking new users and passing that to the server to get to get the game state"""
				if self.GUIManager.elementCategories["New_user"][6].current_str == self.GUIManager.elementCategories["New_user"][7].current_str:
					self.connectToServer(self.GUIManager.elementCategories["New_user"][5].current_str, self.GUIManager.elementCategories["New_user"][6].current_str, self.classstr, True, self.GUIManager.elementCategories["New_user"][8].current_str, 50000)
				else:
					self.gameState = "new_account_failure"
			self.GUIManager.currentGroup = self.gameState

###############################################################################
# Main loop																   #
###############################################################################
	def main(self):
		while True:
			#if self.gameState == "quit" or self.client.connectionState == "quit":
			#	print(self.gameState, self.client.connectionState)
			if self.gameState == "quit" and self.connection.getActive() == False:
				break

			if self.gameState != "quit":
				self.processInput()

			self.update()

			self.render(self.screen)







# Main program
# ============
#  This is temporary until the GUI teams does this in pygame.
#loginMode = "cmd_line"
#loginMode = "legit"
loginMode = "testing"

if loginMode == "cmd_line":
	# Get options from the command line
	if len(sys.argv) < 4:
		print("Usage: client.py uname pass remoteIP [create]")
	uname = sys.argv[1]
	passW = sys.argv[2]
	remoteIP = sys.argv[3]

	createAccount = False
	if len(sys.argv) >= 5 and sys.argv[4].lower() == "create":
		createAccount = True
elif loginMode == "prompt":
	isNew = input("Create new account? (y/n) ").lower()
	if isNew == "y":
		createAccount = True
	elif isNew == "n":
		createAccount = False
	else:
		raise ValueError("You must enter a 'y' or a 'n'")

	uname = input("User name (Press Enter for random): ")
	passW = input("Password (Press Enter for random): ")
	remoteIP = input("Server IP (in the form 206.21.94.143) (Enter for local): ")
	if remoteIP != "":
		if remoteIP.count(".") != 3:
			raise ValueError("Invalid IP address")
		elem = remoteIP.split(".")
		for e in elem:
			if not e.isnumeric():
				raise ValueError("Invalid IP component '" + e + "'")
elif loginMode == "testing":
	uname = ""
	passW = ""
	remoteIP = ""
	createAccount = True



C = Application()
#C.update()
C.renderGUI(C.screen)
#C.connectToServer(uname, passW, createAccount, remoteIP)
C.main()
#C.shutdown()


