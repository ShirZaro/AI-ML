import copy
import math
import random

import numpy as np

class Boards:  # אובייקט לוח השומר רשימת כוכבים, מטריצה של הלוח, אורכו, את כמות ההורים שלו,האבא הישיר שלו ואת הפונקציית עלות שלו
    def __init__(self,state,parent):
        self.state = np.array(state)
        self.parent= parent
        self.stars = []
        self.cost = 0
        self.add_stars()
        self.f_n = 0
        self.len = len(state)
        self.val = 0
        self.grade = 0

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

    def set_value(self,val):
        self.val = val

    def set_grade(self,grade):
        self.grade = grade



def find_path(starting_board,goal_board,search_method,detail_output): # The main function that allows you to send 2 boards and choose a search method and print form
    if search_method ==1:
        myAstar(starting_board,goal_board,detail_output) # Search function A*
    if search_method ==2:
        myHillClimbing(starting_board,goal_board,detail_output) # Search function Hill Climbing
    if search_method==3 :
        mySimulatedAnnealing(starting_board,goal_board,detail_output) # Search function Simulated Annealing
    if search_method ==4:
        mykbeam(starting_board, goal_board, detail_output) # Search function k beam
    if search_method ==5:
        genetic_algorithm(starting_board, goal_board, detail_output) # Search function genetic algorithm

def myAstar(sb,gb,detail_output):
    parent = Boards(sb, None)
    open_list = []
    neighbor = []
    starting_board = Boards(sb, parent)
    goal_board = Boards(gb, parent)
    if check_board(starting_board, goal_board) == True: #Checking end cases
        open_list.append(starting_board)
        neighbor.append(starting_board)
        closed_list = []
        visited = []
        visited.append(copy.deepcopy(starting_board.stars))
        flag = False
        print_all = []
        while len(open_list) > 0:
            min_board = []
            min_f_n = 1000
            for v in open_list:
                neighbor= neighbor + (find_next_steps(v, goal_board, visited,1))
                if v.stars == goal_board.stars: #If I reached my destination
                    flag = True
                    print_all.append(v)
                    find_my_path(v, print_all)
                    print_my_path(print_all,detail_output,1,None,None,None)
                    open_list.remove(v)
                    closed_list.append(v)
                set_all_val(neighbor, 0,goal_board)#A help function that initializes the heuristics for all neighbors
                for n in neighbor:
                    n.set_cost(sum_cost(n)) #Finding the cost of getting to the board
                    n.set_f_n(n.get_cost() + n.val)
                    if n.f_n <= min_f_n:
                        min_f_n = n.f_n
                        min_board = n
                if min_board==[]:
                    print("No path found.")
                    return None
                if flag == False:
                    open_list.append(min_board)
                    open_list.remove(v)
                    neighbor.remove(min_board)


def myHillClimbing(starting_board,goal_board,detail_output):
    parent = Boards(starting_board, None)
    open_list = []
    count = 1
    starting_board = Boards(starting_board, parent)
    goal_board = Boards(goal_board, parent)
    if check_board(starting_board, goal_board) == True: #if the board are legal
        open_list.append(starting_board)
        flag = False
        print_all = []
        visited=[]
        firstneighbor = find_next_steps(starting_board, goal_board, visited, 2) #find the possible next steps
        size = min(len(firstneighbor),5) #if the number of the first neighbor is less than 5 - we cant reset 5 times.
    while len(open_list)>0:
        min_board = []
        set_all_val(open_list,0,goal_board) # set the hueristic values for all the boards
        for v in open_list:
            if count > size:  # if I canr reset anymore and there is no soulotion
                print("No path found.")
                if min_board in open_list:
                    open_list.remove(min_board)
                return None
            min_val = v.val # select the minimum value
            neighbor = find_next_steps(v, goal_board, visited,2)
            if v.stars == goal_board.stars:  # if I reached to the goal
                flag = True
                print_all.append(v)
                find_my_path(v, print_all)
                print_my_path(print_all, detail_output,2,None,None,None)
                open_list.remove(v)
            set_all_val(neighbor,0,goal_board) # set the hueristic values for the possible steps
            for n in neighbor:  #select the minmum step that possible
                if n.val < min_val:
                    min_val = n.val
                    min_board = n
            if min_board == []: # if there is no one better than the current board
                min_board = v
            if min_board not in open_list:
                if flag == False:
                    open_list.append(min_board)
                    open_list.remove(v)
            if min_board.stars == v.stars: # if there is no one better than the current board
                if flag == False:
                    if count <= size: # reset for 5 times (or less if we have less than 5 first neigbors
                        rand = random.choice(firstneighbor) # select random board
                        open_list.append(rand)
                        open_list.remove(min_board)
                        firstneighbor.remove(rand)
                        count = count +1


