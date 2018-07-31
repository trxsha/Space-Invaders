# Trisha
# CS 152 Project 11 extension yay!
# 03 Dec 2017
# an obstacle race hehe

import physics_objects as pho
import graphics as gr
import math
import collision as col
import ship as s
import random
import os

dt = 0.1
# lists to store objects on screen
start = []
bounds = []
play = []
end = []
next = []
score = 0   # initializing score counter

def intro(win):
    ''' draws the start screen comprising of a background image '''
    # start screen
    
    welcome = gr.Image(gr.Point(285, 300), "background.gif")
    welcome.draw(win)
    
    start.append(welcome)
    
def drawGame(win):
    '''draws the background, the bounds and the spaceship'''
    # main game
    stars = gr.Image(gr.Point(300,300), "stars.gif")
    stars.draw(win)
    ship = s.Ship(win, 10, 30)
    
    # drawing bounds
    lowerBound = pho.Floor(win, 0, 60, 60, 10)
    lowerBound.setFill("black")
    upperBound = pho.Floor(win, 0, 0, 60, 10)
    upperBound.setFill("black")
    bounds.append(upperBound)
    bounds.append(lowerBound)
    upperBound.draw()
    lowerBound.draw()
    ship.draw()
    play.append(ship)
    play.append(lowerBound)
    play.append(upperBound)
    play.append(stars)
    return ship
    
def drawAsteroids(win):
    '''
    draws 5 asteroids into the scene, giving them random
    velocities, force and colour. Returns the list of asteroids
    '''
    asteroids = []
    
    for i in range(5):
        asteroid = pho.Ball(win, random.randint(50,60), random.randint(10,40), 1, random.randint(1,3))
        asteroid.setFill(random.choice(['red', 'green', 'yellow']))
        asteroid.setVelocity([-0.1,random.random()])
        asteroid.setForce([-0.1, random.randint(-1, 1)])
        asteroid.setElasticity(0.9)
        asteroids.append(asteroid)
        asteroid.draw()
        play.append(asteroid)
    return asteroids
    
def drawMissile(win, ship):
    missile = pho.Block(win, 15, ship.getPosition()[1], 4, 0)
    missile.setFill('grey')
    missile.setOutline('grey')
    missile.setVelocity([10, 0])
    missile.draw()
    play.append(missile)
    return missile  
    
def drawEndLose(win):
    
    # last screen when you lose :c
    oops = gr.Text(gr.Point(300, 200), "Ooops, you were hit by an asteroid! :( \n\n Your score is: " + str(score) + "\n\n\n Press R followed by S to try again!")
    oops.setSize(25)
    oops.setFill('gold')
    meteor = gr.Image(gr.Point(325, 450), "asteroid.gif")
    end.append(meteor)
    end.append(oops)
    meteor.draw(win)
    oops.draw(win)
    
def drawNextLevel(win):
    next = gr.Text(gr.Point(300, 300))
    next.setFill('blue')
    next.setSize(25)
    next.append(next)
    next.draw()
    
