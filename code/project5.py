# columns_game.py - the view of the Columns game 

import pygame 
import columns 
import random 


_FRAME_RATE = 3
_INITIAL_WIDTH = 300 
_INITIAL_HEIGHT = 650 
_BACKGROUND_COLOR = pygame.Color(0, 0, 0) 
_JEWELS = {
    'A': pygame.Color(255, 0 , 0), 
    'B': pygame.Color(255, 127, 0), 
    'C': pygame.Color(255, 255, 0), 
    'D': pygame.Color(0, 255, 0), 
    'E': pygame.Color(0, 0, 255), 
    'F': pygame.Color(75, 0, 130), 
    'G': pygame.Color(148, 0, 211)
} 


board = columns.create_new_board()


class ColumnGame: 
    def __init__(self): 
        self._running = True 
        self._state = columns.GameState(board) 


    def run(self) -> None: 
        pygame.init() 

        try: 
            clock = pygame.time.Clock() 

            self._create_display((_INITIAL_WIDTH, _INITIAL_HEIGHT))

            while self._running: 
                clock.tick(_FRAME_RATE) 

                self._update_world() 
                self._redraw() 

        finally: 
            pygame.quit()  

    
    def _create_display(self, size: tuple[int, int]) -> None:  
        pygame.display.set_mode(size, pygame.RESIZABLE) 


    def _update_world(self) -> None: 
        for event in pygame.event.get(): 
            self._handle_event(event)

        if not self._state._has_faller and not self._state._has_connection:  
            self._create_random_faller() 
        else: 
            self._state.pass_time() 

        self._state.determine_game_over() 


    def _create_random_faller(self) -> None: 
        board = self._state.get_board() 

        column = random.randint(1, 6) 
        jewels = random.choices(list(_JEWELS.keys()), k = 3) 

        while board[column-1][0] != '   ': 
            column = random.randint(1, 6) 

        self._state.create_faller([column] + jewels) 


    def _handle_event(self, event) -> None: 
        if event.type == pygame.QUIT: 
            self._stop_running()

        elif event.type == pygame.KEYDOWN: 
            self._handle_keys(event) 


    def _stop_running(self) -> None: 
        self._running = False 


    def _handle_keys(self, event) -> None: 
        if event.key == pygame.K_LEFT: 
            self._state.move_faller('<') 

        if event.key == pygame.K_RIGHT: 
            self._state.move_faller('>')

        if event.key == pygame.K_SPACE:  
            self._state.rotate_faller()


    def _redraw(self) -> None: 
        surface = pygame.display.get_surface() 

        surface.fill(_BACKGROUND_COLOR) 
        self._draw_board() 

        pygame.display.flip() 


    def _draw_board(self) -> None: 
        '''draw the board''' 
        board = self._state.get_board() 
        column, row = self._state.get_column(), self._state.get_row()
        surface = pygame.display.get_surface() 
        block_size = (surface.get_width() / column, surface.get_height() / row)  
        self._draw_grid() 

        for i in range(column): 
            for j in range(row): 
                if board[i][j][0] == '[' or board[i][j][0] == '|': 
                    jewel = self._state.get_board()[i][j][1] 
                    color = _JEWELS[jewel] 
                    rect = pygame.Rect(i * block_size[0], j * block_size[1], block_size[0], block_size[1])
                    pygame.draw.ellipse(surface, color, rect) 

                elif board[i][j][0] == '*': 
                    jewel = self._state.get_board()[i][j][1] 
                    color = _JEWELS[jewel] 
                    points = [(i * block_size[0], j * block_size[1]), (i * block_size[0], (j + 1) * block_size[1]), ((i + 1) * block_size[0], (j + 1) * block_size[1])] 
                    pygame.draw.polygon(surface, color, points)   

                elif board[i][j] != '   ':  
                    jewel = self._state.get_board()[i][j][1] 
                    color = _JEWELS[jewel] 
                    rect = pygame.Rect(i * block_size[0], j * block_size[1], block_size[0], block_size[1])
                    pygame.draw.rect(surface, color, rect, width=0)  
                

    def _draw_grid(self) -> None:  
        column, row = self._state.get_column(), self._state.get_row()
        surface = pygame.display.get_surface() 
        block_size = (surface.get_width() / column, surface.get_height() / row) 

        for i in range(column): 
            for j in range(row):  
                rect = pygame.Rect(i * block_size[0], j * block_size[1], block_size[0], block_size[1]) 
                pygame.draw.rect(surface, pygame.Color(255, 255, 255), rect, 1) 



if __name__ == '__main__': 
    ColumnGame().run() 