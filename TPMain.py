
from cmu_112_graphics import *
from tkinter import *
import Player
import Tower
import Balloon
import Board

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
                mode.app.setActiveMode(mode.app.onePlayerMode)

            #2 player button
            if (width*7//10 <= x <= width*9//10 and
                height*3//4 <= y <= height*7//8):
                mode.app.setActiveMode(mode.app.twoPlayerMode)


        def redrawAll(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            #todo: draw background
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))

            #draw logo
            #todo: add image later
            canvas.create_text(width//2, height//2,
                               text="Bloons Tower Defense", font="Arial 50")

            #draw buttons
            canvas.create_rectangle(width*1//10, height*3//4,
                                    width*3//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*2//10, height*13//16,
                               text="1 Player", font="Arial 35")
            canvas.create_rectangle(width*4//10, height*3//4,
                                    width*6//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*5//10, height*13//16,
                               text="Versus AI", font="Arial 35")
            canvas.create_rectangle(width*7//10, height*3//4,
                                    width*9//10, height*7//8,
                                    fill="light blue")
            canvas.create_text(width*8//10, height*13//16,
                               text="2 Player", font="Arial 35")


    class OnePlayerMode(Mode):
        def appStarted(mode):
            mode.player = Player.Player()
            mode.board = Board.Board(mode.width, mode.height)
            mode.clock = 0
            towerImageUnscaled = mode.loadImage("tower.png")
            mode.towerImage = mode.scaleImage(towerImageUnscaled, 1/15)
            mode.backgroundImage = mode.loadImage("sky.jpg")
            #mode.timerDelay = 17 #TODO is this how i can make it faster bc its not working


        def timerFired(mode):
            mode.clock += 1

            #BALLOONS
            if (mode.clock % 10 == 0):
                #a new balloon appears on screen (move a balloon from offBalloons to onBalloons)
                if (len(mode.player.offBalloons) != 0):
                    mode.player.moveBalloonOn(mode.board)

            #if balloon is off board (x value > width of board), decrement player HP and remove it from onBalloon list
            balIndex = 0
            while (balIndex < len(mode.player.onBalloons)):
                balloon = mode.player.onBalloons[balIndex]
                if balloon.position[0] >= mode.width:
                    mode.player.hp -= balloon.hp
                    mode.player.onBalloons.pop(balIndex)
                else:
                    balIndex += 1

            for balloon in mode.player.onBalloons:
                dx, dy = balloon.getDirection(mode.player.towers, mode.app.width, mode.app.height)


            #TOWERS
            for tower in mode.player.towers:
                if tower.currentCoolDown == 0:
                    #add bullet to start of list with position at tower position (if shooting)
                    newBullet = tower.createBulletIfInRange(mode.player.onBalloons)
                    if newBullet != None:
                        mode.player.bullets.append(newBullet)
                    tower.currentCoolDown = tower.defaultCoolDown - 1
                else:
                    tower.currentCoolDown -= 1


            #BULLETS
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
            if mode.player.isPlacingTower:
                newTower = Tower.Tower((event.x, event.y))
                mode.player.towers.append(newTower)
                mode.player.coins -= Tower.Tower.price
                mode.player.isPlacingTower = False


        def keyPressed(mode, event):
            if (event.key == "t"):
                if mode.player.coins >= Tower.Tower.price:
                    mode.player.isPlacingTower = True


        def redrawAll(mode, canvas):
            mode.drawBoard(canvas) #includes bg image
            mode.drawTopBanner(canvas)
            mode.drawBalloons(canvas)
            mode.drawTowers(canvas)
            mode.drawBullets(canvas)

            #TODO finish draw instructions (if in certain placing modes)
            mode.drawInstructions(canvas)

            if len(mode.player.onBalloons) == 0 and len(mode.player.offBalloons) == 0:
                #TODO draw win screen (mode)
                pass
            if mode.player.hp <= 0:
                #TODO draw lose screen (mode)
                pass


        def drawInstructions(mode, canvas):
            #placing towers
            if mode.player.isPlacingTower:
                canvas.create_text(mode.app.width//2, mode.app.height//2, text="Click where you want the tower placed.", font="Arial 30 bold")

        def drawTopBanner(mode, canvas):
            width = mode.app.width
            height = mode.app.height
            canvas.create_rectangle(0, 0, width, mode.board.topMargin, fill="light blue")

            canvas.create_text(width - 40, mode.board.topMargin//2, text=f"Coins: {mode.player.coins}")
            canvas.create_text(width - 100, mode.board.topMargin//2, text=f"HP: {mode.player.hp}")
            canvas.create_text(100, mode.board.topMargin//2, text="B11oons 2ower Defense")
            #TODO change text to logo ^

        def drawBoard(mode, canvas):
            canvas.create_image(mode.app.width//2, mode.app.height//2, image=ImageTk.PhotoImage(mode.backgroundImage))
            """
            for row in range(mode.board.size):
                for col in range(mode.board.size):
                    if mode.board.grid[row][col] != None:
                        canvas.create_rectangle(mode.board.getCellBounds(row, col), fill="yellow")
            """

        def drawBalloons(mode, canvas):
            for balloon in mode.player.onBalloons:
                cx, cy = balloon.position
                r = balloon.radius
                #TODO change this to an image roughly 20x20 pixels
                canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=balloon.color, width=0)

        def drawTowers(mode, canvas):
            for tower in mode.player.towers:
                x = tower.location[0]
                y = tower.location[1]
                canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.towerImage))

        def drawBullets(mode, canvas):
            for bullet in mode.player.bullets:
                cx = bullet.location[0]
                cy = bullet.location[1]
                r = bullet.radius
                canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black")

    class TwoPlayerMode(Mode):
        def appStarted(mode):
            pass

        def timerFired(mode):
            pass

        def mousePressed(mode, event):
            pass

        def keyPressed(mode, event):
            pass

        def redrawAll(mode, canvas):
            pass

    class MyModalApp(ModalApp):
        def appStarted(app):
            app.splashScreenMode = SplashScreenMode()
            app.onePlayerMode = OnePlayerMode()
            app.twoPlayerMode = TwoPlayerMode()
            app.setActiveMode(app.splashScreenMode)


    app = MyModalApp(width=1200, height=720)

runGame()


