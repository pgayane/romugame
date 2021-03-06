import pygame
from colors import *
import random

class Tree:

	def __init__(self, game, index, tree_width):
		''' create a tree with random size '''

		self.game = game
		self.index = index
		self.tree_width = tree_width

		min_root_height = self.game.ground_y//5
		max_root_height = self.game.ground_y//3
		min_leaves_height = self.game.ground_y//4
		max_leaves_height = 2*self.game.ground_y//3

		self.tree_root_height = random.randint(min_root_height, max_root_height)
		self.leaves_height = random.randint(min_leaves_height, max_leaves_height)

		self.root_width = 20 

 	def draw(self, offset):		
 		''' draws the tree with predetermined size '''
 		
		# tree root
		x = self.index*self.tree_width + (self.tree_width)/2 - self.root_width/2 - offset
		y = self.game.ground_y - self.tree_root_height - 5
		width = self.root_width
		height = self.tree_root_height +5
		if x+width> 0 and x <=self.game.screen.get_size()[0]:
			pygame.draw.rect(self.game.screen, TREE_ROOT, [x, y, width, height])
		
		# tree leaves
		leaves_width = self.tree_width - 30
		x = self.index*self.tree_width + self.tree_width/2  - leaves_width/2 - offset
		y = self.game.ground_y - self.tree_root_height - 5 - self.leaves_height
		width = leaves_width
		height = self.leaves_height
		if x+width>0  and x <=self.game.screen.get_size()[0]:
			pygame.draw.ellipse(self.game.screen, DARK_GREEN, [x, y, width, height])

	def get_size(self):
		return self.pic.get_size()
