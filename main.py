import pygame 
from os import path 
from sys import exit
from random import randint
from time import time

pygame.init() 
pygame.font.init()
pygame.mixer.init() 

dimensions = (800, 800)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

landing = True
paused = False
mute = False
isReloading = False
isShooting = False 
reloadStartTime, reloadEndTime = 0, 0
shootStartTime, shootEndTime = 0, 0

clock = pygame.time.Clock()

font = pygame.font.SysFont("monaco", 30)
bulletSound = pygame.mixer.Sound(path.join("data", "bullet.wav"))
hitSound = pygame.mixer.Sound(path.join("data", "explosion.wav"))
bgSound = path.join("data", "background.wav")

screen = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Space Invaders")
pygame.mouse.set_visible(True)

aliens = pygame.sprite.Group() 
bullets = pygame.sprite.Group() 

class Button(): 
	def __init__(self, dim, pos, func): 
		self.dim = dim
		self.pos = pos
		self.rect = pygame.Rect(self.pos, self.dim)
		self.isVisible = False
		self.func = func

	def addText(self, text, color=white): 
		self.string = text
		self.text = font.render(str(text), True, color)

	def setVisibility(self, cond): 
		self.isVisible = cond

	def draw(self, color=white, thick=3):
		pygame.draw.rect(screen, color, self.rect, thick)
		screen.blit(self.text, self.pos)

	def isMouseTouching(self): 
		mousePos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePos):

	def action(self): 
		self.func()

	def __str__(self): 
		return self.string + " button"

buttons = []

def toggleMute(): 
	global mute
	mute = not mute

def switchToGame(): 
	global landing
	landing = False

muteButton = Button((100, 100), (300, 300), toggleMute)
muteButton.addText("Mute")

playButton = Button((100, 100), (300, 300), switchToGame)
playButton.addText("Play")

buttons.append(muteButton)
buttons.append(playButton)

class Alien(pygame.sprite.Sprite): 
	minX = 100
	maxX = 700
	minY = 0 
	maxY = 300
	speed = 3
	maxAliens = 5
	currentAliens = 0

	def __init__(self): 
		randX = randint(Alien.minX, Alien.maxX)
		randY = randint(Alien.minY, Alien.maxY)

		self.image = pygame.image.load(path.join("data", "alien.png"))
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
		#pygame.draw.rect(screen, red, self.rect, 5)
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
	lives = 30
	kills = 0

	def __init__(self): 
		self.image = pygame.image.load(path.join("data", "spaceship.png"))
		self.rect = self.image.get_rect()
		self.rect.x = 400 
		self.rect.y = 700 
		self.put() 

		super(Player, self).__init__()

	def put(self): 
		#pygame.draw.rect(screen, (255, 0, 0), self.rect, 5)
		screen.blit(self.image, self.rect)

	def step_right(self): 
		self.rect.x += Player.speed

	def step_left(self): 
		self.rect.x -= Player.speed

_player = Player()

class Bullet(pygame.sprite.Sprite): 
	speed = 12
	ammo = 15
	maxAmmo = 15
	reloadSeconds = 3
	timeBetweenShots = 0.5

	def __init__(self): 
		self.image = pygame.image.load(path.join("data", "bullet.png"))
		self.rect = self.image.get_rect()
		self.rect.x = _player.rect.x
		self.rect.y = _player.rect.y
		self.bottom_right = self.rect.bottomright

		pygame.mixer.Channel(1).play(bulletSound)	

		super(Bullet, self).__init__()
		bullets.add(self)

	def put(self): 
		#pygame.draw.rect(screen, (255, 0, 0), self.rect, 5)
		screen.blit(self.image, self.rect)

	def step(self): 
		self.rect.y -= Bullet.speed

	def isOutOfBounds(self): 
		return self.rect.y < 50

	def die(self): 
		bullets.remove(self)
		del self

def renderStats():
	livesText = font.render(str(Player.lives), True, white)
	killsText = font.render(str(Player.kills), True, white)
	ammoText = font.render(f"{Bullet.ammo} / {Bullet.maxAmmo}", True, white)
	screen.blit(livesText, (10, 0))
	screen.blit(killsText, (10, 40))
	screen.blit(ammoText, (10, 80))

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
					pygame.mixer.Channel(0).play(hitSound)

def renderLanding(): 
	title = font.render("Space Invaders", True, white)
	screen.blit(title, (400, 200))
	playButton.setVisibility(True)

def play(): 
	muteButton.setVisibility(False)
	playButton.setVisibility(False)
	renderPlayer()
	renderBullets() 
	renderAliens() 
	renderStats()
	checkColl()

def pause():
	pauseText = font.render("Press r to resume", True, white)
	pauseTextRect = pauseText.get_rect(center=(400, 400))
	muteButton.setVisibility(True)
	screen.blit(pauseText, pauseTextRect)

def quit(): 
	exit() 
	pygame.quit()

def canShoot(): 
	return not paused and not isReloading and not isShooting and Bullet.ammo > 0

pygame.mixer.music.load(bgSound)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			quit() 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if canShoot():
					isShooting = True
					Bullet.ammo -= 1
					bullet = Bullet()
			elif event.key == pygame.K_p: 
				paused = True
			elif event.key == pygame.K_r: 
				paused = False
			elif event.key == pygame.K_q: 
				isReloading = True

	if isReloading:
		if reloadStartTime == 0: 
			reloadStartTime = time()
		else: 
			reloadEndTime = time() 
		if reloadEndTime - reloadStartTime >= Bullet.reloadSeconds: 
			Bullet.ammo = Bullet.maxAmmo
			reloadStartTime, reloadEndTime = 0, 0
			isReloading = False 

	if isShooting:
		if shootStartTime == 0: 
			shootStartTime = time()
		else: 
			shootEndTime = time() 
		if shootEndTime - shootStartTime >= Bullet.timeBetweenShots: 
			shootStartTime, shootEndTime = 0, 0
			isShooting = False

	screen.fill(black)

	if not paused:
		if landing: 
			renderLanding() 
		else: 
			play()
	else:
		pause()

	for button in buttons:
		if button.isVisible: 	
			button.draw()
			if button.isMouseTouching(): 
				button.action()

	if mute:
		pygame.mixer.music.set_volume(0.0) 
	else:
		pygame.mixer.music.set_volume(0.4)

	clock.tick(120)
	pygame.display.update() 

