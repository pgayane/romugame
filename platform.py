class Platform(pygame.sprite.Sprite):
	def __init__(self, sprite_sheet_data ):
	""" Platform constructor. Assumes constructed with user passing in
	an array of 5 numbers like what's defined at the top of this code. """
		pygame.sprite.Sprite.__init__(self)
		sprite_sheet = SpriteSheet("tiles_spritesheet.png")
		# Grab the image for this platform
		self.image = sprite_sheet.getImage(sprite_sheet_data[0],
		sprite_sheet_data[1],
		sprite_sheet_data[2],
		sprite_sheet_data[3])
		self.rect = self.image.get_rect()