def mySimulatedAnnealing(starting_board,goal_board,detail_output):
    parent = Boards(starting_board, None)
    open_list = []
    starting_board = Boards(starting_board, parent)
    goal_board = Boards(goal_board, parent)
    if check_board(starting_board, goal_board) == True:
        open_list.append(starting_board)
        flag = False
        f = True
        saved =  False # save the values I want to prrint
        print_all = []
        visited = []
        current = starting_board
        t = 0
        fro = []
        to = []
        my_chance =[]
        chance = 0
        for i in range(0,101):
            T = (100 - t)/40
            if T==0 :
                print("No path found.")
                return current
            current.set_value(heuristoc(current.stars.copy(),goal_board)) # set heuristoc values for the current board
            if f == True:
                neighbor = find_next_steps(current, goal_board, visited, 2)
                set_all_val(neighbor, 0,goal_board) # set all heuristoc values for the possible steps
            if current.stars == goal_board.stars: # if I reached to the goal
                flag = True
                print_all.append(current)
                find_my_path(current, print_all)
                print_my_path(print_all, detail_output,3,fro,to,my_chance)
                return None
            else:
                if f== True:
                    options = neighbor.copy()
                if len(options) == 0:
                    print("No path found.")
                    return None
                rand = random.choice(options) # select random possible step
                delta = current.val - rand.val
                if saved == False: # if I didnt saved yet
                    for s in rand.stars:
                        if s not in current.stars:
                            to.append(s) # to where I wanna go
                    for s1 in current.stars:
                        if s1 not in rand.stars:
                            fro.append(s1) # from where
                if delta >0 : # if the step heuristoc is better than mine
                    chance = 1
                    current = rand
                    f = True
                if delta < 0: # else
                    p = random.uniform(0, 1)
                    m = (delta/T)
                    chance = math.exp(m) #I will go their in e^(delta/T) chance
                    if p < chance:
                        current = rand
                        f = True
                    if p > chance:
                        options.remove(rand)
                        f = False
                if saved == False: # if I didnt finish saving the step
                    my_chance.append(chance)
                    if chance ==1 :
                        saved = True
            t = t +1



def mykbeam(starting_board,goal_board,detail_output):
    parent = Boards(starting_board,None)
    open_list = []
    starting_board = Boards(starting_board, parent)
    goal_board = Boards(goal_board, parent)
    if check_board(starting_board, goal_board) == True:
        open_list.append(starting_board)
        flag = False
        print_all = []
        visited = []
        save = False
        while len(open_list) > 0:
            top3 = []
            neighbor = []
            values = []
            for v in open_list:
                neighbor = neighbor + find_next_steps(v, goal_board, visited, 1)
                if v.stars == goal_board.stars: #if I reached to the goal
                    flag = True
                    print_all.append(v)
                    find_my_path(v, print_all)
                    print_my_path(print_all, detail_output,4,None,None,None)
                    return None
            set_all_val(neighbor, values, goal_board) #set aqkk ny neighbors values
            if len(values) == 0:
                print("No path found.")
                return None
            values.sort() # sort from the min to the max
            for i in range(0,3): # select the best 3 boards from my neighbors
                stop= False
                for j in neighbor:
                    if stop == False:
                        if values[i] == j.val:
                            top3.append(j)
                            neighbor.remove(j)
                            stop = True
            if save == False and detail_output == True:
                print_k_beam(v,top3)
                save = True
            if flag == False:
                open_list = []
                for i in top3:
                    open_list.append(i)
                    visited.append(i)

