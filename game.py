"""
Kofi Darfour jaf7th

Sonia Birate trj8ap

What game is:
Two person player game that has a shooter ship
on each side. you cant cross over the other half but
you can move around while dodging enemies and collecting
power ups/buffs. The goal of the game is to deplete the other's health count to 0.
Neither player can cross over into the others half of the stage.

How to play: 
- player one uses WASD key controls
- player two uses arrow key controls
- beams shoot as soon as it leaves game borders and reloads, both automatically
- must maneuver to get your beam to hit opposing player to take health to zero
- must maneuver in order to hit collectibles for buffs and avoid enemies for debuffs
- loser is who ever's health reaches zero

User input: Using WSAD and arrow keys for movement for each player

Game Over: When one player runs our of health they lose, triggering the game over. 

Graphics: 8bit graphics from the internet (obstacle sprites and player sprites)

Collectibles: powerups and buffs (boost and health)

Enemies: Have one or more characters that can hinder the player from completing goal (damage and slomo)

Two Players Simultaneously: 2 player game

Sprite animation: when taking in directional inputs, the sprite changes for each player

Changes: 
- since CP2 we fixed the glitch that made the game over end not end with the losing player 
being at 0 health but 1 instead.
- added collectibles (boost and health)
- added enemies (slomo and damage)
- made collectibles/enemies have set spawn points but to come out randomly at specific intervals
- added a pop up to show when slomo/boost effects were active
- changed one of the additional features from health bar to enemies


"""

import uvage
import random

playerOneHealth = 100
playerTwoHealth = 100
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

#effect notices, purposley placed out of bounds
slomoNotice_p1 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")
boostNotice_p1 = uvage.from_text(1000, 900, "BOOST ACTIVE!!!", 30, "green")

slomoNotice_p2 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")
boostNotice_p2 = uvage.from_text(1000, 900, "BOOST ACTIVE!!!", 30, "green")

# box barriers
barrierLeft = uvage.from_color(-20, 300, "black", 50, 650)  # left wall
barrierRight = uvage.from_color(820, 300, "black", 50, 650)  # right wall
barrierTop = uvage.from_color(400, -25, "black", 850, 50)  # top wall
barrierBottom = uvage.from_color(400, 625, "black", 850, 50)  # bottom wall
barrierMiddle = uvage.from_color(400, 300, "black", 5, 600)  # middle wall

walls = [barrierLeft, barrierRight, barrierBottom, barrierMiddle, barrierTop]

players_sprite_sheet = uvage.load_sprite_sheet("playerImage.png", 4, 7)

# player sprites and beams
playerOne = uvage.from_image(200, 475, players_sprite_sheet[10])
playerOne.scale_by(0.75)  # make sprites smaller due to game dimensions (.75 of its origninal size)

playerTwo = uvage.from_image(600, 100, players_sprite_sheet[10])
playerTwo.scale_by(0.75)  # make sprites smaller due to game dimensions
playerTwo.flip()  # make player2 sprite face the correct direction (players operate on opposite sides)

p1Beam = uvage.from_color(playerOne.x + 50, playerOne.y, "purple", 12, 6)
p2Beam = uvage.from_color(playerTwo.x - 50, playerTwo.y, "blue", 12, 6)

playerBeams = [p1Beam, p2Beam]
#obstacle sprites and powerups
speedSprite = uvage.from_image(1500, 900, "speedSprite.png")
speedSprite.scale_by(.1)
damageSprite = uvage.from_image(1500, 900, "damageSprite.png")
damageSprite.scale_by(0.2)
slomoSprite = uvage.from_image(1500, 900, "slomoSprite.png")
slomoSprite.scale_by(.1)
healthSprite = uvage.from_image(1500, 900, "healthSprite.png")
healthSprite.scale_by(0.2)

obstacle_sprites = [speedSprite, damageSprite, slomoSprite, healthSprite]

