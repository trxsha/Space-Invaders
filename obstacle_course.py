# Trisha 
# CS 152 Project 10
# 22 Nov 17
# obstacle_course.py
# a simple obstacle course with balls and rotating blocks

import physics_objects as pho
import time
import graphics as gr
import random
import math
import collision as col

# main code
def main():
    win = gr.GraphWin('Space Game', 500, 500, False)
    blocks = [pho.RotatingBlock(win, 10, 20, 5, 5),pho.RotatingBlock(win, 25, 20, 5, 5),pho.RotatingBlock(win, 40, 20, 5, 5),
    pho.RotatingBlock(win, 25, 36, 3, 11), pho.RotatingBlock(win, 25, 36, 11, 3)]
    b = gr.Image(gr.Point(250,250),"background.gif")
    b.draw(win)
    start = gr.Text(gr.Point(250, 250), "Start")
    start.draw(win)
    obstacles = pho.buildGame(win, 50, 50, 50, 4)
    ball = pho.Ball(win, 25, 25)
    pho.launch(ball, 40, 10, 10, 10, 200)
    ball.setVelocity([0, 100])
    ball.setForce([0, -50])
    ball.setElasticity(0.9)
    ball.draw()
    
    for block in blocks:
        block.setRotVelocity(300)
        block.draw()
        
    dt = 0.01
    frame = 0
    
    win.getMouse()
    
    while win.checkMouse() == None:
        collided = False
        for item in obstacles:
            if col.collision(ball, item, dt) == True:
                collided = True
                ball.setFill(gr.color_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        for block in blocks:
            if col.collision(ball, block, dt) == True:
                collided = True
                ball.setFill(gr.color_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255)))            
        if collided == False:
            ball.update(dt)
                    
        for block in blocks:
            block.update(dt)
            block.setFill('grey')
            block.setOutline('grey')
        
        movingBlockDown = obstacles[-1]
        movingBlockUp = obstacles[-2]
        
        n = win.checkKey()
         
        if n == "Right":   
            movingBlockDown.moveBlock(20,0)
            movingBlockDown.update(dt)
            
        if n == "Left":
            movingBlockDown.moveBlock(-20, 0)
            movingBlockDown.update(dt)
            
        if n == "d":   
            movingBlockUp.moveBlock(20,0)
            movingBlockUp.update(dt)
            
        if n == "a":
            movingBlockUp.moveBlock(-20, 0)
            movingBlockUp.update(dt)
            
        if n == "space":
            pho.launch(ball, 10, 10, 20, 20, 100)
            
        if (ball.getPosition()[0] < 0 or ball.getPosition()[0] > win.getWidth()) or (ball.getPosition()[1] < 0 or ball.getPosition()[1] > win.getHeight()):
            ball.setPosition([25, 25])
            ball.setVelocity([0, random.randint(-10, 10)])
            #relaunch the ball
            pho.launch(ball, 10, 10, 20, 20, 100)
            
        if frame % 10 == 0:
            win.update()
                
        frame += 1
            
    win.getMouse()
    win.close()

if __name__ == "__main__":
    main()