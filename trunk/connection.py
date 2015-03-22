import socket
import threading
import time



class Connection(object):
	""" A general-purpose sending/receiving socket on its own thread of control. """
	maxPacketSize = 4096	  # Generally a power of 2

	maxDelay = 4.0	  # The maximum time (in seconds) until a ping message is
						#   sent -- if we pass this the connection is in the
						#   "possibly-dead" state.  If 2 * this time pass
						#   without a message, the server is considered "dead"
						#   and we quit.
	pingFrequency = 0.5 # The time between pings if the connection is in the
						#   "possibly-dead" state

	def __init__(self):
		""" The constructor. """
		# call thread constructor
		#threading.Thread.__init__(self)

		# Find our local IP / host info
		self.__host_name = socket.gethostname()
		self.__local_IP = socket.gethostbyname(self.__host_name)

		# Create place-holders -- these values will be assigned by later calls.
		self.__ID = None
		self.__socket = None
		self.__local_port = None
		self.__active = False
		self.__shutting_down = False

		# Create some buffers used for sending / receiving messages
		self.__recv_message_accum = ""
		self.__recv_messages = []
		self.__send_queued_messages = []
		self.__recv_timer = time.time()	# The time of the last recv packet
		self.__send_counter = 0
		self.__recv_counter = 0

		# Attributes for detecting dead connections.  Really only used by clients.
		self.__ping_timer = 0.0		   # Time since last ping sent
		#self.__time_since_last_recv = 0.0 # Time since the last message from server
		self.__ping_check = False		 # Set this to true to do ping-checks.

		# Miscellaneous attributes
		self.__logLevel = 5		  # 0 = Client startup/shutdown messages
									 # 1 = Major messages from remote and below
									 # 2 = Medium messages from remote and below
									 # 3 = Minor messages from remote and below
									 # 4 = Pings and below
									 # 5 = Debug info and below


	def kill(self):
		""" Just sets our __active attribute to false -- the thread should shortly terminate. """
		self.__shutting_down = True


	def setID(self, ID):
		""" Sets the ID for this Connection.  Generally this is set by the server.  For clients,
			it is usually sent to them from the server. The ID number is passed to all
			listener callbacks. """
		self.__ID = ID

	def setPingEnable(self, enable):
		""" Enables or dis-ables ping-checking. """
		self.__ping_check = enable
		if enable:
			self.__recv_timer = time.time()


	def logMessage(self, s, lvl):
		""" Logs a messages.  By default, this just prints.  If re-defined in a dervied class it
			could 'pipe' information to a GUI. """
		if lvl <= self.__logLevel:
			print("[Connection Thread#" + str(self.__ID) + ": " + str(s) + "]")

	def getLocalIP(self):
		""" Returns the local IP of the machine this thread is running upon. """
		return self.__local_IP

	def getLocalPort(self):
		""" Returns the port number of this connection. """
		return self.__local_port

	def getID(self):
		""" Returns the user-defined user ID """
		return self.__ID

	def getActive(self):
		""" Returns True if this connection is active. """
		return self.__active

	def getTimeSinceLastRecv(self):
		""" Returns the time (in seconds) since the last received data packet. """
		return time.time() - self.__recv_timer

	def createSocket(self, myPort):
		""" Assigns the connected socket/ip/port. """
		if self.__socket != None:
			raise ValueError("This Connection already has an active socket!")
		if not isinstance(myPort, int):
			raise ValueError("Mal-formed local port number")

		# Get local host info
		self.logMessage("New socket on '" + self.__host_name + "' " + self.__local_IP + " (" + str(myPort) + ")", 0)

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__socket.setblocking(False)
		self.__local_port = myPort
		self.__socket.bind((self.__local_IP, self.__local_port))

		# Register this thread as active and start it's thread of control
		self.__active = True

	def hasSocket(self):
		""" Returns True if this connection has a socket. """
		return self.__socket != None

	def checkForDeadConnection(self, remoteIP, remotePort):
		""" If we haven't received a message from the remote connection for a while,
			PING it. """
		if not self.__ping_check:
			return

		if self.getTimeSinceLastRecv() > Connection.maxDelay + Connection.maxDelay:
			self.__active = False
			self.logMessage("Remote connection timed out -- shutting down.", 0)
		elif self.getTimeSinceLastRecv() > Connection.maxDelay and time.time() - self.__ping_timer > Connection.pingFrequency:
			self.sendMessage("<PING>", (remoteIP, remotePort), False)
			self.__ping_timer = time.time()


	def sendMessage(self, s, addr, must_succeed):
		""" Queues a message to be sent.  s should be a string.  Returns
			a 'send_ticket' (an integer) which will be included in any listener callbacks. """
		if not self.__shutting_down:
			self.__send_queued_messages.append((s, addr, must_succeed))

	def getNewMessages(self):
		""" Gets all received messages and empties out our self.__recv_messages buffer """
		rv = self.__recv_messages
		self.__recv_messages = []
		return rv


	def __accumulateMessage(self, s, addr):
		""" Used to assemble a message.  Since a message could be broken up into multiple UDP/TCP
			packets, we package our data messages in a <...> block.  This method takes a (possibly)
			partial message, adds it to an accumulator.  Once a complete block is assembled, it is added to the
			recv_messages buffer. """
		msg = None
		self.__recv_message_accum += s
		if self.__recv_message_accum.count("<") >= 1 and self.__recv_message_accum.count(">") >= 1:
			start = self.__recv_message_accum.find("<")
			end = self.__recv_message_accum[start:].find(">") + start
			msg = self.__recv_message_accum[start+1:end]
			self.__recv_message_accum = self.__recv_message_accum[end+1:]
			self.__recv_messages.append((msg, addr))


	def update(self):
		""" The 'main update' for this thread. Called indirectly be the start command (which here is called
			by setSocket. """
		# If we're not active, do nothing.
		if not self.__active:
			return

		############################
		# RECEIVE DATA			 #
		############################
		# Attempt to receive data -- if it's not ready, ignore the exception
		s = ""
		try:
			s, addr = self.__socket.recvfrom(Connection.maxPacketSize)
			s = s.decode("utf-8")
		except (socket.error, socket.timeout) as inst:
			if isinstance(inst, socket.error) and inst.errno == 10035:
				# Error number 10035 means there is no data ready waiting for us.
				# (a common occurrence since we're in non-blocking mode)
				pass
			elif (isinstance(inst, socket.error) and inst.errno == 10054) or isinstance(inst, socket.timeout):
				# Error number 10054 means the connection unexpectedly quit on the
				# other side.
				#self.__active = False
				pass
			else:
				# Re-raise the exception.  We might need another handler here...
				raise inst
		if s != "":
			# Update the receive timer
			self.__recv_timer = time.time()
			# Pick apart the message -- look for complete message(s)
			self.__accumulateMessage(s, addr)

		###############################
		# SEND DATA				   #
		###############################
		# Attempt to send a queued message
		if len(self.__send_queued_messages) > 0:
			try:
				msg = self.__send_queued_messages[0][0]
				addr = self.__send_queued_messages[0][1]
				must_succeed = self.__send_queued_messages[0][2]
				emsg = msg.encode()
				bytes_sent = self.__socket.sendto(emsg, addr)
				if bytes_sent >= len(emsg) or not must_succeed:
					del self.__send_queued_messages[0]

			except socket.error as inst:
				if inst.errno == 10035:
					# Error number 10035 means we can't immediately send the data.
					# (a common occurrence since we're in non-blocking mode)
					pass
				elif inst.errno == 10054:
					# The other side of the connection was forcibly quit
					# self.__active = False
					pass
				else:
					raise inst

		# Shut down the connection if we've sent all our data
		if self.__shutting_down and len(self.__send_queued_messages) == 0:
			self.__active = False
			self.__socket.close()