#obstacle sprites spawn points
leftSpawn_dLocations = [[-5,150],[100,-5],[250,-5]] # downward slope spawn locations from left
rightSpawn_dLocations = [[805,150],[700,-5],[650,-5]] # downward slope spawn locations from right

downSlopes = [leftSpawn_dLocations, rightSpawn_dLocations] # list of downward slopes

leftSpawn_uLocations = [[-5,450], [100,605], [250,605]] # upward slope spawn locations from left
rightSpawn_uLocations = [[805,450], [700, 605], [650, 605]] # upward slope spawn locations from right

upSlopes = [leftSpawn_uLocations, rightSpawn_uLocations] # list of upward slopes

up_down_Slopes = [upSlopes, downSlopes] # both up and down

#conditions for effects

slope = bool # decides upward or downward slope for obstacle sprites
side =  bool

beamSpeed_p1 = 12 # beam for player 1 speed
beamSpeed_p2 = 12 # beam for player 2 speed

boost_p1 = False #tracks whether boost/slomo effect is on and changes sprites for players (lines 119-123)
boost_p2 = False

slomo_p1 = False
slomo_p2 = False

boostActive_p1 = False # tracks whether or not boost or speed is active (lines 125-129)
slomoActive_p1 = False

boostActive_p2 = False
slomoActive_p2 = False

#tick timer counts
spriteSpawnCount = 0 # count for random sprite spawns
effectTimerCount_p1 = 0 # count for effect timer
effectTimerCount_p2 = 0 # count for effect timer



def setup():
    global playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    global speedSprite, damageSprite, healthSprite, slomoSprite
    camera.draw(uvage.from_text(150, 40, "Player One Health: " + str(int(playerOneHealth)), 30, "green"))
    camera.draw(uvage.from_text(550, 40, "Player Two Health: " + str(int(playerTwoHealth)), 30, "green"))
    camera.draw(speedSprite)
    camera.draw(slomoSprite)
    camera.draw(damageSprite)
    camera.draw(healthSprite)
    createBeams()


def playerOneMovement():
    global walls
    global boost_p1, slomo_p1, boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2

    for wall in walls:  # makes barriers solid when hitting player
        playerOne.move_to_stop_overlapping(wall)

    if uvage.is_pressing("a"):  # left arrow (backwards)
        if boost_p1:
            playerOne.speedx -= .5
        elif slomo_p1:
            playerOne.speedx -= .25
        else:
            playerOne.speedx -= .35
        playerOne.image = players_sprite_sheet[10]

    if uvage.is_pressing("d"):  # right arrow (forward facing)
        if boost_p1:
            playerOne.speedx += 1
            playerOne.image = players_sprite_sheet[0]  # double engine for boost
        elif slomo_p1:
            playerOne.speedx += .25
            playerOne.image = players_sprite_sheet[10]
        else:
            playerOne.speedx += .5
            playerOne.image = players_sprite_sheet[1]

    if uvage.is_pressing("w"):  # up arrow
        if boost_p1:
            playerOne.speedy -= 1
            playerOne.image = players_sprite_sheet[9]  # double engine for boost
        elif slomo_p1:
            playerOne.speedy -= .25
            playerOne.image = players_sprite_sheet[15]
        else:
            playerOne.speedy -= .5
            playerOne.image = players_sprite_sheet[6]

    if uvage.is_pressing("s"):  # down arrow
        if boost_p1:
            playerOne.speedy += 1
            playerOne.image = players_sprite_sheet[14]  # double engine for boost
        elif slomo_p1:
            playerOne.speedy += .25
            playerOne.image = players_sprite_sheet[12]
        else:
            playerOne.speedy += .5
            playerOne.image = players_sprite_sheet[3]
    playerOne.move_speed()


