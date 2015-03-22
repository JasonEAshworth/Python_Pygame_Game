#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     
#
# Author:      vencillv
#
# Created:     19/04/2012
# Copyright:   (c) vencillv 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import soundDB
import pygame

done = False

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((100, 100))


while not done:
	evtList = pygame.event.get()

	for evt in evtList:
		if evt.type == pygame.QUIT:
			done = True
		elif evt.type == pygame.KEYDOWN:
			if evt.key == pygame.K_a:
			   soundDB["warrior"]["3"].play()
			elif evt.key == pygame.K_ESCAPE:
				 done = True


pygame.mixer.quit()
pygame.quit()
    

