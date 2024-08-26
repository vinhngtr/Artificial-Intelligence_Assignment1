import tkinter as tk
from constant import *
from DepthFirstSearch import *
from tkinter import ttk
import os
import json

class WindowGamePlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pipes Puzzle")
        self.currentGridIndex = 0
        self.boardGame = []
        self.searchAlgorithm = ""
        self.pipesGrids = []
        self.totalStep = 0
        self.sourcePosition = []
        self.gridSize = 0
        self.cellSize = 0
        self.selectedTestcase = tk.StringVar()
        self.pipeImages = []
        self.testCase = []
        self.getTestCase()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT + BUTTON_HEIGHT, bg=DARK)
        self.canvas.pack()
        image = tk.PhotoImage(file="Pictures/logo.png")
        self.logo = image.subsample(image.width() // (WIDTH//2) + 1)
        self.drawControlPanel()
    def getTestCase(self):
        folder_path = "Test/"
        self.testCase = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    def getBoardata(self):
        with open("Test/" + self.selectedTestcase.get(), 'r') as file:
            content = file.read()
        try:
            testcase_list = eval(content)
        except SyntaxError:
            testcase_list = json.loads(content)

        return testcase_list
    def drawControlPanel(self):
        self.canvas.config(bg=DARK)

        self.canvas.create_image(WIDTH / 2, HEIGHT / 5, image=self.logo)

        self.selectText = tk.Label(self.root, text="Select Your Testcase", bg= DARK, fg="white")
        self.selectText.place(relx=0.45, rely=0.35, anchor=tk.CENTER)

        self.algorithm_combobox = ttk.Combobox(self.root, textvariable=self.selectedTestcase)
        self.algorithm_combobox['values'] = self.testCase
        self.algorithm_combobox.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.warningText = tk.Label(self.root, text="Error!", bg= DARK, fg=RED)
        

        self.dfs_button = tk.Button(self.canvas, text="DFS", command=self.runDFS, bg=GREEN, width=8, height=1, borderwidth=2)
        self.dfs_button.place(relx=0.25, rely=0.6, anchor=tk.CENTER)

        self.astar_button = tk.Button(self.canvas, text="A*", command=self.runAStar, bg=GREEN, width=8, height=1, borderwidth=2, state="disabled")
        self.astar_button.place(relx=0.75, rely=0.6, anchor=tk.CENTER)


    def runAStar(self):
        try:
            print("\n", self.selectedTestcase.get())
            self.boardGame = self.getBoardata()
            self.gridSize = len(self.boardGame[0])
            self.cellSize = (WIDTH - 2*PADDING) // self.gridSize
            self.pipeImages = self.loadImages()
            self.searchAlgorithm = DepthFirstSearch(self.boardGame, self.gridSize)
            self.searchAlgorithm.solveBoard()
            self.pipesGrids = self.searchAlgorithm.finalPath
            self.totalStep = len(self.pipesGrids)
            self.sourcePosition = self.searchAlgorithm.source
            self.warningText.destroy()
            self.refresh()
            self.astar_button.destroy()
            self.dfs_button.destroy()
            self.selectText.destroy()
            self.algorithm_combobox.destroy()
        except:
            self.warningText.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def runDFS(self):
        try:
            print("\n", self.selectedTestcase.get())
            self.boardGame = self.getBoardata()
            self.gridSize = len(self.boardGame[0])
            self.cellSize = (WIDTH - 2*PADDING) // self.gridSize
            self.pipeImages = self.loadImages()
            self.searchAlgorithm = DepthFirstSearch(self.boardGame, self.gridSize)
            self.searchAlgorithm.solveBoard(1)
            self.pipesGrids = self.searchAlgorithm.finalPath
            self.totalStep = len(self.pipesGrids)
            self.sourcePosition = self.searchAlgorithm.source
            self.warningText.destroy()
            self.refresh()
            self.astar_button.destroy()
            self.dfs_button.destroy()
            self.selectText.destroy()
            self.algorithm_combobox.destroy()
        except:
            self.warningText.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def loadImages(self):
        pipeImages = {}
        pipe_filenames = {
            H: "./Pictures/H.png",V: "./Pictures/V.png",
            UR: "./Pictures/UR.png",UL: "./Pictures/UL.png",DR: "./Pictures/DR.png",DL: "./Pictures/DL.png",
            TU: "./Pictures/TU.png",TD: "./Pictures/TD.png",TL: "./Pictures/TL.png",TR: "./Pictures/TR.png",
            EU: "./Pictures/EU.png",ED: "./Pictures/ED.png",EL: "./Pictures/EL.png",ER: "./Pictures/ER.png",
            CH: "./Pictures/CH.png",CV: "./Pictures/CV.png",
            CUR: "./Pictures/CUR.png",CUL: "./Pictures/CUL.png",CDR: "./Pictures/CDR.png",CDL: "./Pictures/CDL.png",
            CTU: "./Pictures/CTU.png",CTD: "./Pictures/CTD.png",CTL: "./Pictures/CTL.png",CTR: "./Pictures/CTR.png",
            CEU: "./Pictures/CEU.png",CED: "./Pictures/CED.png",CEL: "./Pictures/CEL.png",CER: "./Pictures/CER.png",
            SH: "./Pictures/SH.png",SV: "./Pictures/SV.png",
            SUR: "./Pictures/SUR.png",SUL: "./Pictures/SUL.png",SDR: "./Pictures/SDR.png",SDL: "./Pictures/SDL.png",
            STU: "./Pictures/STU.png", STD: "./Pictures/STD.png", STL: "./Pictures/STL.png", STR: "./Pictures/STR.png",
        }

        for pipe_type, pipe_filename in pipe_filenames.items():
            image = tk.PhotoImage(file=pipe_filename)
            # Scale the image to fit cell size
            scaled_image = image.subsample(image.width() // self.cellSize + 1)
            pipeImages[pipe_type] = scaled_image
        return pipeImages
    
    def drawGrid(self):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                cell_x = PADDING + x * self.cellSize
                cell_y = STEP_AREA + y * self.cellSize
                self.canvas.create_rectangle(cell_x, cell_y, cell_x + self.cellSize, cell_y + self.cellSize, fill=BEIGE)
                
    def drawPipes(self):
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                if [x,y] == self.sourcePosition:
                    pipe_type = self.getSourceValue(x, y)
                else:
                    pipe_type = self.pipesGrids[self.currentGridIndex][y][x]
                image = self.pipeImages[pipe_type]
                cell_x = PADDING + x * self.cellSize
                cell_y = STEP_AREA + y * self.cellSize
                self.canvas.create_image(cell_x + self.cellSize/2, cell_y + self.cellSize/2, image=image)
                border_width = 2  # Độ rộng của border
                self.canvas.create_rectangle(cell_x, cell_y, cell_x + self.cellSize, cell_y + self.cellSize, outline=BLACK, width=border_width)


    def drawStepArea(self):
        bold_font = ('Arial', 10, 'bold')
        self.stepLabel = tk.Label(self.canvas, text=f"Step: {self.currentGridIndex}/{self.totalStep-1}", bg=LIGHT_BLUE, fg=BLACK, font=bold_font)
        self.stepLabel.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    def drawBoardArea(self):
        self.drawGrid()
        self.drawPipes()
        self.canvas.config(bg=LIGHT_BLUE)



    def getSourceValue(self, x, y):
        if self.pipesGrids[self.currentGridIndex][y][x] == CH:
            return SH
        elif self.pipesGrids[self.currentGridIndex][y][x] == CV:
            return SV
        elif self.pipesGrids[self.currentGridIndex][y][x] == CUL:
            return SUL
        elif self.pipesGrids[self.currentGridIndex][y][x] == CUR:
            return SUR
        elif self.pipesGrids[self.currentGridIndex][y][x] == CDL:
            return SDL
        elif self.pipesGrids[self.currentGridIndex][y][x] == CDR:
            return SDR
        elif self.pipesGrids[self.currentGridIndex][y][x] == CTU:
            return STU
        elif self.pipesGrids[self.currentGridIndex][y][x] == CTD:
            return STD
        elif self.pipesGrids[self.currentGridIndex][y][x] == CTL:
            return STL
        elif self.pipesGrids[self.currentGridIndex][y][x] == CTR:
            return STR


    def drawButtons(self):
        self.nextButton = tk.Button(self.canvas, text="Next", command=self.nextGrid, bg=GREEN, width=8, height=1, borderwidth=2)
        self.nextButton.place(relx=0.75, rely=0.9, anchor=tk.CENTER)

        self.homeButton = tk.Button(self.canvas, text="Home", command=self.toHome, bg=GREEN, width=8, height=1, borderwidth=2)
        self.homeButton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        self.prevButton = tk.Button(self.canvas, text="Previous", command=self.prevGrid, bg=GREEN, width=8, height=1, borderwidth=2)
        self.prevButton.place(relx=0.25, rely=0.9, anchor=tk.CENTER)

    def reset(self):
        self.boardGame = None
        self.gridSize = 0
        self.cellSize = 0
        self.pipeImages = []
        self.searchAlgorithm = None
        self.pipesGrids = []
        self.totalStep = 0
        self.sourcePosition = []
        self.selectedTestcase.set("")
        self.currentGridIndex = 0
    def toHome(self):
        self.canvas.delete("all")
        self.reset()
        self.stepLabel.destroy()
        self.nextButton.destroy()
        self.prevButton.destroy()
        self.homeButton.destroy()
        self.drawControlPanel()

    def nextGrid(self):
        if self.currentGridIndex < self.totalStep - 1:
            self.currentGridIndex += 1
        else:
            self.currentGridIndex = 0
        self.refresh()

    def prevGrid(self):
        if self.currentGridIndex > 0:
            self.currentGridIndex -= 1
        else:
            self.currentGridIndex = self.totalStep - 1
        self.refresh()

    def refresh(self):
        self.canvas.delete("all")
        try:
            self.stepLabel.destroy()
            self.nextButton.destroy()
            self.prevButton.destroy()
            self.homeButton.destroy()
        except:
            pass
        self.drawStepArea()
        self.drawBoardArea()
        self.drawButtons()

    def run(self):
        self.root.mainloop()