def playerTwoMovement():
    global walls
    global boost_p2, slomo_p2, boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2

    for wall in walls:  # makes barriers solid when hitting player 
        playerTwo.move_to_stop_overlapping(wall)

    if uvage.is_pressing('right arrow'):  # (going backwards) no engine sprites
        if boost_p2:
            playerTwo.speedx += .5
        elif slomo_p2:
            playerTwo.speedx += .25
        else:
            playerTwo.speedx += .35
        playerTwo.image = players_sprite_sheet[10]

    if uvage.is_pressing('left arrow'):  # forward Facing
        if boost_p2:
            playerTwo.speedx -= 1
            playerTwo.image = players_sprite_sheet[0]  # double engine for boost
        elif slomo_p2:
            playerTwo.speedx -= .25
            playerTwo.image = players_sprite_sheet[10]  # no engine for slomoSprite
        else:
            playerTwo.speedx -= .5
            playerTwo.image = players_sprite_sheet[1]

    if uvage.is_pressing('up arrow'):
        if boost_p2:
            playerTwo.speedy -= 1
            playerTwo.image = players_sprite_sheet[9]  # double engine for boost
        elif slomo_p2:
            playerTwo.speedy -= .25
            playerTwo.image = players_sprite_sheet[15]  # no engine for slomoSprite
        else:
            playerTwo.speedy -= .5
            playerTwo.image = players_sprite_sheet[6]
    if uvage.is_pressing('down arrow'):
        if boost_p2:
            playerTwo.speedy += 1
            playerTwo.image = players_sprite_sheet[14]  # double engine for boost
        elif slomo_p2:
            playerTwo.speedy += .25
            playerTwo.image = players_sprite_sheet[12]  # no engine for slomoSprite
        else:
            playerTwo.speedy += .5
            playerTwo.image = players_sprite_sheet[3]
    playerTwo.move_speed()


def createBeams():
    global p1Beam, p2Beam
    camera.draw(p1Beam)
    camera.draw(p2Beam)


def handle_beams(): # keeps beam speed consisten but move in opposite directions
    global p1Beam, p2Beam
    p1Beam.speedx = beamSpeed_p1
    p2Beam.speedx = -(beamSpeed_p2)

    p1Beam.move_speed()
    p2Beam.move_speed()


def outOfBounds_p1Beam():
    return p1Beam.x > 800


def outOfBounds_p2Beam():
    return p2Beam.x < 0


def reload_p1Beam():
    global p1Beam
    p1Beam = uvage.from_color(playerOne.x + 50, playerOne.y, "purple", 12, 6) 
    # moves beam back in front of player


def reload_p2Beam():
    global p2Beam
    p2Beam = uvage.from_color(playerTwo.x - 50, playerTwo.y, "blue", 12, 6)
    # moves beam back in front of player

def set_spawnPoints():
    global leftSpawn_dLocations, rightSpawn_dLocations, slope, side
    global leftSpawn_uLocations, rightSpawn_uLocations, upSlopes, downSlopes, up_down_Slopes
    up_or_down = random.randint(0,1)
    left_or_right = random.randint(0,1)
    coordinates = random.randint(0,2)

    x = up_down_Slopes[up_or_down][left_or_right][coordinates][0] # gets x coordinate
    y = up_down_Slopes[up_or_down][left_or_right][coordinates][1] # gets y coordinate


    slope = up_or_down == 0
    #stores slope as True aka upwards if 0 
    #stores slope as False aka downwards if 1
    side = left_or_right == 0 
    #stores side as True aka left if 0 
    #stores side as False aka right if 1

    return x, y
    # returns a tuple containing...
    # (x coordinate, y coordinate)

def speedBoost():
    # increases this speed when hitting this buff
    # Uses "speedSprite.png"
    global speedSprite, playerOne, playerTwo, boost_p1, boost_p2, slomo_p1, slomo_p2
    global boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2
    x, y = set_spawnPoints()
    speedSprite = uvage.from_image(x, y, "speedSprite.png")
    speedSprite.scale_by(.1)
    
    
    
