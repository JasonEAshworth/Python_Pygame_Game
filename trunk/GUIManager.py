'''	Rock G Bolton
	ETGG 1802 - TR'''

import pygame
import math


class GUIManager(object):
	def __init__(self, start_screen = "title"):
		# Key=string, e.g. "login", value=list of gui elements
		self.elementCategories = {"title": [], "New_user": [], "new_account_failure": [], "new_account_busy": [], "login": [], "login_failure": [], "login_busy": [],\
				"Game": [], "credits": [], "quit": []}
		# String matching one key in elementCategories
		self.currentGroup = start_screen
		self.font = None
		self.focus = None

	def onKeyEvent(self, keyType, key, mod):
		Text_Found = False
		# TODO: add an if check for tab then increase focus

		if keyType == pygame.KEYDOWN:
			if key == pygame.K_TAB:
				# moves up 1 through list of objects only if the next object is a text entry object

				i = self.elementCategories[self.currentGroup].index(self.focus)
				if isinstance(self.elementCategories[self.currentGroup][i+1], TextEntry):
					self.focus = self.elementCategories[self.currentGroup][i+1]
					self.elementCategories[self.currentGroup][i].isfocused = False
					self.elementCategories[self.currentGroup][i+1].isfocused = True


			elif self.focus and self.focus != None:
				self.focus.gotKeyEvt( keyType, key, mod, None)

	def onMouse(self, mouseType, button, pos):
		""" Go through all gui elements.  If pos is within one, call its gotMouseEvt method and return its ID. If
			pos is NOT within any gui elements, return None. """
		ID = None

		for e in self.elementCategories[self.currentGroup]:
			if isinstance(e, TextEntry)  and mouseType == pygame.MOUSEBUTTONDOWN :
					e.isfocused = False

		for e in self.elementCategories[self.currentGroup]:
			if pos[0] > e.pos[0] and pos[0] < e.pos[0] + e.surf.get_width() and pos[1] > e.pos[1] and pos[1] < e.pos[1] + e.surf.get_height():
				e.gotMouseEvt(mouseType, button)
				if isinstance(e, TextEntry) and mouseType == pygame.MOUSEBUTTONDOWN:
					self.focus = e
					e.isfocused = True
				elif button == 1:
					ID = e.ID

			else:
				e.gotMouseEvt(pygame.MOUSEBUTTONUP, button)
		return ID

	def setFont(self, font):
		self.font = font


	def createButton(self, ID, group_name, pos, bg_img, bg_mousedover_img, bg_pressed_img, colorkey):
		# ID, pos, width, font, surf, text_color, bg_color, caption, pressed_color
		self.elementCategories[group_name].append(Button(ID, group_name, pos, None, bg_img, bg_mousedover_img, bg_pressed_img, colorkey))

	def createTextEntry(self, ID, group_name, pos, width, font, bg_color, text_color):
		self.elementCategories[group_name].append(TextEntry(ID, group_name, pos, width, font, bg_color, text_color))

	def createTextList(self, ID, group_name, pos, width, font, max_number, bg_color, text_color):
		self.elementCategories[group_name].append(TextList(ID, group_name, pos, width, font, max_number, bg_color, text_color, (100)))

	def createLabel(self, ID, group_name, location, bg_img, colorkey):
		self.elementCategories[group_name].append(Label(ID, group_name, location, bg_img, colorkey))

	def render(self, surface):
		#Update all the images of the GUI		  Then draw them
		for i in range (len(self.elementCategories[self.currentGroup])):
			self.elementCategories[self.currentGroup][i].redraw()
			surface.blit(self.elementCategories[self.currentGroup][i].surf, self.elementCategories[self.currentGroup][i].pos)

	def update(self, dtime):
		#updates the elements of the GUI every frame
		for e in self.elementCategories[self.currentGroup]:
			e.update(dtime)





class gui_element(object):


	def __init__(self, ID, group_name, pos, width, font, surf, text_color, bg_color):
		"""Basic Atrributes for Gui Element class"""
		self.ID = ID
		self.pos = pos
		self.width = width
		self.font = font
		self.surf = surf
		self.text_color = text_color
		self.bg_color = bg_color


	def redraw(self):
		"""Redrawing the surface to the screen"""
		pass

	def gotMouseEvt(self, mousetype, button):
		"""Getting mouse events and sending them to Main Program"""
		pass

	def gotKeyEvt(self, Keytype, Key, mod, text):
		"""Getting keyboard events and sending them to Main program"""
		pass

	def update(self, dtime):
		pass







