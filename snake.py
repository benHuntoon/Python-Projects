import turtle
import time
import sys
import random
import os
from Lab5_functions import *

#Coded by Benjamin Huntoon and Isaac Mueske

#creates the head of the snake as a global constant
head = turtle.Turtle()
head.shape("square")
head.color("yellow")
head.penup()
head.direction = "stop"

def main():
    #calls the draw_board function and returns the different size paramaters for the game
    wn, param1, param2, TILE,highest_y,lowest_y,left_x,right_x,grid = startgame()
    head.turtlesize(TILE / 20)

    #moves head to starting point
    head.goto(grid[32][0],grid[32][1])

    #sets initial scores
    score = 0
    best_score = 0
    
    #creates the food for the snake and assigns it a random spot on the board
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    #picks the food location
    food_start = random.choice(grid)
    food_x = food_start[0]
    food_y = food_start[1]
    food.goto(food_x,food_y)

    #moves the head to a starting point
    head.goto(grid[32][0],grid[32][1])

    #initializes the score and instruction pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.up()
    pen.hideturtle()
    #moves pen to score location
    pen.goto(left_x,highest_y + (3*(TILE // 2)))
    pen.color("black")
    pen.write("Best Score: {} ".format(best_score))
    pen.up()
    #moves pen to instructions location
    pen.goto(left_x,highest_y + (2*(TILE //2)))
    pen.write("Score: {} ".format(score))
    pen.goto(left_x + (5*TILE),highest_y + (4*(TILE // 2)))
    pen.write("w: up")
    pen.goto(left_x + (5*TILE), highest_y+(2*(TILE //2)))
    pen.write("s: down")
    pen.goto(left_x + (4*TILE),highest_y+(3*(TILE // 2)))
    pen.write("a: left")
    pen.goto(left_x + (6*TILE), highest_y+(3*(TILE //2)))
    pen.write("d: right")
    pen.goto(left_x + (8*TILE), highest_y+(3*(TILE // 2)))
    pen.write("q: quit")

    #set drawing speed and disable drawing animation
    turtle.speed('fastest')
    turtle.tracer(False)

    #initialize snake length
    segments = []
    
# Main Gameplay
    #sets delay values
    delay = 0.8
    fast_delay = 0.5

    #initialize player input keys
    wn.listen()
    wn.onkeypress(tup,"w")
    wn.onkeypress(tdown,"s")
    wn.onkeypress(tleft,"a")
    wn.onkeypress(tright,"d")
    wn.onkeypress(quitgame,"q")

    #set infinite loop to run main game
    while True:
            #update screen at beginning of each iteration
            wn.update()
            #checks if snake head has crossed outside of grid area
            if head.xcor() > right_x or head.xcor() < left_x or head.ycor() > highest_y or head.ycor() < lowest_y:
                #stops game temporarily
                time.sleep(.5)
                #resets game 
                head.goto(grid[32][0],grid[32][1])
                #stops snake until direction is given
                head.direction = "Stop"

                #hides all previous snake parts
                for segment in segments:
                        segment.goto(1000, 1000)
                #erases all previous snake parts
                segments.clear()
                #resets score and delay
                score = 0
                delay = 0.1
                pen.clear()
                pen.hideturtle()
                #display previous highscore and 0 as current score
                pen.goto(left_x, highest_y + (3*(TILE // 2)))
                pen.write("Best Score : {} ".format(best_score))
                pen.up()
                pen.goto(left_x, highest_y + (2* (TILE // 2)))
                pen.write("Score : {} ".format(score))

            #Draws snake to desired length of five parts
            if len(segments) < 5:
                new_segment = turtle.Turtle()
                new_segment.turtlesize(TILE / 20)
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("green")
                new_segment.penup()
                #adds segments to the list of snake parts
                segments.append(new_segment)

            #checks if snake is close enough to eat the apple
            if head.distance(food) < 20:
                food_coord = random.choice(grid)
                x = food_coord[0]
                y = food_coord[1]
                #moves food again
                food.goto(x, y)

		#adds new segment to the snake after eating
                new_segment = turtle.Turtle()
                new_segment.turtlesize(TILE / 20)
                new_segment.speed(0)
                new_segment.shape("square")
                new_segment.color("green") # tail colour
                new_segment.penup()
                segments.append(new_segment)
                delay -= 0.001
                score += 1

                #checks if player beat their high_score
                if score > best_score:
                    best_score = score
                #if player succeeded then it change score
                pen.clear()
                pen.hideturtle()
                pen.goto(left_x, highest_y + ( 3*(TILE//2)))
                pen.write("Best Score : {} ".format(best_score))
                pen.up()
                pen.goto(left_x, highest_y + (2*(TILE //2)))
                pen.write("Score : {} ".format(score))

            #moves the snake's body in the path of the part in front of it
            for index in range(len(segments)-1, 0, -1):
                x = segments[index-1].xcor()
                y = segments[index-1].ycor()
                segments[index].goto(x, y)
            if len(segments) > 0:
                x = head.xcor()
                y = head.ycor()
                segments[0].goto(x, y)

            #moves the snake according to its direction
            move(TILE)

            #iterates through segments to check if snake hit itself
            for segment in segments:
                #checks if snake hit itself
                if segment.distance(head) < 20:
                    #stops game temporarily
                    time.sleep(.5)
                    #moves head back to start
                    head.goto(grid[32][0],grid[32][1])
                    #stops snake until given direction
                    head.direction = "stop"
                    #removes old snake
                    for segment in segments:
                        segment.goto(1000, 1000)
                    segments = []
                    segment.clear()
                    
                    #resets score and displays 0 as current score and previous best score
                    score = 0
                    delay = 0.1
                    pen.clear()
                    pen.hideturtle()
                    pen.goto(left_x, highest_y + (3*(TILE//2)))
                    pen.write("Best Score : {} ".format(best_score))
                    pen.up()
                    pen.goto(left_x,highest_y + (2*(TILE//2)))
                    pen.write("Score : {} ".format(score))
                    pen.goto(left_x + (5*TILE),highest_y + (4*(TILE // 2)))
                    pen.write("w: up")
                    pen.goto(left_x + (5*TILE), highest_y+(2*(TILE //2)))
                    pen.write("s: down")
                    pen.goto(left_x + (4*TILE),highest_y+(3*(TILE // 2)))
                    pen.write("a: left")
                    pen.goto(left_x + (6*TILE), highest_y+(3*(TILE //2)))
                    pen.write("d: right")
                    pen.goto(left_x + (8*TILE),highest_y+(3*(TILE // 2)))
                    pen.write("q: quit")

            #checks if the player has won the game
            if len(segments) == param1 * param2:
                winner(pen,left_x,highest_y,TILE)

            #starts the game with a slower snake until snake length is 13
            if len(segments) < 13:
                time.sleep(delay)
            #speeds up snake at desired length
            else:
                time.sleep(fast_delay)


def draw_board(param1,param2,TILE):
    turtle.tracer(True)
    #initializes list of tiles
    grid = []
    #draws boxes according to horizontal parameter
    for tile_x in range(param1):
        #draws boxes according to vertical paramer
        for tile_y in range(param2):
            #draws a tile for every other space
            if ((tile_x + tile_y) % 2) == 0:
                pixel_x, pixel_y = tiles_to_pixels(tile_x, tile_y,TILE)
                #initializes individual tile coordinates
                coord = []
                coord.append(turtle.xcor()+(TILE//2))
                coord.append(turtle.ycor()+(TILE//2))
                #draws tile
                draw_rect(pixel_x-(10*param1+(TILE))+10,pixel_y-(10*param2)-(2*TILE)+10,TILE,TILE,'black')
                #appends tile coordiantes to list of all tile coordinates
                grid.append(coord)
            #checks if a coordinate is one of the alternating tiles on checkerboard
            if ((tile_x + tile_y) % 2) != 0:
                #initializes individual tile coordinates
                coord = []
                coord.append(turtle.xcor()+(TILE//2))
                coord.append(turtle.ycor()+(TILE//2))
                #appends tile coordinates to list of all tile coordinates
                grid.append(coord)
    #returns list of coordinates to main
    turtle.tracer(False)
    return grid

def move(TILE):
    #checks for snake's direction and moves the snake by TILE pixels
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+TILE)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-TILE)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-TILE)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+TILE)
    

def quitgame():
    #force quits program in IDLE and in command line
    os._exit(1)
    
def startgame():
    #sets up basic screen
    wn = turtle.Screen()
    wn.title("Snake!")
    wn.bgcolor("light grey")

    #checks if an input for command line was entered
    if len(sys.argv) > 1:
        param1 = int(sys.argv[1])
        param2 = int(sys.argv[2])
        TILE = param1 + param2
        grid = draw_board(param1,param2,TILE)
        highest_y = 0
        lowest_y = 0
        left_x = 0
        right_x = 0

        #finds the farthest x and y coordinates in both directions
        for points in grid:
            if points[1] > highest_y:
                highest_y = points[1]

            if points[1] < lowest_y:
                lowest_y = points[1]

            if points[0] > right_x:
                right_x = points[0]

            if points[0] < left_x:
                left_x = points[0]

        #sets up screen coordinates so the game will scale accoridng to command line        
        wn.setup(width = (param1 * TILE) + (3*TILE), height = (param2 * TILE) + (8*TILE))
        #returns positional values into main
        return wn, param1, param2, TILE, highest_y, lowest_y, left_x, right_x, grid
    else:
        #initializes default paramaters if not extra input is given
        param1 = 10
        param2 = 10
        TILE = 20
        grid = draw_board(param1,param2,TILE)
        highest_y = 0
        lowest_y = 0
        left_x = 0
        right_x = 0
        #finds the farthest x and y points in both directions
        for points in grid:
            if points[1] > highest_y:
                highest_y = points[1]
                
            if points[1] < lowest_y:
                lowest_y = points[1]

            if points[0] > right_x:
                right_x = points[0]

            if points[0] < left_x:
                left_x = points[0]

        #sets up screen coordinates so the game will scale accordingly    
        wn.setup(width = (param1 * TILE) + (3*TILE), height = (param2 * TILE)+(8*TILE))
        #returns positional values into main
        return wn, param1, param2, TILE, highest_y, lowest_y, left_x, right_x, grid
        
def tiles_to_pixels(tile_x, tile_y,TILE):
    #converts screen coordinates into more digestable numbers
    return tile_x * TILE, tile_y * TILE

def tup():
    #checks if snake is heading down and if not moves snake up
    if head.direction != "down":
        head.direction = "up"

def tdown():
    #checks if snake is heading up and if not moves snake down
    if head.direction != "up":
        head.direction = "down"

def tleft():
    #checks if snake is heading right and if not moves snake left
    if head.direction != "right":
        head.direction = "left"

def tright():
    #checks if snake is heading left and if not moves snake right
    if head.direction != "left":
        head.direction = "right"

def winner(pen,left_x,highest_y,TILE):
     #stops snake
     head.direction = "stop"
     #displays winning message
     pen.color("blue")
     pen.goto(left_x+(3*TILE),highest_y + (3*TILE))
     pen.write("You Win!",align="center",font=("candara",24,"bold"))
     #stops game and then quits
     time.sleep(3)
     quitgame()



main()
