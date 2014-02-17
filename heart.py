import random
import pygame
from colors import * 

class Heart:

	game = None

	def __init__(self, game, rect):
		x = random.randint(rect[0], rect[0] + rect[2])
		y = random.randint(rect[1], rect[1] + rect[3])
		
		self.pic = pygame.image.load("resources/heart.png").convert_alpha()
		self.rect = self.pic.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.game = game

	def update(self):
		''' bubble up the heart untill it reaches the top of the screen'''
		speed = 5
		if self.rect.bottom - speed >=0:
			self.rect.bottom -=speed

	def draw(self, offset):
		self.game.screen.blit(self.pic, [self.rect.left-offset, self.rect.top])
		
	def getSize(self):
		return self.pic.get_size()