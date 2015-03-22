import pygame
import player
import connection
import random
import sys
import time

def generateRandomString(numChars):
    """ A utility function for generating random passwords or unames """
    s = ""
    for i in range(numChars):
        s += chr(random.choice(tuple(range(65,91)) + tuple(range(97,123))))
    return s


class Client(connection.ConnectionListener):
    """ A client application base class. """
    maxDelay = 4.0      # The maximum time (in seconds) until a ping message is 
                        #   sent -- if we pass this the connection is in the 
                        #   "possibly-dead" state.  If 2 * this time pass  
                        #   without a message, the server is considered "dead"  
                        #   and we quit.
    pingFrequency = 0.5 # The time between pings if the connection is in the 
                        #   "possibly-dead" state
                        
    def __init__(self, uname="", passW="", remoteIP="", createAccount=True, remotePort=50000):
        """ Constructor. """
        # Generate a random user-name / password if none is given.
        if uname == "":
            uname = generateRandomString(random.randint(4,12))
        if passW == "":
            passW = generateRandomString(random.randint(4,12))

        # Make sure we have a valid uname and password.
        if uname.count("<") or uname.count(">") or uname.count(":") or len(uname) >= 32:
            raise ValueError("uname must not contain '<', '>', or ':' and must be less than 32 characters")
        if passW.count("<") or passW.count(">") or passW.count(":") or len(passW) >= 32:
            raise ValueError("passW name must not contain '<', '>', or ':' and must be less than 32 characters")

        # Connection-related attributes
        self.serverMessages = []    # A list of messages we've received
                                    #    from the server but haven't 
                                    #    processed yet.
        self.players = {}       # A list of all player objects 
                                #    (including us)     
        self.playerID = None # The key of our player within 
                             #    self.players
        self.state = "???"   # The state of the application.
                             #    'login' => Attempting to into the server
                             #    'running' => Running the game (connected)
                             #    'qutting' => Waiting for QUIT_ACK from server
                             #    'quit' => Shutdown
        self.logLevel = 5  # 0 = Client startup/shutdown messages
                           # 1 = Connection made/lost/new-account/login 
                           #              messages and below
                           # 2 = PLAYER_JOING / PLAYER_LEFT and below
                           # 3 = Updates from server and below
                           # 4 = Pings and below
                           # 5 = Debug info and below

        self.remoteIP = remoteIP      # IP of the server
        self.remotePort = remotePort  # Port the server is listening on
        self.ping_timer = 0.0         # Time since the last message from server
        

        # Create the connection with the server.  
        rv = self.initClientConnection(uname, passW, createAccount, remoteIP)

###############################################################################
# Callback methods the connection thread will call for us (since we're        #
#      registered as a listener)                                              #
###############################################################################
    def onNewMessage(self, m, addr):
        """ Called after we get a new complete message """
        #self.logMessage("got a message '" + m + "'")
        self.serverMessages.append(m)

    def onThreadExit(self):
        """ Called just before the connection thread shuts down. """
        self.state = "quitting"

    def onAbnormalDisconnect(self):
        """ Called if the other end of the socket abnormally terminates. """
        self.state = "quitting"

    def logMessage(self, s, lvl):
        """ Displays a log message if our log level attribute is <= lvl """
        if lvl <= self.logLevel:
            print("* Client(" + str(self.connection.getID()) + "): " + s)

###############################################################################
# Methods for establishing / breaking connections with the server             #
###############################################################################
    def initClientConnection(self, uname, password, newAccount=False, remoteIP=""):
        """ Establishes a connection with the server. """
        # Create the connection object and register ourself as its listener
        self.connection = connection.Connection()
        self.connection.setListener(self)

        # Set our state and the initial message to send to the server
        if newAccount:
            self.state = "login"
            initialMessage = "<NEW_ACCOUNT:uname=" + uname + ":pass=" + password + ">"
        else:
            self.state = "login"
            initialMessage = "<LOGIN:uname=" + uname + ":pass=" + password + ">"


        # See if we were given a remoteIP -- if not assume we're looking for a local server
        if remoteIP == "":
            self.remoteIP = self.connection.getLocalIP()
        else:
            self.remoteIP = remoteIP
        self.logMessage("Attempting to connect to server: " + str(remoteIP), 0)

        # Save our user name
        self.uname = uname
        self.password = password

        # Connect to the server and send our initial message
        self.connection.createSocket(random.randint(10000,49999))
        self.connection.sendMessage(initialMessage, (self.remoteIP, self.remotePort), True)

        return 0
    
    def shutdownClientConnection(self):
        """ Shutdown the connection with the server """
        if self.state != "quitting":
           self.logMessage("Shutting down client connection.", 0)
           #self.connection.setBlocking(True, 2.0)
           self.connection.sendMessage("<QUIT>", (self.remoteIP, self.remotePort), True)
           self.state = "quitting"


