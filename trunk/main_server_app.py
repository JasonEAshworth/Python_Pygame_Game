import socket
import threading
import time
import player
import connection
import pygame


# Trying in pyscripter:
# X. Tabs to spaces off
# 2. Trim trailing spaces off
# 3. Smart tabs off
# 4. Un-tabify all source code.
# X. Tabify all source code.
# X. Turn off auto-indent

class ClientInfo(object):
	""" Just a simple class for holding all info about a single
		client connection. """
	ipIndex = {}	# Key="x.y.z.w:port"   Value=ConnectionInfo object

	def __init__(self, ID, addr):
		""" Constructor """
		self.ID = ID
		self.addr = addr
		self.ping_timer = 0.0
		self.recv_timer = 0.0
		self.recv_count = 0
		self.send_count = 0

		ClientInfo.ipIndex[addr[0] + ":" + str(addr[1])] = self

	def __del__(self):
		""" Destructor """
		del ClientInfo.ipIndex[self.addr[0] + ":" + str(self.addr[1])]






class Server(object):
	""" Contains the 'master' list of all player objects.  Updates the
		simulation (if any), and periodically sends "heartbeat" packets to
		all connected players.  A heartbeat contains all data in the game. """
	maxDelay = 4.0	  # The maximum time (in seconds) until a ping message is
						#   sent -- if we pass this the connection is in the
						#   "possibly-dead" state.  If 2 * this time pass
						#   without a message, the client is considered "dead"
						#   and is removed.
	pingFrequency = 0.5 # The time between pings if a client is in the
						#   "possibly-dead" state
	def __init__(self, maxPlayers, myPort):
		""" maxPlayers is the maximum number of players we'll allow.
			myPort is the socket port# """
		# Server attributes
		self.maxPlayers = maxPlayers

		# "Tweak" values the control operations on the server
		self.heartbeatTimer = 0.0
		self.heartbeatCounter = 0
		self.heartbeatFreq = 0.5

		# A list of ID,msg,addr tuples.  We'll process this in our 'main' loop
		self.pendingMessages = []

		# The database -- when a client joins / leaves this will be synced
		self.dbase = {}	   # Key=uname; Value=string of data
		self.dbase_fname = "dbase.dat"

		# Information on connected clients
		self.clientNextID = 0
		self.clients = {}		  # Key=ID#, Value=ClientInfo

		# All game data we want to represent on the server goes here...
		self.players = {}			 # The player objects

		# The thread responsible for listening for data
		self.connection = connection.Connection()
		self.connection.createSocket(myPort)



###############################################################################
# Methods for loading/saving/updating the database of users				   #
###############################################################################
	def loadDBase(self):
		""" Loads the database file from disk """
		self.dbase = {}
		fp = open(self.dbase_fname, "r")
		for line in fp:
			line = line.strip()
			lineElem = line.split(":")
			uname = lineElem[0].split("=")[1]
			self.dbase[uname] = line
		fp.close()

	def addToDBase(self, newPlayer, newPassword):
		""" Adds an entry to the database and saves the file. """
		self.dbase[newPlayer.uname] = newPlayer.serialize(3, False) + \
					":pass=" + newPassword

	def updateDBase(self, playerObj):
		""" Updates the entry in the database matching this uname. """
		if playerObj.uname in self.dbase:
			curLine = self.dbase[playerObj.uname]
			passW = curLine[curLine.rfind(":")+1:].split("=")[1]
			curLine = playerObj.serialize(3, False) + ":pass=" + passW
			self.dbase[playerObj.uname] = curLine
		else:
			self.connection.logMessage("User '" + playerObj.uname + \
						"' doesn't exist in the database -- can't update!", 2)

	def saveDBase(self):
		""" Writes self.dbase out to the file. """
		fp = open(self.dbase_fname, "w")
		for uname in self.dbase:
			line = self.dbase[uname]
			fp.write(line + "\n")
		fp.close()


###############################################################################
# Miscellaneous methods													   #
###############################################################################
	def findByAddr(self, addr):
		""" Find a ClientInfo by address (ip-addr, port).
			Returns None if not found """
		addrStr = addr[0] + ":" + str(addr[1])
		if addrStr in ClientInfo.ipIndex:
			return ClientInfo.ipIndex[addrStr]
		else:
			return None