def print_k_beam(v,top3):
    print('Board 1 (starting position):')
    for i in range(0, 6):
        temp = ''
        if i == 0:
            print('    1 2 3 4 5 6')
        for j in range(0, 6):
            if v.state[i][j] == 1:
                x = '@ '
            if v.state[i][j] == 2:
                x = '* '
            if v.state[i][j] == 0:
                x = '  '
            temp = temp + x
        print(i + 1, ":", temp)
    if len(top3) >0 :
        print('Board 2a')
        for i in range(0, 6):
            temp = ''
            if i == 0:
                print('    1 2 3 4 5 6')
            for j in range(0, 6):
                if top3[0].state[i][j] == 1:
                    x = '@ '
                if top3[0].state[i][j] == 2:
                    x = '* '
                if top3[0].state[i][j] == 0:
                    x = '  '
                temp = temp + x
            print(i + 1, ":", temp)
    if len(top3) >1 :
        print('Board 2b:')
        for i in range(0, 6):
            temp = ''
            if i == 0:
                print('    1 2 3 4 5 6')
            for j in range(0, 6):
                if top3[1].state[i][j] == 1:
                    x = '@ '
                if top3[1].state[i][j] == 2:
                    x = '* '
                if top3[1].state[i][j] == 0:
                    x = '  '
                temp = temp + x
            print(i + 1, ":", temp)
    if len(top3) >2 :
        print('Board 2c:')
        for i in range(0, 6):
            temp = ''
            if i == 0:
                print('    1 2 3 4 5 6')
            for j in range(0, 6):
                if top3[2].state[i][j] == 1:
                    x = '@ '
                if top3[2].state[i][j] == 2:
                    x = '* '
                if top3[2].state[i][j] == 0:
                    x = '  '
                temp = temp + x
            print(i + 1, ":", temp)

def genetic_algorithm(sb,gb,detail_output):
    parent = Boards(sb, None)
    starting_board = Boards(sb, parent)  # turning starting board to a board object
    goal_board = Boards(gb, parent)  # same on goal board
    counter = 0
    if check_board(starting_board, goal_board) == True:  # checking that the boards are legal
        print_all = []
        visited = []
        population = []
        f1 = False
        toprint = []
        mutation= False
        neighbor = find_next_steps(starting_board, goal_board, visited,2) # finding all my neighbors
        alloptions = neighbor.copy() # help array - keeps all the possible result boards. after matching between 2 boards-
        #their child could be zero, one or tow steps max after one of them.it helps me kipping that agent will not desapper or appear in the match.
        for n in neighbor :
            alloptions =alloptions+ find_next_steps(n, goal_board, visited,2) #inserting 2 steps forward
        if len(neighbor)>=10:
            for k in range(0,10):
                i = random.randint(0, (len(neighbor)-1))
                population.append(neighbor[i])
                neighbor.remove(neighbor[i])
                f1 = True
        if len(neighbor)<10 and f1 == False: # if i have less then 10 neighbor, I will put all myneighbor to the population
            for n in neighbor:
                population.append(n)
        while len(population)>0:
            if counter == 300: # if it takes more than 5000 steps - there is no solution
                print("No path found.")
                if detail_output == True:
                    print_genetic( toprint)
                return None
            all_vals = []
            for i in population:
                if i.stars == goal_board.stars: # if I reached to my goal
                    print_all.append(i)
                    find_my_path(i, print_all)
                    print_my_path(print_all, detail_output,5,None,None,None)
                    if detail_output == True:
                        print_genetic(toprint)
                    return None
            newpop=[] # help array - new population
            set_all_val_genety(population,all_vals,goal_board)
            sum_values = sum(all_vals)
            give_grades(population,sum_values)
            count = 0
            flag = False
            while flag == False: # I want to make 10 childrends to keep the population size k = 10
                p= []
                parents = []
                for j in range(0,2):
                    p.append(Choose_parents(population))
                parents.append(p)
                child = make_children(parents,alloptions,visited,goal_board,mutation,toprint)
                if child != None: # if I succeeded to make a child
                    newpop.append(child)
                    count = count+1
                if count == 10: # if I have 10 childrend
                    flag = True
            population = newpop.copy() # replacing my population in new one
            neighbor = []
            for i in population:
                neighbor =neighbor+ find_next_steps(i, goal_board, visited, 2)
            alloptions = neighbor.copy() # replacing my options
            for n in neighbor:
                alloptions = alloptions + find_next_steps(n, goal_board, visited, 2)
            counter += 1 # count to 5000 steps



