Readme File for B11oons 2ower Defense


PROJECT DESCRIPTION: 

Modeled after the classic browser game “Bloons Tower Defense” by Kiwi, B11oons 2ower Defense involves a board with balloons that travel from the entrance (top-left corner) to the exit (bottom-left corner). The player must purchase and place towers or cacti on the board to pop balloons and earn coins. Unpopped balloons that reach the exit decrement the player’s health, and eventually the player loses the game when the health reaches 0. The player wins when they have cleared all the balloons. Because there are no paths, each balloon must optimize a direction to travel in to reach the exit, avoiding the towers. Aside from the Octo Tower and Cactus, towers have the ability to aim at a balloon. Players have the option to play in easy or hard mode, which changes the number of balloons each game, the speed at which they emerge, and the starting coin balance. 

The balloons are: 

Red: 1 HP, 3 speed
Blue 2 HP, 4 speed
Green: 3 HP, 5 speed
Yellow 4 HP, 6 speed
Pink: 5 HP, 7 speed
Disappearing: 1 HP, 3 speed, disappears every 3rd second
Blimp: 200 HP, 2 speed

The towers are: 

Tower: key=“t”, price=20, shoots a bullet every 2 sec
Super Tower: key=“s”, price=40, shoots a bullet every 1 sec
Freeze Tower: key=“f”, price=40, shoots a freeze bullet every 2 sec that freezes balloon for 5 sec
Octo Tower: key=“8”, price=60, shoots 8 bullets outward every 2 sec + greater range
Cactus: key=“c”, price=20, every 2 sec, pops balloons that cross it + Invisible to balloons



HOW TO RUN:

All modules are included in the compressed file. Simply run TPMain(). 



LIBRARIES:

Included in the file. 



SHORTCUTS:
control-p to pause & view help screen
"L" to decrease player hp to 1
"W" to remove all balloons not currently on the screen

