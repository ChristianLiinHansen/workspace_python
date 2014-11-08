# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 15:39:22 2014

@author: christian
"""

import turtle
import time

def draw_square(some_turtle, sizeOfSquare,increment):   
    for movements in range(0,4):
        #Move in a give length forward
        some_turtle.forward(sizeOfSquare)
        #And then move 90 degree to the right
        some_turtle.right(90)
        
def draw_art():    
    # Add a window screen
    window = turtle.Screen()
    
    #And make the bagground red
    window.bgcolor("red")
    
    #Creates the turtle brad
    brad = turtle.Turtle()
    #Change the shape of the turtle
    brad.shape("turtle")
    #Change the color of the turtle
    brad.color("yellow")
    #And the speed of the turtle
    brad.speed(10)  
    
    #And draw the square of brad
    for iteration in range(0,50):
        draw_square(brad,200,iteration)
        brad.right(10)
        
        
    
    
    """
    #Creates the turtle angie
    angie = turtle.Turtle()
    #Change the shape of the turtle
    angie.shape("turtle")
    #Change the color of the turtle
    angie.color("black")
    #And the speed of the turtle
    angie.speed(2)   
    
    #Call the draw_circle
    draw_circle(angie)
    """
        
    #Make the program close down, when only we click on the window
    window.exitonclick()
    

"""        
def draw_circle(some_turtle):
    # Grap a turtle, which we call angie
    some_turtle = turtle.Turtle()
    
    #Change the shape of the turtle
    some_turtle.shape("turtle")
    
    #Change the color of the turtle
    some_turtle.color("blue")
    
    #Make the angie turtle draw a circle within 100 radius..
    some_turtle.circle(100)
"""   
#Here the program starts...

print("This is mindstorm")

draw_art()

    
    