class Button(gui_element):
	"""This class creates a button for the Gui Manager to place on our surface"""
	def __init__(self, ID, group_name, pos, width, bg_img, bg_mousedover_img, bg_pressed_img, colorkey):

		if not isinstance(ID, int):
			raise ValueError("The value passed to ID (" + str(ID) + ") must be an integer")
		if not isinstance(pos, tuple):
			raise TypeError("The values passed to pos (" + str(pos) + ") must be a tuple")
		# if not isinstance(Font, ) or not isinstance(Font, pygame.font.SysFont):
			# raise TypeError("The type of value passed to Font must be a Font object")
		# Need to check for bg img but don't know how
		self.bPressed = False
		self.mouse_over = False
		self.colorkey = colorkey
		self.surf = bg_img
		self.bg_img = bg_img
		self.bg_pressed_img = bg_pressed_img
		self.bg_mousedover_img = bg_mousedover_img
		self.surf.set_colorkey((colorkey))


		#ID, pos, width, font, surf, text_color, bg_color
		gui_element.__init__(self, ID, group_name, pos, None, None, self.surf, None , None)

		self.redraw()

	def redraw(self):
		""" Re-generate self.surf using our internal data. """
		# Fill self.surf with the background color
		if self.bPressed:
			self.surf.set_colorkey((self.colorkey))
			self.surf = self.bg_pressed_img
		elif self.mouse_over:
			self.surf.set_colorkey((self.colorkey))
			self.surf = self.bg_mousedover_img
		else:
			self.surf.set_colorkey((self.colorkey))
			self.surf = self.bg_img




	def gotMouseEvt(self, mouseType, button):
		""" Allows the button to interact with mouse when button is pressed """
		if mouseType == pygame.MOUSEBUTTONDOWN and button == 1:
			self.bPressed = True
			self.mouse_over = False
			self.redraw()

		elif mouseType == pygame.MOUSEBUTTONUP and button == 1:
			self.bPressed = False
			self.redraw()
		elif mouseType == pygame.MOUSEMOTION:
			self.mouse_over = True
			self.redraw()
		else:
			self.mouse_over = False
			self.bpressed = False

		return self.ID






window = pygame.display.set_mode((1280, 704))
class Label(gui_element):

	def __init__(self, ID, group_name, pos, bg_img, colorkey):
		self.bg_img = pygame.image.load(bg_img).convert_alpha()
		self.width= self.bg_img.get_width()
		self.height= self.bg_img.get_height()
		self.ID = ID
		self.pos= pos
		surf = pygame.Surface((self.width, self.height))
		surf.set_colorkey((colorkey))
		surf.blit(self.bg_img, (0,0))


		gui_element.__init__(self, ID , group_name, pos, self.width, None, surf, None, None)

	def render(self):
		pass










timer = 0

