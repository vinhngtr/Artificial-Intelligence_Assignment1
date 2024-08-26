import pygame
import os
class Pipe:
   def __init__(self, display_surface, imageName, location)-> None:
      self.display_surface = display_surface
      self.location = location
      self.imageName = imageName
      self.image = None
      self.load()
      self.angle = 0
      self.bump = False
      pass
   def load(self):
      self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),'images',self.imageName +'.png'))
      self.image = pygame.transform.scale(self.image, (50,50))
   def display(self):
      self.display_surface.blit(self.image, self.location)
      empty_rect = pygame.Rect(self.location[0] , self.location[1], 50, 50)
      pygame.draw.rect(self.display_surface, (255,0,0), empty_rect, 3) 

   
   def rotate(self):
      self.angle -= 90
      self.angle %= 360
      self.image = pygame.transform.rotate(self.image, self.angle)
      self.display_surface.blit(self.image, self.location)
   def bumpWater(self):
      '''
      Nếu ống đó có nước, dùng hàm này để set ống có nước
      '''
      if '-' not in self.imageName:
         self.imageName = self.imageName[0:5] + '-water'
      self.load()
      temp = abs(self.angle)
      self.angle = 0
      self.setRotatePipe(temp)
   def resetWater(self):
      if '-' in self.imageName:
         self.imageName = self.imageName[0:5]
      self.load()
      temp = abs(self.angle)
      self.angle = 0
      self.setRotatePipe(temp)
   def setRotatePipe(self, x):
      '''
      chỉ định quay theo góc cụ thể
      '''
      x = - x
      temp = abs(x - self.angle)
      
      if  x < self.angle:
         self.image = pygame.transform.rotate(self.image, -temp)
      elif x > self.angle:
         self.image = pygame.transform.rotate(self.image, temp)
      self.angle = x
      self.display()