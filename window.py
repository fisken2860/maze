from tkinter import Tk, BOTH, Canvas,Button

import random
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        
                # Add a button in the bottom-left corner
        self.__button = Button(self.__root, text="Click Me", command=self.on_button_click)
        self.__button.place(x=10, rely=1.0, anchor="sw")  # Position at bottom-left
       
        self.btn_clear = Button(self.__root, text="Clear Canvas", command=self.clear_canvas)
        self.btn_clear.place(x=400, rely=1.0, anchor="sw")
      
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    def clear_canvas(self):
        self.__canvas.delete("all")
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False
        
    def on_button_click(self):
        from blocks import Maze
        print("Button clicked!")
        num_cols = 12
        num_rows = 10
        margin = 50
        screen_x = 800
        screen_y = 600
        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows
        self.__canvas.delete("all")
        randomness = random.choice(range(1, 100))
        maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, self,randomness)
        maze.solve()
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def draw (self, canvas: Canvas, fill = 'red'):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill = fill, width = 2)
        

        