###############################################################################
# Methods for setting up / shutting down the pygame environment               #
###############################################################################
    def initPygame(self):
        """ Initializes pygame """
        pygame.display.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()

    def initPygameScreen(self):
        """ Creates the pygame window """
        self.screen = pygame.display.set_mode((800,600))

    def shutdownPygame(self):
        """ Shutdown pygame """
        self.logMessage("Shutting down pygame", 1)
        pygame.font.quit()
        pygame.display.quit()

    

###############################################################################
# Connection update methods                                                   #
###############################################################################
    def checkForDeadServer(self):
        """ If we haven't received a message from the server for a while, 
            PING it. """
        if self.connection.getTimeSinceLastRecv() > Client.maxDelay + \
                                                    Client.maxDelay:
            self.connection.kill()
            self.state = "quit"
            self.logMessage("Server timed out -- shutting down.", 0)
        elif self.connection.getTimeSinceLastRecv() > Client.maxDelay and time.time() - self.ping_timer > Client.pingFrequency:
            self.connection.sendMessage("<PING>", (self.remoteIP, self.remotePort), False)
            self.ping_timer = time.time()
            
    def sendUpdateToServer(self):
        """ Send updates to the server if our player has changed state. """
        if self.state == "running" and self.playerID != None and self.playerID in self.players:
            serialStr = self.players[self.playerID].serialize(0)
            if len(serialStr) > 0:
                self.logMessage("\tSending '" + serialStr + "'", 4)
                self.connection.sendMessage("<UPDATE:" + serialStr + ">", (self.remoteIP, self.remotePort), True)


    def processNewMessages(self):
        """ Gets and handles new messages from the server. """
        msgList = self.serverMessages
        self.serverMessages = []
        for newMsg in msgList:
            self.logMessage("Processing message '" + newMsg + "'", 5)
            opcode = newMsg.split(":")[0]

            if opcode == "NEW_ACCOUNT_ACK":
                rv = self.__processNewAccountMsg(newMsg)
                if rv != 0:
                    self.state = "qut"
            elif opcode == "LOGIN_ACK":
                rv = self.__processLoginMsg(newMsg)
                if rv != 0:
                    self.state = "qut"
            elif opcode == "FULL_UPDATE_ACK":
                rv = self.__processFullUpdateMsg(newMsg)
                if rv == 0 and self.state == "login":
                    self.initPygameScreen()
                    self.state = "running"
            elif opcode == "HEARTBEAT":
                self.__processHeartbeatMsg(newMsg)
            elif opcode == "PLAYER_JOINED":
                self.__processPlayerJoinedMsg(newMsg)
            elif opcode == "PLAYER_LEFT":
                self.__processPlayerLeftMsg(newMsg)
            elif opcode == "PING":
                self.__processPingMsg(newMsg)
            elif opcode == "PING_ACK":
                pass    # Don't need to do anything -- the connection should have updated it's time-since-last message value.
            elif opcode == "QUIT_ACK":
                self.__processQuitAckMsg(newMsg)
            else:
                raise ValueError("Unhandled opcode '" + opcode + "'")

    def updateClientConnection(self):
        """ (Possibly) send an update to the server and look for new messages from the server. """
        # Ping the server if we haven't heard from it for a while
        self.checkForDeadServer()
    
        # Update the server if we've changed.
        self.sendUpdateToServer()
        
        # Get updates from the server
        self.processNewMessages()
        
