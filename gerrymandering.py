from turtle import *
from Lab5_functions import *

#This function prints the intro information as well as accepts the initial
#input from the user and prints an error message if that input is not in
#the given file. This function also calls the other functions into action.
def main():
    width = 500
    height = 500
    print("This program allows you to search through")
    print("data bout congressional voting districts")
    print("and determine wether a particular state is")
    print("gerrymandered")
    print()
    state = input("Which state did you want to look up? ")
    eligible_line = find_line(state, 'districts.txt')
    if eligible_line == None:
        print('"' + state + '"' + ' not found.')
        return 0
    else:
        setworldcoordinates(0,height,width,0)
        clear()
        shape('turtle')
        bgcolor('grey')
        speed(9999)
        line,dem,gop,end = static_graphics(eligible_line,state,height,width)
        eligible_voters = process_line(line,state)
        draw_districts(gop,dem,end,height,width)
        gop,dem = calculate_wastage(dem,gop,line,end)
        is_gerrymandered(gop,dem,eligible_voters,width)

#this function searches for the line in districts.txt that begins with
#the users input, returning the desired line and its votes as a list
def find_line(state,filename):
    with open(filename) as file:
        lines = file.readlines()
        for i in range(len(lines)):
            eligible_line = lines[i]
            if eligible_line.lower().startswith(state.lower()):
                return str(eligible_line)

#This function separates the the unaltered list for a state into dem votes
#and gop votes as different lists. This funtion also draws the basic lines for the graph.
def static_graphics(eligible_line,state,height,width):
    new_line = eligible_line.split(",")
    data_list = []
    fake_list = []
    for data in new_line:
        try:
            int(data)
            data_list.append(int(data))
        except ValueError:
            fake_list.append(data)
    draw_line((width // 2),0,(width // 2),height,'black')
    draw_line(0,0,width,0,'black')
    up()
    goto(0,0)
    write(new_line[0],font = 20)
    up()
    dem = []
    gop = []
    for demvotes in data_list[1:len(data_list):3]:
        dem.append(demvotes)
    for gopvotes in data_list[2:len(data_list):3]:
        gop.append(gopvotes)
    if new_line[1] == 'AL':
        end = data_list[1]
        dem = data_list[0]
        gop = data_list[1]
    else:
        end = data_list[-3]
    line = data_list
    return line,dem,gop,end

#This function takes the altered line for a states list of total votes
#and returns it without string charcters and opens the eligible voter file,
#returning that information for each state.
def process_line(line,state):
    with open('eligible_voters.txt') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            voters = lines[i]
            if voters.lower().startswith(state.lower()):
                list_of_voters = voters.split(",")
                total_voters = []
                fake_list = []
                for voters in list_of_voters:
                    try:
                        int(voters)
                        total_voters.append(voters)
                    except ValueError:
                        fake_list.append(voters)
                eligible_voters = int(total_voters[0])
                return eligible_voters

#THis function calculates the total wasted votes for both parties in one state
#then printing that information below the original prompt.
def calculate_wastage(dem,gop,line,end):
    election_totals = []
    winning_votes = []
    total_wasted_dem = 0
    total_wasted_gop = 0
    if end == line[1]:
        election_totals.append(gop + dem)
        winning_total = election_totals[0]
        if line[0] > line[1]:
            wasted_gop = line[1]
            total_wasted_gop += wasted_gop
            wasted = line[0] - ((winning_total // 2) + 1)
            total_wasted_dem += wasted
        if line[1] > line[0]:
            wasted_dem = line[0]
            total_wasted_dem += wasted_dem
            wasted = line[1] - ((winning_total // 2) + 1)
            total_wasted_gop += wasted
        if line[0] == line[1]:
            total_wasted_dem = 0
            total_wasted_gop = 0

    if end != line[1]:
        for (item1, item2) in zip(dem, gop):
            election_totals.append(item1 + item2)
        for wins in election_totals:
            winning_amount = (wins // 2) + 1
            winning_votes.append(winning_amount)
        for elections in range(0,len(winning_votes)):
            if gop[elections] > dem[elections]:
                wasted = gop[elections] - winning_votes[elections]
                dem_wasted = dem[elections]
                total_wasted_dem += dem_wasted
                total_wasted_gop += wasted
            if dem[elections] > gop[elections]:
                wasted = dem[elections] - winning_votes[elections]
                gop_wasted = gop[elections]
                total_wasted_gop += gop_wasted
                total_wasted_dem += wasted
            if dem[elections] == gop[elections]:
                wasted = 0
                total_wasted_dem += wasted
                total_wasted_gop += wasted
    print("Total Wasted Republican Votes: " + str(total_wasted_gop))
    print("Total Wasted Democratic Votes: " + str(total_wasted_dem))
    return total_wasted_gop,total_wasted_dem

#This function uses the total wasted votes from a state and
#compares this to the total eligible voters to predict if
#gerrymandering ocured.
def is_gerrymandered(gop,dem,eligible_voters,width):
    if dem > gop:
        dif = dem - gop
        if dif > (eligible_voters * .07):
            print("Gerrymandered benefiting the Republicans")
    if gop > dem:
        dif = gop - dem
        if dif > (eligible_voters * .07):
            print("Gerrymandered benefiting the Democrats")
    print(eligible_voters,"eligible voters")
    goto(width - 120,0)
    write(str(eligible_voters) + " eligible voters",font = 20)

#This function draws the red and blue parts of the graph to visually
#demonstrate the district votes from each states
def draw_districts(gop,dem,end,width,height):
    goto(0,25)
    dem_widths_list = []
    gop_widths_list = []
    gop_xval_list = []
    for districts in range(end):
        dem_widths = int((dem[districts] / (dem[districts] + gop[districts])) * width)
        dem_widths_list.append(dem_widths)
        gop_widths = int((gop[districts] / (dem[districts] + gop[districts])) * width)
        gop_widths_list.append(gop_widths)
    dem_yval = 25
    gop_yval = 25
    for bars in dem_widths_list:
        draw_rect(0,dem_yval,bars,25,'blue')
        dem_yval += 25 + 5
    for xvals in gop_widths_list:
        gop_xvals = width - xvals
        gop_xval_list.append(gop_xvals)
    for bars in gop_xval_list:
        draw_rect(bars,gop_yval,(width - bars)- 5 ,25,'red')
        gop_yval += 25 + 5
    
main()
