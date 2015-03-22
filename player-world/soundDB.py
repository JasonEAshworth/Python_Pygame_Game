import pygame

done = False

pygame.init()
pygame.mixer.init()

##window = pygame.display.set_mode((100, 100))

# Dictionary of sounds
# Keys are:
#	  mage: sounds from mage_sounds dictionary
#	  cleric: sounds from cleric_sounds dictionary
#	  warrior: sounds from warrior_sounds dictionary
#	  thief: sounds from thief_sounds dictionary
#     hub: sounds from enemies in hub
#     forest: sounds from enemies in forest
#     sea: sounds from enemies in sea
#     glacier: sounds from enemies in glacier
#     wasteland: sounds from enemies in wasteland
#     volcano: sounds from enemies in volcano
#     finalBoss: sounds from enemies in Doom's Path and Doom's Chasm

soundDB = {}

# Dictionaries for each class that will go into the main soundDB
# Player sound dictionaries will have these keys:
#	  0: standard attack sound
#	  1: first ability sound
#	  2: second ability sound
#	  3: third ability sound
#	  4: fourth ability sound
#	  5: final ability sound

mage_sounds = {}
cleric_sounds = {}
thief_sounds = {}
warrior_sounds = {}

# Dictionaries for enemies in each zone, key name will be the enemy name.
hub_sounds = {}
forest_sounds = {}
sea_sounds = {}
glacier_sounds = {}
wasteland_sounds = {}
volcano_sounds = {}
finalBoss_sounds = {}

# Mage
mage_sounds["0"] = pygame.mixer.Sound("Player Sounds\\CasterAttack.wav")
mage_sounds["1"] = pygame.mixer.Sound("Player Sounds\\MageFireball.wav")
mage_sounds["2"] = pygame.mixer.Sound("Player Sounds\\MageLightning.wav")
mage_sounds["3"] = pygame.mixer.Sound("Player Sounds\\MageCurse.wav")
mage_sounds["4"] = pygame.mixer.Sound("Player Sounds\\MageBlizzard.wav")
mage_sounds["5"] = pygame.mixer.Sound("Player Sounds\\MageTrinity.wav")

soundDB["mage"] = mage_sounds


# Warrior
warrior_sounds["0"] = pygame.mixer.Sound("Player Sounds\\WarriorAttack.wav")
warrior_sounds["1"] = pygame.mixer.Sound("Player Sounds\\WarriorSweep.wav")
warrior_sounds["2"] = pygame.mixer.Sound("Player Sounds\\WarriorTaunt.wav")
warrior_sounds["3"] = pygame.mixer.Sound("Player Sounds\\WarriorPowerSwing.wav")
warrior_sounds["4"] = pygame.mixer.Sound("Player Sounds\\WarriorShout.wav")
warrior_sounds["5"] = pygame.mixer.Sound("Player Sounds\\WarriorBerserk.wav")

soundDB["warrior"] = warrior_sounds

# Thief
thief_sounds["0"] = pygame.mixer.Sound("Player Sounds\\ThiefAttack.wav")
thief_sounds["1"] = pygame.mixer.Sound("Player Sounds\\ThiefPoisonDart.wav")
thief_sounds["2"] = pygame.mixer.Sound("Player Sounds\\ThiefSmokeBomb.wav")
thief_sounds["3"] = pygame.mixer.Sound("Player Sounds\\ThiefCloak.wav")
thief_sounds["4"] = pygame.mixer.Sound("Player Sounds\\ThiefThrowBomb.wav")
thief_sounds["5"] = pygame.mixer.Sound("Player Sounds\\ThiefNinjaJump.wav")

soundDB["thief"] = thief_sounds

# Cleric
cleric_sounds["0"] = pygame.mixer.Sound("Player Sounds\\CasterAttack.wav")
cleric_sounds["1"] = pygame.mixer.Sound("Player Sounds\\ClericHeal.wav")
cleric_sounds["2"] = pygame.mixer.Sound("Player Sounds\\ClericTransfusion.wav")
cleric_sounds["3"] = pygame.mixer.Sound("Player Sounds\\ClericSmite.wav")
cleric_sounds["4"] = pygame.mixer.Sound("Player Sounds\\ClericHealOverTime.wav")
cleric_sounds["5"] = pygame.mixer.Sound("Player Sounds\\ClericBuff.wav")

soundDB["cleric"] = cleric_sounds

# Hub
hub_sounds["cow"] = pygame.mixer.Sound("Monster Unique Sounds\\cow.wav")
hub_sounds["pig"] = pygame.mixer.Sound("Monster Unique Sounds\\pig.wav")
hub_sounds["unicorn"] = pygame.mixer.Sound("Monster Unique Sounds\\unicorn.wav")

soundDB["hub"] = hub_sounds

# Forest
forest_sounds["wolf"] = pygame.mixer.Sound("Monster Unique Sounds\\wolf.wav")
#forest_sounds["bandit"] = pygame.mixer.Sound("Monster Unique Sounds\\bandit.wav")
forest_sounds["bear"] = pygame.mixer.Sound("Monster Unique Sounds\\bear.wav")
forest_sounds["panther"] = pygame.mixer.Sound("Monster Unique Sounds\\panther.wav")
forest_sounds["werewolf"] = pygame.mixer.Sound("Monster Unique Sounds\\werewolf.wav")
forest_sounds["ghost"] = pygame.mixer.Sound("Monster Unique Sounds\\ghost.wav")
#forest_sounds["undead"] = pygame.mixer.Sound("Monster Unique Sounds\\undead.wav")
#forest_sounds["darkwind"] = pygame.mixer.Sound("Monster Unique Sounds\\darkwind.wav")

soundDB["forest"] = forest_sounds