###############################################################################
# Methods for processing data **FROM** the client(s)						  #
###############################################################################
	def getNewMessages(self):
		# Get new messages from connection
		newMsgs = self.connection.getNewMessages()

		for item in newMsgs:
			msg, addr = item

			# See if we need to add this to our map of connections
			if self.findByAddr(addr) == None:
				cinfo = ClientInfo(self.clientNextID, addr)
				self.clients[self.clientNextID] = cinfo
				self.clientNextID += 1
				self.connection.logMessage("Creating new cinfo structure", 1)
			else:
				cinfo = self.findByAddr(addr)
				self.connection.logMessage("Using old cinfo structure", 1)

			cinfo.recv_timer = time.time()
			cinfo.recv_count += 1

			self.pendingMessages.append([cinfo.ID, msg, cinfo.addr])


	def processPendingData(self):
		""" Pulls any waiting data from self.pendingMessages and calls a
			helper function to process it """
		# Remove the messages from the pendingMessages list, making sure
		# no one else is appending
		itemList = None
		itemList = self.pendingMessages
		self.pendingMessages = []

		for item in itemList:
			ID = item[0]
			print(ID)
			msg = item[1]
			addr = item[2]
			opcode = msg.split(":")[0]
			print(opcode)
			self.connection.logMessage("Processing '" + opcode + "'", 5)

			if opcode == "NEW_ACCOUNT":
				self.__processNewAccountMsg(msg, ID, addr)
			elif opcode == "LOGIN":
				self.__processLoginMsg(msg, ID, addr)
			elif opcode == "UPDATE":
				self.__processUpdateMsg(msg, ID, addr)
			elif opcode == "FULL_UPDATE":
				self.__processFullUpdateMsg(msg, ID, addr)
			elif opcode == "PLAYER_LEFT":
				self.__processPlayerLeftMsg(msg, ID, addr)
			elif opcode == "QUIT":
				self.__processQuitMsg(msg, ID, addr)
			elif opcode == "PING_ACK":
				self.__processPingAckMsg(msg, ID, addr)
			elif opcode == "PING":
				self.__processPingMsg(msg, ID, addr)
			elif opcode == "CHAT":
				self.__processChatMsg(msg)
			else:
				raise ValueError("Unhandled message: '" + opcode + "'")

	def __processChatMsg(self, msg):
		"""Process Chat msg's from Client"""
		msg = "<" + msg + ">"
		for k2 in self.players:
				self.sendMessage(msg, k2, True)


	def __processNewAccountMsg(self, msg, ID, addr):
		""" Creates a new account in the database file. """
		self.connection.logMessage("Processing NEW_ACCOUNT msg", 1)
		me = msg.split(":")
		if len(me) == 4 and len(me[1]) > 6 and me[1].find("=") == 5 and \
						len(me[2]) > 5 and me[2].find("=") == 4 and \
						len(me[3]) > 6 and me[3].find("=") == 5:
			self.connection.logMessage("Creating new account", 2)
			# Pull out the username and password from the message
			uname = me[1].split("=")[1]
			passW = me[2].split("=")[1]
			# When we do have an ability to assign class values we have it stored here
			# in classType
			classType = me[3].split("=")[1]

			# See if we have a username with this value already
			if uname in self.dbase:
				self.connection.logMessage("Sending NEW_ACCOUNT_ACK - rejected", 1)
				self.connection.sendMessage("<NEW_ACCOUNT_ACK:accepted=F>", ID, True)
			else:
				self.connection.logMessage("Sending NEW_ACCOUNT_ACK - accepted", 1)
				self.sendMessage("<NEW_ACCOUNT_ACK:accepted=T:ID=" + str(ID) + ">", ID, True)
				tempPlayer = player.Player(uname, classType)
				self.addToDBase(tempPlayer, passW)
				self.saveDBase()
		else:
			self.connection.logMessage("Corrupt NEW_ACCOUNT message from client #" + \
								  str(ID), 1)

	def __processLoginMsg(self, msg, ID, addr):
		""" Process a LOGIN message.  Checks the database for a uname/pass
		that matches.  If found, returns
		the player's state in the LOGIN_ACK message. """
		self.connection.logMessage("Processing LOGIN msg", 1)
		me = msg.split(":")
		if len(me) == 4 and len(me[1]) > 6 and me[1].find("=") == 5 and \
							   len(me[2]) > 5 and me[2].find("=") == 4 and \
							   len(me[3]) > 6 and me[3].find("=") == 5:
			# Get the user-name and password
			uname = me[1].split("=")[1]
			passW = me[2].split("=")[1]
			classtype = me[3].split("=")[1]


			# Send a busy response to the client if we're saturated
			if len(self.players) >= self.maxPlayers:
				self.sendMessage("<LOGIN_ACK:accepted=B>", ID, True)
				return

			# See if they match the uname/pass in the dbase
			correct = False
			if uname in self.dbase:
				string = self.dbase[uname]
				print(string)
				pos = string.rfind(":")
				print(pos)
				serialStr = string[:pos]
				print(serialStr)
				testPass = string[pos+1:].split("=")[1]
				if passW == testPass:
					correct = True

			# Send a accepted/rejected message to the client.
			if not correct:
				self.sendMessage("<LOGIN_ACK:accepted=F>", ID, True)
			else:
				# Create the player
				self.connection.logMessage("Creating new player (" + str(ID) + ")", 1)
				self.players[ID] = player.Player(uname, classtype)
				self.connection.logMessage("Deserialize String = '" + serialStr + "'", 6)
				self.players[ID].deserialize(serialStr)

				msg = "<LOGIN_ACK:accepted=T:ID=" + str(ID) + ":" + \
										   self.players[ID].serialize(2) + ">"
				self.sendMessage(msg, ID, True)

				# Send a PLAYER_JOINED message to all other players
				msg = "<PLAYER_JOINED:ID=" + str(ID) + ":" + \
									   self.players[ID].serialize(2) + ">"
				for k2 in self.players:
					if k2 != ID:
						self.sendMessage(msg, k2, True)
		else:
			self.connection.logMessage("Corrupt LOGIN message from client #" + str(ID), 1)

	def __processUpdateMsg(self, msg, ID, addr):
		""" Processes an UPDATE message from a client.  This method relays that
			info to all other players *and* updates our player object. """
		self.connection.logMessage("Processing UDPATE msg '" + str(msg) + "' from ID#" + \
									str(ID), 3)
		serialStr = msg[7:]
		if ID in self.players:
		   self.connection.logMessage("Updating Player#" + str(ID) + " with '" + \
						serialStr + "'", 3)
		   self.players[ID].deserialize(serialStr)
		   self.connection.logMessage("Player#" + str(ID) + "=" + str(self.players[ID]), 3)

		# Notify all other connections of this change
		msg = "<HEARTBEAT:ID=" + str(ID) + ":" + serialStr + ">"
		#msg = "<FULL_UPDATE_ACK:ID=" + str(ID) + ":" + serialStr + ">"
		for k in self.players:
			if k != ID:
				self.connection.logMessage("\tSending '" + msg + " to (" + str(k) + ")", 3)
				self.sendMessage(msg, k, True)

	def __processFullUpdateMsg(self, msg, ID, addr):
		""" Processes a FULL_UPDATE message from a client.  The response we
			send back contains the state of everything in the game world. """
		self.connection.logMessage("Processing FULL_UPDATE msg", 3)
		response = "<FULL_UPDATE_ACK"
		for k in self.players:
			response += ":ID=" + str(k) + ":" + self.players[k].serialize(2)
		response += ">"
		self.sendMessage(response, ID, True)

	def __processPlayerLeftMsg(self, msg, ID, addr):
		""" Processes a PLAYER_LEFT messages.  This method relays a PLAYER_LEFT
			message to all other players. """
		self.connection.logMessage("Processing PLAYER_LEFT msg", 1)
		me = msg.split(":")
		for k in self.players:
			if k != ID:
				self.sendMessage("<PLAYER_LEFT:ID=" + str(ID) + ">", k, True)
		#if ID in self.players:
		#	del self.players[ID]

	def __processQuitMsg(self, msg, ID, addr):
		""" Similar to a PLAYER_LEFT message, but also updates the database. """
		self.connection.logMessage("Processing QUIT msg", 1)
		self.sendMessage("<QUIT_ACK>", ID, True)
		me = msg.split(":")
		playersToDelete = []
		if ID in self.players:
			self.connection.logMessage("Deleting Player#" + str(ID), 1)
			self.updateDBase(self.players[ID])
			self.saveDBase()
			del self.players[ID]

		# Add a PLAYER_LEFT message to the queue -- it'll be sent to
		# other players then
		self.pendingMessages.append((ID, "PLAYER_LEFT:ID=" + str(ID), self.clients[ID].addr))

	def __processPingMsg(self, msg, ID, addr):
		""" Processes a PING message from a client.  Tell them we're still
			alive with a PING_ACK message. """
		self.connection.logMessage("Processing PING message", 5)
		self.sendMessage("<PING_ACK>", ID, True)

	def __processPingAckMsg(self, msg, ID, addr):
		""" Processes a PING_ACK message from a client. """
		# Don't need to do aything -- the server should now have updated
		# the recv_timer value for this client.
		pass