###############################################################################
# Handlers for individual messages from the server.  Called by                #
#     self.processNewMessages()                                               #
###############################################################################
    def __processNewAccountMsg(self, msg):
        """ Process a NEW_ACCOUNT_ACK message """
        # See if the server accepted this uname / password pair
        self.logMessage("handling NEW_ACCOUNT_ACK msg", 1)
        me = msg.split(":")
        if len(me) == 2 and me[1].find("=") > 0 and me[1].find("=") == len(me[1])-2:
            response = me[1].split("=")[1]
        else:
            self.logMessage("Corrupt NEW_ACCOUNT_ACK message from server.", 1)
            return 3

        if response == "T":
            # Now, actually attempt to log-in
            self.connection.sendMessage("<LOGIN:uname=" + self.uname + ":pass=" + self.password + ">", (self.remoteIP, self.remotePort), True)
            return 0
        else:
            return 100

    def __processLoginMsg(self, msg):
        """ Process a LOGIN_ACK message """
        # See if the server accepted this uname
        self.logMessage("handling LOGIN_MSG msg", 1)
        me = msg.split(":")
        if len(me) < 2 or me[1].find("=") < 0 or me[1].find("=") != len(me[1])-2:
            self.logMessage("Corrupt LOGIN_ACK message from server.", 1)
            return 3
        response = me[1].split("=")[1]
        if response == "F":
            self.logMessage("Incorrect uname and/or password", 1)
            return 100
        elif response == "B":
            self.logMessage("Server is busy -- check again later")
            return 101
        if len(me) < 3 or me[2].find("=") != 2 or len(me[2]) <= 3:
            self.logMessage("Corrupt LOGIN_ACK message from server.", 1)
            return 5
        else:
            # Initialize pygame
            self.initPygame()
            # Get the ID number.  Set our connection ID# and playerID number to this value
            idNum = int(me[2].split("=")[1])
            serialStr = ""
            for i in range(3, len(me)):
                if i > 3:
                    serialStr += ":"
                serialStr += me[i]
            self.players[idNum] = player.Player("???")
            self.players[idNum].deserialize(serialStr)
            self.connection.setID(idNum)
            self.playerID = idNum

        # Ask the server for a full update
        self.connection.sendMessage("<FULL_UPDATE>", (self.remoteIP, self.remotePort), True)

        return 0

    def __processFullUpdateMsg(self, msg):
        """ Process a full update of everything in the game. """
        self.logMessage("Processing FULL_UPDATE_ACK msg '" + msg + "'", 3)
        # Create and initialize the player and any existing players
        me = msg.split(":")
        serializeStr = ""
        idNum = None
        includedPlayers = []
        for i in range(1, len(me)):
            if me[i][:3] == "ID=":
                if serializeStr != "":
                    if idNum not in self.players:
                        self.logMessage("Creating player #" + str(idNum), 2)
                        self.players[idNum] = player.Player("???")
                    #if self.playerID != idNum:
                    if True:
                        self.players[idNum].deserialize(serializeStr)
                    serializeStr = ""
                idNum = int(me[i].split("=")[1])
                includedPlayers.append(idNum)
            else:
                if len(serializeStr) > 0:
                    serializeStr += ":"
                serializeStr += me[i]
        if serializeStr != "":
            if idNum not in self.players:
                self.logMessage("Creating player' #" + str(idNum), 2)
                self.players[idNum] = player.Player("???")
            #if self.playerID != idNum:
            if True:
                self.players[idNum].deserialize(serializeStr)
        # See if there are any players we need to destroy -- this is possible if we lost the PLAYER_LEFT
        # message
        players_to_delete = []
        for idNum in self.players:
            if idNum not in includedPlayers:
                players_to_delete.append(idNum)
        for idNum in players_to_delete:
            self.logMessage("Removing player#" + str(idNum) + " in response to a FULL_UPDATE", 2)
            del self.players[idNum]

        return 0


    def __processHeartbeatMsg(self, msg):
        """ Process some kind of data from the server. """
        self.logMessage("Processing HEARTBEAT msg", 4)
        me = msg.split(":")
        curPlayerID = None
        curSerialStr = ""
        for i in range(1, len(me)):
            if me[i][:3] == "ID=" and len(me[i]) > 3:
                if curPlayerID != None:
                    #if curPlayerID != self.playerID and curPlayerID in self.players:
                    if curPlayerID in self.players:
                        self.players[curPlayerID].deserialize(curSerialStr)
                    curSerialStr = ""
                curPlayerID = int(me[i][3:])
            else:
                if len(curSerialStr) > 0:
                    curSerialStr += ":"
                curSerialStr += me[i]
        #if curPlayerID != None and curPlayerID != self.playerID and len(curSerialStr) > 0 and curPlayerID in self.players:
        if curPlayerID != None and len(curSerialStr) > 0 and curPlayerID in self.players:
            self.players[curPlayerID].deserialize(curSerialStr)

    def __processPlayerJoinedMsg(self, msg):
        """ A new player has joined the game.  This message should include a serialized string for that player. """
        self.logMessage("Processing PLAYER_JOINED msg", 2)
        me = msg.split(":")
        IDnum = None
        serialStr = ""
        for i in range(1, len(me)):
            if me[i][:3] == "ID=":
                if IDnum != None and IDnum != self.connection.getID() and IDnum not in self.players:
                    self.players[IDnum] = player.Player("???")
                    self.players[IDnum].deserialize(serialStr)
                    serialStr = ""
                IDnum = int(me[i].split("=")[1])
            else:
                if serialStr != "":
                    serialStr += ":"
                serialStr += me[i]
        if IDnum != None and IDnum != self.connection.getID() and IDnum not in self.players:
            self.players[IDnum] = player.Player("???")
            self.players[IDnum].deserialize(serialStr)

    def __processPlayerLeftMsg(self, msg):
        """ A player has dropped out.  Remove them from our players list. """
        self.logMessage("Processing PLAYER_LEFT msg", 2)
        me = msg.split(":")
        if len(me) == 2 and len(me[1]) > 3 and me[1].find("=") == 2:
            idNum = int(me[1].split("=")[1])
            if idNum in self.players:
                del self.players[idNum]
        else:
            self.logMessage("Corrupt PLAYER_LEFT message", 2)


    def __processPingMsg(self, msg):
        self.logMessage("Processing PING msg -- sending to " + self.remoteIP + ":" + str(self.remotePort), 2)
        self.connection.sendMessage("<PING_ACK>", (self.remoteIP, self.remotePort), True)


    def __processQuitAckMsg(self, msg):
        self.logMessage("Processing QUIT_ACK msg", 0)
        self.connection.kill()
        self.state = "quit"
        
