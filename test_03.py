import time

def loadBoard(filename):
    #check for last text file
    if(filename[-4:] == ".txt"):
        #initialize variables
        board = []
        row = []
        #open the file
        with open(filename, "r") as file:
            #read the first line
            line = file.readline()
            #loop until end of file
            while line:
                #row = list(line.strip())
                row = [char for char in line.strip() if char != ' ']
                #prepare 2D array
                board.append(row)
                #read next line
                line = file.readline()
            #after reading the whole file return the board
            return board

    #otherwise display error
    else:
        print("\nError, txt file not found. Please try again.\n")
        return None

def printBoard(board):
    #loop throw rows
    for rows in board:
        #loop through coloumns
        for cols in rows:
            print(str(cols), end="")
        print("\n")

def possibleMoves(xy_pair, board):
    #make a set of valid moves
    ok_moves = []
    #ok_moves = set()
    #create an array with all posible movements
    possible_moves = [(1,1),(1,-1),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)]
    #collect size N
    size = len(board[0])
    #set variables for the x and y position
    x,y = xy_pair
    #check each possible move
    for moves in possible_moves:
        temp_x = x + moves[0]
        temp_y = y + moves[1]
        #check if the move is viable given board dimensions
        if((temp_x >= 0 and temp_x < size)and(temp_y >= 0 and temp_y < size)):
            #add the valid move to ok moves
            ok_moves.append((temp_x,temp_y))
    #display final move list
    #print(ok_moves)
    #print("\n")
    return ok_moves

#NEW FUNCTIONS
def legalMoves(moves, path):
    #create a set to hold legal moves
    legal_moves = set()
    #iterate through each potential move
    for point in moves:
        #check for point already covered
        if point not in path:
            #add the non-explored points to the legal moves
            legal_moves.add(point)
    #return the set of legal moves
    return legal_moves

def readDictionary(filename):
    #check for last text file
    if(filename[-4:] == ".txt"):
        #initialize variables
        dictionary = set()
        #open the file
        with open(filename, "r") as file:
            #read the first line
            line = file.readline()
            #loop until end of file
            while line:
                #collect each word and format them correctly
                word = line.strip().upper()
                #add the word to the dictionary
                dictionary.add(word)
                #read next line
                line = file.readline()
            #after reading the whole file return the collected dictionary
            return dictionary

def examineState(myBoard, position, path, myDict):
    #create a sample string
    word = ""
    #read each letter in path
    for spots in path:
        #add each letter to the string
        word += myBoard[spots[0]][spots[1]]
    #check if word is in dictionary
    if word in myDict:
        return word, "Yes"
    return word, "No"

def runBoard(board_filename, dictionary_filename):
    #load the board and dictionary
    board = loadBoard(board_filename)
    dictionary = readDictionary(dictionary_filename)

    #set up prefixes to improve search time
    prefixes = set()
    for word in dictionary:
        for letters in range (1, len(word) + 1):
            prefixes.add(word[:letters])
    
    #begin display
    printBoard(board)
    print("And we're off!\nRunning with cleverness ON")
    #initialize a set of verified words
    valid_words = set()

    #set the time and move count variables
    start = time.time()
    moves_searched = 0

    #begin DFS
    #loop through rows
    for row in range(len(board)):
        #loop through columns
        for col in range(len(board[row])):
            #start the stack at each letter iteratively
            stack = [((row,col),[(row,col)])]

            # Perform DFS using the stack
            while stack:
                position, path = stack.pop()  # Get the current position and path
                word, is_in_dict = examineState(board, position, path, dictionary)
                #stop search if prefix is not found
                if word not in prefixes:
                    #stop the current search
                    continue
                #add verified words to the set
                if len(word) > 1 and is_in_dict == "Yes":
                    valid_words.add(word)
                #collect all valid moves
                legal_moves = legalMoves(possibleMoves(position, board), path)
                # Add legal moves to the stack
                for next_move in legal_moves:
                    stack.append((next_move, path + [next_move]))
                #increment the moves searched
                moves_searched += 1
                
    #get the finishing time
    end = time.time()
    total_time = end - start
                    
    #begin run board display
    print("All done\n")
    print(f"Searched total of {moves_searched} moves in {total_time} seconds\n")
    #create mini lists of each word size
    words_2 = []
    words_3 = []
    words_4 = []
    words_5 = []

    #set empty sets for words of each length
    for word in valid_words:
        if len(word) == 2:
            words_2.append(word)
        if len(word) == 3:
            words_3.append(word)
        if len(word) == 4:
            words_4.append(word)
        if len(word) == 5:
            words_5.append(word)
    #sort each mini list for easy reading
    words_2 = sorted(words_2)
    words_3 = sorted(words_3)
    words_4 = sorted(words_4)
    words_5 = sorted(words_5)

    #display stats
    #NOTE: conditions are added in the event smaller grids don't have five letter words.
    print("Words found:")
    if words_2:
        print("2 -letter words: ",end="")
        for words in words_2:
            if words == words_2[len(words_2)-1]:
                print(words)
            else:
                print(words + ", ",end="")
    if words_3:        
        print("3 -letter words: ",end="")
        for words in words_3:
            if words == words_3[len(words_3)-1]:
                print(words)
            else:
                print(words + ", ",end="")
    if words_4:
        print("4 -letter words: ",end="")
        for words in words_4:
            if words == words_4[len(words_4)-1]:
                print(words)
            else:
                print(words + ", ",end="")
    if words_5:
        print("5 -letter words: ",end="")
        for words in words_5:
            if words == words_5[len(words_5)-1]:
                print(words)
            else:
                print(words + ", ",end="")

    print(f"\nFound {len(valid_words)} in total.")
    print("Alpha-sorted list words:")
    valid_words = sorted(list(valid_words))
    for words in valid_words:
        if words != list(valid_words)[len(valid_words) - 1]:
            print(words + ", ",end="")
        else:
            print(words)
    print("\n")
    

# TODO define runBoard and other functions.
runBoard("board2.txt", "twl06.txt")
runBoard("board3.txt", "twl06.txt")
runBoard("board4.txt", "twl06.txt")