# Sea
#sea_sounds["pirate"] = pygame.mixer.Sound("Monster Unique Sounds\\pirate.wav")
sea_sounds["cannon"] = pygame.mixer.Sound("Monster Unique Sounds\\cannon.wav")
#sea_sounds["magepirate"] = pygame.mixer.Sound("Monster Unique Sounds\\magepirate.wav")
#sea_sounds["brutepirate"] = pygame.mixer.Sound("Monster Unique Sounds\\brutepirate.wav")
#sea_sounds["seadrake"] = pygame.mixer.Sound("Monster Unique Sounds\\seadrake.wav")
sea_sounds["native"] = pygame.mixer.Sound("Monster Unique Sounds\\native.wav")
sea_sounds["medicineman"] = pygame.mixer.Sound("Monster Unique Sounds\\medicineman.wav")
sea_sounds["chief"] = pygame.mixer.Sound("Monster Unique Sounds\\chief.wav")
#sea_sounds["stormfire"] = pygame.mixer.Sound("Monster Unique Sounds\\stormfire.wav")

soundDB["sea"] = sea_sounds

# Glacier
glacier_sounds["polarbear"] = pygame.mixer.Sound("Monster Unique Sounds\\polarbear.wav")
glacier_sounds["wisp"] = pygame.mixer.Sound("Monster Unique Sounds\\wisp.wav")
glacier_sounds["yeti"] = pygame.mixer.Sound("Monster Unique Sounds\\yeti.wav")
#glacier_sounds["frostbandit"] = pygame.mixer.Sound("Monster Unique Sounds\\bandit.wav")
glacier_sounds["spirit"] = pygame.mixer.Sound("Monster Unique Sounds\\spirit.wav")
glacier_sounds["mammoth"] = pygame.mixer.Sound("Monster Unique Sounds\\mammoth.wav")
#glacier_sounds["skyekraken"] = pygame.mixer.Sound("Monster Unique Sounds\\skyekraken.wav")

soundDB["glacier"] = glacier_sounds

# Wasteland
#wasteland_sounds["mole"] = pygame.mixer.Sound("Monster Unique Sounds\\mole.wav")
#wasteland_sounds["giantlizard"] = pygame.mixer.Sound("Monster Unique Sounds\\giantlizard.wav")
#wasteland_sounds["giantworm"] = pygame.mixer.Sound("Monster Unique Sounds\\giantworm.wav")
#wasteland_sounds["livingcactus"] = pygame.mixer.Sound("Monster Unique Sounds\\livingcactus.wav")
#wasteland_sounds["zombie"] = pygame.mixer.Sound("Monster Unique Sounds\\undead.wav")
#wasteland_sounds["necromancer"] = pygame.mixer.Sound("Monster Unique Sounds\\necromancer.wav")
#wasteland_sounds["golem"] = pygame.mixer.Sound("Monster Unique Sounds\\golem.wav")
#wasteland_sounds["furyclaw"] = pygame.mixer.Sound("Monster Unique Sounds\\furyclaw.wav")

soundDB["wasteland"] = wasteland_sounds

# Volcano
#volcano_sounds["orc"] = pygame.mixer.Sound("Monster Unique Sounds\\orc.wav")
volcano_sounds["goblin"] = pygame.mixer.Sound("Monster Unique Sounds\\goblin.wav")
volcano_sounds["whelp"] = pygame.mixer.Sound("Monster Unique Sounds\\whelp.wav")
volcano_sounds["dragonkin"] = pygame.mixer.Sound("Monster Unique Sounds\\dragonkin.wav")
#volcano_sounds["pyrospirit"] = pygame.mixer.Sound("Monster Unique Sounds\\pyrospirit.wav")
#volcano_sounds["demon"] = pygame.mixer.Sound("Monster Unique Sounds\\demon.wav")
#volcano_sounds["gorgon"] = pygame.mixer.Sound("Monster Unique Sounds\\gorgon.wav")
#volcano_sounds["bloodflight"] = pygame.mixer.Sound("Monster Unique Sounds\\bloodflight.wav")

soundDB["volcano"] = volcano_sounds

# Final Boss
#finalBoss_sounds["drayt1"] = pygame.mixer.Sound("Monster Unique Sounds\\drayt1.wav")
#finalBoss_sounds["drayt2"] = pygame.mixer.Sound("Monster Unique Sounds\\drayt2.wav")
#finalBoss_sounds["drayt3"] = pygame.mixer.Sound("Monster Unique Sounds\\drayt3.wav")
finalBoss_sounds["darkwhelp"] = pygame.mixer.Sound("Monster Unique Sounds\\darkwhelp.wav")
finalBoss_sounds["dragonkin"] = pygame.mixer.Sound("Monster Unique Sounds\\dragonkin.wav")
#finalBoss_sounds["deathbringer1"] = pygame.mixer.Sound("Monster Unique Sounds\\deathbringer1.wav")
#finalBoss_sounds["deathbringer2"] = pygame.mixer.Sound("Monster Unique Sounds\\deathbringer2.wav")
#finalBoss_sounds["deathbringer3"] = pygame.mixer.Sound("Monster Unique Sounds\\deathbringer3.wav")

soundDB["finalBoss"] = finalBoss_sounds

### Test loop
##while not done:
##	evtList = pygame.event.get()
##
##	for evt in evtList:
##		if evt.type == pygame.QUIT:
##			done = True
##		elif evt.type == pygame.KEYDOWN:
##			if evt.key == pygame.K_a:
##			   soundDB["cleric"]["3"].play()
##			elif evt.key == pygame.K_b:
##			   soundDB["glacier"]["wisp"].play()
##			elif evt.key == pygame.K_ESCAPE:
##				 done = True
##
##
##pygame.mixer.quit()
##pygame.quit()