###############################################################################
# Client application (non-connection-related) methods                         #
###############################################################################
    def handleInput(self):
        """ Handle user input """
        # Take an input snapshot
        pygame.event.pump()
        pressed = pygame.key.get_pressed()
        
        # Quit on escape
        if pressed[pygame.K_ESCAPE]:
            self.shutdownClientConnection()
        # Move with arrow keys, 'activate' with space
        if self.playerID in self.players:
            if pressed[pygame.K_LEFT]:
                self.players[self.playerID].setMove(horiz="Left")
            elif pressed[pygame.K_RIGHT]:
                self.players[self.playerID].setMove(horiz="Right")
            else:
                self.players[self.playerID].setMove(horiz="-")

            if pressed[pygame.K_UP]:
                self.players[self.playerID].setMove(vert="Up")
            elif pressed[pygame.K_DOWN]:
                self.players[self.playerID].setMove(vert="Down")
            else:
                self.players[self.playerID].setMove(vert="-")

            if pressed[pygame.K_SPACE]:
                self.players[self.playerID].active = True
            else:
                self.players[self.playerID].active = False
                    
    def updatePlayers(self, dT):
        """ Updates all players. """
        for idNum in self.players:
            self.players[idNum].update(dT)
            
    def renderWorld(self, surf):
        """ Renders the entire world """
        if self.state == "running":
            for idNum in self.players:
                self.players[idNum].render(surf)
            pygame.display.flip()
        

###############################################################################
# Client's main program                                                       #
###############################################################################
    def main(self):
        while self.state != "quit":
            if self.state == "running":
                self.screen.fill((64,64,64))

                # Get user input
                self.handleInput()
                
                # Other game-related updates
                dT = self.clock.tick() / 1000.0
                self.updatePlayers(dT)
                
                # Rendering
                self.renderWorld(self.screen)
                
            # Update our server connection and get / handle new messages
            self.updateClientConnection()

            
        # Kill the pygame window.
        self.shutdownPygame()
        


################
# Main program #
################
#loginMode = "cmd_line"
loginMode = "prompt"
#loginMode = "testing"

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


C = Client(uname, passW, remoteIP, createAccount)
C.main()

