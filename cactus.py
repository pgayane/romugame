import pygame
import colors
import random

class Cactus:

	rect = [0,0,0,0]
	game = None

	margin = 0
	def __init__(self, game):
		type = random.randint(0,1)
		if type == 0:
			self.pic = pygame.image.load("resources/cactus_small.png").convert()
			self.margin = 20
		else:
			self.pic = pygame.image.load("resources/cactus.png").convert()
			self.margin = 35

		self.pic.set_colorkey(colors.WHITE)
		
		self.rect = self.pic.get_rect()

		self.game = game
		#print self.cat_pic.get_size()

 	def setLocation(self, newLoc):
		self.rect.bottomleft = newLoc
		self.rect.y +=self.margin

	def drawAt(self, screen, loc):
		screen.blit(self.pic, loc)

	def draw(self, screen, offset):
		screen.blit(self.pic, [self.rect.left-offset, self.rect.top])
		#pygame.draw.rect(screen, colors.RED, self.rect, 1)

	def getSize(self):
		return self.pic.get_size()