def Choose_parents(population):
    n = random.uniform(0, 1)
    parent = None
    allGrades = []
    for p in population:
        allGrades.append(p.grade)
    allGrades.sort()  # sorting my grades array For setting boundaries
    for i in range(0,len(population)-1):
        if allGrades[i] < n :
            if allGrades[i+1] >n:
                for p in population:
                    if p.grade == allGrades[i+1]:
                        parent= p  # chosing my parents according to the grades and random number
    if n > max(allGrades):
        for p in population:
            if p.grade == max(allGrades):
                parent= p
    return parent


def make_children(parents,alloptions,visited,goal_board,mutation,toprint):
    saved = False
    parent1= parents[0][0]
    parent2= parents[0][1]
    children = parent1.state.copy() # the board as state and not as an object
    cut = random.randint(1,5)
    stars = []
    v = []
    child = None
    f = False
    for i in range(0,5): # cuting and attach the boards to a child board
        for j in range(0,cut):
            children[i][j]=parent1.state[i][j].copy()
    for i in range(0,5):
        for j in range(cut+1,5):
            children[i][j]=parent2.state[i][j].copy()
    for row in range(0, len(children)): # setting an agents list for our child
        for col in range(0, len(children)):
            if children[row, col] == 2:
                stars.append([row, col])
    for i in alloptions:
        if f == False:
            if stars == i.stars: # if the board is possible(no one appear or desapear)
                n = random.uniform(0, 1) # The probability of creating a mutation
                if n >= 0.65: # 35% to creat a mutation
                    mutation = True
                    options = find_next_steps(i,goal_board,v,2) # the mutation is a random Neighbor of my child
                    x = random.randint(0, (len(options) - 1))
                    child = options[x]
                if n <0.65: # if there is no mutation
                    if stars == parent1.stars:
                        my_parent = parent1.parent
                    if stars == parent2.stars:
                        my_parent = parent2.parent
                    if stars != parent1.stars:# if the agents are moving in both of the boards - we will split it to 2 steps and We will restore the steps he took
                        if stars != parent2.stars:
                            for s in stars:
                                for m in parent1.stars:
                                    if m != s:
                                        temp_state = parent1.state.copy()
                                        temp_state[m[0]][m[1]]= 0
                                        temp_state[s[0]][s[1]] = 2
                            temp1 = Boards(temp_state.copy(),parent1)
                            my_parent = temp1
                    child = Boards(children,my_parent) # creating a new board object with his parent information
                f = True
                if saved == False:
                    toprint.append(parent1)
                    toprint.append(parent2)
                    toprint.append(child)
                    if mutation == True:
                        toprint.append(0)
                    saved = True
    return child



def give_grades(population,sum_values):
    maxgrade = 0
    for p in population:
        if p.val> maxgrade:
            maxgrade = p.val
    for p in population:
        p.set_grade((maxgrade-p.val)/maxgrade) # spliting the population to Ranges according to their heuristics


def set_all_val(my_list,all_vals,goal_board):
    for l in my_list:
        l.set_value(heuristoc(l.stars.copy(), goal_board))
        if all_vals != 0:
            all_vals.append(heuristoc(l.stars.copy(),goal_board))

def set_all_val_genety(my_list,all_vals,goal_board):#setting the heuristics to the population
    for l in my_list:
        l.set_value(heuristoc(l.stars.copy(), goal_board))
        all_vals.append(heuristoc(l.stars.copy(),goal_board))