def speedBoostMove():
    global speedSprite, playerOne, playerTwo, boost_p1, boost_p2, slomo_p1, slomo_p2
    global boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2
    global effectTimerCount_p1, effectTimerCount_p2, slope, walls, side
    if speedSprite.touches(playerOne): 
    #when the sprite touches player this function activates the boost effect,
    #changing the player character sprite and setting off the effect timer
        speedSprite = uvage.from_image(1500, 900, "speedSprite.png") # moves sprite out of bounds
        speedSprite.scale_by(.1)
        boost_p1 = True # turns on boost effect and changes sprite
        slomo_p1 = False # turns off slomo effect if active
        boostActive_p1 = True # sets off effect timer for boost
        slomoActive_p1 = False # if slomo is active it turns off
        effectTimerCount_p1 = 0 # sets timer to zero for reassurance
        #every move function for speed/slomo sprites follow the same patter but for its specific
        #player/effect

    if speedSprite.touches(playerTwo):
        speedSprite = uvage.from_image(1500, 900, "speedSprite.png") # moves sprite out of bounds
        speedSprite.scale_by(.1)
        boost_p2 = True
        slomo_p2 = False
        boostActive_p2 = True
        slomoActive_p2 = False
        effectTimerCount_p2 = 0
    #this if statement spawns the sprite at a random location preset above and changes 
    #its movement appropriately with the spawn point
    # every move function for an obstacle sprite works the same way
    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            speedSprite.speedy = -5
            speedSprite.speedx = 5
        elif not side: # if right side condiiton 
            speedSprite.speedy = -5
            speedSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            speedSprite.speedy = 5
            speedSprite.speedx = 5
        elif not side: # if right side condiiton 
            speedSprite.speedy = 5
            speedSprite.speedx = -5
    speedSprite.move_speed()

def speedReduce():
    # reduces speed when hitting this debuff
    # uses "slomoSprite.png" sprite
    global slomoSprite, playerOne, playerTwo, boost_p1, boost_p2, slomo_p1, slomo_p2
    global boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2
    x, y = set_spawnPoints() #sets x and y to the return values
    slomoSprite = uvage.from_image(x,y, "slomoSprite.png")
    slomoSprite.scale_by(.1)

def speedReduceMove():
    global slomoSprite, playerOne, playerTwo, boost_p1, boost_p2, slomo_p1, slomo_p2
    global boostActive_p1 , slomoActive_p1, boostActive_p2 , slomoActive_p2, slope, walls, side
    global effectTimerCount_p1, effectTimerCount_p2

    if slomoSprite.touches(playerOne):
        slomoSprite = uvage.from_image(1500, 900, "slomoSprite.png") #moves sprite out of bounds
        slomoSprite.scale_by(.1)
        slomo_p1 = True
        boost_p1 = False
        boostActive_p1 = False
        slomoActive_p1 = True
        effectTimerCount_p1 = 0
    if slomoSprite.touches(playerTwo):
        slomoSprite = uvage.from_image(1500, 900, "slomoSprite.png") # moves sprite out of bounds
        slomoSprite.scale_by(.1)
        slomo_p2 = True
        boost_p2 = False
        boostActive_p2 = False
        slomoActive_p2 = True
        effectTimerCount_p2 = 0

    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            slomoSprite.speedy = -5
            slomoSprite.speedx = 5
        elif not side: # if right side condiiton 
            slomoSprite.speedy = -5
            slomoSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            slomoSprite.speedy = 5
            slomoSprite.speedx = 5
        elif not side: # if right side condiiton 
            slomoSprite.speedy = 5
            slomoSprite.speedx = -5

    slomoSprite.move_speed()


def healthIncrease():
    # adds health to player when hitting this buff
    # uses "healthSprite.png" sprite
    global healthSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth
    x, y = set_spawnPoints()
    healthSprite = uvage.from_image(x, y, "healthSprite.png")
    healthSprite.scale_by(0.2)

