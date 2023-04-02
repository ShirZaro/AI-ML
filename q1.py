import copy
import numpy as np


class Boards:  # A board object that stores a list of stars, a matrix of the board, its length, the amount of its parents, its direct parent and its cost function
    def __init__(self,state,parent):
        self.state = np.array(state)
        self.parent= parent
        self.stars = []
        self.cost = 0
        self.add_stars()
        self.f_n = 0
        self.len = len(state)

    def set_cost(self,cost): # Allows update of the board cost
        self.cost = cost

    def get_cost(self):
        return self.cost

    def add_stars(self): # Initialize the list of stars in the matrix
        for row in range(0, len(self.state)):
            for col in range(0, len(self.state)):
                if self.state[row, col] == 2:
                    self.stars.append([row, col])

    def set_f_n(self,f_n):
        self.f_n = f_n




def find_path(starting_board,goal_board,search_method,detail_output): # The main function that allows you to send 2 boards and choose a search method and print form
    if search_method ==1:
        myAstar(starting_board,goal_board,detail_output) # Search function A*


def myAstar(starting_board,goal_board,detail_output):
    parent = Boards(starting_board, 0)
    open_list = []
    neighbor = []
    starting_board = Boards(starting_board, parent) # Converting the start board to a panel object
    goal_board = Boards(goal_board, parent) # Converting the end board to a panel object
    if check_board(starting_board, goal_board) == True: # Checking possible edge cases
        open_list.append(starting_board) # Adding the start panel to the list of open boards
        neighbor.append(starting_board)
        closed_list = []
        manhattan_board = copy.deepcopy(goal_board.state)
        manhattan_distance(goal_board, starting_board, manhattan_board) # Initialize a Manhattan board with the distances between the indices of each slot from its nearest target
        visited = []
        visited.append(copy.deepcopy(starting_board.stars)) # The list of boards I've already visited, so that I don't get stuck in an endless loop between 2 boards
        flag = False
        print_all = []
        while len(open_list) > 0 :
            min_board = []
            min_f_n = 1000
            for v in open_list:
                neighbor= neighbor + (find_next_steps(v, goal_board, visited)) # Finding all possible steps - all the following boards
                if v.stars == goal_board.stars: # If the list of stars on my board and the target board are the same - I have reached the destination
                    flag = True
                    print_all.append(v)
                    find_my_path(v, print_all)
                    print_my_path(print_all,detail_output)
                    open_list.remove(v)
                    closed_list.append(v)
                for n in neighbor: # If I didn't reach the goal - going through all the possible steps and choosing the step with the minimum cost function
                    n.set_cost(sum_cost(n))
                    n.set_f_n(n.get_cost() + heuristoc(n.stars.copy(), manhattan_board))
                    if n.f_n <= min_f_n:
                        min_f_n = n.f_n
                        min_board = n
                if min_board==[]:
                    print("No path found")
                    return None
                if flag == False:
                    open_list.append(min_board)
                    open_list.remove(v)
                    neighbor.remove(min_board)





def check_board(starting_board,goal_board): # A function that checks if the obstacles at the start and at the destination are not the same, and if there is an agent out of place and blocked by barriers from all directions
    for i in range(0,starting_board.len):
        for j in range(0,starting_board.len):
            if starting_board.state[i][j]== 2:
                if i ==0:
                    if starting_board.state[i+1][j]==1 and starting_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                        print("there is no solution for this board")
                        return False
                if i == 5:
                    if starting_board.state[i-1][j]==1 and starting_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                        print("there is no solution for this board")
                        return False
                if j ==0 :
                    if starting_board.state[i-1][j]==1 and starting_board.state[i+1][j]==1 and  starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                        print("there is no solution for this board")
                        return False
                if j ==5:
                    if starting_board.state[i-1][j]==1 and starting_board.state[i+1][j]==1 and  starting_board.state[i][j-1]==1 and goal_board.state[i][j] != 2:
                        print("there is no solution for this board")
                        return False
                else:
                    if starting_board.state[i-1][j]==1 and starting_board.state[i+1][j]==1 and starting_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                        print("No path found")
                        return False
            if starting_board.state[i][j] ==1 and goal_board.state[i][j] != 1:
                print("the blocks are not in the same location, the boards are not legal")
                return False
            if starting_board.state[i][j] != 1 and goal_board.state[i][j] == 1:
                print("the blocks are not in the same location, the boards are not legal")
                return False
    return True