###############################################################################
# Methods specifically for sending data *TO* clients (some of the 'handler'   #
#	messages above also send data -- these are just the server-initiated	 #
#	sends)																   #
###############################################################################
	def sendHeartBeat(self, dT):
		""" Send an update to all connected players if enough time has
			passed since the last update. """
		# See if we have more than 1 player connected and enough time
		# has passed since our last hearbeat
		if len(self.players) > 1:
			self.heartbeatTimer += dT
			if self.heartbeatTimer < self.heartbeatFreq:
				return
		else:
			return
		# If we get here, we want to send a heartbeat.  Start by resetting
		# the heartbeat timer.
		self.heartbeatTimer= 0.0

		# Create the heartbeat message.  Actually, this is more of a
		# full update -- we might want to change the name...
		self.connection.logMessage("Sending heartbeat", 4)
		m = "<FULL_UPDATE_ACK"
		for k in self.players:
			m += ":ID=" + str(k) + ":"
			p = self.players[k]
			m += p.serialize(2)
		m += ">"

		# Send it to all connections
		#self.connection.sendBroadcastMessage(m)
		for idNum in self.players:
			self.sendMessage(m, idNum, False)

	def sendMessage(self, msg, ID, must_succeed):
		""" Sends a message to a single client. """
		self.clients[ID].send_count += 1
		self.connection.sendMessage(msg, self.clients[ID].addr, must_succeed)

	def checkForDeadClients(self):
		""" See if we have clients that haven't been heard from for a while.
			This method sends a PING message to these clients.  If we haven't
			heard from them for even longer, remove them from our list. """
		players_to_delete = []
		for idNum in self.players:
			clientData = self.clients[idNum]
			if time.time() - clientData.recv_timer >= Server.maxDelay + \
													  Server.maxDelay:
				# 2x the maxDelay has passed since the last received
				# message -- let's consider them dead
				players_to_delete.append(idNum)
			elif time.time() - clientData.recv_timer >= Server.maxDelay:
				# Send a ping to the client (if enough time has passed
				# since the last ping)
				if time.time() - clientData.ping_timer >= \
									Server.pingFrequency:
					self.sendMessage("<PING>", idNum, True)
					clientData.ping_timer = time.time()
		# Remove dead clients
		for idNum in players_to_delete:
			self.__processQuitMsg("QUIT", idNum, self.clients[idNum].addr)