def healthIncreaseMove():
    global healthSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth, slope, side, walls
    if healthSprite.touches(playerOne):
    #because healthsprite/damagesprite dont have an effect it simple adds or removes health depending
    #on effect and player
        healthSprite = uvage.from_image(1500, 900, "healthSprite.png") # moves sprite out of bounds
        healthSprite.scale_by(0.2)
        if playerOneHealth <= 90: # if the health is greater than or equal to 90, we can add 10
            playerOneHealth += 10
        else:
            playerOneHealth = 100 # other wise set it to 100 to avoid going above limit of 100
    
    if healthSprite.touches(playerTwo):
        healthSprite = uvage.from_image(1500, 900, "healthSprite.png") # moves sprite out of bounds
        healthSprite.scale_by(0.2)
        if playerTwoHealth <= 90:
            playerTwoHealth += 10
        else:
            playerTwoHealth = 100

    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            healthSprite.speedy = -5
            healthSprite.speedx = 5
        elif not side: # if right side condiiton 
            healthSprite.speedy = -5
            healthSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            healthSprite.speedy = 5
            healthSprite.speedx = 5
        elif not side: # if right side condiiton 
            healthSprite.speedy = 5
            healthSprite.speedx = -5
    
    healthSprite.move_speed()


def damage():
    # player takes more damage when hitting this debuff+ str(int(playerTwoHealth)))
    # uses "damageSprite.png" sprite
    global damageSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth
    x, y = set_spawnPoints()
    damageSprite = uvage.from_image(x , y , "damageSprite.png")
    damageSprite.scale_by(0.2)  
        
def damageMove():
    global damageSprite, playerOne, playerTwo, playerOneHealth, playerTwoHealth, slope, side, walls

    if damageSprite.touches(playerOne):
        damageSprite = uvage.from_image(1500, 900, "damageSprite.png") # moves sprite out of bounds
        damageSprite.scale_by(0.2)
        if playerOneHealth >= 10:
            playerOneHealth -= 10
        else:
            playerOneHealth = 0
    if damageSprite.touches(playerTwo):
        damageSprite = uvage.from_image(1500, 900, "damageSprite.png") # moves sprite out of bounds
        damageSprite.scale_by(0.2)
        if playerTwoHealth >= 10:
            playerTwoHealth -= 10
        else:
            playerTwoHealth = 0
    
    if slope: # if upwards slope condition---------------------------------------------------------------
        if side: # if left side condition
            damageSprite.speedy = -5
            damageSprite.speedx = 5
        elif not side: # if right side condiiton 
            damageSprite.speedy = -5
            damageSprite.speedx = -5
    elif not slope: # if downards slope condition---------------------------------------------------------
        if side: # if left side condition
            damageSprite.speedy = 5
            damageSprite.speedx = 5
        elif not side: # if right side condiiton 
            damageSprite.speedy = 5
            damageSprite.speedx = -5

    damageSprite.move_speed()

def handle_health():
    global playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    # as the player touches a beam they lose one health
    if p2Beam.touches(playerOne): 
        playerOneHealth -= 1
    if p1Beam.touches(playerTwo):
        playerTwoHealth -= 1

def gameOver(): #ends the game after game over message is displayed
    if playerOneHealth == -1: # set at -1 because game quits at health value 1 (lines 509, 511, 603, 608)
        return True
    elif playerTwoHealth == -1:
        return True  # player 1 wins
    return False


