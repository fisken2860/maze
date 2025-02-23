import random
import time
from window import  Line, Point
class Cell():
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.visited = False
        self.win = win
        
    def draw(self, x1, y1, x2, y2):
        if self.win is None:
            return
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        
        l = Line(Point(x1, y1), Point(x1, y2 )) 
        t = Line(Point(x1, y1), Point(x2, y1))
        r = Line(Point(x2, y1), Point(x2,y2))
        b = Line(Point(x1, y2), Point(x2 ,y2)) 
        if self.has_left_wall:
            self.win.draw_line(l)  
        else:
            self.win.draw_line(l, fill_color="white")  
        if self.has_top_wall:
            self.win.draw_line(t)
        else:   
            self.win.draw_line(t, fill_color="white") 
        if self.has_right_wall:
            self.win.draw_line(r)
        else:
            self.win.draw_line(r, fill_color="white") 
        if self.has_bottom_wall:
            self.win.draw_line(b) 
        else:
            self.win.draw_line(b, fill_color="white") 
            

            
    def draw_move(self, to_cell, undo=False):
        if self.x1 is None or self.x2 is None or self.y1 is None or self.y2 is None:
            print(f"self.x1 : {self.x1} self.x2 : {self.x2} self.y1 : {self.__y1} self.__y2 : {self.__y2} ")
            return
        half_lengthx = abs(self.x2 - self.x1) // 2
        half_lengthy = abs(self.y2 - self.y1) // 2
        x_center = half_lengthx + self.x1
        y_center = half_lengthy + self.y1

        half_lengthx2 = abs(to_cell.x2 - to_cell.x1) // 2
        half_lengthy2 = abs(to_cell.y2 - to_cell.y1) // 2
        x_center2 = half_lengthx2 + to_cell.x1
        y_center2 = half_lengthy2 + to_cell.y1

        fill_color = "red"
        if undo:
            fill_color = "yellow"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        self.win.draw_line(line, fill_color)

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed = None,
        
    ):
        self.cells: list[list[Cell]] = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
        
            

    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
    def __repr__(self):
        return f"Maze({self.x1}, {self.y1}, {self.num_rows}, {self.num_cols}, {self.cell_size_x}, {self.cell_size_y}, {self.win})"

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        #time.sleep(0.00)
    
    def _draw_cell(self, i, j):
        if self.win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    def _break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False   
        self._draw_cell(self.num_cols - 1, self.num_rows - 1) 
        print(f'hat___break_entrance_and_exit : 0 , 0 {self.cells[0][0].has_top_wall}')
        print(f'hat___break_entrance_and_exit : {self.num_cols - 1} , {self.num_rows - 1} {self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall}')
    
    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False
   
    def _break_walls_r(self, col, row):
        self.cells[col][row].visited = True
        while True:
            unvisited_neighbors = []

            # determine unvisited neighbors
            if col > 0 and not self.cells[col - 1][row].visited:  # left
                unvisited_neighbors.append((col - 1, row))
            if col < self.num_cols - 1 and not self.cells[col + 1][row].visited:  # right
                unvisited_neighbors.append((col + 1, row))
            if row > 0 and not self.cells[col][row - 1].visited:  # up
                unvisited_neighbors.append((col, row - 1))
            if row < self.num_rows - 1 and not self.cells[col][row + 1].visited:  # down
                unvisited_neighbors.append((col, row + 1))

            # if no unvisited neighbors, draw the cell and return
            if not unvisited_neighbors:
                self._draw_cell(col, row)
                return

            # choose a random unvisited neighbor
            next_col, next_row = random.choice(unvisited_neighbors)

            # remove walls between current cell and chosen cell
            if next_col == col + 1:  # right
                self.cells[col][row].has_right_wall = False
                self.cells[next_col][next_row].has_left_wall = False
            elif next_col == col - 1:  # left
                self.cells[col][row].has_left_wall = False
                self.cells[next_col][next_row].has_right_wall = False
            elif next_row == row + 1:  # down
                self.cells[col][row].has_bottom_wall = False
                self.cells[next_col][next_row].has_top_wall = False
            elif next_row == row - 1:  # up
                self.cells[col][row].has_top_wall = False
                self.cells[next_col][next_row].has_bottom_wall = False

            # recursively visit the chosen cell
            self._break_walls_r(next_col, next_row)
    
    
    
    def _break_walls_r2(self, col, row):
        self.cells[col][row].visited = True
        unvisited_neighbors = []

        # Determine unvisited neighbors
        if col > 0 and not self.cells[col - 1][row].visited:  # Left
            unvisited_neighbors.append((col - 1, row))
        if col < self.num_cols - 1 and not self.cells[col + 1][row].visited:  # Right
            unvisited_neighbors.append((col + 1, row))
        if row > 0 and not self.cells[col][row - 1].visited:  # Up
            unvisited_neighbors.append((col, row - 1))
        if row < self.num_rows - 1 and not self.cells[col][row + 1].visited:  # Down
            unvisited_neighbors.append((col, row + 1))

        # Shuffle to ensure random traversal order
        random.shuffle(unvisited_neighbors)

        for next_col, next_row in unvisited_neighbors:
            if not self.cells[next_col][next_row].visited:
                # Remove walls between current and chosen cell
                if next_col == col + 1:  # Right
                    self.cells[col][row].has_right_wall = False
                    self.cells[next_col][next_row].has_left_wall = False
                elif next_col == col - 1:  # Left
                    self.cells[col][row].has_left_wall = False
                    self.cells[next_col][next_row].has_right_wall = False
                elif next_row == row + 1:  # Down
                    self.cells[col][row].has_bottom_wall = False
                    self.cells[next_col][next_row].has_top_wall = False
                elif next_row == row - 1:  # Up
                    self.cells[col][row].has_top_wall = False
                    self.cells[next_col][next_row].has_bottom_wall = False

                # Recursively visit the chosen cell
                self._break_walls_r(next_col, next_row)
                
    def solve (self):
        return self.solve_r( 0, 0)
    
            
    
    
    def solve_r(self,col,row):
        self._animate()
        self.cells[col][row].visited = True
        # if we are at the end cell, we are done!
        if col == self.num_cols - 1 and row == self.num_rows - 1:    
            return True
        neighbors = []
        if col > 0 and not self.cells[col - 1][row].visited and not self.cells[col ][row].has_left_wall:  # left
            self.cells[col][row].draw_move(self.cells[col - 1][row])
            if self.solve_r(col - 1,row):
                return True
            else:
                self.cells[col][row].draw_move(self.cells[col - 1][row],True)
            neighbors.append((col - 1, row))
            
        if col < self.num_cols - 1 and not self.cells[col + 1][row].visited and not self.cells[col][row].has_right_wall:  # right
            self.cells[col][row].draw_move(self.cells[col + 1][row])
            if self.solve_r(col + 1, row):
                return True
            else:
                self.cells[col][row].draw_move(self.cells[col + 1][row], True)
            neighbors.append((col + 1, row))
            
        if row > 0 and not self.cells[col][row - 1].visited and not self.cells[col][row].has_top_wall:  # up
            self.cells[col][row].draw_move(self.cells[col][row - 1])
            if self.solve_r(col,row - 1 ):
                return True
            else:
                self.cells[col][row].draw_move(self.cells[col][row - 1], True)
            neighbors.append((col, row - 1))
            
        if row < self.num_rows - 1 and not self.cells[col][row + 1].visited and not self.cells[col][row].has_bottom_wall:  # down
            self.cells[col][row].draw_move(self.cells[col][row + 1])
            if self.solve_r(col, row + 1):
                return True
            else:
                self.cells[col][row].draw_move(self.cells[col][row + 1], True)
            neighbors.append((col, row + 1))
            
        return False
        
        '''for next_col, next_row in neighbors:
            if self.solve_r(next_col, next_row):
                return True
            else:
                self.cells[col][row].draw_move(self.cells[col][row],undo=True)
                return True'''