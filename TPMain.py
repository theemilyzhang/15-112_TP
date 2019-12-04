
from cmu_112_graphics import *
from tkinter import *
import Player
import Tower
import Board
import math
import Balloon

#animation and graphics framework from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#modal app from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#tower image from https://www.pngguru.com/free-transparent-background-png-clipart-lbpet/download
#sky image from http://www.alpharoofinginc.com/roofing-sky-background-3-2-jpg/

def runGame():

    class SplashScreenMode(Mode):
        def appStarted(mode):
            mode.backgroundImage = mode.loadImage("sky.jpg")

        def mousePressed(mode, event):
            x = event.x
            y = event.y
            width = mode.app.width
            height = mode.app.height

            # 1 player button
            if (width*1//10 <= x <= width*3//10 and
                height*3//4 <= y <= height*7//8):
                mode.app.setActiveMode(mode.app.easyMode)

            #2 player button
            if (width*7//10 <= x <= width*9//10 and
                height*3//4 <= y <= height*7//8):
                mode.app.setActiveMode(mode.app.hardMode)


        def redrawAll(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))

            #draw logo
            canvas.create_text(width//2, height//2,
                               text="Bloons Tower Defense", font="Raleway 50")

            #draw buttons
            canvas.create_rectangle(width*1//10, height*3//4,
                                    width*3//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*2//10, height*13//16,
                               text="Easy Mode", font="Raleway 35")
            canvas.create_rectangle(width*4//10, height*3//4,
                                    width*6//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*5//10, height*13//16,
                               text="Medium Mode", font="Raleway 35")
            canvas.create_rectangle(width*7//10, height*3//4,
                                    width*9//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*8//10, height*13//16,
                               text="Hard Mode", font="Raleway 35")


    class EasyMode(Mode):
        def appStarted(mode):
            mode.player = Player.Player()
            mode.board = Board.Board(mode.width, mode.height)
            mode.clock = 0

            #images
            towerImageUnscaled = mode.loadImage("tower.png")
            mode.towerImage = mode.scaleImage(towerImageUnscaled, 1/15)
            supertowerImageUnscaled = mode.loadImage("supertower.png")
            mode.supertowerImage = mode.scaleImage(supertowerImageUnscaled, 1/15)
            octotowerImageUnscaled = mode.loadImage("octotower.png")
            mode.octotowerImage = mode.scaleImage(octotowerImageUnscaled, 1/15)
            freezetowerImageUnscaled = mode.loadImage("freezetower.png")
            mode.freezetowerImage = mode.scaleImage(freezetowerImageUnscaled, 1/15)

            mode.backgroundImage = mode.loadImage("sky.jpg")
            #mode.timerDelay = 17 #TODO is this how i can make it faster bc its not working


        def timerFired(mode):
            mode.clock += 1

            ############################################################################################################
            # BALLOONS
            ############################################################################################################

            if (mode.clock % 10 == 0):
                #a new balloon appears on screen (move a balloon from offBalloons to onBalloons)
                if (len(mode.player.offBalloons) != 0):
                    mode.player.moveBalloonOn(mode.board)

            #if balloon is off board (x value > width of board), remove it from onBalloon list and decrement player HP
            balIndex = 0
            while (balIndex < len(mode.player.onBalloons)):
                balloon = mode.player.onBalloons[balIndex]
                if balloon.position[0] >= mode.width:
                    mode.player.hp -= balloon.hp
                    mode.player.onBalloons.pop(balIndex)
                else:
                    balIndex += 1

            #1: move balloons by ideal direction
            #2: turn disappearingBalloons on/off
            #3: change color for toughBalloon if hp
            for balloon in mode.player.onBalloons:
                if balloon.isFrozen:
                    continue #never gets here
                #1
                direction = balloon.getDirection(mode.player.towers, mode.app.width, mode.app.height)
                dx, dy = math.cos(direction), -math.sin(direction) #unit vectors
                balloon.position = (balloon.position[0] + dx*balloon.speed, balloon.position[1] + dy*balloon.speed)
                balloon.distanceTraveled += balloon.speed
                #2
                if isinstance(balloon, Balloon.DisappearingBalloon):
                    balloon.timeSinceCreation += 1
                    if 20 <= (balloon.timeSinceCreation % 30) < 30:
                        balloon.isVisible = False
                    else:
                        balloon.isVisible = True
                #3
                elif isinstance(balloon, Balloon.ToughBalloon):
                    if balloon.hp == 1:
                        balloon.color = "red"

            ############################################################################################################
            # TOWERS
            ############################################################################################################

            for tower in mode.player.towers:
                if tower.currentCoolDown == 0:
                    #add bullet to start of list with position at tower position (if shooting)
                    newBullets = tower.createBulletIfInRange(mode.player.onBalloons)
                    mode.player.bullets.extend(newBullets)
                    tower.currentCoolDown = tower.defaultCoolDown - 1
                else:
                    tower.currentCoolDown -= 1

            ############################################################################################################
            # BULLETS
            ############################################################################################################

            bulIndex = 0
            while (bulIndex < len(mode.player.bullets)):
                bullet = mode.player.bullets[bulIndex]
                #move each bullet by its given dx, dy
                oldX = bullet.location[0]
                oldY = bullet.location[1]
                newX = oldX + (bullet.dx * bullet.speed)
                newY = oldY + (bullet.dy * bullet.speed)
                bullet.location = (newX, newY)
                bullet.distanceTraveled += bullet.speed

                #check for collision with balloon (checkCollision() decreases balloon hp and removes if necessary), then remove bullet + add coins
                if bullet.checkCollision(mode.player.onBalloons):
                    mode.player.bullets.pop(bulIndex)
                    mode.player.coins += 1

                #if last bullet exceeds range of tower, remove it from list
                elif bullet.distanceTraveled >= bullet.bulletRange:
                    mode.player.bullets.pop(bulIndex)

                else:
                    bulIndex += 1


        def mousePressed(mode, event):
            #if in placing tower mode, create tower where player clicked (if position is valid),
            #decrease player's coins, and turn mode off
            towerRadius = Tower.Tower((0, 0)).radius #pointless tower created just to access its radius
            if mode.player.placingTower != None:
                if mode.player.canPlaceTowerHere(event.x, event.y, towerRadius, mode.width, mode.height):
                    mode.player.illegallyPlacedTower = False
                    mode.player.placingTower.location = (event.x, event.y)
                    mode.player.towers.append(mode.player.placingTower)
                    mode.player.coins -= Tower.Tower.price
                    mode.player.placingTower = None
                else:
                    mode.player.illegallyPlacedTower = True


        def keyPressed(mode, event):
            if (event.key == "t"):
                if mode.player.coins >= Tower.Tower.price:
                    mode.player.placingTower = Tower.Tower((0, 0))
            elif (event.key == "s"):
                if mode.player.coins >= Tower.SuperTower.price:
                    mode.player.placingTower = Tower.SuperTower((0, 0))
            elif (event.key == "8"):
                if mode.player.coins >= Tower.OctoTower.price:
                    mode.player.placingTower = Tower.OctoTower((0, 0))
            elif (event.key == "f"):
                if mode.player.coins >= Tower.FreezeTower.price:
                    mode.player.placingTower = Tower.FreezeTower((0, 0))



        def redrawAll(mode, canvas):
            mode.drawBoard(canvas) #includes bg image
            mode.drawTopBanner(canvas)
            mode.drawBalloons(canvas)
            mode.drawTowers(canvas)
            mode.drawBullets(canvas)
            mode.drawInstructions(canvas)

            if len(mode.player.onBalloons) == 0 and len(mode.player.offBalloons) == 0:
                #TODO draw win screen (mode)
                pass
            if mode.player.hp <= 0:
                #TODO draw lose screen (mode)
                pass


        def drawInstructions(mode, canvas):
            #placing towers
            if mode.player.illegallyPlacedTower:
                canvas.create_text(mode.app.width//2, mode.app.height//2, text="You cannot place the tower there. Try again.", font="Raleway 30 bold")
            elif mode.player.placingTower != None:
                if isinstance(mode.player.placingTower, Tower.FreezeTower):
                    canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the freeze tower placed.", font="Raleway 30 bold")
                elif isinstance(mode.player.placingTower, Tower.OctoTower):
                    canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the octo tower placed.", font="Raleway 30 bold")
                elif isinstance(mode.player.placingTower, Tower.SuperTower):
                    canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the super tower placed.", font="Raleway 30 bold")
                else:
                    canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the tower placed.", font="Raleway 30 bold")


        def drawTopBanner(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            canvas.create_rectangle(0, 0, width, mode.board.topMargin, fill="light blue")

            canvas.create_text(width - 40, mode.board.topMargin//2, text=f"Coins: {mode.player.coins}")
            canvas.create_text(width - 100, mode.board.topMargin//2, text=f"HP: {mode.player.hp}")
            canvas.create_text(100, mode.board.topMargin//2, text="B11oons 2ower Defense")

        def drawBoard(mode, canvas):
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))

        def drawBalloons(mode, canvas):
            for balloon in mode.player.onBalloons:
                if isinstance(balloon, Balloon.DisappearingBalloon) and not balloon.isVisible:
                    continue
                cx, cy = balloon.position[0], balloon.position[1]
                r = balloon.radius

                if balloon.isFrozen:
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="white", width=0)
                else:
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=balloon.color, width=0)

        def drawTowers(mode, canvas):
            for tower in mode.player.towers:
                x = tower.location[0]
                y = tower.location[1]
                #r = tower.radius
                #canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
                if isinstance(tower, Tower.SuperTower):
                    image = mode.supertowerImage
                elif isinstance(tower, Tower.OctoTower):
                    image = mode.octotowerImage
                elif isinstance(tower, Tower.FreezeTower):
                    image = mode.freezetowerImage
                else:
                    image = mode.towerImage
                canvas.create_image(x, y, image=ImageTk.PhotoImage(image))

        def drawBullets(mode, canvas):
            for bullet in mode.player.bullets:
                cx = bullet.location[0]
                cy = bullet.location[1]
                r = bullet.radius
                canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black")

    class MyModalApp(ModalApp):
        def appStarted(app):
            app.splashScreenMode = SplashScreenMode()
            app.easyMode = EasyMode()

            app.setActiveMode(app.splashScreenMode)


    app = MyModalApp(width=1200, height=720)

runGame()