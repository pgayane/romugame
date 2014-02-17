import pygame
from colors import *
import time

class Cat(pygame.sprite.Sprite):

	game = None
	rect = [0,0,0,0]

	stepSize = 1
	direction = 'R'
	change_y = 0
	change_x = 0

	lives = 7
	injury_timestamp = None

	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self) 

		self.cat_pic = pygame.image.load("resources/romu.png").convert()
		self.cat_pic.set_colorkey(WHITE)

		self.rect = self.cat_pic.get_rect()
		self.game = game

		#print self.cat_pic.get_size()

 	def setLocation(self, newLoc):
		self.rect.bottomleft = newLoc
		self.rect.y +=20

	def setStepSize(self, s):
		self.stepSize = s

	def moveForward(self):
		if self.change_y == 0:
			self.change_x = self.stepSize
			
	def moveBackwards(self):
		if self.change_y == 0:
			self.change_x = -self.stepSize

	def drawAt(self, screen, loc):
		screen.blit(self.cat_pic, loc)

	def draw(self, screen, offset):
		screen.blit(self.cat_pic, [self.rect.left-offset, self.rect.top])
		#pygame.draw.rect(screen, RED, [self.rect.left-offset, self.rect.y, self.rect.width, self.rect.height], 1)

		font = pygame.font.Font(None, 25)
		text = font.render(str(self.rect.right), True, DARK_ORANGE)
		screen.blit(text, [200, 5])

	def getSize(self):
		return self.cat_pic.get_size()

	def win(self, winPoint):
		if self.rect.right > winPoint and self.change_y == 0:
			return True
		return False

	def calc_grav(self):
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += 1

		# See if we are on the ground.
		if self.rect.bottom >= self.game.ground_y +20and self.change_y >= 0:
			self.change_y = 0
			self.rect.bottom = self.game.ground_y+20
			

	def jump(self):
		if self.change_y == 0:
			self.direction = ''
			self.change_y = -15

	def jumpAndLeft(self):
		if self.change_y == 0:
			self.direction = 'L'
			self.change_y = -15

	def jumpAndRight(self):
		if self.change_y == 0:
			self.direction = 'R'
			self.change_y = -15

	def displayLives(self):
		
		margin = 5
	
		font = pygame.font.Font(None, 30)
		text = font.render(str(self.lives) , True, DARK_GREEN)
		self.game.screen.blit(text, [self.game.screen.get_size()[0]-text.get_size()[0]-margin, margin])
		x = text.get_size()[0]

		text = font.render("Cat lives: " , True, DARK_ORANGE)
		self.game.screen.blit(text, [self.game.screen.get_size()[0]-text.get_size()[0]-x-margin, margin])
		
	def isAlive(self):
		return self.lives>0

	def update(self):
		# Gravity
		self.calc_grav()
	
		# Move left/right

		# dont move left or right if in jump
		if self.change_y != 0:
			if self.direction == 'R':
				self.change_x = self.stepSize
			elif self.direction == 'L':
				self.change_x = -self.stepSize

		if self.rect.x + self.change_x < 0 or self.rect.right + self.change_x >= self.game.path_size:
			bump_sound = pygame.mixer.Sound("resources/bump.wav")
			bump_sound.play()			
		else:

			self.rect.x += self.change_x
			cactus_hit_list = pygame.sprite.spritecollide(self, self.game.cactus_list, False)

			if len(cactus_hit_list) > 0 :
				bump_sound = pygame.mixer.Sound("resources/bump.wav")
				bump_sound.play()

				if self.injury_timestamp == None or time.time() - self.injury_timestamp > 1:
					self.lives -=1
					self.injury_timestamp = time.time()


			for cactus in cactus_hit_list:
				if self.change_x > 0:
					self.rect.right = cactus.rect.left
				elif self.change_x < 0:
				# Otherwise if we are moving left, do the opposite.
					self.rect.left = cactus.rect.right
		self.change_x = 0

		# Move up/down
		self.rect.y += self.change_y

			