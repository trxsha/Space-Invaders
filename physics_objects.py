# Trisha
# CS 152 Project 9
# 08 Nov 2017
# physics_objects.py
# grouping subclasses into a superclass 'Thing'

import graphics as gr
import collision as col
import random
import math as m

class Thing:
    def __init__(self, win, the_type, pos = [0, 0], mass=1, radius=1):
        self.type = the_type
        self.mass = mass
        self.radius = radius
        self.pos = pos[:]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.force = [0, 0]
        self.elasticity = 1.0
        self.green = 0
        
        # visualization fields
        self.scale = 10
        self.win = win
        # self.vis = [gr.Circle( gr.Point(self.pos[0]*self.scale, win.getHeight()-self.pos[1]*self.scale), self.radius*self.scale)]
        
    def getVelocity(self):
        '''returns a 2-element tuple with the x and y velocities.'''
        return (self.vel[0], self.vel[1])
        
    def setVelocity(self, v):
        '''sets the velocity to the new velocity v'''
        self.vel[0] = v[0]
        self.vel[1] = v[1]
        
    def getAcceleration(self):
        '''returns a 2-element tuple with the x and y acceleration values.'''
        return (self.acc[0], self.acc[1])
        
    def setAcceleration(self, a):
        '''sets the acceleration to the new acceleration a'''
        self.acc[0] = a[0]
        self.acc[1] = a[1]
        
    def getForce(self):
        '''returns a 2-element tuple with the current x and y force values.'''
        return (self.force[0]. self.force[1])
        
    def setForce(self, f):
        '''sets the force to the new force f'''
        self.force[0] = f[0]
        self.force[1] = f[1]
        
    def getMass(self):
        '''Returns the mass of the object as a scalar value'''
        return self.mass[:]
        
    def setMass(self, m):
        '''sets the mass to the new mass m'''
        self.mass = m
        
    def getRadius(self):
        '''returns the radius of the ball'''
        return self.radius
        
    def getPosition(self):
        '''returns a 2-element tuple with the x, y position'''
        return  (self.pos[0], self.pos[1]) # return a tuple or a copy [:]
        
    def setPosition(self, p):
        '''sets the position to the new position p'''
        self.pos[0] = p[0]
        self.pos[1] = p[1]
        
    def getType(self):
        '''returns the type of objects '''
        return self.type
        
    def setType(self, type):
        '''sets the type of the object to type '''
        self.type = type
        
    def getElasticity(self):
        '''returns the elasticity'''
        return self.elasticity
        
    def setElasticity(self, e):
        '''sets the elasticity to e'''
        self.elasticity = e
        
    def setFill(self, colour):
        '''loops through the self.vis list and adds colour to the item'''
        for item in self.vis:
            item.setFill(colour)
        if colour == "green":
            self.green = 1
            
    def isGreen(self):
        '''loops through the self.vis list and adds colour to the item'''
        return self.green
            
    def setOutline(self, colour):
        for item in self.vis:
            item.setOutline(colour)
            
    def draw(self):
        '''draws the items in the self.vis list to the window'''
        for i in self.vis:
            i.draw(self.win)
            
    def undraw(self):
        for i in self.vis:
            i.undraw()
            
    def update(self, dt):
        self.pos[0] += self.vel[0]*dt
        self.pos[1] += self.vel[1]*dt
        
        dx = self.vel[0]*self.scale*dt
        dy = -1*self.vel[1]*self.scale*dt
        
        for item in self.vis:
            item.move(dx, dy)
            #print(self.pos)

        self.vel[0] += self.acc[0]*dt
        self.vel[1] += self.acc[1]*dt
        
        self.vel[0] += dt*self.force[0]/self.mass
        self.vel[1] += dt*self.force[1]/self.mass
    
        #self.vel[0] *= 0.998
        #self.vel[1] *= 0.998
        
class Ball(Thing):
    
    def __init__(self, win, x0, y0, mass=1, radius=1):
        Thing.__init__(self, win, "ball", pos = [x0, y0], mass = mass, radius = radius)
        self.vis = [gr.Circle( gr.Point(self.pos[0]*self.scale, win.getHeight()-self.pos[1]*self.scale), self.radius*self.scale)]
        
    def setPosition(self, p):
        '''sets the position to the new position p'''
        self.pos[0] = p[0]
        self.pos[1] = p[1]

        for i in self.vis:
            c = i.getCenter()
            dx = (self.scale*p[0]) - c.getX()
            dy = self.win.getHeight() - (self.scale*p[1]) - c.getY()
            i.move(dx, dy)
        
