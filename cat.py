import pygame
from colors import *
import time

class Cat(pygame.sprite.Sprite):
	
	ROMU_PATH = "resources/romu.png"
	MINOU_PATH = "resources/minou.png"

	def __init__(self, game, pic_path, loc):
		pygame.sprite.Sprite.__init__(self) 
		
		self.cat_pic = pygame.image.load(pic_path).convert()
		self.cat_pic.set_colorkey(WHITE)

		self.rect = self.cat_pic.get_rect()
		self.rect.bottomleft = loc
		self.rect.y +=20

		self.game = game
		self.step_size = 10

		self.change_y = 0
		self.change_x = 0

		self.lives = 7
		self.injury_timestamp = None

	def set_location(self, loc):
		self.rect.bottomleft = loc
		self.change_x = 0
	
	def moveTo(self, loc_x):
		''' gradually move to specified location'''
		if loc_x > self.rect.x:
			self.change_x = min(loc_x-self.rect.x, self.step_size/2)
		else:
			self.change_x = -min(self.rect.x-loc_x, self.step_size/2)
	
 	def moveForward(self):
		self.change_x = self.step_size
			
	def moveBackwards(self):
		self.change_x = -self.step_size

	def drawAt(self, screen, loc):
		screen.blit(self.cat_pic, loc)

	def draw(self, screen, offset):
		screen.blit(self.cat_pic, [self.rect.left-offset, self.rect.top])

	def getSize(self):
		return self.cat_pic.get_size()

	def win(self, winPoint):
		''' if the cat reach or passed the end sign then win '''
		if self.rect.right > winPoint and self.rect.bottom == self.game.ground_y+20:
			return True
		return False

	def calc_grav(self):
		''' calculates the vertical change of the object during the jump '''
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += 1

		# See if we are on the ground.
		if self.rect.bottom >= self.game.ground_y +20and self.change_y >= 0:
			self.change_y = 0
			self.rect.bottom = self.game.ground_y+20
			
	def is_jumping(self):
		return self.rect.bottom < self.game.ground_y +20

	def stop(self):
		self.change_x = 0

	def key_presses(self, keys_pressed):
		
		if not self.is_jumping():
			if keys_pressed[pygame.K_RIGHT]:
				self.moveForward()
			elif keys_pressed[pygame.K_LEFT]:
				self.moveBackwards()
			else:
				self.stop()

			if keys_pressed[pygame.K_SPACE]:
				self.jump()
			
		
	def jump(self):
		''' if not currently in jump then jump '''
		self.change_y = -15

	def get_direction(self):
		if self.change_x < 0:
			return 'L'
		elif self.change_x > 0:
			return 'R'

	def display_lives(self):
		''' on the info bar displays how many lives are left '''
		margin = 5
	
		font = pygame.font.Font(None, 30)
		text = font.render(str(self.lives) , True, DARK_GREEN)
		self.game.screen.blit(text, [self.game.screen.get_size()[0]-text.get_size()[0]-margin, margin])
		x = text.get_size()[0]

		text = font.render("Cat lives: " , True, DARK_ORANGE)
		self.game.screen.blit(text, [self.game.screen.get_size()[0]-text.get_size()[0]-x-margin, margin])
		
	def is_alive(self):
		return self.lives>0

	def meow(self):
		bump_sound = pygame.mixer.Sound("resources/meow1.wav")
		bump_sound.play()			

	def handle_sidewise_jump(self):
		# dont move left or right if in jump
		if self.change_y != 0:
			if self.get_direction() == 'R':
				self.change_x = self.step_size
			elif self.get_direction() == 'L':
				self.change_x = -self.step_size

	def check_collision_with_cactus(self):
		cactus_hit_list = pygame.sprite.spritecollide(self, self.game.cactus_list, False)

		if len(cactus_hit_list) > 0 :
			if self.injury_timestamp == None or time.time() - self.injury_timestamp > 1:
				self.meow()
				self.lives -=1
				self.injury_timestamp = time.time()

		# if collision ocurred move the cat before the cactus
		for cactus in cactus_hit_list:
			if self.change_x > 0:
				self.rect.right = cactus.rect.left
			elif self.change_x < 0:
			# Otherwise if we are moving left, do the opposite.
				self.rect.left = cactus.rect.right

	def check_offscreen(self):
		if self.rect.x + self.change_x < 0 or self.rect.right + self.change_x >= self.game.path_size:
			self.moew()		
		else:
			self.rect.x += self.change_x

	def update(self):
		''' updates location of the objected based on the vertical and horizontal chnage taking into account collisons '''

		# Gravity
		self.calc_grav()
	
		# Move left/right during a jump
		self.handle_sidewise_jump()

		
		# checks the collision only based on the x, because there are no obsticles located vertically to cat
		self.check_offscreen()
		self.check_collision_with_cactus()
		
		# Move up/down
		self.rect.y += self.change_y

			