def check_board(starting_board,goal_board): # checking if the boards are legal and possible
    for i in range(0,starting_board.len):
        for j in range(0,starting_board.len):
            if starting_board.state[i][j]== 2:
                if i ==0:
                    if j  == 0:
                        if starting_board.state[i + 1][j] == 1 and starting_board.state[i][j + 1] == 1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    if j == 5:
                        if starting_board.state[i+1][j]==1 and starting_board.state[i][j-1]==1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    else:
                        if starting_board.state[i+1][j]==1 and starting_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                if i == 5:
                    if j == 5:
                        if starting_board.state[i-1][j]==1 and starting_board.state[i][j-1]==1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    if j == 0 :
                        if starting_board.state[i-1][j]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    else:
                        if starting_board.state[i-1][j]==1 and starting_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and goal_board.state[i][j] != 2:
                            print("No path found.")
                            return False
            if goal_board.state[i][j]== 2:
                if i ==0:
                    if j  == 0:
                        if goal_board.state[i + 1][j] == 1 and goal_board.state[i][j + 1] == 1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    if j == 5:
                        if goal_board.state[i+1][j]==1 and goal_board.state[i][j-1]==1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    else:
                        if goal_board.state[i+1][j]==1 and goal_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                if i == 5:
                    if j == 5:
                        if goal_board.state[i-1][j]==1 and goal_board.state[i][j-1]==1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    if j == 0 :
                        if goal_board.state[i-1][j]==1 and goal_board.state[i][j+1]==1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
                    else:
                        if goal_board.state[i-1][j]==1 and goal_board.state[i][j-1]==1 and starting_board.state[i][j+1]==1 and starting_board.state[i][j] != 2:
                            print("No path found.")
                            return False
            if starting_board.state[i][j] ==1 and goal_board.state[i][j] != 1:
                print("the blocks are not in the same location, the boards are not legal")
                return False
            if starting_board.state[i][j] != 1 and goal_board.state[i][j] == 1:
                print("the blocks are not in the same location, the boards are not legal")
                return False
    return True



def print_my_path(print_all,detail_output,num,fro,to,chance): # printing the soulotion
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
        if num ==1:
            if s == 2 and detail_output== True:
                print("Heuristic", print_all[s].f_n -print_all[s].cost + 1 )
        if num ==3:
            if s == 1 and detail_output == True:
                for i in range(0,len(chance)):
                    print("action:(",fro[i][0],",",fro[i][1], ")->(",to[i][0],",",to[i][1],"); probability:",chance[i])



def print_genetic(toprint): # printing the detail output = true for the genetic
    parent1 = toprint[0]
    parent2 = toprint[1]
    child = toprint[2]
    if toprint[3] == 0:
        answere = 'yes'
    else:
        answere = 'no'
    print('Starting board 1 (probability of selection from population:', parent1.grade, '):')
    for i in range(0, 6):
        temp = ''
        if i == 0:
            print('    1 2 3 4 5 6')
        for j in range(0, 6):
            if parent1.state[i][j] == 1:
                x = '@ '
            if parent1.state[i][j] == 2:
                x = '* '
            if parent1.state[i][j] == 0:
                x = '  '
            temp = temp + x
        print(i + 1, ":", temp)
    print('Starting board 2 (probability of selection from population:', parent2.grade, '):')
    for i in range(0, 6):
        temp = ''
        if i == 0:
            print('    1 2 3 4 5 6')
        for j in range(0, 6):
            if parent2.state[i][j] == 1:
                x = '@ '
            if parent2.state[i][j] == 2:
                x = '* '
            if parent2.state[i][j] == 0:
                x = '  '
            temp = temp + x
        print(i + 1, ":", temp)
    print('Result board (mutation happened:', answere, '):')
    for i in range(0, 6):
        temp = ''
        if i == 0:
            print('    1 2 3 4 5 6')
        for j in range(0, 6):
            if child.state[i][j] == 1:
                x = '@ '
            if child.state[i][j] == 2:
                x = '* '
            if child.state[i][j] == 0:
                x = '  '
            temp = temp + x
        print(i + 1, ":", temp)



