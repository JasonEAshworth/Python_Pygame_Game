#jordan c Johnson
#lab 5 part 1 text scroller

import pygame

#create a list of strings
text = [ "-13,000"]

#initialization
pygame.font.init()
pygame.display.init()

courierFont = pygame.font.SysFont("Courier New", 20)
screen = pygame.display.set_mode((800,600))
done = False
top = 600


#clock object
clockObj = pygame.time.Clock()
#my font object
courierFont = pygame.font.SysFont("Courier New", 20)
nextline = 0
#game loop
while done == False:
    screen.fill((0,0,0))
    dT = clockObj.tick() / 1000
    #the rate that top is moving
    top -= 100*dT
    tempS =""

    nextline = 0
    #get user input
    eList = pygame.event.get()
    # ...cycle through all events
    for e in eList:
        # e.type is an (integer) variable indicating the type of event.
        if e.type == pygame.QUIT:
            done = True
        #elif e.type == pygame.KEYUP:
        #    KeyList[e.key] = False
        elif e.type == pygame.KEYDOWN:
            #KeyList[e.key] = True
            #print(e.key)
            if e.key == pygame.K_ESCAPE:
                done = True
    #This gets and prints one line of text to the screen
    currentline = 0
    while currentline < len(text):


        y = top + nextline
        #length = tempS.get_width()/2
        # ...Render the fps in the lower-left corner
        color = (255,255,255)
        #color fade
        if y < 0 :
            val = 0
        elif y < 200:
            val = (y/200)*255

        elif y < 400:
            val = 255

        elif y < 600:
            val = 255-((y-400)/200)*255
        else:
            val  = 0
        color = (val,val,val)

        tempS = courierFont.render(text[currentline], False, color)

        screen.blit(tempS, (400 - tempS.get_width()/2,y))

        currentline += 1
        nextline += 20




#flip the screen
    pygame.display.flip()


#ShutDown
pygame.display.quit()
