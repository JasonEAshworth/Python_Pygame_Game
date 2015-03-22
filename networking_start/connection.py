import socket
import threading
import time

class ConnectionListener(object):
	""" Meant to be used as a derived class.  If a new class a) derives itself from this class, and
		b) registers itself through Connection.registerListener, it will receive callbacks when
		key events in a Connection happen (getting a message, completing a send, disconnecting, etc).
		NOTE: the callback functions should be very simple -- they should very quickly return
		since the Connection thread will be running the code in its thread of control -- we don't
		want to ignore messages / dropped connections / etc. """
	def onNewMessage(self, m, addr):
		""" Called after we get a new complete message """
		pass

	def onSendCompletion(self, ticketID):
		""" Called after a send is completed.  ticketID will match the ticket returned by
			calling the Connection's sendMessage method. """
		pass

	def onThreadStart(self):
		""" Called just after the thread starts. """
		pass

	def onThreadExit(self):
		""" Called just before the connection thread shuts down. """
		pass

	def onAbnormalDisconnect(self):
		""" Called if the other end of the socket abnormally terminates. """
		pass


class Connection(threading.Thread):
	""" A general-purpose sending/receiving socket on its own thread of control. """
	maxPacketSize = 4096	  # Generally a power of 2
	#recvBufferSize = 2**15

	def __init__(self):
		""" The constructor. """
		# call thread constructor
		threading.Thread.__init__(self)

		# Find our local IP / host info
		self.__host_name = socket.gethostname()
		self.__local_IP = socket.gethostbyname(self.__host_name)

		# Create place-holders -- these values will be assigned by later calls.
		self.__ID = None
		self.__socket = None
		self.__socket_IP = None
		self.__socket_port = None
		self.__active = False
		self.__finished = False

		# Create some buffers used for sending / receiving messages
		self.__recv_message_accum = ""
		self.__send_queued_messages = []
		self.__recv_timer = time.time()    # The time of the last recv packet
		self.__send_counter = 0
		self.__recv_counter = 0

		# A semaphore to prevent two threads/processes from removing / adding to the received messages queue
		# at the same time.
		self.__semaphore = threading.Semaphore(1)

		# The currently registered listener
		self.__listener = None

	def acquireSemaphore(self):
		""" Meant to be called externally.  Blocks until the semaphore is freed. Make sure
		    releaseSemaphore is called QUICKLY after acquiring it -- or bad things (deadlock) will happen."""
		self.__semaphore.acquire()

	def releaseSemaphore(self):
		""" Meant to be called externally. Releases the semaphore. """
		self.__semaphore.release()

	def kill(self):
		""" Just sets our __active attribute to false -- the thread should shortly terminate. """
		self.__active = False

	def setListener(self, L=None):
		""" Attaches (or replaces) the listener on this Connection.  If a listener is no longer
			being used, pass None to this function. """
		if not isinstance(L, ConnectionListener):
			raise TypeError("You must pass an instance of (a class derived from) ConnectionListener.")
		self.__listener = L

	def setID(self, ID):
		""" Sets the ID for this Connection.  Generally this is set by the server.  For clients,
			it is usually sent to them from the server. The ID number is passed to all
			listener callbacks. """
		self.__ID = ID

	def setBlocking(self, isBlocking, timeoutTime=None):
		""" Sets the blocking mode of the socket. """
		if not isinstance(isBlocking, bool):
			raise TypeError("isBlocking must be a boolean.")
		self.__socket.setblocking(isBlocking)
		if isBlocking and timeoutTime != None:
			self.__socket.settimeout(timeoutTime)

	def logMessage(self, s, lvl):
		""" Logs a messages.  By default, this just prints.  If re-defined in a dervied class it
			could 'pipe' information to a GUI. """
		print("[Connection Thread#" + str(self.__ID) + ": " + str(s) + "]")

	def getLocalIP(self):
		""" Returns the local IP of the machine this thread is running upon. """
		return self.__local_IP

	def getID(self):
		""" Returns the user-defined user ID """
		return self.__ID

	def getFinished(self):
		""" Returns True if this thread has completed. """
		return self.__finished

	def getTimeSinceLastRecv(self):
		""" Returns the time (in seconds) since the last received data packet. """
		return time.time() - self.__recv_timer

	def createSocket(self, myPort):
		""" Assigns the connected socket/ip/port.  Also starts the thread of control. """
		if self.__socket != None:
			raise ValueError("This Connection already has an active socket!")
		if not isinstance(myPort, int):
			raise ValueError("Mal-formed local port number")

		# Get local host info
		localName = socket.gethostname()
		localIP = socket.gethostbyname(localName)
		self.logMessage("New socket on '" + localName + "' " + localIP + " (" + str(myPort) + ")", 0)

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__socket.setblocking(False)
		self.__socket_IP = localIP
		self.__socket_port = myPort
		self.__socket.bind((self.__socket_IP, self.__socket_port))

		# Register this thread as active and start it's thread of control
		self.__active = True
		self.start()


	def sendMessage(self, s, addr, must_succeed):
		""" Queues a message to be sent.  s should be a string.  Returns
			a 'send_ticket' (an integer) which will be included in any listener callbacks. """
		sendTicket = None
		self.__semaphore.acquire()
		self.__send_queued_messages.append((s, addr, must_succeed))
		self.__semaphore.release()

		return sendTicket

	def __accumulateMessage(self, s, addr):
		""" Used to assemble a message.  Since a message could be broken up into multiple UDP/TCP
			packets, we package our data messages in a <...> block.  This method takes a (possibly)
			partial message, adds it to an accumulator.  Once a complete block is assembled, it is added to the
			recv_messages buffer. """
		msg = None
		self.__semaphore.acquire()
		self.__recv_message_accum += s
		if self.__recv_message_accum.count("<") >= 1 and self.__recv_message_accum.count(">") >= 1:
			start = self.__recv_message_accum.find("<")
			end = self.__recv_message_accum[start:].find(">") + start
			msg = self.__recv_message_accum[start+1:end]
			self.__recv_message_accum = self.__recv_message_accum[end+1:]
		self.__semaphore.release()

		if msg and self.__listener:
			self.__listener.onNewMessage(msg, addr)

	def run(self):
		""" The 'main program' for this thread. Called indirectly be the start command (which here is called
			by setSocket. """
		#print("Connection thread #" + str(self.__ID) + " started (" + str(self.__socket_IP) + ")")
		# Notify the listener we're starting
		if self.__listener:
			self.__listener.onThreadStart()


		while self.__active:
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
					self.__active = False
					if self.__listener:
						self.__listener.onAbnormalDisconnect()
					break
				else:
					# Re-raise the exception.  We might need another handler here...
					raise inst
			if s != "":
				#print("Connection thread #" + str(self.__ID) + " message received '" + s + "'")
				# Update the receive timer
				self.__recv_timer = time.time()
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
					#print(len(msg), len(emsg), bytes_sent)
					if bytes_sent >= len(emsg) or not must_succeed:
						self.__semaphore.acquire()
						del self.__send_queued_messages[0]
						self.__semaphore.release()

					if self.__listener:
						self.__listener.onSendCompletion(-1)
				except socket.error as inst:
					if inst.errno == 10035:
						# Error number 10035 means we can't immediately send the data.
						# (a common occurrence since we're in non-blocking mode)
						pass
					elif inst.errno == 10054:
						# The other side of the connection was forcibly quit
						self.__active = False
						if self.__listener:
							self.__listener.onAbnormalDisconnect()
					else:
						raise inst

		#print("Connection thread #" + str(self.__ID) + " Shutting down")
		# Notify the listener we're about to quit.
		if self.__listener:
			self.__listener.onThreadExit()
		# Set our finished flag
		self.__finished = True

