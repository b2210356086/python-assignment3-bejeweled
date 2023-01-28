import sys

def print_board():
    remove_toprow()
    for row in board:
        for column in row:
            print(column,end=" ")
        print()
    print()

def is_valid(row,column):
    try:
        cell = board[row][column]
        if cell != " ":
            return True
        else:
            return False
    except:
        return False

def cell_to_explode(row,column):
    if board[row][column] == "X" and [row,column] not in explode_list:
        explode_list.append([row,column])
        for x in range(len(board)):
            if [x,column] not in explode_list and x != row:
                if board[x][column] != "X":
                    explode_list.append([x,column])
                else:
                    cell_to_explode(x,column)
        for y in range(len(board[-1])):
            if [row,y] not in explode_list and y != column:
                if board[row][y] != "X":
                    explode_list.append([row,y])
                else:
                    cell_to_explode(row,y)
    else:
        try:
            if board[row][column] == board[row][column+1]:
                if [row,column] not in explode_list and row >= 0 and column >= 0:
                    explode_list.append([row,column])
                if [row,column+1] not in explode_list and row >= 0 and column+1 >= 0:
                    explode_list.append([row,column+1])
        except:
            pass
        try:
            if board[row][column] == board[row][column-1]:
                if [row, column] not in explode_list and row >= 0 and column >= 0:
                    explode_list.append([row,column])
                if [row,column-1] not in explode_list and row >= 0 and column-1 >= 0:
                    explode_list.append([row, column-1])
        except:
            pass
        try:
            if board[row][column] == board[row+1][column]:
                if [row, column] not in explode_list and row >= 0 and column >= 0:
                    explode_list.append([row, column])
                if [row+1,column] not in explode_list and row+1 >= 0 and column >= 0:
                    explode_list.append([row+1, column])
        except:
            pass
        try:
            if board[row][column] == board[row-1][column]:
                if [row, column] not in explode_list and row >= 0 and column >= 0:
                    explode_list.append([row,column])
                if [row-1,column] not in explode_list and row-1 >= 0 and column >= 0:
                    explode_list.append([row-1, column])
        except:
            pass

def explode():
    for coordinate in explode_list:
        board[coordinate[0]][coordinate[1]] = " "
    check_blanks()

def new_score():
    global score , old_score
    for coordinate in explode_list:
        if board[coordinate[0]][coordinate[1]] == "F":
            score += 1
        elif board[coordinate[0]][coordinate[1]] == "D":
            score += 2
        elif board[coordinate[0]][coordinate[1]] == "O":
            score += 3
        elif board[coordinate[0]][coordinate[1]] == "P":
            score += 4
        elif board[coordinate[0]][coordinate[1]] == "R":
            score += 5
        elif board[coordinate[0]][coordinate[1]] == "Y":
            score += 6
        elif board[coordinate[0]][coordinate[1]] == "W":
            score += 7
        elif board[coordinate[0]][coordinate[1]] == "G":
            score += 8
        elif board[coordinate[0]][coordinate[1]] == "B":
            score += 9
        else:
            continue
    old_score = score
    return score

def check_blanks():
    for i in range(len(board[-1])):
        blank_count = 0
        for j in range(len(board)):
            if board[j][i] == " ":
                blank_count += 1
                if blank_count != len(board):
                    for y in range(len(board)-1,-1,-1):
                        for x in range(len(board[-1])):
                            if board[y][x] == " ":
                                drop_tiles(x,y)
    for i in range(len(board[-1]) - 1):
        blank_count = 0
        for j in range(len(board)):
            if board[j][i] == " ":
                blank_count += 1
                if blank_count == len(board):
                    for k in range(len(board)):
                        while board[k][i+1] != " ":
                            fill_column()
                            i -= 1

def drop_tiles(x,y):
    for row in range(y,0,-1):
        board[row][x] = board[row-1][x]
    board[0][x] = " "

def fill_column():
    for i in range(len(board[-1]) - 1):
        blank_count = 0
        for j in range(len(board)):
            if board[j][i] == " ":
                blank_count += 1
                if blank_count == len(board):
                    for k in range(len(board)):
                        board[k][i] = board[k][i+1]
                        board[k][i+1] = " "

def remove_toprow():
    rows_to_delete = []
    for row in range(len(board)):
        if all(elem == " " for elem in board[row]):
            rows_to_delete.append(row)
    for row in reversed(rows_to_delete):
        del board[row]

def game_over():
    global temp_check , explode_list
    item_list , explode_list = [] , []
    temp_check = False
    for row in range(len(board)):
        for column in range(len(board[-1])):
            if board[row][column] != " ":
                item_list.append(board[row][column])
    if "X" in item_list:
        temp_check = True
    if temp_check != True:
        for row in range(len(board)):
            for column in range(len(board[-1])):
                if board[row][column] != " ":
                    cell_to_explode(row,column)
                    if len(explode_list) > 0:
                        temp_check = True
                        break

def new_game():
    global explode_list , score , temp_check
    explode_list = []
    score = 0
    temp_check = True
    print_board()
    print("Your score is: "+str(score)+"\n")
    game_over()
    while temp_check:
        rc_input = input("Please enter a row and column number: ")
        print()
        row, column = int(rc_input.split()[0]), int(rc_input.split()[1])
        explode_list = []
        if is_valid(row, column) == False:
            print("Please enter a valid size!\n")
        if is_valid(row, column):
            cell_to_explode(row, column)
            if board[row][column] != "X":
                for coordinate in explode_list:
                    cell_to_explode(coordinate[0], coordinate[1])
            new_score()
            explode()
            break
    game_over()
    while temp_check:
        print_board()
        print("Your score is: " + str(old_score)+"\n")
        game_over()
        while temp_check:
            rc_input = input("Please enter a row and column number: ")
            print()
            row, column = int(rc_input.split()[0]), int(rc_input.split()[1])
            if is_valid(row,column) == False:
                print("Please enter a valid size!\n")
            explode_list = []
            if is_valid(row, column):
                cell_to_explode(row, column)
                if board[row][column] != "X":
                    for coordinate in explode_list:
                        cell_to_explode(coordinate[0], coordinate[1])
                new_score()
                explode()
                game_over()
                break
        game_over()
    if temp_check == False:
        print_board()
        print("Your score is: " + str(old_score) + "\n")
        print("Game over!")

templist = []
with open(sys.argv[1],"r") as inputtxt:
    board = inputtxt.read().splitlines()
for row in board:
    templist.append(row.split())
board = templist

new_game()