def tick():
    global walls, playerOne, playerTwo, playerOneHealth, playerTwoHealth, p1Beam, p2Beam
    global p1_Health, p2_Health, rand_num, spriteSpawnCount, effectTimerCount_p1, effectTimerCount_p2
    global boost_p1, boost_p2, slomo_p1, slomo_p2 
    global slomoNotice_p1, slomoNotice_p2, boostNotice_p1, boostNotice_p2
    camera.clear('black')
    setup() # creates beams, player health notices, and sprites
    
    if gameOver():
        return
    
    handle_health()
    
    spriteSpawnCount +=1
    
    playerOneMovement() # sets all the movements in order
    playerTwoMovement()
    speedBoostMove()
    speedReduceMove()
    healthIncreaseMove()
    damageMove()
    handle_beams()

    if spriteSpawnCount == 90: # every 3 seconds a sprite spawns
        random_effect = random.randint(0,4) # randomly selects an obstacle sprite
        if random_effect == 0:
            speedBoost()
        elif random_effect == 1:
            speedReduce()
        elif random_effect == 2:
            healthIncrease()
        elif random_effect == 3:
            damage()
        spriteSpawnCount = 0

    # in the following 4 if statments, the variable that displays the current effect moves into view
    # when said effects are applied
    if boostActive_p1: # 10 second timer boost on player 1
        effectTimerCount_p1 +=1 # starts the timer
        boostNotice_p1 = uvage.from_text(150, 75, "BOOST ACTIVE!!!", 30, "green")

        if effectTimerCount_p1 == 300:#when it hits 300/10 seconds it cancels effect
            boost_p1 = False
            effectTimerCount_p1 = 0 #resets the effect timer

    if boostActive_p2: # 10 second timer for boost on player 2
        effectTimerCount_p2 +=1
        boostNotice_p2 = uvage.from_text(550, 75, "BOOST ACTIVE!!!", 30, "green")
        
        if effectTimerCount_p2 == 300: #when it hits 300 it cancels effect
            boostNotice_p2 = uvage.from_text(1000, 900, "BOOST ACTIVE!!!", 30, "green")
            boost_p2 = False
            effectTimerCount_p2 = 0

    if slomoActive_p1: # 10 second timer for slomo on player 1
        effectTimerCount_p1 +=1
        slomoNotice_p1 = uvage.from_text(150, 75, "SLOMO ACTIVE!!!", 30, "red")
        
        if effectTimerCount_p1 == 300:#when it hits 300 it cancels effect
            slomo_p1 = False
            effectTimerCount_p1 = 0

    if slomoActive_p2: # 10 second timer for slomo on player 2
        effectTimerCount_p2 +=1
        slomoNotice_p2 = uvage.from_text(550, 75, "SLOMO ACTIVE!!!", 30, "red")

        if effectTimerCount_p2 == 300:#when it hits 300 it cancels effect
            slomo_p2 = False
            effectTimerCount_p2 = 0

    # when effect is up, it moves the messages back out of view
    if not slomo_p1:
        slomoNotice_p1 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")
    if not slomo_p2:
        slomoNotice_p2 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")
    if not boost_p1:
        boostNotice_p1 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")
    if not boost_p2:
        boostNotice_p2 = uvage.from_text(1000, 900, "SLOMO ACTIVE!!!", 30, "red")

    if outOfBounds_p1Beam():  
        # reshoots player 1 beam when it goes out of bounds by moving it back in front of the player
        reload_p1Beam()
    if outOfBounds_p2Beam():  
        # reshoots player 2 beam when it goes out of bounds by moving it back in front of the player
        reload_p2Beam()

    if playerOneHealth <= -1:  # if player 2 wins
        for i in range(21, 28):  
        # ship explosion animation is created in this loop and the next for the appropriate players
            playerOne.image = players_sprite_sheet[i]
        camera.draw(uvage.from_text(360, 300, "Game ovaaa....PLAYER 2 WINS", 50, "red"))
    if playerTwoHealth <= -1:  # if player 1 wins
        for i in range(21, 28):
            playerTwo.image = players_sprite_sheet[i]
        camera.draw(uvage.from_text(360, 300, "Game ovaaa....PLAYER 1 WINS", 50, "red"))

    camera.draw(playerOne)
    camera.draw(playerTwo)
    camera.draw(boostNotice_p1) 
    camera.draw(boostNotice_p2)
    camera.draw(slomoNotice_p1)
    camera.draw(slomoNotice_p2)
    camera.display()

uvage.timer_loop(30, tick)