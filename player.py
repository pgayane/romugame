import colors
import pygame

class Player:
	score = 0

	def displayScore(self, screen):
		margin = 5
		font = pygame.font.Font(None, 25)
		text = font.render("Score: " + str(self.score), True, colors.DARK_ORANGE)
		screen.blit(text, [screen.get_size()[0]-text.get_size()[0]-margin, margin])
