# Trisha
# CS 152 Project 10
# 15 Nov 2017
# rot.py

import graphics as gr
import time
import math as m

class RotatingLine:
    def __init__(self, win, x0, y0, length, Ax = None, Ay = None):
        self.pos = [x0, y0]
        self.length = length
        
        if Ax != None and Ay != None:
            self.anchor = [Ax, Ay]
            
        else:
            self.anchor = [x0, y0]
            
        self.points = [[-length/2.0, 0.0], [length/2.0, 0.0]]
        self.angle = 0.0
        self.rvel = 0.0
        self.win = win
        self.scale = 10
        self.vis = []
        self.drawn = False
        
    def render(self):
        
        theta = self.angle*m.pi/180.0
        cth = m.cos(theta)
        sth = m.sin(theta)
        pts = []
        
        for vertex in self.points:
            x = vertex[0] + self.pos[0] - self.anchor[0]
            y = vertex[1] + self.pos[1] - self.anchor[1]
            
            xt = x*m.cos(theta) - y*m.sin(theta)
            yt = x*m.sin(theta) + y*m.cos(theta)
            
            # yt = x*m.cos(theta) + y*m.cos(theta)
            x = self.anchor[0] + xt
            y = self.anchor[1] + yt
            
            pts.append(gr.Point(self.scale * x, self.win.getHeight() - self.scale*y))
        
        self.vis = [gr.Line(pts[0], pts[1])]
        
    def draw(self):
    
        for item in self.vis:
            item.undraw()
            
        self.render()
        
        for item in self.vis:
            item.draw(self.win)
            
        self.drawn = True
        
    def getAngle(self):
        return self.angle
      
    def setAngle(self, angle):
        self.angle = angle
        
        if self.drawn == True:
            self.draw()
            
    def rotate(self, angle):
        self.angle += angle
        
        if self.drawn == True:
            self.draw()
            
    def setAnchor(self, x1, y1):
        self.anchor = [x1, y1]
        
    
def test1():
    win = gr.GraphWin('line thingy', 500, 500, False)

    line = RotatingLine(win, 25, 25, 10)
    line.draw()

    while win.checkMouse() == None:
        line.setAnchor(30, 25)
        line.rotate(3)
        time.sleep(0.08)
        win.update()

    win.getMouse()
    win.close()

if __name__ == "__main__":
    test1()