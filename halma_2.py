#import tkinter
import tkinter as tk
import math
import time

#cell size constant
CELL_SIZE = 45

#main function
def main():
    #create the root instance
    root = tk.Tk()
    #start the game
    #if you want to change the N value edit the line below
    #i.e.: Halma(root, toggle_ai, 10)
    #Halma(root,False)
    Halma(root)
    #run the window loop
    root.mainloop()


#game class
class Halma:
    def __init__(self, window, toggle_ai = True, length=8):
        #initialization calls
        self.length = length
        self.window = window
        #label the window
        self.label = self.window.title("Halma")
        #create the turn window
        self.turn_window = tk.Label(window, text="White's Turn", font=("Arial", 16))
        self.turn_window.pack()
        #create the canvas
        self.canvas = tk.Canvas(window, width=CELL_SIZE*self.length, height=CELL_SIZE*self.length)
        self.canvas.pack()
        #listen for mouse input
        self.canvas.bind("<Button-1>", self.click)
        #create list of pieces
        self.circles = {}
        #create object to hold corner locations
        self.top_corner = set()
        self.bottom_corner = set()
        #draw the board
        self.draw_board()
        #draw the pieces
        self.draw_pieces()
        #create a list of possible moves
        self.moves = []
        #create an object to hold the selected piece
        self.selected_piece = None
        self.selected_piece_color = None
        #create an onject to indicate which players turn
        self.turn = 1
        #set ai variable
        self.ai_enabled = toggle_ai
        #check for ai enabled
        if self.ai_enabled:
            self.ai = Ai(self)

    #move piece function
    def move_circle(self, x_val, y_val):
        #collect the previous location from the selection
        prev_x = self.selected_piece[0]
        prev_y = self.selected_piece[1]
        #remove the old location from the list of pieces
        old_loc = self.circles.pop((prev_x,prev_y))
        self.circles[(x_val, y_val)] = {"circle_id": old_loc["circle_id"], "color": self.selected_piece_color}
        #delete the old location from the canvas
        self.canvas.delete(old_loc["circle_id"])
        #draw the piece in the new location
        self.draw_circle(self.selected_piece_color, x_val, y_val)
        #undo the selection
        self.unselect_piece()
        #reset the selected piece aspects
        self.selected_piece = None
        self.selected_piece_color = None
        #update the turn number
        self.show_turns()
        #update turn number
        if(self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1
        #show the turn window
        self.show_turns()
        #check for win conditions
        self.check_win()

        #check for player 2 turn and ai_enabled
        if self.ai_enabled and self.turn == 2:
            #run the ai move
            self.move_ai()

    #function to run ai move
    def move_ai(self):
        #collect the best move for the ai
        move = self.ai.find_best_move()

        #check for best move found
        if move:
            #select the piece to move
            self.select_piece(move[0][0], move[0][1])
            #move the piece
            self.move_circle(move[1][0], move[1][1])


    #display move functions
    def display_moves(self):
        #iterate through possible moves
        for move in self.moves:
            #collect the x start
            x_start = move[0] * CELL_SIZE
            #collect the y start
            y_start = move[1] * CELL_SIZE
            #collect the x stop
            x_stop = x_start + CELL_SIZE
            #collect the y stop
            y_stop = y_start + CELL_SIZE
            #highlight any possible move to make
            self.canvas.create_rectangle(x_start, y_start, x_stop, y_stop, fill="yellow", outline="black", tags=f"move_{move[0]}_{move[1]}")


    #function to get the pieces adjacent moves
    def get_moves(self, curr_x, curr_y):
        #create a list of possible moves
        possible_moves = []
        #create a list of all directions
        directions = [(-1,0), (1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        #loop through each direction
        for direction in directions:
            potential_move = (direction[0] + curr_x, direction[1] + curr_y)
            #check for valid x value
            if(potential_move[0] >= 0 and potential_move[0] < self.length):
                #check for valid y value
                if(potential_move[1] >= 0 and potential_move[1] < self.length):
                    #check for move not already occupied
                    if(potential_move not in self.circles):
                        #add the move to the list of moves
                        possible_moves.append(potential_move)
            #otherwise assume an invalid move
        #recursively search for possible jump moves
        self.get_jumps(possible_moves, curr_x, curr_y, set())
        #set the possible moves
        self.moves = possible_moves

    #recursive function to find any possible jump moves DFS
    def get_jumps(self, possible_moves, x_val, y_val, visited_set):
        #mark the current point as having been visited
        visited_set.add((x_val, y_val))
        #create a list of all directions
        directions = [(-1,0), (1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

        #loop through directions
        for direction in directions:
            #find the next x
            next_x = x_val + direction[0]
            #find the next y
            next_y = y_val + direction[1]
            #calculate the jumped x
            x_jump = x_val + (2*direction[0])
            #calculate the jumped y
            y_jump = y_val + (2*direction[1])

            #check for valid jump moves
            if((x_jump >= 0 and x_jump < self.length) and (y_jump >= 0 and y_jump < self.length)):
                #check for valid adjacent move
                if((next_x >= 0 and next_x < self.length) and (next_y >= 0 and next_y < self.length)):
                    #check for jump conditions
                    if((next_x, next_y) in self.circles and (x_jump, y_jump) not in self.circles):
                        #check if the jump cell has been visited
                        if((x_jump, y_jump)not in visited_set):
                            #add the jump to moves
                            possible_moves.append((x_jump, y_jump))
                            #recursivley check for further jumps from the jump point
                            self.get_jumps(possible_moves, x_jump, y_jump, visited_set)


    #deselect piece function
    def unselect_piece(self):
        #reset the possible moves
        for cell in self.moves:
            self.canvas.delete(f"move_{cell[0]}_{cell[1]}")
        self.moves = []        

    #select piece function
    def select_piece(self, x_val, y_val):
        piece = self.circles.get((x_val, y_val))

        #check if piece alredy selected
        if(self.selected_piece == (x_val, y_val)):
            #clear the selection
            self.unselect_piece()
            #remove the piece from the canvas
            piece = self.circles.pop((x_val, y_val))
            self.canvas.delete(piece["circle_id"])
            #redraw the original color circle
            self.draw_circle(self.selected_piece_color, x_val, y_val)
            #reset the selected piece attributes
            self.selected_piece = None
            self.selected_piece_color = None

        #check for appropriate piece selection based on turn
        if (self.turn == 1 and piece["color"] != "white") or (self.turn == 2 and piece["color"] != "black"):
            return

        #otherwise assume piece newly selected
        elif(self.selected_piece == None):
            #set the selection
            self.selected_piece = (x_val, y_val)
            #remove the piece from the canvas
            piece = self.circles.pop((x_val, y_val))

            #set the selected piece's color
            self.selected_piece_color = piece["color"]
            self.canvas.delete(piece["circle_id"])
            #draw a new highlighted circle
            self.draw_circle("blue", x_val, y_val)

            #get the possible moves of the selected piece
            self.get_moves(x_val, y_val)
            #display the possible moves
            self.display_moves()
            


    #set click function
    def click(self, click):
        #collect the click x point
        click_x = click.x // CELL_SIZE
        #collect the click y point
        click_y = click.y // CELL_SIZE
        #check if the selected cell is a piece
        if((click_x, click_y) in self.circles):
            #select the piece
            self.select_piece(click_x,click_y)
        #otherwise check for cell in possible moves
        elif((click_x, click_y) in self.moves):
            #move the piece
            self.move_circle(click_x,click_y)
        #otherwise assume cell not selectable

    #draw individual piece function
    def draw_circle(self, color, x_val, y_val):
        #collect the starting x point
        x_start = x_val * CELL_SIZE
        #collect the starting y point
        y_start = y_val * CELL_SIZE
        #collect the x stop point
        x_stop = x_start + CELL_SIZE
        #collect the y stop point
        y_stop = y_start + CELL_SIZE
        #draw the circle and collect the piece id
        circle_id = self.canvas.create_oval(x_start, y_start, x_stop, y_stop, fill=color, outline="black")
        #add the circle to the list of circles
        self.circles[(x_val, y_val)] = {"color": color, "circle_id": circle_id}
    
    #piece function
    def draw_pieces(self):
        #get peice diemensions
        piece_limit = self.length // 2
        #handle top left pieces
        #loop for peice placement
        for row in range(piece_limit):
            #calculate the pieces in row
            pieces_in_row = piece_limit - row
            #loop through the peices in row
            for circles in range(pieces_in_row):
                #collect the x start
                x_val = circles
                #collect the y start
                y_val = row 
                #draw each circle
                self.draw_circle("white",x_val,y_val)

        #handle bottom right pieces
        #loop for piece placement
        for row in range(4,self.length):
            pieces_in_row = row - 3
            #loop through the circles in each row
            for circles in range(pieces_in_row):
                #collect the x value
                x_val = (self.length - 1) - circles
                #draw each circle
                self.draw_circle("black", x_val, row)


    #board function
    def draw_board(self):
        #clear the corner ending position sets
        self.bottom_corner.clear()
        self.top_corner.clear()
        piece_limit = self.length // 2

        #loop through each row
        for row in range(self.length):
            #loop through each column
            for col in range(self.length):
                #collect the starting x val
                x_start = row * CELL_SIZE
                #collect the ending x val
                x_stop = x_start + CELL_SIZE
                #collect the starting y val
                y_start = col * CELL_SIZE
                #collect the ending y val
                y_stop = y_start + CELL_SIZE

                #check the bottom corner for coloration and win conditions
                if(row >= piece_limit and col >= self.length - (row - piece_limit + 1)):
                    #add the square to the set
                    self.bottom_corner.add((row, col)) 
                    #set the corner color
                    fill_color = "wheat1"
                #otherwise checkfor top corner condirions
                elif(row < piece_limit and col < piece_limit - row):
                    #add the square to the set
                    self.top_corner.add((row, col)) 
                    #set the corner color
                    fill_color = "wheat1"
                #otherwise assume non corner square
                else:
                    #set the fill color
                    fill_color = "gray"            

                #draw the rectangle on the window
                self.canvas.create_rectangle(x_start, y_start, x_stop, y_stop, fill=fill_color, outline="black")

    #function to display player turns
    def show_turns(self):
        #check for player one turn
        if(self.turn == 1):
            #display message
            self.turn_window.config(text="White's Turn")
        #check for ai_enabled
        elif(self.turn == 2 and self.ai_enabled):
            self.turn_window.config(text="AI's Turn")
        #otherwise assume player two's turn
        else:
            #display message
            self.turn_window.config(text="Black's Turn")
    
    #function to check if the white pieces have one
    def check_win_white(self):
        #check each corner square
        for squares in self.bottom_corner:
            #check for piece on square
            if(squares in self.circles):
                #check for correct color
                if(self.circles[squares]["color"] != "white"):
                    #return failure
                    return False
            #otherwise assume empty square
            else:
                #return failure
                return False
        #return success
        return True

    #function to check if the black pieces have one
    def check_win_black(self):
        #check each corner square
        for squares in self.top_corner:
            #check for piece on square
            if(squares in self.circles):
                #check for correct color
                if(self.circles[squares]["color"] != "black"):
                    #return failure
                    return False
            #otherwise assume empty square
            else:
                #return failure
                return False
        #return player win
        return True

    #function to check win for both players
    def check_win(self):
        #check for player 1 win
        player_one_flag = self.check_win_white()
        #check for player 2 win
        player_two_flag = self.check_win_black()

        #handle player 1 win
        if(player_one_flag):
            #update the turn window to show win message
            self.turn_window.config(text="Player 1 wins!!")
            #close the window
            self.window.after(3000, self.window.destroy)  

        #handle player 2 win
        if(player_two_flag):
            #update the turn window to show win message
            self.turn_window.config(text="Player 2 wins!!")
            #close the window
            self.window.after(3000, self.window.destroy)


#new class to handle AI
class Ai:
    def __init__(self, halma, is_pruning=True):
        self.halma = halma
        self.is_pruning = is_pruning
        self.prune_count = 0
        self.nodes_explored = 0

    #function to check for terminal state, similar to check win
    def check_terminal(self, halma):
        #set terminal flag
        term_flag = False
        #check for white win
        white_flag = self.halma.check_win_white()
        #check for black win
        black_flag = self.halma.check_win_black()
        #check for terminal state
        if(white_flag or black_flag):
            #reset the terminal flag
            term_flag = True
        #return the terminal flag
        return term_flag

    #min max function
    def min_max(self, board, max_flag, depth, player, time_start, time_limit, alpha=-float("inf"), beta=float("inf")):
        #increment the plies traveled
        self.nodes_explored += 1
        #check for time limit not exceeded
        if time.time() - time_start > time_limit:
            depth = 0
            #raise TimeoutError("Minimax search timed out")

        #handle base state
        if self.check_terminal(board) or depth == 0:
            #return the utility of the base state
            return self.utility(board),None
        
        #check for player turn
        if player == 0:
            #collect the list of moves
            moves = self.find_all_white_moves(board)
        #otherwise assume ai turn
        elif player == 1:
            #collect ai moves
            moves = self.find_all_black_moves(board)
        #set a variable for the best move
        best = None
        #handle maximizing
        if max_flag:
            #set the first max value
            max_val = -float("inf")
            #loop through each move in the moves list
            for(from_loc, to_loc) in moves:
                #creat a copy of the board state
                new_board = board.copy()
                #run the move for that copied board
                new_board[to_loc] = new_board.pop(from_loc)
                #continue recursive search
                move_val, _ = self.min_max(new_board, False, depth - 1, 0, time_start, time_limit, alpha, beta)
                #check for move value greater than maximum
                if move_val > max_val:
                    #set new max value
                    max_val = move_val
                    #set the best move
                    best = (from_loc, to_loc)
                #check for pruning
                if self.is_pruning:
                    #set the new alpha value
                    alpha = max(move_val, alpha)
                    #check if the beta meets pruning conditions
                    if beta <= alpha:
                        #increment the pruning conditions
                        self.prune_count +=1
                        #stop the loop
                        break
            #return the best move with its value
            return move_val, best
        #handle minimizing
        else:
            #set the first min value
            min_val = float("inf")
            #loop through each move in the moves list
            for(from_loc, to_loc) in moves:
                #create a copy of the board
                new_board = board.copy()
                #run the move on the copied board
                new_board[to_loc] = new_board.pop(from_loc)
                #continue the recursive search
                move_val, _ = self.min_max(new_board, True, depth - 1, 1, time_start, time_limit, alpha, beta)
                #check for move value less than minimum
                if move_val < min_val:
                    #set new min val
                    min_val = move_val
                    #set the best move
                    best = (from_loc, to_loc)

                #check if pruning
                if self.is_pruning:
                    #set the new beta
                    beta = min(move_val, beta)
                    #check if pruning conditions are met
                    if beta <= alpha:
                        #increment the pruning events
                        self.prune_count += 1
                        #stop the loop
                        break
            #return the best move and the heuristic value
            return move_val, best

    #utility function for heauristic value based on distance to goal and total pieces in goal space
    def utility(self, board):
        #set utility variables
        pieces_in_goal = 0
        dist_from_goal = 0
        #set utility weights
        piece_weight = 20
        dist_weight = -0.5

        #loop through each piece on the board
        for (x_pos, y_pos), piece in board.items():
            #check for proper piece color
            if piece["color"] == "black":
                #check for piece in goal
                if (x_pos, y_pos) in self.halma.top_corner:
                    #increment count of pieces in goal
                    pieces_in_goal += 1
                #otherwise use distance as utility
                else:
                    #set a temporary minimum distance as infinity
                    min_dist = float("inf")
                    #loop through goal slots
                    for(goal_x, goal_y) in self.halma.top_corner:
                        #calcualte piece distance
                        dist = math.sqrt((x_pos - goal_x)**2 + (y_pos - goal_y)**2)
                        #check for new minimum
                        if dist < min_dist:
                            #set the new minimum dist
                            min_dist = dist
                    #add the minimum distance to the total
                    dist_from_goal += min_dist

        #return the heuristic value of the given board state
        return ((pieces_in_goal * piece_weight) + (dist_from_goal * dist_weight))

    #function to get best moves
    def find_best_move(self, depth=4):
        #reset AI stats
        self.prune_count = 0
        self.plies_traveled = 0
        self.nodes_explored = 0
        #set time limit
        time_limit = 3
        #start timer
        start = time.time()
        #get the best move for the AI
        _, move = self.min_max(self.halma.circles.copy(), True, depth, 1, start, time_limit,  -float("inf"), float("inf"))
        #end the timer
        end = time.time()
        #calculate time searched
        time_searched = abs(round(start - end, 2))
        #display search stats
        print("===SEARCH STATS===")
        #check for pruning enabled
        if self.is_pruning:
            print("PRUNING ENABLED:")
            print(f"Times pruned: {self.prune_count}")
        else:
            print("PRUNING NOT ENABLED")
        print(f"Plies Traveled: {depth}")
        print(f"Nodes/Boards Explored: {self.nodes_explored}s")
        print(f"Time Spent Searching: {time_searched}s")
        print("============\n")
        #return the best move
        return move

    #function to get all moves for ai pieces
    def find_all_black_moves(self, pieces):
        #set a variable for all ai moves
        all_moves = []
        ai_pieces = []
        #set the original game state to a variable
        og_game_state = self.halma.circles.copy()
        #replace the game state with a temporary one
        self.halma.circles = pieces.copy()
        #loop through game pieces and collect each black/ai piece
        ai_pieces = [ai_pos for ai_pos, piece in pieces.items() if piece["color"] == "black"]
        #loop through each collected pieces
        for (x, y) in ai_pieces:
            #get the current circle's possible moves
            self.halma.get_moves(x, y)
            #add each collected move to all_moves
            for ai_move in self.halma.moves:
                #add the move to all moves
                all_moves.append(((x, y), ai_move))
        #reset the game pieces
        self.halma.circles = og_game_state
        #return all black piece moves
        return all_moves

    #function to find all white piece moves
    def find_all_white_moves(self, pieces):
        #set a variable for all ai moves
        all_moves = []
        player_pieces = []
        #set the original game state to a variable
        og_game_state = self.halma.circles.copy()
        #replace the game state with a temporary one
        self.halma.circles = pieces.copy()
        #loop through game pieces and collect each player piece
        player_pieces = [player_pos for player_pos, piece in pieces.items() if piece["color"] == "white"]
        #loop through each collected pieces
        for (x, y) in player_pieces:
            #get the current circle's possible moves
            self.halma.get_moves(x, y)
            #add each collected move to all_moves
            for player_move in self.halma.moves:
                #add the move to all moves
                all_moves.append(((x, y), player_move))
        #reset the game pieces
        self.halma.circles = og_game_state
        #return all player moves
        return all_moves         


main()