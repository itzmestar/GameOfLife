from time import sleep
import tkinter
class Life:
    def __init__(self, seed, rule, edge):
        self.grid = seed
        self.grid_row = len(seed)
        self.grid_col = len(seed[0])
        self.edge = edge
        self.born_rule = []
        self.survive_rule = []
        self._find_rules(rule)


    def _find_rules(self, rule):
        '''
        converts the string to rule list
        :param rule: rule string
        :return: nothing
        '''

        #split rule into two strings
        (a, b) = rule.split('/')
        #store all digits in survive rule
        for i in range(len(a)):
            self.survive_rule.append(int(a[i]))

        # store all digits in born rule
        for i in range(len(b)):
            self.born_rule.append(int(b[i]))

    def __str__(self):
        string = ''
        #print all the rows
        for i in range(self.grid_row):
            #print all the columns
            for j in range(self.grid_col):
                string += str(self.grid[i][j])
            if i != self.grid_row - 1:
                string += '\n'
        return string

    def tick(self):
        '''
        Perform a tick

        '''
        next_gen = self._grid_copy()

        # check & change state of each cell
        for i in range(self.grid_row):
            for j in range(self.grid_col):
                num = self._num_neighbours(i, j)

                if self.grid[i][j] == 1: #alive case
                    if num not in self.survive_rule:
                        next_gen[i][j] = 0
                else: #dead case
                    if num in self.born_rule:
                        next_gen[i][j] = 1

        self.grid = next_gen

    def _num_neighbours(self, x, y):
        '''
        calculates the number of alive neighbors for a cell
        :param x: row
        :param y: col
        :return: number of alive neighbors
        '''
        #number of neighbors
        num = 0
        # check for x-1, x & x+1 rows
        for dx in [-1, 0, 1]:
            nx = x + dx
            xedge = False

            if nx < 0 or nx >= self.grid_row:
                if self.edge == 3:
                    nx = nx % self.grid_row
                    xedge = False
                else:
                    xedge = True

            # check for y-1, y & y+1 columns
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                ny = y + dy
                yedge = False

                if ny < 0 or ny >= self.grid_col:
                    if self.edge == 3:
                        ny = ny % self.grid_col
                        yedge = False
                    else:
                        yedge = True

                if xedge or yedge:
                    if self.edge == 2:
                        num += 1
                else:
                    if self.grid[nx][ny] == 1:
                        num += 1
        return num

    def _grid_copy(self):
        '''
        create a new copy of grid
        :return: temp list
        '''

        temp = []
        #copy all the rows
        for i in range(self.grid_row):
            temp.append([])
            #copy all the columns
            for j in range(self.grid_col):
                temp[i].append(self.grid[i][j])
        return temp

    def run(self):
        '''
        run infinite loop to update the life generation
        '''
        while True:
            sleep(1)
            self.tick()
            print(self)
            print()


class LifeVisualizer():
    def __init__(self):
        #self.tk = tk
        self.master = tkinter.Tk()
        tkinter.Label(self.master, text="Row").grid(row=0)
        tkinter.Label(self.master, text="Column").grid(row=1)

        self.entry1 = tkinter.Entry(self.master)
        self.entry2 = tkinter.Entry(self.master)

        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)

        self.grid = []

        construct_button = tkinter.Button(self.master, text='Create', command=self.create).grid(row=3, column=1, sticky=tkinter.W, pady=4)

        self.master.mainloop()

    def create(self):
        '''
        read the number of rows & columns.
        then create on a canvas for seed, rule & edge input
        '''
        self.flag = True
        row = self.entry1.get()
        col = self.entry2.get()

        if row == "" or col == "":
            return
        self.master.destroy()
        self.master = tkinter.Tk()

        self.row = int(row)
        self.col = int(col)
        self.width = self.col * 30 + 60
        self.height = self.row * 30 + 100
        for i in range(self.row):
            self.grid.append([])
            for j in range(self.col):
                self.grid[i].append(0)
        self.draw()
        self.master.mainloop()

    def sel(self):
        '''
        When a edge option is selected

        '''
        if self.flag:
            self.edge = int(self.edge_var.get())
            #print(self.edge)

    def mouse_click(self, event):
        '''
        when a grid is clicked, mark it dead/alive;
        '''
        if self.flag == False:
            return
        #print(event.x)

        if event.x < 30:
            return

        if event.y < 100:
            return

        #print(event.y)
        j = int((event.x - 30) / 30)
        i = int((event.y - 100) / 30)
        #print(i)
        #print(j)
        if i >= self.row:
            return

        if j >= self.col:
            return

        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
            self.draw_square(i, j, "black")
        else:
            self.grid[i][j] = 0
            self.draw_square(i, j, "white")


    def draw(self):
        '''
        draw the entry, radio button, button & grid on the canvas
        '''

        self.canvas = tkinter.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_text(self.width/5, 15, text="Rule")

        self.rule_entry = tkinter.Entry(self.canvas)
        self.canvas.create_window((self.width / 5)-30, 30, anchor=tkinter.NW, window=self.rule_entry)

        self.edge_var = tkinter.IntVar()

        radio1 = tkinter.Radiobutton(self.canvas, text="Fields outside are white", variable=self.edge_var, value=1, command=self.sel)
        radio2 = tkinter.Radiobutton(self.canvas, text="Fields outside are black", variable=self.edge_var, value=2, command=self.sel)
        radio3 = tkinter.Radiobutton(self.canvas, text="Torus Shaped playing field", variable=self.edge_var, value=3, command=self.sel)
        self.canvas.create_window((self.width/5)*3, 5, anchor=tkinter.NW, window=radio1)
        self.canvas.create_window((self.width / 5) * 3, 25, anchor=tkinter.NW, window=radio2)
        self.canvas.create_window((self.width / 5) * 3, 45, anchor=tkinter.NW, window=radio3)

        self.start_button = tkinter.Button(self.canvas, text='Start Life', width=15, command=self.start)
        self.canvas.create_window(self.width/2 - 60, 70, anchor=tkinter.NW, window=self.start_button)

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.mouse_click)
        self.canvas.update()

    def draw_square(self, i, j, color):
        '''
        draw the square on the canvas
        '''
        x = j*30 + 30
        y = i*30 + 100
        self.canvas.create_rectangle(x, y, x + 30, y + 30, fill=color)

    def draw_grid(self):
        '''
        draw the grid on the canvas
        '''
        for i in range(self.row):
            for j in range(self.col):
                #x = i*30 + 30
                #y = j*30 + 100
                if self.grid[i][j] == 0:
                    #self.canvas.create_rectangle(x, y, x + 30, y + 30, fill="white")
                    self.draw_square(i, j, "white")
                else:
                    self.draw_square(i, j, "black")
                    #self.canvas.create_rectangle(x, y, x + 30, y + 30, fill="black")

    def start(self):
        '''
        start the game if not started already.
        once game is started any button wont work
        '''

        if self.flag == False:
            return

        rule = self.rule_entry.get()
        if rule == "":
            return

        self.flag = False
        #print(self.grid)
        #print(rule)
        #print(self.edge)
        self.life = Life(self.grid, rule, self.edge)
        self.run()

    def run(self):
        '''
        run in an infinite loop
        '''
        while True:
            sleep(1)
            self.life.tick()
            self.grid = self.life.grid
            self.canvas.destroy()
            self.draw()



app = LifeVisualizer()