class TextEntry(gui_element):

	"""this is a class that prints Text to the screen"""
	def __init__(self,ID, group_name, pos, width, font, bg_color, text_color):
		self.current_str = ""
		self.carrotpos = 0
		self.isfocused= False
		self.blink = 0
		surf = pygame.Surface((width,font.get_linesize()))

		gui_element.__init__(self,ID, group_name, pos, width, font,surf, bg_color,text_color)
		self.redraw()
	#this draws the buttons and the texts to the surface
	def redraw(self):
		self.surf.fill(self.bg_color)
		tempS = self.font.render(self.current_str, False, self.text_color)

		#this is the position of the cusor




		black = (0,0,0)
		tempstr = self.current_str[0:self.carrotpos]
		endpos_y = self.surf.get_height()-1
		x = self.font.size(tempstr)
		if self.isfocused:
			if self.blink >= 30 and self.blink <= 60:
				pygame.draw.line(self.surf, black,(x[0],0),(x[0],endpos_y), 1)
			self.blink +=1
			if self.blink >= 60:
				self.blink = 0
		#bliting to the screen
		self.surf.blit(tempS,(0,0))

	def gotKeyEvt(self,type,key,mod,text):
		#I need to look for backspace and take aways from my current screen

		if key == pygame.K_BACKSPACE and len(self.current_str) > 0:
			self.carrotpos -= 1
			# Delete a character

			self.current_str = self.current_str[:-1]
		elif key == pygame.K_LEFT:
			self.carrotpos -= 1
		elif key == pygame.K_RIGHT:
			self.carrotpos += 1
		elif key == pygame.K_UP:
			self.carrotpos += 1
		elif key == pygame.K_DOWN:
			self.carrotpos -= 1

		elif key not in (pygame.K_BACKSPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
			self.carrotpos += 1
			# Add something to currentStr

			# When shift is pressed and you press keys

			if mod & pygame.KMOD_SHIFT:
				if key == pygame.K_1:
					t = "!"
				elif key == pygame.K_2:
					t = "@"
				elif key == pygame.K_3:
					t = "#"
				elif key == pygame.K_4:
					t = "$"
				elif key == pygame.K_5:
					t = "%"
				elif key == pygame.K_6:
					t ="^"
				elif key == pygame.K_7:
					t = "&"
				elif key == pygame.K_8:
					t = "*"
				elif key == pygame.K_9:
					t = "("
				elif key == pygame.K_SPACE:

					t = " "
				elif key == pygame.K_0:
					t = ")"
				elif key == pygame.K_EQUALS:
					t = "+"
				elif key == pygame.K_PERIOD:
					t = ">"
				elif key == pygame.K_COMMA:
					t = "<"
				elif key == pygame.K_SLASH:
					t = "?"
				elif key == pygame.K_SEMICOLON:
					t = ":"
				elif key == pygame.K_BACKQUOTE:
					t = "~"
				elif key == pygame.K_QUOTE:
					t ="\""
				else:
					t = pygame.key.name(key).upper()

			elif key == pygame.K_KP1:
				t = "1"
			elif key == pygame.K_KP2:
				t = "2"
			elif key == pygame.K_KP3:
				t = "3"
			elif key == pygame.K_KP4:
				t = "4"
			elif key == pygame.K_KP5:
				t = "5"
			elif key == pygame.K_KP6:
				t = "6"
			elif key == pygame.K_KP7:
				t = "7"
			elif key == pygame.K_KP8:
				t = "8"
			elif key == pygame.K_KP9:
				t = "9"
			elif key == pygame.K_KP0:
				t = "0"
			elif key == pygame.K_KP_PERIOD:
				t = "."
			elif key == pygame.K_KP_DIVIDE:
				t = "/"
			elif key == pygame.K_KP_MULTIPLY:
				t = "*"
			elif key == pygame.K_KP_MINUS:
				t = "-"
			elif key == pygame.K_KP_PLUS:
				t = "+"



			elif key == pygame.K_SPACE:
				t = " "
			elif key == pygame.K_RETURN:
				self.current_str = ""
				t = ""
			else:
				t = pygame.key.name(key)
			# this will take away from  the current string
			length_of_text= self.font.size(self.current_str+t)
##			if length_of_text[0] > self.width:
##				return
			#else:
			temp1 = self.current_str[0:self.carrotpos-1]
			temp1 += t
			temp2 = self.current_str[self.carrotpos-1:len(self.current_str)]
			self.current_str = temp1 + temp2
			#self.current_str += t

		self.redraw()









class TextList(gui_element):


	def __init__(self, ID, group_name, pos, width, font, max_number, bg_color, text_color, alphakey):
		#Error Checking
		if not isinstance(ID, int):
			raise ValueError("The value passed to ID (" + str(ID) + ") must be an integer")
		if not isinstance(max_number, int):
			raise ValueError("The value passed to max_number (" + str(max_number) + ") must be an integer")
		if not isinstance(pos, tuple):
			raise TypeError("The values passed to pos (" + str(pos) + ") must be a tuple")
		if not isinstance(width, int):
			raise ValueError("The value passed to width (" + str(width) + ") must be an integer")
		#The Font check isn't working right now for whatever reason
		#if not isinstance(Font, pygame.font.Font) or not isinstance(Font, pygame.font.SysFont):
			#raise TypeError("The type of value passed to Font must be a Font object")

		self.TextListdraw = []
		self.Textdrawstart = 0
		self.alphakey = alphakey
		self.max_number =  max_number
		surf = pygame.Surface((width, (font.get_linesize()*10)))
		surf.convert_alpha()
		surf.set_alpha((self.alphakey))
		gui_element.__init__(self, ID, group_name, pos, width, font, surf, text_color, bg_color)


	def addTextdraw(self, text):
		"""Should be called when the user presses the enter key to change the text"""
		if( len(self.TextListdraw) >= self.max_number):
			#Pull off the first line if it is over max_number
			self.TextListdraw.pop(len(self.TextListdraw)-1)
			#The add to the list
			self.TextListdraw.insert(0,text)
		else:
			#Otherwise just a normal add
			self.TextListdraw.insert(0,text)

		self.redraw()

	def redraw(self):
		"""Regenerate surface"""
		temp_surf = pygame.Surface((self.width,(10*self.font.get_linesize())))
		#Drawing the text on the text path
		newList = []
		for i in range(len(self.TextListdraw)):
			if len(self.TextListdraw[i]) > 65:
				k = int(len(self.TextListdraw[i]) / 65)
				if len(self.TextListdraw[i]) % 65 > 0:
					k += 1
				for b in range(k,0,-1):
					tmpTxt = self.TextListdraw[i][(b-1)*65:b*65]
					newList.append(tmpTxt)
			else:
				newList.append(self.TextListdraw[i])
				#del self.TextListdraw[i]
		self.TextListdraw = newList



		for i in range ((len(self.TextListdraw)-1),-1, -1):
			temp_surf2 = self.font.render(self.TextListdraw[i], True, self.bg_color)
			temp_surf.blit(temp_surf2,(0, (10-(i+1))*self.font.get_linesize()))
		self.surf.blit(temp_surf, (0,0))




	def gotKeyEvt(self, Keytype, Key, mod, text):
		if Keytype == pygame.KEYDOWN:
			if Key == pygame.K_RETURN:
				self.addTextdraw(text)


if __name__ == "__main__":
	pygame.display.init()
	pygame.font.init()
	screen = pygame.display.set_mode((1280,720))
	testGUI = GUIManager()
	testGUI.setFont(pygame.font.SysFont("Courier New", 20))
	done = False
	#this is for holding the backspace
	pygame.key.set_repeat(500, 50)
	#You need to create the TextList before entry because, if you don't it will clear the string before sending it to the textList
	# This is for Main screen
	#testGUI.createLabel(2, "title", (0,0), "gui_inventory.png", (0, 0, 0))
	#testGUI.createTextList(2, "title", (10,400), 300, 50)
	#def createButton(self, ID, group_name, pos, bg_img, bg_pressed_img, bg_mousedover_img, colorkey):
	testGUI.createButton(2, "title", (550, 300), pygame.image.load("GUIassets\\Login\\button_login_1.png"), pygame.image.load("GUIassets\\Login\\button_login_2.png"),  pygame.image.load("GUIassets\\Login\\button_login_3.png"),  (0,255,0) )

	#testGUI.createTextEntry(3, "title", (10,100), 400)
	#testGUI.createTextEntry(4, "title", (700,500), 400)

	# This is for the Login Screen
	#testGUI.createTextEntry(2, "start_menu", (500, 300), 400)
	#testGUI.createTextEntry(3, "start_menu", (500, 400), 400)
	#testGUI.createTextEntry(4, "start_menu", (500, 500), 400)


	# Game Screen
	clock = pygame.time.Clock()
	while not done:
		screen.fill((255,255,255))
		dtime = clock.tick()
		eList = pygame.event.get()
		for e in eList:
			hitID = None

			if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
				if e.key == pygame.K_ESCAPE:
					done = True
				else:
					testGUI.onKeyEvent(e.type, e.key,e.mod)
			elif e.type == pygame.MOUSEBUTTONDOWN:
				hitID = testGUI.onMouse(pygame.MOUSEBUTTONDOWN, e.button, e.pos)
			elif e.type == pygame.MOUSEBUTTONUP:
				hitID = testGUI.onMouse(pygame.MOUSEBUTTONUP, e.button, e.pos)
			elif e.type == pygame.MOUSEMOTION:
				hitID == testGUI.onMouse(pygame.MOUSEMOTION, None, e.pos)

			if hitID == 1:
				done = True

		testGUI.update(dtime)
		testGUI.render(screen)
		pygame.display.flip()

	pygame.display.quit()

