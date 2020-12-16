# tkinter application package
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import *
from tkinter import messagebox

# Time for timer
import time

# Random number of mines and random sub sample of board for mine placement
from random import randint, sample

# tkinter Application
root = tk.Tk()
root.update_idletasks()

# Root Geometry
root_Width = 1400
root_Length = 850

# Coordinates of top left pixel of application for centred
x_off = root.winfo_rootx() - root.winfo_x()  # Horizontal pixel offset
y_off = root.winfo_rooty() - root.winfo_y()  # Vertical pixel offset

# Top left (x,y) of pixel for application in centre of screen
x_left = (root.winfo_screenwidth() - root_Width - x_off) // 2
y_top = (root.winfo_screenheight() - root_Length - y_off) // 2

# Apply application position
root_Pos = "+" + str(x_left) + "+" + str(y_top - 30)
root.geometry(str(root_Width) + "x" + str(root_Length) + root_Pos)
# App Title
root.title("Minesweeper")

# tk Fonts
fontTimer = Font(family='Verdana', size=20)
fontBottom = Font(family='Verdana', size=15)
fontBtnBot = Font(family='Verdana', size=12)
fontStart = Font(family="CenturyGothic", size=20)
fontCheck = Font(family="CenturyGothic", size=15)


# Application Design
class ClsGameGui:
    def __init__(self, master):
        # Variables
        Padding = 5
        self.curSetting = -1  # What button is pressed

        self.dicGridButtons = {}  # Stores all grid buttons when made
        self.dicGridFrames = {}  # Stores all grid buttons frames when made
        self.gameBoard = []  # Game Board

        self.dicCheckButtons = {}  # Store start screen Check buttons
        self.GridSizes = [(10, 25), (20, 45), (25, 60), (30, 70)]  # Possible grid sizes

        self.timeVar = 0  # Timer

        # Widget Variables
        self.chkGridSize = tk.IntVar()  # Start Screen check buttons

        ## Root Frames
        # Game | Start Frames
        self.frm_Start = tk.Frame(root, width=root_Width, height=root_Length, bg="lightgreen")
        self.frm_Game = tk.Frame(root, width=root_Width, height=root_Length)
        frm_Start = self.frm_Start  # Short cut variables
        frm_Game = self.frm_Game

        # Place
        self.frm_Start.grid(row=0, column=0, sticky="news")
        frm_Game.grid(row=0, column=0, sticky="news")
        frm_Game.grid_remove()

        ## Game play frames
        frm_Top = tk.Frame(frm_Game, bd=4, relief=tk.GROOVE)  # Aesthetic frame
        frm_Timer = tk.Frame(frm_Game, bd=4, relief=tk.SUNKEN)  # Timer frame
        self.frm_Main = tk.Frame(frm_Game, bg="lightgrey")  # Main frame (for game)
        frm_Bot = tk.Frame(frm_Game, bd=4, relief=tk.SUNKEN)  # Settings and buttons

        # Match visible game frame to main frame
        frm_Game.config(bg=self.frm_Main.cget("bg"))

        # Frame placements
        frm_Top.place(width=root_Width, height=40, x=1, y=0)
        frm_Timer.place(width=260, height=50, x=root_Width // 2, y=25, anchor=tk.CENTER)
        self.frm_Main.place(width=root_Width, height=600, x=0, y=80 - 1)
        frm_Bot.place(width=root_Width, height=140, x=0, y=710)

        ## Start frame
        # Start game button
        btn_Start = tk.Button(self.frm_Start, text="Start", font=fontStart, bg="Green", bd=4)

        # Generate check buttons (allows for dynamic change of board sizes)
        chkSize = len(self.GridSizes) * 100  # 100 x pixels per checkbutton
        # c in possible grid sizes and i in range len of number of grid sizes
        for c, i in tuple(zip(self.GridSizes, [x for x in range(len(self.GridSizes))])):
            # Grid sizes are keys with value pair check button
            # Shared variable and text equal to the grid area
            self.dicCheckButtons[c] = tk.Checkbutton(frm_Start, text=str(c[0] * c[1]),
                                                     variable=self.chkGridSize, onvalue=i + 1,
                                                     bg=frm_Start.cget("bg"), activebackground=frm_Start.cget("bg"),
                                                     font=fontCheck)

            # Place each checkbutton evenly
            self.dicCheckButtons[c].place(y=400, x=root_Width // 2 - chkSize // 2 + i * 100)

        # Placements
        btn_Start.place(x=root_Width // 2, y=470, anchor=tk.CENTER)

        ## Timer Frame
        self.lbl_Timer = tk.Label(frm_Timer, text="TIMER", font=fontTimer)
        self.lbl_Timer.place(x=260 // 2 - 2, y=20, anchor=tk.CENTER)

        ## Bottom Frame
        # Grid Size
        lbl_GridSize = tk.Label(frm_Bot, text="Grid Size:", font=fontBottom)
        self.lbl_GridSize = tk.Label(frm_Bot, text="#", font=fontBottom)

        # Mines
        lbl_MinesNo = tk.Label(frm_Bot, text="Mines:", font=fontBottom)
        self.lbl_MinesNo = tk.Label(frm_Bot, text="#", font=fontBottom)

        # Flag / Sweep Buttons
        lbl_RedFlag = tk.Label(frm_Bot, text="Flag", fg="Red", font=fontBottom)
        lbl_BlueFlag = tk.Label(frm_Bot, text="Flag", fg="Blue", font=fontBottom)
        lbl_Sweep = tk.Label(frm_Bot, text="Sweep", fg="Orange", font=fontBottom)
        self.btn_RedFlag = tk.Button(frm_Bot, bg="Red", bd=6)
        self.btn_BlueFlag = tk.Button(frm_Bot, bg="Blue", bd=6)
        self.btn_Sweep = tk.Button(frm_Bot, bg="Orange", bd=6)

        # Tech buttons
        btn_Reset = tk.Button(frm_Bot, text="Reset", font=fontBtnBot)
        btn_Quit = tk.Button(frm_Bot, text="Quit", font=fontBtnBot)
        self.btn_Cheat = tk.Button(frm_Bot, text="Cheat", font=fontBtnBot)

        # Placements
        # Grid size
        lbl_GridSize.place(x=Padding + 140, y=20, anchor=tk.NE)
        self.lbl_GridSize.place(x=Padding * 2 + 140, y=20, width=50, anchor=tk.NW)
        # Mines
        lbl_MinesNo.place(x=Padding + 140, y=70, anchor=tk.NE)
        self.lbl_MinesNo.place(x=Padding * 2 + 140, y=70, width=50, anchor=tk.NW)
        # Flag / Sweep buttons
        self.btn_RedFlag.place(x=root_Width // 2 - 2, y=50, anchor=tk.CENTER, width=50, height=50)
        lbl_RedFlag.place(x=root_Width // 2 - 2, y=90, anchor=tk.CENTER, width=50, height=50)
        self.btn_BlueFlag.place(x=root_Width // 2 - 2 - 80, y=50, anchor=tk.CENTER, width=50, height=50)
        lbl_BlueFlag.place(x=root_Width // 2 - 2 - 80, y=90, anchor=tk.CENTER, width=50, height=50)
        self.btn_Sweep.place(x=root_Width // 2 - 2 + 80, y=50, anchor=tk.CENTER, width=50, height=50)
        lbl_Sweep.place(x=root_Width // 2 - 2 + 80, y=90, anchor=tk.CENTER, width=70, height=50)
        # Tech Buttons
        btn_Reset.place(x=1100 - 50, y=40, width=70)
        btn_Quit.place(x=1200 - 50, y=40, width=70)
        self.btn_Cheat.place(x=1300 - 50, y=40, width=70)

        # Bind functions
        root.bind("<Shift_L>", lambda x: self.quickSwap())

        # Attach Functions
        # Start Button
        btn_Start.config(command=self.startGame)
        # Restart button
        btn_Reset.config(command=self.resetGame)
        # Settings Functions
        self.btn_RedFlag.config(command=lambda: self.settingsButton("Red"))
        self.btn_BlueFlag.config(command=lambda: self.settingsButton("Blue"))
        self.btn_Sweep.config(command=lambda: self.settingsButton("Sweep"))

    # Function for Start button
    def startGame(self):

        # Check grid size selected
        if self.chkGridSize.get() == 0:
            for i in self.dicCheckButtons:
                self.dicCheckButtons[i].flash()  # Flash if no selection
            return

        # Reveal game frame
        self.frm_Game.grid()
        # Remove start frame
        self.frm_Start.grid_remove()

        # Find selected area from check button
        gridArea = self.GridSizes[self.chkGridSize.get() - 1]

        # Generate Grid of selected area
        self.spawnGrid(gridArea)

        # Load Game play class
        # Initialised here to ensure relevant information is available
        GamePlay = ClsGamePlay()
        self.updateClock()

    # Function for reset back to title
    def resetGame(self):

        # Delete game buttons and frames
        for i, j in tuple(zip(self.dicGridButtons, self.dicGridFrames)):
            self.dicGridButtons[i].destroy()
            self.dicGridFrames[j].destroy()

        # Reset button/frame dictionary/lists
        self.dicGridButtons = {}
        self.dicGridFrames = {}
        self.gameBoard = []

        # Reset timer
        root.after_cancel(self.timeFunc)
        self.timeVar = 0

        # Hide and show frames
        self.frm_Start.grid()
        self.frm_Game.grid_remove()

    # Current Settings functions:
    # Controls what current setting is selected
    def settingsButton(self, btnType):

        # References for settings buttons
        lstBtn = [self.btn_RedFlag, self.btn_BlueFlag, self.btn_Sweep]
        dicBtn = {"Red": 0, "Blue": 1, "Sweep": 2}

        # Ensure function used correctly
        if btnType not in dicBtn:
            print("Type Error")
            return

        # One setting button pressed at a time
        for i in range(len(lstBtn)):
            # Press, Disable and Lock button when pushed
            if i == dicBtn[btnType]:
                lstBtn[i].config(state=tk.DISABLED, relief=tk.SUNKEN)
                self.curSetting = i  # Set reference to current button push
            else:
                # Un-press, Reactivate and Unlock other buttons
                lstBtn[i].config(state=tk.NORMAL, relief=tk.RAISED)

    # Bind function: Quick swap between red and sweep on key press
    def quickSwap(self):

        # Ref of settings buttons
        lstRef = ["Red", "Blue", "Sweep"]

        # Swap between red: 0 and sweep: 2
        if self.curSetting == 1:
            nextSetting = self.curSetting - 1  # If Blue swap to red
        else:
            nextSetting = (self.curSetting + 2) % 4  # Swap between 0 and 2

        # Load settings buttons with determined reference
        self.settingsButton(lstRef[nextSetting])

    # Function for spawning buttons for game board
    # Buttons are put to dicGridButtons dictionary
    def spawnGrid(self, tupGrid):

        # Get info from tuple
        row = tupGrid[0]
        col = tupGrid[1]

        # Shorten class variables
        gameBoard = self.gameBoard
        dicGridButtons = self.dicGridButtons
        dicGridFrames = self.dicGridFrames

        root.update()  # Update to get widget info
        frmWidth = self.frm_Main.winfo_width()  # Main frame width
        frmHeight = self.frm_Main.winfo_height()  # Main frame height

        # Variables
        Padding = 3

        # Calculate maximum width / height given space between buttons
        maxWidth = frmWidth - Padding * (col + 1)
        maxHeight = frmHeight - Padding * (row + 1)
        # Find minimum square such that all buttons fit both horizontally and vertically
        minSquare = min(maxWidth / col, maxHeight / row)

        # Determine remaining space from min square
        # Halved to find start position of button such that space is split on both sides
        rowOff = (frmWidth - (col * minSquare + (col - 1) * Padding)) // 2
        colOff = (frmHeight - (row * minSquare + (row - 1) * Padding)) // 2

        # Generate board and populate game board list to correct size
        for i in range(row):
            gameBoard.append([])
            for j in range(col):
                # Append to Game board
                gameBoard[i].append("")

                # Create frames for buttons
                frm_btn = "frm_" + str(i) + str(j)
                frm_btn = tk.Frame(self.frm_Main)
                frm_btn.grid_propagate(False)
                frm_btn.columnconfigure(0, weight=1)
                frm_btn.rowconfigure(0, weight=1)
                frm_btn.place(width=minSquare, height=minSquare,
                              x=rowOff + j * (Padding + minSquare),
                              y=colOff + i * (Padding + minSquare),
                              anchor=tk.NW)

                dicGridFrames[(i, j)] = frm_btn

                # Create current button and add to dictionary
                btn_Game = tk.Button(frm_btn)
                dicGridButtons[(i, j)] = btn_Game
                dicGridButtons[(i, j)].grid(sticky="wens")

    # Recursive clock function
    def updateClock(self):

        # Increase by 1 every second
        self.timeVar += 1
        # change the text of the time_label according to the current time
        self.lbl_Timer.config(text=time.strftime("%H:%M:%S", time.gmtime(self.timeVar)))

        # reschedule update_clock function to update time_label every 100 ms
        self.timeFunc = root.after(1000, self.updateClock)


# Class for Game play functions
# Loaded after start button
class ClsGamePlay:
    def __init__(self):
        ## Variables
        self.firstClick = 0

        # Shared variables
        self.gameBoard = GameGui.gameBoard
        self.dicGridButtons = GameGui.dicGridButtons

        # Game Board
        self.rowSize = len(self.gameBoard)
        self.colSize = len(self.gameBoard[0])
        self.boardArea = self.rowSize * self.colSize

        # Number of mines
        self.minesNumber = randint(int(0.1 * self.boardArea), int(0.2 * self.boardArea))  # Randomise number of mines
        self.minesRef = self.minesNumber

        ## Modify GUI settings labels
        GameGui.lbl_GridSize.config(text=self.boardArea)
        GameGui.lbl_MinesNo.config(text=self.minesNumber)

        ## Attach Button commands
        GameGui.btn_Cheat.config(command=self.cheatButton)
        # Attach command to all board buttons
        for i in range(self.rowSize):
            for j in range(self.colSize):
                self.dicGridButtons[(i, j)].config(command=lambda i=i, j=j: self.gameButton(i, j))

    # Command for game buttons
    # Takes own row, col and switch
    # switch determines if sweep command is disabled (off = works)
    def gameButton(self, row, col, switch="off"):

        # Get current button and setting
        curButton = self.dicGridButtons[(row, col)]
        curSetting = GameGui.curSetting

        # If setting is a flag (red/blue)
        if curSetting in [0, 1]:

            # Reference of flags
            lstColours = ["red", "blue"]

            # Swap to current colour if not flagged
            if switch == "off" or lstColours[curSetting] != curButton.cget("bg"):
                curButton.config(bg=lstColours[curSetting],
                                 command=lambda: self.gameButton(row, col, "on"))

                # Change mine count when flagged
                if switch == "off":
                    self.updateMines(-1)

            # If flagged un-flag and allow sweeping
            elif switch == "on":
                curButton.config(bg="systemButtonFace",
                                 command=lambda: self.gameButton(row, col, "off"))

                # Increase mine count when un-flagged
                self.updateMines(1)

        # Sweep setting
        if curSetting == 2 and switch == 'off':
            # Fist sweep press generates board
            # Ensures first button isn't mine
            if self.firstClick == 0:
                self.firstClick += 1
                # Populate function generates mines and board
                self.populateBoard(row, col)

            # Press button
            self.pressButton(row, col)

        # Check win regardless of current setting
        self.checkWin()

    # Generates mines and numbers for board
    def populateBoard(self, row, col):

        # Keys of Grid button dictionary are tuples of grid
        # Make list copy of dictionary
        lstBoard = list(self.dicGridButtons)

        # Reference of near by coordinates around some point
        # Nearby:  self, square around and 1 point centre up,left,right,down beyond square
        # E.g: For some point (x,y)  and (x0,y0) in list then neighbours are (x+x0,y+y0)
        lstNear = [(-2, 0), (-1, -1), (-1, 0), (-1, 1), (0, -2), (0, -2), (0, -1),
                   (0, 0), (0, 1), (0, 2), (1, -1), (1, 0), (1, 1), (2, 0)]

        # Remove self and neighbours from grid of coordinates copy
        for i, j in lstNear:
            # Try or pass, in case of non existent neighbours
            try:
                # If (x+x0, y+y0) neighbour is range of entry on grid
                if row + i >= 0 and col + j >= 0:
                    lstBoard.remove((row + i, col + j))
            except:
                pass

        # Random subsample of size Number of mines of modified board
        # Denotes placement of all mines, therefore first press and neighbours are never mines
        # Ensures first press is fair
        lstMines = sample(lstBoard, self.minesNumber)

        # Assign mines to coordinates in game board
        for i, j in lstMines:
            self.gameBoard[i][j] = "M"

        # Assign all non mines the count of mines in square around
        for i in range(self.rowSize):
            for j in range(self.colSize):
                if self.gameBoard[i][j] != "M":
                    # Count function
                    self.gameBoard[i][j] = self.countNeighbours(i, j, "M")

    # Counts gameBoard neighbours for item unless item is None
    # Will return list if "Yes" instead of integer of count
    # Neighbours are square around given (row,col) coordinate
    def countNeighbours(self, row, col, item, fullList="No"):

        # Variables
        gameBoard = self.gameBoard
        itemNeighbours = []

        # Reference of near by coordinates around some point
        # Nearby:  square around
        # E.g: For some point (x,y)  and (x0,y0) in list then neighbours are (x+x0,y+y0)
        lstNear = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # Find all neighbours of point (x+x0,y+y0)
        for i, j in lstNear:
            if 0 <= row + i <= self.rowSize - 1 and 0 <= col + j <= self.colSize - 1:
                # No item, collect all neighbours
                if item is None:
                    itemNeighbours.append((row + i, col + j))
                # Append neighbour if item
                elif gameBoard[row + i][col + j] == item:
                    itemNeighbours.append((row + i, col + j))
        # Return list
        if fullList == "Yes":
            return itemNeighbours
        # Return int count of item in neighbours
        else:
            return len(itemNeighbours)

    # Press button, sweep for mines
    def pressButton(self, row, col):

        # Variables
        gameBoard = self.gameBoard

        # If button is mine then lose
        if gameBoard[row][col] == "M":
            self.endGame()
            messagebox.showinfo("YOU LOSE")
            return

        # Skip if button has been pushed already
        elif gameBoard[row][col] == "X":
            return

        # Get current button widget
        curButton = self.dicGridButtons[(row, col)]
        # Get current count of neighbouring mines
        curNumber = gameBoard[row][col]

        # Update game board reference
        gameBoard[row][col] = "X"  # Button has been pushed

        # Colour function
        curColour = self.colourText(curNumber)  # Get relevant colour

        # No mines nearby then no text
        if curNumber == 0:
            curNumber = ""

        # Current button: Sink, remove command, text is number of mines and colour text
        curButton.config(relief=tk.SUNKEN, text=curNumber, command=lambda: None, fg=curColour,
                         activebackground="lightgrey", bg="lightgrey")

        # If no neighbouring mines automatically push neighbouring buttons
        # Recursive function
        if curNumber == "":
            lstNeighbours = self.countNeighbours(row, col, None, "Yes")
            for i, j in lstNeighbours:
                self.pressButton(i, j)

    # Update Mines display number as buttons are flagged
    def updateMines(self, delta):

        self.minesNumber = self.minesNumber + delta
        GameGui.lbl_MinesNo.config(text=self.minesNumber)

    # Check if win conditions met
    def checkWin(self):

        # Count number of pushed buttons
        lstCount = [i.count("X") for i in self.gameBoard]
        totalCount = sum(lstCount)

        # If all mines flagged and all non mines pushed then win
        if self.minesNumber == 0 and totalCount + self.minesRef == self.boardArea:
            self.endGame()  # End Game
            messagebox.showinfo("YOU WIN")

    # End Game freezes board state
    def endGame(self):

        # Stop timer
        root.after_cancel(GameGui.timeFunc)

        # Remove game button commands
        for i, j in self.dicGridButtons:
            self.dicGridButtons[(i, j)].config(command=lambda: None)
            # Reveal all buttons (for lose)
            if self.gameBoard[i][j] == "M":
                self.dicGridButtons[(i, j)].config(bg="red")
            elif self.gameBoard[i][j] != "X" and self.gameBoard[i][j] != 0:
                self.dicGridButtons[(i, j)].config(text=self.gameBoard[i][j])

    # Determine colour of game button text based on number
    @staticmethod
    def colourText(textNumber):

        lstRef = {0: "systemButtonFace", 1: "blue", 2: "green", 3: "red", 4: "purple",
                  5: "maroon", 6: "turquoise", 7: "black", 8: "grey"}

        return lstRef[textNumber]

    # Cheat button reveals all non pushed buttons
    def cheatButton(self):
        dicGridButtons = self.dicGridButtons
        gameBoard = self.gameBoard
        for i, j in list(dicGridButtons):
            if gameBoard[i][j] != "X":
                dicGridButtons[(i, j)].config(text=gameBoard[i][j])


# Declare GUI class
GameGui = ClsGameGui(root)

# Run root
root.mainloop()

# Changes:
# - quick add function can be combined with normal function
# - Optimise loading of game buttons (Try combine iterations where possible)
# - Streamline functions (Combine some)

# - Add pause button
# - Add Player name
# - Save Load features
# - Score Leaderboard
