import pygame
from colors import *
import random

class Cactus:

	def __init__(self, game, loc):
		type = random.randint(0,1)
		if type == 0:
			self.pic = pygame.image.load("resources/cactus_small.png").convert()
			self.margin = 20
		else:
			self.pic = pygame.image.load("resources/cactus.png").convert()
			self.margin = 35

		self.pic.set_colorkey(WHITE)
		
		self.rect = self.pic.get_rect()
		self.rect.bottomleft = loc
		self.rect.y +=self.margin

		self.game = game
		
	def drawAt(self, screen, loc):
		screen.blit(self.pic, loc)

	def draw(self, screen, offset):
		screen.blit(self.pic, [self.rect.left-offset, self.rect.top])

	def get_size(self):
		return self.pic.get_size()

	