class Floor(Thing):

    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "floor", [x0, y0])
        self.width = length
        self.height = thickness
        self.vis = [gr.Rectangle(gr.Point(x0*self.scale, self.win.getHeight()-(y0+thickness/2)*self.scale), 
                   gr.Point((x0+length)*self.scale, self.win.getHeight() - (y0-thickness/2)*self.scale))]
                   
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
        
class Wall(Thing):

    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "ball", [x0, y0])
        self.width = length
        self.height = thickness
        self.vis = [gr.Rectangle(gr.Point((x0-thickness/2)*self.scale, self.win.getHeight()-y0*self.scale),
                    gr.Point((x0+thickness/2)*self.scale, self.win.getHeight()-(y0+ thickness)*self.scale))]
                    
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
        
class Block(Thing):

    def __init__(self, win, x0, y0, length, thickness):
        Thing.__init__(self, win, "ball", [x0, y0])
        self.width = length
        self.height = thickness
        self.vis = [gr.Rectangle(gr.Point((x0-length/2)*self.scale, self.win.getHeight()-(y0-thickness/2)*self.scale),
                    gr.Point((x0+length/2)*self.scale, self.win.getHeight()-(y0+ thickness/2)*self.scale))]
                    
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
    
    def moveBlock(self,dx, dy):
        for vis in self.vis:
            vis.move(dx, dy)
    
            
class Polygon(Thing):
    def __init__(self, win, x0, y0):
        Thing.__init__(self, win, "ball", [x0, y0])
        self.vis = [gr.Polygon(gr.Point(x0*5, win.getHeight()-(y0*5)), gr.Point((x0+5)*5, win.getHeight()-((y0+5)*5)),
        gr.Point((x0+10)*5, win.getHeight()-(y0*5)),gr.Point((x0+7.5)*5, win.getHeight()-(y0*5)), gr.Point((x0+7.5)*5, win.getHeight()-(y0-3)*5),
        gr.Point((x0+2.5)*5, win.getHeight()-(y0-3)*5),gr.Point((x0+2.5)*5, win.getHeight()-(y0*5)))]
        
class RotatingBlock(Thing):
    def __init__(self, win, x0, y0, width, height, Ax=None, Ay=None):
        Thing.__init__(self, win, "rotating block", [x0, y0])
        self.width = width
        self.height = height
        
        self.points = [[-width/2, -height/2],[width/2, -height/2],
                      [width/2, height/2], [-width/2, height/2]]
                        
        if Ax != None and Ay != None:
            self.anchor = [Ax, Ay]
            
        else:
            self.anchor = [x0, y0]
            
        self.angle = 0.0
        self.rvel = 0.0
        self.drawn = False
        
    def moveBlock(self,dx, dy):
        for vis in self.vis:
            vis.move(dx, dy)
        
        
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
     
    def getAnchor(self):
        return self.anchor
    
    def setAnchor(self, x1, y1):
        self.anchor = [x1, y1]
        
    def getRotVelocity(self):
        return self.rvel
        
    def setRotVelocity(self, nrvel):
        self.rvel = nrvel
        
            
    def rotate(self, angle):
        self.angle += angle
        
        if self.drawn == True:
            self.draw()
        
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
        
        self.vis = [gr.Polygon(pts[0], pts[1], pts[2], pts[3])]
        
    def update(self, dt):
        da = self.rvel*dt
        
        if da != 0:
            self.rotate(da)
            
            Thing.update(self, dt)
        
# build the obstacle course
def buildGame(win, x0, y0, width, height):
    obstacleList = [Wall(win, -20, 0, 50, 50), Wall(win, 70, 0, 50, 50),
               RotatingBlock(win, 37, 45, 12, 2), RotatingBlock(win, 13, 5, 12, 2)]
               
    for item in obstacleList:
        item.setElasticity(1.5)
        item.setFill("black")
        item.draw()
    # Block(win, 13, 5, 12, 2) moving block
    # obstacleList[2].setFill("blue") Block(win, 12.7, 2, 2, 5)
    # obstacleList[3].setFill("gold")
    # obstacleList[4].setFill("purple") Block(win, 36.7, 2, 2, 5)
    obstacleList[-2].setFill("pink")
    obstacleList[-1].setFill("gold")
    
    return obstacleList

# launch the ball into the scene
def launch( ball, x0, y0, dx, dy, forceMag ):

    d = m.sqrt(dx*dx + dy*dy)
    dx /= d
    dy /= d

    fx = dx * forceMag
    fy = dy * forceMag

    ball.setElasticity( 0.6 )
    ball.setPosition( (x0, y0) )
    ball.setForce( (fx, fy) )

    for i in range(5):
        ball.update(0.03)

    ball.setForce( (0., 0.) )
    ball.setAcceleration( (0., -1.) )
        
        