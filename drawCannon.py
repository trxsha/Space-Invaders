# drawCannon.py
# Dale Skrien
# CS 152, Fall 2017

import time
import graphics as gr
import os


def buildCannon():
    tlPt = gr.Point(200,100)
    brPt = gr.Point(300, 126)
    rect = gr.Rectangle(tlPt, brPt)
    rect.setFill("black")
    barrelEnd = gr.Circle(gr.Point(200,113), 13)
    barrelEnd.setFill("black")
    rearwheel = gr.Circle(gr.Point(200, 140), 15)
    frontwheel = gr.Circle(gr.Point(250, 140), 15)
    rearwheel.setFill("brown")
    frontwheel.setFill("brown")
    fuse = gr.Line(gr.Point(210,100), gr.Point(210, 90))
    fuse.setWidth(3)
    return [rect, barrelEnd, rearwheel, frontwheel, fuse]

def buildBullet():
    bullet = gr.Polygon(gr.Point(270, 102),
                        gr.Point(270, 124),
                        gr.Point(290, 124),
                        gr.Point(300, 113),
                        gr.Point(290, 102))
    bullet.setFill("orange")
    bulletBack = gr.Rectangle(gr.Point(270,102),gr.Point(280,124))
    bulletBack.setFill("black")
    return [bullet, bulletBack]

def drawList(myList,win):
    for part in myList:
        part.draw(win)

def moveList(myList,dx,dy):
    for part in myList:
        part.move(dx,dy)

def drawBoom(win):
    msg = gr.Text(gr.Point(130,50), "BOOM!!")
    msg.setSize(20)
    msg.setTextColor("red")
    msg.draw(win)

def main():
    # create the window
    win = gr.GraphWin("Demo", 500, 300)

    # build the cannon and bullet
    cannonPartsList = buildCannon()
    bulletPartsList = buildBullet()

    # draw everything
    drawList(bulletPartsList,win)
    drawList(cannonPartsList,win)

    # pause 1 second
    time.sleep(1)

    # camera! action! sound!
    drawBoom(win)
    os.system("afplay cannon.mp3 &")
    for frame in range(1,20):
        time.sleep(0.1)
        moveList(bulletPartsList,30,0)
        moveList(cannonPartsList,-10/frame,0)
        win.update()

    win.getMouse()  # pause for a click in the window
    win.close()

if __name__=="__main__":
    main()