def find_my_path(v,print_all): # finding all the previos boards for given board
    if v.parent !=None:
        print_all.append(v.parent)
        find_my_path(v.parent,print_all)


def sum_cost(v): #findinig the cost for each board
    all = []
    find_my_path(v,all)
    return(len(all))




def heuristoc(my_stars,goal_board): # finding my heuristoc
    Gstars = copy.deepcopy(goal_board.stars)
    hefresh = len(my_stars) - len(goal_board.stars)
    my_heuristoc = 0
    for s in my_stars:
        f = False
        minD= 1000
        minG = None
        row = s[0]
        col = s[1]
        if hefresh > 0:
            f = True
            Gstars.append([6,col])
        for g in Gstars:
            dist1 = row - g[0]
            dist2 = col - g[1]
            totdist = abs(dist1) + abs(dist2)
            if totdist < minD :
                minD = totdist
                minG = g
        if minG == [6,col]:
            hefresh = hefresh - 1
        if f == True:
            if minG != [6,col]:
                Gstars.remove([6,col])
        my_heuristoc = my_heuristoc + minD
        Gstars.remove(minG)
    return my_heuristoc





def find_next_steps(v,goal_board,visited,num): # finding the next possible steps - if the number is 1 , I will save the boards tht im finding
    # and will not repeat them. if the number is 2 - I can find the same board more  than once.
    optionsList = []
    if num ==2:
        visited = []
    for s in v.stars:
        if s[0] < 5:
            if v.state[s[0] + 1,s[1]] == 0:
                new_board = copy.deepcopy(v.state)
                new_board[s[0] + 1, s[1]] = 2
                new_board[s[0],s[1]] = 0
                temp = Boards(new_board,v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    if num == 1:
                        visited.append(copy.deepcopy(temp.stars))

        if s[1] < 5:
            if v.state[s[0], s[1] + 1] == 0:
                new_board2 = copy.deepcopy(v.state)
                new_board2[s[0],s[1]+1] = 2
                new_board2[s[0], s[1]] = 0
                temp = Boards(new_board2, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    if num == 1:
                        visited.append(copy.deepcopy(temp.stars))

        if s[1] > 0:
            if v.state[s[0], s[1] - 1] == 0:
                new_board3 = copy.deepcopy(v.state)
                new_board3[s[0], s[1] - 1] = 2
                new_board3[s[0], s[1]] = 0
                temp = Boards(new_board3, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    if num == 1:
                        visited.append(copy.deepcopy(temp.stars))

        if s[0] > 0:
            if v.state[s[0] - 1, s[1]] == 0:
                new_board4 = copy.deepcopy(v.state)
                new_board4[s[0]-1, s[1]] = 2
                new_board4[s[0], s[1]] = 0
                temp = Boards(new_board4, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    if num == 1:
                        visited.append(copy.deepcopy(temp.stars))

        if len(v.stars) > len(goal_board.stars):
            if s[0] == 5 :
                new_board5 = copy.deepcopy(v.state)
                new_board5[s[0], s[1]] = 0
                temp = Boards(new_board5, v)
                if temp.stars not in visited:
                    optionsList.append(temp)
                    if num == 1:
                        visited.append(copy.deepcopy(temp.stars))

    return optionsList



starting_board = [[2,0,2,0,2,0],[0,0,0,2,1,2],[1,0,0,0,0,0],[0,0,1,0,1,0],[2,0,0,0,0,0],[0,1,0,0,0,0]]
goal_board = [[2,0,2,0,0,2],[0,0,0,2,1,0],[1,0,0,0,0,2],[0,0,1,0,1,0],[0,0,0,0,0,0],[0,1,0,0,0,0]]

#   search_method 1 is A*, 2 is Hill Climbing, 3 is Simulated Annealing , 4 is  k beam, 5 is genetic algorithm
search_method = 2
find_path(starting_board,goal_board,search_method,True)