###############################################################################
# Methods for updating the server GUI and other non-connection-related tasks  #
###############################################################################
	def updateGUI(self):
		""" Updates the server's GUI """
		self.screen.fill((0,0,0))

		self.screen.blit(self.font.render("SERVER   " + \
						  self.connection.getLocalIP() + ":" + \
						  str(self.connection.getLocalPort()), False, (255,255,255)), (0,0))

		pos = [0, 30, 180, 300, 340, 380]
		texts = ["ID", "IP", "UName", "RCnt", "SCnt", "RTime"]
		ht = self.font.get_linesize()
		y = ht*2

		for i in range(len(pos)):
			tempS = self.font.render(texts[i], False, (255,255,0))
			self.screen.blit(tempS, (pos[i],y))
			pygame.draw.line(self.screen, (255,255,0), (pos[i],y+ht), \
							   (pos[i]+tempS.get_width(),y+ht))
		y += ht

		for j in self.players:
			clientData = self.clients[j]
			texts = [str(j), str(clientData.addr[0]) + ":" + \
								   str(clientData.addr[1]), \
								   self.players[j].uname, \
								   str(clientData.recv_count), \
								   str(clientData.send_count), \
								   str(round(clientData.recv_timer,1))]
			for i in range(len(pos)):
				tempS = self.font.render(texts[i], False, (100,255,100))
				self.screen.blit(tempS, (pos[i],y))
			y += ht

		pygame.display.flip()

	def updateGame(self, dT):
		""" Update the game variables. """
		for idNum in self.players:
			self.players[idNum].update(dT)



###############################################################################
# The 'main program' for the server										   #
###############################################################################
	def run(self):
		""" The server's 'main' program """
		# Start the GUI
		pygame.display.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((500,500))
		self.font = pygame.font.SysFont("Courier New", 14)

		# Load the database of users
		self.loadDBase()

		# Get the initial time value
		stime = time.time()

		# Start the main loop
		while True:
			pygame.event.pump()
			if pygame.key.get_pressed()[pygame.K_ESCAPE]:
				break

			# Get the time since last iteration
			dT = time.time() - stime
			stime = time.time()

			# Update the connection
			self.connection.update()

			# Determine if we need to send a "heartbeat" message
			self.sendHeartBeat(dT)

			# Get new messages
			self.getNewMessages()

			# Get any client messages and update our game data
			self.processPendingData()

			# See if we need to send out a ping to any clients or remove them
			self.checkForDeadClients()

			# Run any other updates
			self.updateGame(dT)


			# Draw the GUI
			self.updateGUI()

		# Save the database
		self.saveDBase()

		# Kill the connection thread
		self.connection.kill()

		# Shutdown pygame
		pygame.font.quit()
		pygame.display.quit()


# Start of the program
S = Server(5, 50000)
S.run()