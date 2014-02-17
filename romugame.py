import pygame
from cat import Cat
from player import Player
from colors import * 
import datetime as dt
from cactus import Cactus

class RomuGame:

	screen_size = (700, 500)
	path_size = 4000
	ground_y = screen_size[1] * 0.9
	score = 0

	cactus_list = []

	romu  = None
	initTime = None
	screen = None
	win_point = 3700

	def __init__(self):
		self.screen = pygame.display.set_mode(self.screen_size)
	
		self.romu = Cat(self)		
		self.romu.setStepSize(10)
		self.romu.setLocation([0, self.ground_y])
	
		for i in range(1,8):
			cactus = Cactus(self)
			cactus.setLocation([500*i, self.ground_y])
			self.cactus_list.append(cactus)

	
	def run(self):
	
	
		done = False
		clock = pygame.time.Clock()
	
		#self.displayStartFrame(self.ground_y, clock)
		
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
			print "won the game"
		pygame.quit()

	def draw(self):
			
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
			self.romu.draw(self.screen, visible_x1)

			for cactus in self.cactus_list:
				cactus.draw(self.screen, visible_x1)

			self.romu.displayLives()
			self.displayTime(dt.datetime.now()-self.initTime)
			
			self.drawEnd(self.win_point-visible_x1)

			pygame.display.flip()

	def drawGameOver(self):
		x_margin  = 5
		y_margin  = 20
		done  = False
		clock = pygame.time.Clock()
	

		while not done:
			for event in pygame.event.get(): 
				if event.type == pygame.QUIT: 
					done = True 

			self.draw_background(self.screen, self.ground_y)

			start_rect = [130, 70, 445, 360]
			pygame.draw.rect(self.screen, WHITE, start_rect)
			pygame.draw.rect(self.screen, DARK_ORANGE, start_rect, 2)
			
			font = pygame.font.Font(None, 50)
			text = font.render("Game over :(((", True, DARK_ORANGE)
			self.screen.blit(text, [start_rect[2]/2-text.get_size()[0]/2 + start_rect[0], start_rect[3]/2-text.get_size()[1]/2 + start_rect[1]])
		
			pygame.display.flip()

			clock.tick(1)

	def drawEnd(self, loc_x):
		pointlist = [[loc_x-100, 200],[loc_x, 100],[loc_x +100, 200], [loc_x, 300]]

		pygame.draw.polygon(self.screen, YELLOW, pointlist)
		pygame.draw.polygon(self.screen, BLACK, pointlist, 3)

		font = pygame.font.Font(None, 60)
		text = font.render("END", True, BLACK)
		self.screen.blit(text, [loc_x - text.get_size()[0]/2, 200 - text.get_size()[1]/2])

		pygame.draw.rect(self.screen, BLACK, [loc_x - 2, 300, 4, 150])
	
	def displayStartFrame(self, ground_y, clock):
		x_margin  = 5
		y_margin  = 20
		for wait in range(10, 0, -1):
			self.draw_background(self.screen, self.ground_y)

			start_rect = [130, 70, 445, 360]
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

			clock.tick(1)


	def displayTime(self, time):
			x_margin = 5
			font = pygame.font.Font(None, 25)
			text = font.render("Time: " + str(time), True, DARK_ORANGE)
			self.screen.blit(text, [x_margin, x_margin])
		

	def draw_background(self, ground_y, offset):
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
		number_of_trees = 24	
		tree_root_height = self.ground_y/3
		root_width = 20 
		

		for i in xrange(0,number_of_trees):
			# tree root
			x = i*self.path_size/number_of_trees + (self.path_size/number_of_trees)/2 - root_width/2 - offset
			y = self.ground_y - tree_root_height - 5
			width = root_width
			height = tree_root_height +5
			if x+width> 0 and x <=screen_width:
				pygame.draw.rect(self.screen, TREE_ROOT, [x, y, width, height])
			
			# tree leaves
			leaves_width = self.path_size/number_of_trees - 30
			x = i*self.path_size/number_of_trees + (self.path_size/number_of_trees)/2  - leaves_width/2 - offset
			y = 0
			width = leaves_width
			height = self.ground_y - tree_root_height
			if x+width>0  and x <=screen_width:
				pygame.draw.ellipse(self.screen, DARK_GREEN, [x, y, width, height])
		
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