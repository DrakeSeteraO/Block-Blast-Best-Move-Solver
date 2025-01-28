from copy import deepcopy as dc
import os



class Progress:
    
    def __init__(self):
        self.progress = 0
    
    def add(self):
        self.progress += 1
    
    def set(self, num: int):
        self.progress = num
    
    def get(self):
        return self.progress



def solve(board: list, pieces: list) -> list:
    prog = Progress()
    progress_bar(prog)
    
    highest_score = -1
    best_coords = -1
    best_pieces = list()
    
    Bpieces, Bcoords, Bscore = piece1(board, pieces[0],pieces[1:], prog)
    if Bcoords != -1 and Bscore > highest_score:
            highest_score = Bscore
            best_coords = Bcoords
            best_pieces = Bpieces
            
    prog.set(127)
    progress_bar(prog)
    
    Bpieces, Bcoords, Bscore = piece1(board, pieces[1],[pieces[0],pieces[2]], prog)
    if Bcoords != -1 and Bscore > highest_score:
            highest_score = Bscore
            best_coords = Bcoords
            best_pieces = Bpieces
            
    prog.set(259)
    progress_bar(prog)
    
    Bpieces, Bcoords, Bscore = piece1(board, pieces[2],pieces[:2], prog)
    if Bcoords != -1 and Bscore > highest_score:
            highest_score = Bscore
            best_coords = Bcoords
            best_pieces = Bpieces
            
    prog.set(388)
    progress_bar(prog)
    
    #pieces, coord
    return best_pieces, best_coords



def piece1(board: list, placing_piece: list, other_pieces: list, prog: Progress) -> list:
    locations = place_locations(board, placing_piece)
    
    highest_score = -1
    best_coords = -1
    pieces = list()
    
    for l in locations:
        new_board = dc(board)
        new_board = insert_piece(new_board, placing_piece, l)
        score = update_lines(new_board)
        
        Bpieces, Bcoords, Bscore = piece2(new_board, other_pieces[0], other_pieces[1], prog)
        if Bcoords != -1 and score + Bscore > highest_score:
            highest_score = score + Bscore
            best_coords = [l, Bcoords[0], Bcoords[1]]
            pieces = [placing_piece, Bpieces[0], Bpieces[1]]
        
        
        Bpieces, Bcoords, Bscore = piece2(new_board, other_pieces[1], other_pieces[0], prog)
        if Bcoords != -1 and score + Bscore > highest_score:
            highest_score = score + Bscore
            best_coords = [l, Bcoords[0], Bcoords[1]]
            pieces = [placing_piece, Bpieces[0], Bpieces[1]]
    
    progress_bar(prog)
    #pieces, coord, score
    return pieces, best_coords, highest_score



def piece2(board: list, placing_piece: list, other_piece: list, prog: Progress) -> list:
    locations = place_locations(board, placing_piece)
    
    highest_score = -1
    best_coords = -1
    pieces = [placing_piece, other_piece]
    
    for l in locations:
        
        new_board = dc(board)
        new_board = insert_piece(new_board, placing_piece, l)
        score = update_lines(new_board)
        
        Bcoord, Bscore = piece3(new_board, other_piece)
        
        
        if Bcoord != -1 and score + Bscore > highest_score:
            highest_score = score + Bscore
            best_coords = [l, Bcoord]
    
    progress_bar(prog)
    #pieces, coord, score
    return pieces, best_coords, highest_score
        



def piece3(board: list, placing_piece: list) -> list:
    locations = place_locations(board, placing_piece)
    
    highest_score = -1
    best_coord = -1
    
    for l in locations:
        new_board = dc(board)
        new_board = insert_piece(new_board, placing_piece, l)
        score = update_lines(new_board)
        
        if score > highest_score:
            highest_score = score
            best_coord = l
    
    #coord, score
    return best_coord, highest_score
        

def place_locations(board: list, piece: list) -> list:
    locations = list()
    section = [[0 for i in range(len(piece[0]))] for j in range(len(piece))]
    
    xp = 0
    yp = 0
    while yp <= len(board) - len(piece) and xp <= len(board[yp]) - len(piece[0]):
        
        section = copy_section(board, section, xp, yp)
        valid_loc = check_location(section, piece)
        if valid_loc:
            locations.append([xp,yp])
        
        xp += 1
        if xp >= len(board[yp]) - len(piece[0]) + 1:
            xp = 0
            yp += 1    
        
    return locations
        
            
  
def copy_section(board: list, section: list, xp: int, yp: int) -> list:
    for y in range(len(section)):
        for x in range(len(section[y])):
            section[y][x] = board[yp+y][xp+x]
    return section



def check_location(board_spot: list, piece: list) -> bool:
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x] == 1 and board_spot[y][x] == 1:
                return False
    return True



def insert_piece(board: list, piece: list, coord: list) -> list:
    for y in range(len(piece)):
        for x in range(len(piece[y])):
            if piece[y][x] == 1:
                board[y+coord[1]][x+coord[0]] = 1
    return board



def update_lines(board: list) -> int:
    rows_amount = [0] * len(board)
    cols_amount = [0] * len(board[0])
    
    
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] >= 1:
                rows_amount[y] += 1
                cols_amount[x] += 1
            if board[y][x] == 2:
                board[y][x] = 1

    rows_scored = list()
    cols_scored = list()
    
    for r in range(len(rows_amount)):
        if rows_amount[r] == len(board[0]):
            rows_scored.append(r)
    
    for c in range(len(cols_amount)):
        if cols_amount[c] == len(board):
            cols_scored.append(c)
    
    
    for r in rows_scored:
        for x in range(len(board[r])):
            board[r][x] = 0
    
    for c in cols_scored:
        for y in range(len(board)):
            board[y][c] = 0
    
    score = len(rows_scored) + len(cols_scored)
    return score


def progress_bar(prog: Progress) -> None:
    
    os.system('cls')
    percent = (prog.get() * 100) // 388
    if prog.get() >= 388:
        percent = 100
    title = f"Progress: {percent} %"
    
    print(f'{title:^26}')
    output = '['
    for i in range(24):
        if i * 100 // 24 <= percent :
            output += '#'
        else:
            output += '-'
    output += ']'

    print(output)
    prog.add()
    
