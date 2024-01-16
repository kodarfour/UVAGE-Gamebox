# UVAGE-Gamebox
An outerspace, shooter game with health-based competition that utilizes 8-bit graphics, keyboard controls, and real-time effects

Supports simultaneous two-player mode at 30 FPS, utilizing a UVA-made api wrapper for pygame

# Dependencies:
- [pygame 2.5.0+](https://www.pygame.org/wiki/GettingStarted)
- [Python 3.10.2+](https://www.python.org/downloads/)

# Instructions:
**<em>FIRST: Install Dependencies and set up virtualenv for Flask</em>**

**<em>SECOND: Run uvage.py</em>**

 - This window should pop up if succesful:
  <br>
  ![uvage test popup image](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/uvagewindow.png?raw=true)

**<em>FINALLY: Run game.py and ENJOY!!</em>**
How to play and game information:
 - Player 1 (left side) uses WASD keys to move
 - Player 2 (right side) uses ARROW keys to move
 - Sprite Guide:
   - Healing Sprite:
     - Adds 10 HP back to health
        ![healthsprite image](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/healthSprite.png?raw=true)
   - Damage Sprite:
     - Removes 10 HP from health
        ![damagesprite image](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/damageSprite.png?raw=true)
   - Slomo Sprite:
     - Cuts off battleship engine and reduces movement speed
        ![slomosprite image](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/slomoSprite.png?raw=true)
   - Boost Sprite:
     - Powers battleship engine and increases movement speed
        ![boostsprite image](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/speedSprite.png?raw=true)

# Demo 

Watch video below for a demo:

[![Demo video thumbnail](https://github.com/kodarfour/UVAGE-Gamebox/blob/main/demothumbnail.png?raw=true)](https://www.youtube.com/watch?v=dvznsLTuLQg)