def print_my_path(print_all,detail_output): # Print the solution
    print_all.reverse()
    for s in range(1,len(print_all)):
        if s == 1:
            print('Board', s, '(starting position):')
        if s == len(print_all)-1:
            print('Board', s, '(goal position):')
        if s != len(print_all)-1 and s != 1:
            print('Board', s, ':')
        for i in range(0,6):
            temp = ''
            if i == 0:
                print('    1 2 3 4 5 6')
            for j in range(0,6):
                if print_all[s].state[i][j] == 1:
                    x='@ '
                if print_all[s].state[i][j] == 2:
                    x='* '
                if print_all[s].state[i][j] == 0:
                    x= '  '
                temp = temp+ x
            print(i+1,":",temp)
        if s == 2 and detail_output== True:
            print("Heuristic", print_all[s].f_n -print_all[s].cost + 1 )




def find_my_path(v,print_all): # A recursive function that finds all the previous boards to the target board I reached
    if v.parent !=0:
        print_all.append(v.parent)
        find_my_path(v.parent,print_all)


def sum_cost(v): # A function that finds the number of fathers of each board - the number of steps taken up to it
    all = []
    find_my_path(v,all)
    return(len(all)-1)




def heuristoc(stars,manhattan_board): # A function that calculates my heuristic, the Manhattan distances of the stars in the current board
    totdist = 0
    for s in stars:
        distance = manhattan_board[s[0],s[1]]
        totdist = totdist + distance
    return totdist




def manhattan_distance(goal_board,starting_board,manhattan_board): # Initialization of help board - Manhattan board
    for row in range(0,len(goal_board.state)):
        for col in range(0,len(goal_board.state)):
            all_distance = []

            for star in goal_board.stars:
                dist1 = row - star[0]
                dist2 = col - star[1]
                totdist = abs(dist1) + abs(dist2)
                all_distance.append(totdist)
            mind = min(all_distance)
            manhattan_board[row][col] = mind
    if len(goal_board.stars) < len(starting_board.stars):
        for col in range(0, len(manhattan_board)):
            if manhattan_board[5][col] > 1:
                manhattan_board[5][col] = 1
        for col in range(0, len(manhattan_board)):
            if manhattan_board[4][col] > 2:
                manhattan_board[4][col] = 2
        for col in range(0, len(manhattan_board)):
            if manhattan_board[3][col] > 3:
                manhattan_board[3][col] = 3
        for col in range(0, len(manhattan_board)):
            if manhattan_board[2][col] > 4:
                manhattan_board[2][col] = 4
        for col in range(0, len(manhattan_board)):
            if manhattan_board[1][col] > 5:
                manhattan_board[1][col] = 5


def find_next_steps(v,goal_board,visited):
    optionsList = []
    for s in v.stars:
        if s[0] < 5:
            if v.state[s[0] + 1,s[1]] == 0:
                new_board = copy.deepcopy(v.state)
                new_board[s[0] + 1, s[1]] = 2
                new_board[s[0],s[1]] = 0
                temp = Boards(new_board,v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    visited.append(copy.deepcopy(temp.stars))

        if s[1] < 5:
            if v.state[s[0], s[1] + 1] == 0:
                new_board2 = copy.deepcopy(v.state)
                new_board2[s[0],s[1]+1] = 2
                new_board2[s[0], s[1]] = 0
                temp = Boards(new_board2, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    visited.append(copy.deepcopy(temp.stars))


        if s[1] > 0:
            if v.state[s[0], s[1] - 1] == 0:
                new_board3 = copy.deepcopy(v.state)
                new_board3[s[0], s[1] - 1] = 2
                new_board3[s[0], s[1]] = 0
                temp = Boards(new_board3, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    visited.append(copy.deepcopy(temp.stars))

        if s[0] > 0:
            if v.state[s[0] - 1, s[1]] == 0:
                new_board4 = copy.deepcopy(v.state)
                new_board4[s[0]-1, s[1]] = 2
                new_board4[s[0], s[1]] = 0
                temp = Boards(new_board4, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    visited.append(copy.deepcopy(temp.stars))

        if len(v.stars) > len(goal_board.stars):
            if s[0] == 5 :
                new_board5 = copy.deepcopy(v.state)
                new_board5[s[0], s[1]] = 0
                temp = Boards(new_board5, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    visited.append(copy.deepcopy(temp.stars))

    return optionsList



starting_board = [[2,0,2,0,2,0],[0,0,0,2,1,2],[1,0,0,0,0,0],[0,0,1,0,1,0],[2,0,0,0,0,0],[0,1,0,0,0,0]]
goal_board = [[2,0,2,0,0,2],[0,0,0,2,1,0],[1,0,0,0,0,2],[0,0,1,0,1,0],[0,0,0,0,0,0],[0,1,0,0,0,0]]

find_path(starting_board,goal_board,1,True)


