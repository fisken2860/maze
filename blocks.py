import random
import time
from window import Window, Line, Point
class Cell():
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = None
        self.__x2 = None
        self.__y1 = None
        self.__y2 = None
        self.win = win
        
    def draw(self, x1, y1, x2, y2):
        if self.win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
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
        half_length = abs(self.__x2 - self.__x1) // 2
        x_center = half_length + self.__x1
        y_center = half_length + self.__y1

        half_length2 = abs(to_cell.__x2 - to_cell.__x1) // 2
        x_center2 = half_length2 + to_cell.__x1
        y_center2 = half_length2 + to_cell.__y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

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
    ):
        self.cells = [] 
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
            
    def __repr__(self):
        return f"Maze({self.x1}, {self.y1}, {self.num_rows}, {self.num_cols}, {self.cell_size_x}, {self.cell_size_y}, {self.win})"

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.02)
    
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
        if self.win is None:
            return 
        self.cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self.cells[self.num_cols - 1][self.num_rows - 1].has_right_wall = False   
        self._draw_cell(self.num_cols - 1, self.num_rows - 1) 