def main():

    # ----setting up----
    win = gr.GraphWin('Survival',600, 600, False)
    win.setBackground("black")
    win.setCoords(0,0,600,600)
    
    dt = 0.1
    frame = 0
    gamma = 2
    START_PHASE = 1
    PLAY_PHASE = 2
    PLAY_PHASE2 = 4
    STOP_PHASE = 3
    missile = None
    
    phase = 1
    intro(win)
    
    # Event loop
    while True:
        key= win.checkKey()
        if key == 'q':
            # get outta here altogether
            win.close()
            return
            
        if phase == START_PHASE:
            if key == 's':
                # Break down this phase and set-up next phase
                for item in start:
                    item.undraw()
                ship = drawGame(win)
                asteroids = drawAsteroids(win)
                phase = PLAY_PHASE
        elif phase == PLAY_PHASE:

            collided = False
            if missile != None:
                if missile.getPosition()[0] > win.getWidth()+5/10:  #if missile goes off screen
                    missile = None
                else:
                    missile.update(dt)
                
            for asteroid in asteroids:
                asteroid.update(dt)
                # handling collisions
                if col.collision(asteroid, bounds[0], dt) == True:
                    collided = True
                    
                if col.collision(asteroid, bounds[1], dt) == True:
                    collided = True

                    
                if missile != None:
                    if col.collision(asteroid, missile, dt) == True:
                        os.system("afplay cannon.mp3 &")
                        missile.undraw()
                        asteroid.undraw()
                        global score
                        score += 10 # increment score for each hit
                        collided = True
                    else:
                        missile.undraw()
                        collided = True
                # lose game        
                if col.collision(asteroid, ship, dt) == True:
                    collided = True
                    phase = STOP_PHASE
            
                if collided == False:
                   asteroid.update(dt)
                
                # relaunching asteroids into scene when they go off screen
                if (asteroid.getPosition()[0] < 0 or asteroid.getPosition()[0] > win.getWidth()) or (asteroid.getPosition()[1] < 0 or asteroid.getPosition()[1] > win.getHeight()):
                    asteroid.setPosition([60, 30])
                    asteroid.setVelocity([-0.1,random.randint(-2,2)])
                    asteroid.setForce([-0.1, random.randint(-2,2)])
                    
            # move ship up        
            if key == 'Up':
                ship.moveShip(0, -gamma)
                ship.setFlickerOn()
                ship.update(dt)
            
            # move ship down
            elif key == 'Down':
                ship.moveShip(0, gamma)
                ship.setFlickerOn()
                ship.update(dt)
            
            # fire a missile
            elif key == 'space':
                missile = drawMissile(win, ship)
                ship.update(dt)
                
            if score >= 100:
                phase == PLAY_PHASE2
                
        elif phase == PLAY_PHASE2:
            for item in play:
                item.undraw()
            for item in next:
                item.draw(win)
            for item in play:
                item.draw()
            collided = False
            if missile != None:
                if missile.getPosition()[0] > win.getWidth()+5/10:  #if missile goes off screen
                    missile = None
                else:
                    missile.update(dt)
                
            for asteroid in asteroids:
                asteroid.update(dt)
                # handling collisions
                if col.collision(asteroid, bounds[0], dt) == True:
                    collided = True
                    
                if col.collision(asteroid, bounds[1], dt) == True:
                    collided = True

                    
                if missile != None:
                    if col.collision(asteroid, missile, dt) == True:
                        os.system("afplay cannon.mp3 &")
                        missile.undraw()
                        if asteroid.isGreen():  # if the asteroid is green
                            asteroid.undraw()
                            missile.undraw()
                            global score
                            score += 10 # increment score for each hit
                            collided = True
                        else:
                            missile.undraw()
                            collided = True
                # lose game        
                if col.collision(asteroid, ship, dt) == True:
                    collided = True
                    phase = STOP_PHASE
            
                if collided == False:
                   asteroid.update(dt)
                
                # relaunching asteroids into scene when they go off screen
                if (asteroid.getPosition()[0] < 0 or asteroid.getPosition()[0] > win.getWidth()) or (asteroid.getPosition()[1] < 0 or asteroid.getPosition()[1] > win.getHeight()):
                    asteroid.setPosition([60, 30])
                    asteroid.setVelocity([-0.1,random.randint(-2,2)])
                    asteroid.setForce([-0.1, random.randint(-2,2)])
                    
            # move ship up        
            if key == 'Up':
                ship.moveShip(0, -gamma)
                ship.setFlickerOn()
                ship.update(dt)
            
            # move ship down
            elif key == 'Down':
                ship.moveShip(0, gamma)
                ship.setFlickerOn()
                ship.update(dt)
            
            # fire a missile
            elif key == 'space':
                missile = drawMissile(win, ship)
                ship.update(dt)
                
        # --- last phase ---        
        elif phase == STOP_PHASE:
            for item in play:
                item.undraw()
            drawEndLose(win)
            
            # replay
            if key == 'r':
                for item in end:
                    item.undraw()
                score = 0
                phase = START_PHASE
                
            if frame % 10 == 0:
                win.update()
                    
                frame += 1
        
if __name__ == "__main__":
    main()
    