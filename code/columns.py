# columns.py - model of the Columns game 
import sys


class GameState: 
    def __init__(self, board):   
        self._board = board
        self._column = len(board) 
        self._row = len(board[0]) 
        self._has_connection = False 
        self._has_faller = False 
        self._hidden_faller = []


    def get_board(self):
        '''return the board''' 
        return self._board


    def get_column(self): 
        return self._column 


    def get_row(self): 
        return self._row


    def quit_game(self):
        '''quit the game''' 
        sys.exit() 


    def pass_time(self): 
        '''pass the time'''
        if self._has_connection: 
            self.del_connection() 
        elif self._has_faller: 
            self.drop_faller() 
        
        self.check_connection() 


    def create_faller(self, info: list): 
        '''create a new faller'''
        col, faller = int(info[0])-1, info[1:]
        if self._board[col][0] == '   ': 
            self._board[col][0] = '[' + faller[-1] + ']' 
        self._has_faller = True 
        self._hidden_faller = faller[:-1] 


    def drop_faller(self): 
        '''drop faller down one block'''
        for i in range(self._column-1, -1, -1): 
            for j in range(self._row-1, -1, -1): 
                if self._board[i][j][0] == '[': 
                    if j + 1 < self._row and self._board[i][j+1] == '   ': 
                        self._board[i][j+1], self._board[i][j] = self._board[i][j], '   ' 

                        if self._hidden_faller and self._board[i][0] == '   ': 
                            self._board[i][0] = '[' + self._hidden_faller[-1] + ']' 
                            self._hidden_faller.pop()
                    
                    self.land_faller()

                elif self._board[i][j][0] == '|': 
                    if j + 1 >= self._row: 
                        self._board[i][j] = ' ' + self._board[i][j][1] + ' ' 
                        self._has_faller = False 
        
                    elif self._board[i][j+1] != '   ' and self._board[i][j+1][0] != '[':  
                        self._board[i][j] = ' ' + self._board[i][j][1] + ' ' 
                        self._has_faller = False 

                    else: 
                        self._board[i][j] = '[' + self._board[i][j][1] + ']' 


    def land_faller(self) -> bool:  
        '''if faller cannot fall anymore, make it land'''
        for i in range(self._column-1, -1, -1): 
            for j in range(self._row-1, -1, -1): 
                if self._board[i][j][0] == '[': 
                    if j + 1 >= self._row: 
                        self._board[i][j] = '|' + self._board[i][j][1] + '|'
                    
                    elif self._board[i][j+1] != '   ' and self._board[i][j+1][0] != '[':  
                        self._board[i][j] = '|' + self._board[i][j][1] + '|' 


    def rotate_faller(self): 
        '''rotate the faller'''
        for i in range(self._column-1, -1, -1): 
            for j in range(self._row-1, -1, -1): 
                if self._board[i][j][0] == '[' or self._board[i][j][0] == '|': 
                    status1 = self._board[i][j][0]
                    status2 = self._board[i][j][2] 
                    if len(self._hidden_faller) == 1: 
                        self._board[i][j], self._board[i][j-1], self._hidden_faller[-1] = \
                            self._board[i][j-1], status1 + self._hidden_faller[-1] + status2, self._board[i][j][1] 
                    elif len(self._hidden_faller) == 2: 
                        self._board[i][j], self._hidden_faller[-1], self._hidden_faller[-2] = \
                            status1 + self._hidden_faller[-1] + status2, self._hidden_faller[-2], self._board[i][j][1] 
                    else: 
                        self._board[i][j], self._board[i][j-1], self._board[i][j-2] = \
                            self._board[i][j-1], self._board[i][j-2], self._board[i][j]
                    break 
        
        


    def move_faller(self, direction): 
        '''move the faller to the right or left'''
        if direction == '<': 
            for i in range(self._column): 
                for j in range(self._row-1, -1, -1): 
                    if self._board[i][j][0] == '[' or self._board[i][j][0] == '|':
                        if i - 1 >= 0 and self._board[i-1][j] == '   ': 
                            self._board[i-1][j], self._board[i][j] = self._board[i][j], '   '
                        else: 
                            break 

        elif direction == '>':
            for i in range(self._column-1, -1, -1): 
                for j in range(self._row-1, -1, -1): 
                    if self._board[i][j][0] == '[' or self._board[i][j][0] == '|':
                        if i + 1 < self._column and self._board[i+1][j] == '   ': 
                            self._board[i+1][j], self._board[i][j] = self._board[i][j], '   '
                        else: 
                            break
        self.land_faller()

    
    def determine_game_over(self): 
        '''determine if game is over'''
        faller = False 
        for i in range(self._column): 
            for j in range(self._row): 
                if self._board[i][j][0] == '[' or self._board[i][j][0] == '|' or self._board[i][j][0] == '*':
                    faller = True
        if not faller and self._hidden_faller: 
            print('GAME OVER') 
            self.quit_game() 


    def check_connection(self) -> list[list]: 
        '''check if there are connection between jewels'''
        for i in range(self._column): 
            for j in range(self._row): 
                if self._board[i][j] != '   ' and self._not_faller(i, j):  
                    self._horizontal_connection(i, j)  
                    self._vertical_connection(i, j)  
                    self._diagonal_connection1(i, j) 
                    self._diagonal_connection2(i, j) 


    def del_connection(self): 
        '''delete the connected jewels'''
        for i in range(self._column): 
            for j in range(self._row): 
                if self._board[i][j][0] == '*': 
                    self._board[i][j] = '   ' 
        _fill(self._board) 
        self._has_connection = False 

    
    def _horizontal_connection(self, col, row): 
        i = 1 
        while i < self._column - col: 
            if self._board[col][row][1] == self._board[col+i][row][1] and self._not_faller(col+i, row): 
                i += 1 
            else: 
                break 
        if i >= 3: 
            for a in range(i): 
                self._board[col+a][row] = '*' + self._board[col+a][row][1] + '*'
            self._has_connection = True 

    
    def _vertical_connection(self, col, row): 
        i = 1 
        while i < self._row - row: 
            if self._board[col][row][1] == self._board[col][row+i][1] and self._not_faller(col, row+i): 
                i += 1
            else: 
                break 
        if i >= 3: 
            for a in range(i): 
                self._board[col][row+a] = '*' + self._board[col][row+a][1] + '*' 
            self._has_connection = True 


    def _diagonal_connection1(self, col, row): 
        i = 1 
        while i < self._column - col and i < self._row - row:
            if self._board[col][row][1] == self._board[col+i][row+i][1] and self._not_faller(col+i, row+i): 
                i += 1
            else: 
                break 
        if i >= 3: 
            for a in range(i): 
                self._board[col+a][row+a] = '*' + self._board[col+a][row+a][1] + '*' 
            self._has_connection = True 


    def _diagonal_connection2(self, col, row): 
        i = 1 
        while i < self._column - col and row - i >= 0: 
            if self._board[col][row][1] == self._board[col+i][row-i][1] and self._not_faller(col+i, row-i): 
                i += 1 
            else: 
                break 
        if i >= 3: 
            for a in range(i): 
                self._board[col+a][row-a] = '*' + self._board[col+a][row-a][1] + '*' 
            self._has_connection = True 


    def _not_faller(self, i, j): 
        if self._board[i][j][0] != '[' and self._board[i][j][0] != '|': 
            return True


def create_new_board(row = 13, column = 6, field = ['EMPTY']): 
    '''create the new board after reading user input''' 
    if field[0] == 'EMPTY': 
        board = [] 
        curr_column = [] 
        for i in range(column): 
            for j in range(row): 
                curr_column.append('   ') 
            board.append(curr_column) 
            curr_column = [] 
        return board 

    elif field[0] == 'CONTENTS': 
        board = [] 
        curr_column = [] 
        content = field[1:] 
        for i in range(column): 
            for j in range(row): 
                if content[j][i] == ' ': 
                    curr_column.append('   ') 
                else: 
                    curr_column.append(' ' + content[j][i] + ' ')  
            board.append(curr_column) 
            curr_column = [] 
        return _fill(board)


def _fill(board: list[list]) -> list[list]: 
    for i in range(len(board)):  
        for j in range(len(board[i])-1, -1, -1): 
            if board[i][j] == '   ': 
                for a in range(j-1, -1, -1): 
                    if board[i][a] != '   ': 
                        board[i][j], board[i][a] = board[i][a], '   ' 
                        break 
    return board 