import pygame
import random


class Player(object):
    fontObj = None

    def __init__(self, uname):
        self.uname = uname
        self.horizMovement = "None"
        self.vertMovement = "None"
        self.x = random.randint(20, 780)
        self.y = random.randint(20, 580)
        self.moveSpeed = 100.0
        self.active = False
        self.color = [random.randint(100,255), random.randint(100,255), random.randint(100,255)]

        # Shadow values.  Used to detect if we need to transmit data to a client/server
        self.oldHorizMovement = None
        self.oldVertMovement = None
        self.oldUname = None
        self.oldX = None
        self.oldY = None
        self.oldActive = None
        self.oldColor = None

        # Create the font
        if Player.fontObj == None and pygame.font.get_init():
            Player.fontObj = pygame.font.SysFont("Courier New", 12)
            
    def __str__(self):
        return "[Player." + self.uname + ".(" + str(self.x) + "," + \
                           str(self.y) + ").(" + self.horizMovement + "," + \
                           self.vertMovement + ").(" + str(self.color[0]) + \
                           "," + str(self.color[1]) + "," + \
                           str(self.color[2]) + ")." + str(self.active) + "]"

    def render(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), 20, 0)
        if self.active:
            pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), 23, 1)
        if Player.fontObj:
            tempS = Player.fontObj.render(str(self.uname), False, (255,255,255), (0,0,0))
            surf.blit(tempS, (int(self.x) - tempS.get_width()/2, int(self.y) - tempS.get_height()/2))

    def setMove(self, horiz=None, vert=None):
        if horiz:
            self.horizMovement = horiz
        if vert:
            self.vertMovement = vert

    def update(self, dT):
        if self.horizMovement == "Left":
            self.x -= self.moveSpeed * dT
        elif self.horizMovement == "Right":
            self.x += self.moveSpeed * dT

        if self.vertMovement == "Up":
            self.y -= self.moveSpeed * dT
        elif self.vertMovement == "Down":
            self.y += self.moveSpeed * dT


    def serialize(self, level, updateOldValues=True):
        """ If level==0, only serialize those things that need to be sent from client to server (or vice-versa) during normal updates
            If level==1, only serialize those things that have changed.
            If level==2, serialize everything.
            If level==3, serialize those things that need to go in the account database (on the server)
            In either case, if updateOldValues is true, update the "shadow" copies of attributes. """
        if level not in [0, 1, 2, 3]:
            raise ValueError("Level must be 0-3")

        s = ""

        if level == 0 or level == 1:
            if self.oldHorizMovement == None or self.horizMovement != self.oldHorizMovement:   s += ":hmove=" + self.horizMovement
            if self.oldVertMovement == None or self.vertMovement != self.oldVertMovement:       s += ":vmove=" + self.vertMovement
            if level == 0:
                if self.oldActive == None or self.active != self.oldActive:                       s += ":active=" + str(self.active)
            if len(s) > 0:
                s = s[1:]
        if level == 1:
            s = ""
            if self.oldUname == None or self.uname != self.oldUname:      s += ":uname=" + str(self.uname)
            if self.oldX == None or int(self.x) != int(self.oldX):        s += ":x=" + str(int(self.x))
            if self.oldY == None or int(self.y) != int(self.oldY):        s += ":y=" + str(int(self.y))
            if self.oldActive == None or self.active != self.oldActive:   s += ":active=" + str(self.active)
            if self.oldColor == None or self.color != self.oldColor:      s += ":c0=" + str(self.color[0]) + ":c1=" + str(self.color[1]) + ":c2=" + str(self.color[2])
            if len(s) > 0:
                s = s[1:]
        if level == 2:
            s = "uname=" + self.uname + ":x=" + str(int(self.x)) + ":y=" + str(int(self.y)) + ":active=" + str(self.active)
            s += ":c0=" + str(self.color[0]) + ":c1=" + str(self.color[1]) + ":c2=" + str(self.color[2])
            s += ":hmove=" + self.horizMovement + ":vmove=" + self.vertMovement
        if level == 3:
            s = "uname=" + self.uname + ":x=" + str(int(self.x)) + ":y=" + str(int(self.y)) 
            s += ":c0=" + str(self.color[0]) + ":c1=" + str(self.color[1]) + ":c2=" + str(self.color[2])


        if updateOldValues:
            self.oldHorizMovement = self.horizMovement
            self.oldVertMovement = self.vertMovement
            self.oldUname = self.uname
            self.oldX = self.x
            self.oldY = self.y
            self.oldActive = self.active
            self.oldColor = self.color[:]

        return s

    def deserialize(self, s):
        #print("De-serializing '" + s + "'")
        #if s.count(":") == 0:
        #   return    # Nothing to de-serialize!
        elem = s.split(":")
        for e in elem:
            if not e.find("=") or e == "":
                continue
            key, value = e.split("=")
            if key == "hmove":
                self.horizMovement = value
            elif key == "vmove":
                self.vertMovement = value
            elif key == "active":
                if value[0] == "T":
                    self.active = True
                else:
                    self.active = False
            elif key == "x":
                self.x = float(value)
            elif key == "y":
                self.y = float(value)
            elif key == "c0":
                self.color[0] = int(value)
            elif key == "c1":
                self.color[1] = int(value)
            elif key == "c2":
                self.color[2] = int(value)
            elif key == "uname":
                self.uname = value
            else:
                raise ValueError("Undefined deserialize key ('" + key + "')")