from BlockBlastAI import solve, update_lines
import os




def main():
    end = False
    board = get_cur_board_state()
    
    while not end:
        valid_input = False
        
        piece1 = get_piece(1)
        piece2 = get_piece(2)
        piece3 = get_piece(3)
        pieces, coords = solve(board, [piece1, piece2, piece3])
        print_steps(board, pieces, coords)
        
        while not valid_input:
                user_input = input('Would you like to continue? (y/n):')
                
                try:
                    if user_input.lower() == 'n':
                        valid_input = True
                        end = True
                        
                    elif user_input.lower() == 'y':
                        valid_input = True
                    else:
                        print('Invalid input please try again')
                
                except:
                    print('Invalid input please try again')
        



def get_cur_board_state() -> list:
    board = [[0 for i in range(8)] for j in range(8)]
    
    
    user_input = ''
    while user_input != 'n':
        valid_input = False
        os.system('cls')
        title = 'Current Board State'
        print(f'{title:^26}')
        print_screen(board)
        
        while not valid_input:
            user_input = input('Next block (letter)(number)\nMove to next step (n):')
            
            try:
                if user_input.lower() == 'n':
                    valid_input = True
                    
                elif 0 <= int(user_input[1]) <= 7 and 97 <= ord(user_input[0].lower()) <= 105:
                    valid_input = True
                    board[int(user_input[1])][ord(user_input[0].lower()) - 97] = 1
                else:
                    print('Invalid input please try again')
            
            except:
                print('Invalid input please try again')
        
    return board



def print_screen(board: list) -> None:
    output = '  A  B  C  D  E  F  G  H |\n'
    
    for y in range(len(board)):
        output += str(y) 
        for x in board[y]:
            if x == 1:
                output += '[ ]'
            elif x == 2:
                output += '[X]'
            else:
                output += '   '
        output += '|\n'
    output += '-------------------------'
    print(output)
    


def get_piece(num: int) -> list:
    board = [[0 for i in range(8)] for j in range(8)]
    parts = list()
    min_x = 8
    max_x = -1
    min_y = 8
    max_y = -1
    
    
    user_input = ''
    while user_input != 'n':
        valid_input = False
        os.system('cls')
        title = f'Create Piece {num}'
        print(f'{title:^26}')
        print_screen(board)
        
        while not valid_input:
            user_input = input('Next piece block (letter)(number)\nMove to next block (n):')
            
            try:
                if user_input.lower() == 'n':
                    valid_input = True
                    
                elif 0 <= int(user_input[1]) <= 7 and 97 <= ord(user_input[0].lower()) <= 105:
                    valid_input = True
                    board[int(user_input[1])][ord(user_input[0].lower()) - 97] = 1
                    parts.append(user_input)
                    
                    
                    if ord(user_input[0].lower()) - 97 < min_x:
                        min_x = ord(user_input[0].lower()) - 97
                    if ord(user_input[0].lower()) - 97 > max_x:
                        max_x = ord(user_input[0].lower()) - 97
                    if int(user_input[1]) < min_y:
                        min_y = int(user_input[1])
                    if int(user_input[1]) > max_y:
                        max_y = int(user_input[1])
                        
                        
                else:
                    print('Invalid input please try again')
            
            except:
                print('Invalid input please try again')


    for i in range(len(parts)):
        letter_loc = (ord(parts[i][0].lower()) - 97) - min_x
        num_loc = int(parts[i][1]) - min_y
        parts[i] = str(letter_loc) + str(num_loc)
    
    piece = [[0 for i in range(max_x-min_x+1)] for j in range(max_y-min_y+1)]
    for p in parts:
        piece[int(p[1])][int(p[0])] = 1

    return piece



def print_steps(board: list, pieces: list, coords: list) -> None:
    #os.system('cls')
    
    for i in range(3):
        board = insert_new_piece(board, pieces[i], coords[i])
        title = f'Step {i+1}'
        print(f'{title:^26}')
        print_screen(board)
        
        update_lines(board)
    
    

def insert_new_piece(board: list, piece: list, coord: list) -> list:
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x] == 1:
                board[y+coord[1]][x+coord[0]] = 2
    return board
        
    
                    
if __name__ == '__main__':
    main()