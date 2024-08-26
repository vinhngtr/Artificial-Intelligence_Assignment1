from runningPuzzle import PipesPuzzle
from operator_pipe import Pipe
from buttonGame import Button
import pygame
import os
import setConstant



pygame.init()
# -------------- Initialization ------------

width = 700
height = 700


class PuzzleInterface:
    def __init__(self, puzzle_obj: PipesPuzzle):
        self.display_surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pipe-puzzles")
        self.display_surface.fill(setConstant.white)
        self.pipe_puzzle = puzzle_obj
        self.index = 0
        self.head = []
        self.auto = False

        # load button image 
        next_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'images','next.png'))
        self.next_button = Button(520, 100, next_img, 0.8)

        pre_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'images','previous.png'))
        self.pre_button = Button(400, 100, pre_img, 0.8)   
        auto_img = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'images','autorun.png'))
        self.auto_button = Button(450, 200, auto_img, 0.5)
        self.font = pygame.font.Font(None, 50)
        
        
        # load label 
        

        if len(self.pipe_puzzle.path) != 0:
            for i in range(5):
                for j in range(5):
                    t = self.pipe_puzzle.path[0].head[i][j]["type"]
                    if j == 0:
                        self.head.append([Pipe(self.display_surface, f"type{t}",(100 + j * 50,300 - 50 * i))])
                    else:
                        self.head[i].append(Pipe(self.display_surface, f"type{t}",(100 + j * 50, 300 - i * 50)))
                    if self.pipe_puzzle.path[0].head[i][j]["bump"] == True:
                        self.head[i][j].angle = self.pipe_puzzle.path[0].head[i][j]["heading"]
                        self.head[i][j].bumpWater()
                    else:
                        self.head[i][j].setRotatePipe(self.pipe_puzzle.path[0].head[i][j]["heading"])  
        self.display()
        pygame.display.update() 

    def display(self):
        self.display_surface.blit(self.next_button.image, (self.next_button.rect.topleft[0],self.next_button.rect.topleft[1]))
        self.display_surface.blit(self.pre_button.image, (self.pre_button.rect.topleft[0],self.pre_button.rect.topleft[1]))
        self.display_surface.blit(self.auto_button.image, (self.auto_button.rect.topleft[0],self.auto_button.rect.topleft[1]))
        displayStep = self.font.render("STEP: " + str(self.index), True, setConstant.red)
        self.display_surface.blit(displayStep, (5, 5))
        for i in range(5):
            for j in range(5):
                self.head[i][j].display()  
        pygame.draw.circle(self.display_surface,setConstant.red,[225,225],10,0)
                    

    def next_step(self):
        """
        go to the next step in self.pipes.path
        """
        if self.index == len(self.pipe_puzzle.path) - 1:
            return False
        self.index += 1
        for i in range(5):
            for j in range(5):
                if self.pipe_puzzle.path[self.index].head[i][j]["heading"] != self.pipe_puzzle.path[self.index - 1].head[i][j]["heading"]:
                    if self.pipe_puzzle.path[self.index].head[i][j]["bump"] == self.pipe_puzzle.path[self.index - 1].head[i][j]["bump"]:
                        self.head[i][j].setRotatePipe(self.pipe_puzzle.path[self.index].head[i][j]["heading"])
                    else:
                        if self.pipe_puzzle.path[self.index].head[i][j]["bump"]:
                            self.head[i][j].angle = self.pipe_puzzle.path[self.index].head[i][j]["heading"] 
                            self.head[i][j].bumpWater()
                        else:
                            self.head[i][j].angle = self.pipe_puzzle.path[self.index].head[i][j]["heading"] 
                            self.head[i][j].resetWater()             
                else:
                    if self.pipe_puzzle.path[self.index].head[i][j]["bump"] != self.pipe_puzzle.path[self.index - 1].head[i][j]["bump"]:
                        if  self.pipe_puzzle.path[self.index].head[i][j]["bump"]:
                            self.head[i][j].bumpWater()
                        else:
                            self.head[i][j].resetWater()
        return True

    def previous_step(self):
        if self.index == 0:
            return False
        self.index -= 1
        for i in range(5):
            for j in range(5):
                if self.pipe_puzzle.path[self.index].head[i][j]["heading"] != self.pipe_puzzle.path[self.index + 1].head[i][j]["heading"]:
                    if self.pipe_puzzle.path[self.index].head[i][j]["bump"] == self.pipe_puzzle.path[self.index + 1].head[i][j]["bump"]:
                        self.head[i][j].setRotatePipe(self.pipe_puzzle.path[self.index].head[i][j]["heading"])
                    else:
                        if self.pipe_puzzle.path[self.index].head[i][j]["bump"]:
                            self.head[i][j].angle = self.pipe_puzzle.path[self.index].head[i][j]["heading"] 
                            self.head[i][j].bumpWater()
                        else:
                            self.head[i][j].angle = self.pipe_puzzle.path[self.index].head[i][j]["heading"] 
                            self.head[i][j].resetWater()             
                else:
                    if self.pipe_puzzle.path[self.index].head[i][j]["bump"] != self.pipe_puzzle.path[self.index + 1].head[i][j]["bump"]:
                        if  self.pipe_puzzle.path[self.index].head[i][j]["bump"]:
                            self.head[i][j].bumpWater()
                        else:
                            self.head[i][j].resetWater()
        return True
    def running(self):
        self.display_surface.fill(setConstant.white)
        self.display()
        pygame.display.update()
        run = True
        while run:        
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run ==False
                    pygame.quit()
                    return
            if self.auto_button.draw(self.display_surface):
                self.auto = not(self.auto)          
            if self.auto == True:
                font1 = pygame.font.Font(None,30)
                autoTurnOn =font1.render("Auto-run is turn on" , True, setConstant.black)
                self.display_surface.blit(autoTurnOn, (450, 300))
                pygame.display.update()
            if self.auto == False:
                self.display_surface.fill( setConstant.white,(450,300, 200, 100))
                pygame.display.update()
            if self.next_button.draw(self.display_surface):
                if self.auto:
                    while self.next_step():
                        self.display_surface.fill(setConstant.white,(0,0, 300, 200))
                        self.display()
                        pygame.display.update()
                        pygame.time.delay(200) 
                    self.auto = False                      
                else:
                    self.next_step()
                    self.display_surface.fill(setConstant.white,(0,0, 300, 100))
                    self.display()
                    pygame.display.update()
                    pygame.time.delay(500)
            if self.pre_button.draw(self.display_surface):
                if self.auto:
                    while self.previous_step():   
                        self.display_surface.fill(setConstant.white,(0,0, 300, 100)) 
                        self.display()
                        pygame.display.update()
                        pygame.time.delay(200)
                        self.auto = False
                else:
                    self.previous_step()
                    self.display_surface.fill(setConstant.white,(0,0, 300, 100))
                    self.display()
                    pygame.display.update()
                    pygame.time.delay(500) 
        




