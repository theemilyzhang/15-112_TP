
from cmu_112_graphics import *
from tkinter import *
import Player
import Tower
import Board
import Balloon
import Cactus
from mathFunctions import *
from playsound import playsound

#animation and graphics framework from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#modal app from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
#tower image from https://www.pngguru.com/free-transparent-background-png-clipart-lbpet/download
#sky image from http://www.alpharoofinginc.com/roofing-sky-background-3-2-jpg/
#cactus image from https://www.pexels.com/photo/three-potted-cactus-plants-1903965/

def runGame():

    class SplashScreenMode(Mode):
        def appStarted(mode):
            mode.backgroundImage = mode.loadImage("sky.jpg")
            playsound("bgm.mp3", block=False)
            mode.inInstructionsMode = False

        def mousePressed(mode, event):
            x = event.x
            y = event.y
            width = mode.app.width
            height = mode.app.height

            #easy mode button
            if (width*1//10 <= x <= width*3//10 and
                height*3//4 <= y <= height*7//8):
                mode.app.setActiveMode(mode.app.easyMode)

            #hard mode button
            if (width*7//10 <= x <= width*9//10 and
                height*3//4 <= y <= height*7//8):
                mode.app.setActiveMode(mode.app.hardMode)

            #instructions button
            if (width*4//10 <= x <= width*6//10 and
                height*25//32 <= y <=  height*27//32):
                mode.inInstructionsMode = True

            #back button in instructions
            if mode.inInstructionsMode:
                cx = mode.app.width//2
                cy = mode.app.height//2
                if (cx-280 <= x <= cx-220 and cy+240 <= y <= cy+280):
                    mode.inInstructionsMode = False
                    mode.app.setActiveMode(mode.app.splashScreenMode)


        def redrawAll(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))

            #draw logo
            canvas.create_text(width//2, height//2,
                               text="Bloons Tower Defense", font="Raleway 50")

            #easy mode button
            canvas.create_rectangle(width*1//10, height*3//4,
                                    width*3//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*2//10, height*13//16,
                               text="Easy Mode", font="Raleway 35")

            #hard mode button
            canvas.create_rectangle(width*7//10, height*3//4,
                                    width*9//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*8//10, height*13//16,
                               text="Hard Mode", font="Raleway 35")

            #instructions button
            canvas.create_rectangle(width*4//10, height*25//32,
                                    width*6//10, height*27//32,
                                    fill="white")
            canvas.create_text(width*5//10, height*13//16,
                               text="Instructions", font="Raleway 25")

            if mode.inInstructionsMode:
                mode.drawInstructions(canvas)

        def drawInstructions(mode, canvas):
            cx = mode.app.width//2
            cy = mode.app.height//2
            canvas.create_rectangle(cx-300, cy-300, cx+300, cy+300, fill="white")
            canvas.create_text(cx, cy-275, text="Instructions", font="raleway 30 bold")
            #TODO add instructions here

            #back button
            canvas.create_rectangle(cx-280, cy+240, cx-220, cy+280, fill="light blue")
            canvas.create_text(cx - 250, cy+260, text="Back", font="raleway 15")


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
            cactusImageUnscaled = mode.loadImage("cactus.png")
            mode.cactusImage = mode.scaleImage(cactusImageUnscaled, 1/10)


            mode.backgroundImage = mode.loadImage("sky.jpg")


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
            for balloon in mode.player.onBalloons:
                if balloon.frozenCountdown != 0:
                    balloon.frozenCountdown -= 1
                    continue
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
            # CACTI
            ############################################################################################################

            for cactus in mode.player.cacti:
                if cactus.currentCoolDown == 0:
                    #attack if balloon intersect
                    cx = cactus.location[0]
                    cy = cactus.location[1]
                    cr = cactus.radius
                    for balloon in mode.player.onBalloons:
                        bx = balloon.position[0]
                        by = balloon.position[1]
                        br = balloon.radius
                        if itemsOverlap(cx, cy, bx, by, cr, br):
                            newBalloon = balloon.getWeakerBalloon()
                            mode.player.onBalloons.remove(balloon)
                            if newBalloon.hp > 0:
                                mode.player.onBalloons.append(newBalloon)
                            mode.player.coins += 1
                    cactus.currentCoolDown = cactus.defaultCoolDown - 1
                else:
                    cactus.currentCoolDown -= 1

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

            ############################################################################################################
            # GAME OVER
            ############################################################################################################
            if (mode.player.hp <= 0) or (len(mode.player.onBalloons) == 0 and len(mode.player.offBalloons) == 0):
                mode.app._paused = True


        def mousePressed(mode, event):
            #if in placing tower mode, create tower where player clicked (if position is valid),
            #decrease player's coins, and turn mode off
            towerRadius = Tower.Tower((0, 0)).radius #pointless tower created just to access its radius
            if mode.player.placingTower != None:
                if mode.player.canPlaceItemHere(event.x, event.y, towerRadius, mode.width, mode.height):
                    mode.player.illegallyPlacedItem = False
                    mode.player.placingTower.location = (event.x, event.y)
                    mode.player.towers.append(mode.player.placingTower)
                    mode.player.coins -= Tower.Tower.price
                    mode.player.placingTower = None
                else:
                    mode.player.illegallyPlacedItem = True
            #ditto for cactus
            cactusRadius = Cactus.Cactus((0, 0)).radius #pointless tower created just to access its radius
            if mode.player.placingCactus != None:
                if mode.player.canPlaceItemHere(event.x, event.y, towerRadius, mode.width, mode.height):
                    mode.player.illegallyPlacedItem = False
                    mode.player.placingCactus.location = (event.x, event.y)
                    mode.player.cacti.append(mode.player.placingCactus)
                    mode.player.coins -= Cactus.Cactus.price
                    mode.player.placingCactus = None
                else:
                    mode.player.illegallyPlacedItem = True


        def mouseMoved(mode, event):
            if mode.player.placingTower != None:
                mode.player.placingTower.location = (event.x, event.y)
            if mode.player.placingCactus != None:
                mode.player.placingCactus.location = (event.x, event.y)


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
            elif (event.key == "c"):
                if mode.player.coins >= Cactus.Cactus.price:
                    mode.player.placingCactus = Cactus.Cactus((0, 0))


        def redrawAll(mode, canvas):
            mode.drawBoard(canvas) #includes bg image
            mode.drawCacti(canvas)
            mode.drawTowers(canvas)
            mode.drawBullets(canvas)
            mode.drawBalloons(canvas)

            mode.drawTopBanner(canvas)
            mode.drawInstructions(canvas)
            if mode.player.placingTower != None:
                mode.drawNewTowerOutline(canvas)
            if mode.player.placingCactus != None:
                mode.drawNewCactusOutline(canvas)

            if mode.app._paused:
                mode.drawHelp(canvas)

            if len(mode.player.onBalloons) == 0 and len(mode.player.offBalloons) == 0:
                mode.drawWinScreen(canvas)
            if mode.player.hp <= 0:
                mode.drawLoseScreen(canvas)

        def drawHelp(mode, canvas):
            cx = mode.app.width//2
            cy = mode.app.height//2
            canvas.create_rectangle(cx-300, cy-300, cx+300, cy+300, fill="white")
            canvas.create_text(cx, cy-275, text="Help Screen", font="raleway 30 bold")
            #TODO add help instructions

        def drawCacti(mode, canvas):
            for cactus in mode.player.cacti:
                x = cactus.location[0]
                y = cactus.location[1]
                r = cactus.radius
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="dark green", width=0)
                canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.cactusImage))

        def drawWinScreen(mode, canvas):
            cx = mode.app.width//2
            cy = mode.app.height//2
            canvas.create_rectangle(cx-200, cy-200, cx+200, cy+200, fill="white")
            canvas.create_text(cx, cy, text="Congrats! You won!", font="raleway 30 bold")

        def drawLoseScreen(mode, canvas):
            cx = mode.app.width//2
            cy = mode.app.height//2
            canvas.create_rectangle(cx-200, cy-200, cx+200, cy+200, fill="white")
            canvas.create_text(cx, cy, text="Oh no! You lost.", font="raleway 30 bold")

        def drawInstructions(mode, canvas):
            #placing towers/cacti
            if mode.player.illegallyPlacedItem:
                canvas.create_text(mode.app.width//2, mode.app.height//2, text="You cannot place anything there. Try again.", font="raleway 30 bold")
            elif mode.player.placingTower != None:
                canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the " + mode.player.placingTower.name + " placed.", font="raleway 30 bold")
            elif mode.player.placingCactus != None:
                canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the cactus placed.", font="raleway 30 bold")

        def drawNewTowerOutline(mode, canvas):
            x = mode.player.placingTower.location[0]
            y = mode.player.placingTower.location[1]
            r = mode.player.placingTower.radius
            canvas.create_oval(x-r, y-r, x+r, y+r)

        def drawNewCactusOutline(mode, canvas):
            x = mode.player.placingCactus.location[0]
            y = mode.player.placingCactus.location[1]
            r = mode.player.placingCactus.radius
            canvas.create_oval(x-r, y-r, x+r, y+r, outline="green")

        def drawTopBanner(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            canvas.create_rectangle(0, 0, width, mode.board.topMargin, fill="light blue")

            canvas.create_text(width - 40, mode.board.topMargin//2, text=f"Coins: {mode.player.coins}")
            canvas.create_text(width - 100, mode.board.topMargin//2, text=f"HP: {mode.player.hp}")
            canvas.create_text(100, mode.board.topMargin//2, text="B11oons 2ower Defense")

        def drawBoard(mode, canvas):
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))
            towerRadius = Tower.Tower((0,0)).radius #pointless location, just to get radius
            r = 4 * towerRadius
            canvas.create_oval(-r, -r, r, r, fill="white", width=0)
            canvas.create_text(towerRadius+20, towerRadius+15, text="Entrance", font="Raleway 20")
            canvas.create_oval(mode.app.width-r, mode.app.height-r, mode.app.width+r, mode.app.height+r, fill="white", width=0)
            canvas.create_text(mode.app.width - towerRadius - 5, mode.app.height - towerRadius - 5, text="Exit", font="Raleway 20")

        def drawBalloons(mode, canvas):
            for balloon in mode.player.onBalloons:

                if isinstance(balloon, Balloon.DisappearingBalloon) and not balloon.isVisible:
                    continue

                cx, cy = balloon.position[0], balloon.position[1]
                r = balloon.radius
                if balloon.frozenCountdown != 0:
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="white", width=0)
                else:
                    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=balloon.color, width=0)

                if isinstance(balloon, Balloon.Blimp):
                    canvas.create_text(cx, cy, text=str(balloon.hp), font="Raleway 10",)

        def drawTowers(mode, canvas):
            for tower in mode.player.towers:
                x = tower.location[0]
                y = tower.location[1]
                r = tower.radius
                canvas.create_oval(x-r, y-r, x+r, y+r)
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

    class HardMode(EasyMode):
        def appStarted(mode):
            super().appStarted()
            mode.player.hp = 20
            mode.player.offBalloons = mode.player.createBalloons("hard")

    class MyModalApp(ModalApp):
        def appStarted(app):
            app.splashScreenMode = SplashScreenMode()
            app.easyMode = EasyMode()
            app.hardMode = HardMode()
            app.setActiveMode(app.splashScreenMode)


    app = MyModalApp(width=1200, height=720)

runGame()