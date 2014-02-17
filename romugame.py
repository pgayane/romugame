# -*- coding: latin-1 -*-

import pygame
from cat import Cat
from colors import * 
import datetime as dt
from cactus import Cactus
from heart import Heart
from tree import Tree
import random

class RomuGame:

	screen_size = (700, 500)
	path_size = 4000
	ground_y = screen_size[1] * 0.9
	score = 0

	cactus_list = []
	trees_list = []

	romu  = None
	initTime = None
	screen = None
	win_point = 3400

	def __init__(self):
		''' generates all the objects necessary for the game '''

		self.screen = pygame.display.set_mode(self.screen_size)
	
		self.romu = Cat(self, True)		
		self.romu.setStepSize(10)
		self.romu.setLocation([0, self.ground_y])
	
		for i in range(1,9):
			cactus = Cactus(self)
			cactus.setLocation([420*i, self.ground_y])
			self.cactus_list.append(cactus)

		number_of_trees = 24	
		tree_width = self.path_size/number_of_trees
		for i in xrange(0,number_of_trees):
			tree = Tree(self, i, tree_width)
			self.trees_list.append(tree)

	
	def run(self):
		self.showStartFrame(self.ground_y)
		self.startGame()

	def startGame(self):
		''' runs the actual game '''

		done = False
		clock = pygame.time.Clock()
	
		self.initTime = dt.datetime.now()

		while self.romu.isAlive() and not done and not self.romu.win(self.win_point):
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					done = True 
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.romu.moveForward()
					if event.key == pygame.K_LEFT:
						self.romu.moveBackwards()
					if event.key == pygame.K_SPACE:
						keys_pressed = pygame.key.get_pressed()
						if keys_pressed[pygame.K_LEFT]:
							self.romu.jumpAndLeft()
						elif keys_pressed[pygame.K_RIGHT]:
							self.romu.jumpAndRight()						
						else:
							self.romu.jump()
						

			keys_pressed = pygame.key.get_pressed()

			if keys_pressed[pygame.K_LEFT]:
				self.romu.moveBackwards()
			if keys_pressed[pygame.K_RIGHT]:
				self.romu.moveForward()

			self.draw()
			
			clock.tick(30)	

		if not self.romu.isAlive():
			self.drawGameOver()

		if self.romu.win(self.win_point):
			self.drawWinGame()
	
	def draw(self):
			''' draws everything for the running game '''

			cat_loc = self.romu.rect.centerx

			visible_x1 = max(0, cat_loc - self.screen.get_size()[0]/2)
			visible_x2 = min(self.path_size, cat_loc + self.screen.get_size()[0]/2)

			# heppens in the end of the path
			# then we should not move the sceen anymore 
			if visible_x2  == self.path_size:				
				visible_x1 = visible_x2 - self.screen.get_size()[0]


			#Clear the screen
			self.screen.fill(WHITE)

			#Draw everything 		
			self.draw_background(self.ground_y, visible_x1)
			self.romu.update()
			seB.romu.draw(self.screen, visible_x1)

			for cactus in self.cactus_list:
				cactus.draw(self.screen, visible_x1)

			self.drawEnd(self.win_point-visible_x1)

			self.romu.displayLives()
			self.displayTime(dt.datetime.now()-self.initTime)
				

			pygame.display.flip()

	def drawWinGameFrame(self):
		''' draws the animation after the user won the game '''

		done  = False
		clock = pygame.time.Clock()
		
		romu_end_right = self.win_point+300
		minou_end_left = self.win_point+300

		minou = Cat(self, False)
		minou.setStepSize(10)
		minou.setLocation([4000-minou.rect.width, self.ground_y])

		offset = 3300
		clock = pygame.time.Clock()
		met = False

		# move romu and minou towards each other
		while not done and not met:
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					done = True 

			self.draw_background(self.screen, self.ground_y)
			

			Blf.romu.moveTo(romu_end_right-self.romu.rect.width)
			minou.moveTo(minou_end_left)

			self.romu.update()
			self.romu.draw(self.screen, offset)

			minou.update()
			minou.draw(self.screen, offset)

			self.drawEnd(self.win_point-offset)

			self.romu.displayLives()
			self.displayTime(dt.datetime.now()-self.initTime)
			
			if self.romu.rect.right == romu_end_right and minou.rect.left == minou_end_left:
				met = True
			pygame.display.flip()

			clock.tick(20)

		# after romu and minou met creat hearts and move them up as bubbles
		# also draw the Valentine's day message
		hearts_list = []
		for i in range(0,15):
			hearts_list.append(Heart(self, [3600, 200, 200, 200]))

		while not done:
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					done = True 

			self.draw_background(self.screen, self.ground_y)
			

			Blf.romu.draw(self.screen, offset)
			minou.draw(self.screen, offset)

			self.drawEnd(self.win_point-offset)

			self.romu.displayLives()
			self.displayTime(dt.datetime.now()-self.initTime)
			


			start_rect = [260, 70, 320, 110]
			pygame.draw.rect(self.screen, WHITE, start_rect)
			pygame.draw.rect(self.screen, RED, start_rect, 4)
		
			font = pygame.font.Font(None, 30)
			text = font.render(unicode("Tu as gagné mon cœur", 'utf-8'), True, RED)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], start_rect[1] + 10])

			text = font.render("Je ne peux pas vivre sans toi", True, RED)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], start_rect[1] + 45])

			text = font.render("Merci pour etre mon Valentine", True, RED)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], start_rect[1] + 80])

			for heart in hearts_list:
				heart.update()
				heart.draw(offset)

			pygame.display.flip()

			clock.tick(10)

	
	
	def drawGameOver(self):
		''' draws a rectangle with the 'Game Over' messgae '''

		x_margin  = 5
		y_margin  = 20
		done  = False
		clock = pygame.time.Clock()
	
		while not done:
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					done = True 

			self.draw_background(self.screen, self.ground_y)

			stBt_rect = [130, 70, 445, 360]
			pygame.draw.rect(self.screen, WHITE, start_rect)
			pygame.draw.rect(self.screen, DARK_ORANGE, start_rect, 2)
			
			font = pygame.font.Font(None, 50)
			text = font.render("Game over :(((", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], start_rect[3]/2-text.get_size()[1]/2 + start_rect[1]])
		
			pygame.display.flip()

			clock.tick(1)

	def drawEnd(self, loc_x):
		''' draws the dimond end sign '''

		pointlist = [[loc_x-100, 200],[loc_x, 100],[loc_x +100, 200], [loc_x, 300]]

		pygame.draw.polygon(self.screen, YELLOW, pointlist)
		pygame.draw.polygon(self.screen, BLACK, pointlist, 3)

		font = pygame.font.Font(None, 60)
		text = font.render("END", True, BLACK)
		self.screen.blit(text, [loc_x - text.get_size()[0]/2, 200 - text.get_size()[1]/2])

		pygame.draw.rect(self.screen, BLACK, [loc_x - 2, 300, 4, 150])
	
	def showStartFrame(self, ground_y):
		''' shows a flash screen in the beginning of the game 
		countdown to start the game or hit 'ENTER' '''

		clock = pygame.time.Clock()

		x_margin  = 5
		y_margin  = 20
		stop = False

		for wait in range(10, 0, -1):

			for event in pygame.event.get(): 
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						stop = True

			if stop:
				break

			self.draw_background(self.screen, self.ground_y)

			stBt_rect = [130, 70, 445, 360]
			pygame.draw.rect(self.screen, WHITE, start_rect)
			pygame.draw.rect(self.screen, DARK_ORANGE, start_rect, 2)
			
			y = start_rect[1]
			font = pygame.font.Font(None, 50)
			text = font.render("Welcome", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], y + y_margin])
			y +=text.get_size()[1]

			font = pygame.font.Font(None, 30)
			text = font.render("the world of the most advantures cat", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], y + y_margin])
			y +=text.get_size()[1]

			font = pygame.font.Font(None, 50)
			text = font.render("Romu", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2+ start_rect[0], y + y_margin])
			y +=text.get_size()[1]

			self.romu.drawAt(self. screen, [start_rect[2]/2 - self.romu.rect.width/2+ start_rect[0], y+y_margin])
			y += self.romu.rect.height

			font = pygame.font.Font(None, 50)
			text = font.render("Game starts in ", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[0] + x_margin, y + y_margin])
			x_offset = text.get_size()[0]

			text = font.render(str(wait), True, DARK_GREEN)
			self.screen.blit(text, [start_rect[0] + x_margin + x_offset, y + y_margin])
			x_offset += text.get_size()[0]

			text = font.render(" seconds", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[0] + x_margin + x_offset, y + y_margin])
			
			pygame.display.flip()

			# one frame per second to correspond to countdown
			clock.tick(1)


	def displayTime(self, time):
			''' on the top info bar displays how much time passed after the game started '''
			x_margin = 5
			font = pygame.font.Font(None, 25)
			text = font.render("Time: " + str(time), True, DARK_ORANGE)
			self.screen.blit(text, [x_margin, x_margin])
		

	def drawBackground(self, ground_y, offset):
		''' draws the background, info bar and the platform on which hero walks '''

		screen_width = self.screen.get_size()[0]
		screen_height  = self.screen.get_size()[1]

		# draw grass
		grass_height = screen_height - self.ground_y 

		x = 0
		y = self.ground_y
		width = screen_width
		height = grass_height
		pygame.draw.rect(self.screen, GRASS_COLOR, [x, y, width, height])

		# draw sky
		x = 0
		y = 0
		width = screen_width
		height = self.ground_y
		pygame.draw.rect(self.screen, SKY_COLOR, [x, y, width, height])

		# draw trees
		for tree in self.trees_list:
			tree.draw(offset)

		# draw info bar
		x = 0
		y = 0
		width = screen_width
		height = 30
		pygame.draw.rect(self.screen, WHITE, [x, y, width, height])


if  __name__ =='__main__':
	pygame.init()
	game = RomuGame()
	game.run()