import pygame 
import os 
import sys 
import random 

pygame.init() 
pygame.font.init()

dimensions = (800, 800)
black = (0, 0, 0)
white = (255, 255, 255)

player = pygame.image.load(os.path.join("data", "spaceship.png"))
bullet = pygame.image.load(os.path.join("data", "bullet.png"))
alien = pygame.image.load(os.path.join("data", "alien.png"))

font = pygame.font.SysFont("monaco", 30)

screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(True)

aliveAliens = []
aliveBullets = []

def renderFonts():
	livesText = font.render(str(Player.lives), True, white)
	killsText = font.render(str(Player.kills), True, white)
	screen.blit(livesText, (10, 0))
	screen.blit(killsText, (10, 40))


def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
    if distance <= 50:
        return True
    else:
        return False

class Alien: 
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

		self.x = randX 
		self.y = randY

		Alien.currentAliens += 1

	def die(self): 
		print(f"killing alien id {id(self)}")
		Alien.currentAliens -= 1
		Player.lives -= 1
		aliveAliens.remove(self)
		del self

	def put(self): 
		screen.blit(alien, (self.x, self.y))

	def step(self): 
		self.y += Alien.speed

	def isOutOfBounds(self): 
		return self.x > 700 or self.x < 100 or self.y > 700 


class Player: 
	speed = 6 
	lives = 3
	kills = 0

	def __init__(self): 
		self.x = 400 
		self.y = 700 

		screen.blit(player, (self.x, self.y))

	def put(self): 
		screen.blit(player, (self.x, self.y))

	def step_right(self): 
		self.x += Player.speed

	def step_left(self): 
		self.x -= Player.speed

_player = Player()

class Bullet: 
	speed = 12 

	def __init__(self, x, y): 
		self.x = x
		self.y = y

	def put(self): 
		screen.blit(bullet, (self.x, self.y))

	def step(self): 
		self.y -= Bullet.speed

	def isOutOfBounds(self): 
		return self.y < 50

	def die(self): 
		print(f"killing bullet id {id(self)}")
		aliveBullets.remove(self)
		del self

def renderBullets(): 
	for _bullet in aliveBullets: 
		_bullet.put() 
		_bullet.step()

		if _bullet.isOutOfBounds(): 
			_bullet.die()


def renderAliens():
	if Alien.currentAliens < Alien.maxAliens: 
		aliveAliens.append(Alien())

	for _alien in aliveAliens: 
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
		sys.exit() 

	_player.put() 

running = True

while running: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				aliveBullets.append(Bullet(_player.x, _player.y))	

	screen.fill(black)

	renderPlayer()
	renderBullets() 
	renderAliens() 
	renderFonts()

	pygame.display.update() 

