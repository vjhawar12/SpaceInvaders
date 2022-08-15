import pygame 
import os 
import sys 
import random 

pygame.init() 
pygame.font.init()

dimensions = (800, 800)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

font = pygame.font.SysFont("monaco", 30)

screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(True)

aliens = pygame.sprite.Group() 
bullets = pygame.sprite.Group() 

def quit(): 
	sys.exit() 
	pygame.quit()

def renderFonts():
	livesText = font.render(str(Player.lives), True, white)
	killsText = font.render(str(Player.kills), True, white)
	screen.blit(livesText, (10, 0))
	screen.blit(killsText, (10, 40))

class Alien(pygame.sprite.Sprite): 
	minX = 100
	maxX = 700
	minY = 0 
	maxY = 300
	speed = 3
	maxAliens = 5
	currentAliens = 0

	def __init__(self): 
		randX = random.randint(Alien.minX, Alien.maxX)
		randY = random.randint(Alien.minY, Alien.maxY)

		self.image = pygame.image.load(os.path.join("data", "alien.png"))
		self.rect = self.image.get_rect()
		self.rect.x = randX 
		self.rect.y = randY

		Alien.currentAliens += 1

		super(Alien, self).__init__()
		aliens.add(self)

	def die(self): 
		Alien.currentAliens -= 1
		aliens.remove(self)
		del self

	def put(self): 
		pygame.draw.rect(screen, red, self.rect, 5)
		screen.blit(self.image, self.rect)

	def step(self): 
		self.rect.y += Alien.speed

	def isOutOfBounds(self): 
		if self.rect.x > 700 or self.rect.x < 100 or self.rect.y > 700:
			Player.lives -= 1
			return True
		return False


class Player(pygame.sprite.Sprite): 
	speed = 6 
	lives = 3
	kills = 0

	def __init__(self): 
		self.image = pygame.image.load(os.path.join("data", "spaceship.png"))
		self.rect = self.image.get_rect()
		self.rect.x = 400 
		self.rect.y = 700 
		self.put() 

		super(Player, self).__init__()

	def put(self): 
		pygame.draw.rect(screen, (255, 0, 0), self.rect, 5)
		screen.blit(self.image, self.rect)

	def step_right(self): 
		self.rect.x += Player.speed

	def step_left(self): 
		self.rect.x -= Player.speed

_player = Player()

class Bullet(pygame.sprite.Sprite): 
	speed = 12 

	def __init__(self): 
		self.image = pygame.image.load(os.path.join("data", "bullet.png"))
		self.rect = self.image.get_rect()
		self.rect.x = _player.rect.x
		self.rect.y = _player.rect.y
		self.bottom_right = self.rect.bottomright

		super(Bullet, self).__init__()
		bullets.add(self)

	def put(self): 
		pygame.draw.rect(screen, (255, 0, 0), self.rect, 5)
		screen.blit(self.image, self.rect)

	def step(self): 
		self.rect.y -= Bullet.speed

	def isOutOfBounds(self): 
		return self.rect.y < 50

	def die(self): 
		bullets.remove(self)
		del self

def renderBullets(): 
	for _bullet in bullets.sprites(): 
		_bullet.put() 
		_bullet.step()

		if _bullet.isOutOfBounds(): 
			_bullet.die()
		

def renderAliens():
	if Alien.currentAliens < Alien.maxAliens: 
		alien = Alien()

	for _alien in aliens.sprites(): 
		_alien.put() 
		_alien.step()

		if _alien.isOutOfBounds(): 
			_alien.die()


def renderPlayer(): 
	keys = pygame.key.get_pressed() 
	if keys[pygame.K_RIGHT]: 
		_player.step_right()
	elif keys[pygame.K_LEFT]: 
		_player.step_left()

	if Player.lives <= 0: 
		quit() 

	_player.put() 


def checkColl(): 
	for _alien in aliens.sprites(): 
		for _bullet in bullets.sprites(): 
			if _alien.rect.colliderect(_bullet.rect): 
				if _bullet.rect.top - _alien.rect.bottom < 30: 
					_alien.die()
					_bullet.die()
					Player.kills += 1

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			quit() 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bullet = Bullet()

	screen.fill(black)

	renderPlayer()
	renderBullets() 
	renderAliens() 
	renderFonts()

	checkColl()

	pygame.display.update() 

