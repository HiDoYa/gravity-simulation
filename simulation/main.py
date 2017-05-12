import pygame
import random
import math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize for program
pygame.init()
pygame.font.init()
size = (960, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test")
done = False

clock = pygame.time.Clock()
random.seed()

# Constants
# GRAV_CONST = 6.67408 * (10 ** (-11))
GRAV_CONST = 6.67408 * (10 ** (1))

# class
class Object:
	def __init__ (self, mass, posX, posY):
		self.mass = mass

		self.posX = posX
		self.posY = posY

		self.accX = 0
		self.accY = 0

		self.velX = 0
		self.velY = 0 

	def calcNewPos(self, forceX, forceY):
		# F = ma -> a = F / m
		self.accX = forceX / self.mass
		self.accY = forceY / self.mass

		# Acceleration is change in velocity
		self.velX += self.accX
		self.velY += self.accY

		# Velocity is change in displacement
		self.posX += self.velX
		self.posY += self.velY

	def calcAngle(self, obj):
		diffX = obj.posX - self.posX
		diffY = obj.posY - self.posY

		angle = math.atan(diffY/diffX)

		if diffX < 0:
			angle += math.pi

		return angle

	def calcGrav(self, obj):
		# F = G * (m1 * m2 / r^2)
		distance = math.sqrt((self.posX - obj.posX)**2 + (self.posY - obj.posY)**2)
		return GRAV_CONST * (self.mass * obj.mass) / (distance**2)

	def calcHandle(self, obj):
		angle = self.calcAngle(obj)
		force = self.calcGrav(obj)
		if self.collision(obj):
			self.velX = 0
			self.velY = 0
			force = 0
		x.calcNewPos(force * math.cos(angle), force * math.sin(angle))

	def collision(self, obj):
		selfRight = self.posX + self.mass
		selfLeft = self.posX - self.mass
		selfBot = self.posY + self.mass
		selfTop = self.posY - self.mass

		objRight = obj.posX + obj.mass
		objLeft = obj.posX - obj.mass
		objBot = obj.posY + obj.mass
		objTop = obj.posY - obj.mass

		if selfRight > objLeft and selfBot > objTop and selfLeft < objRight and selfTop < objBot:
			return True
		if selfRight < objLeft and selfBot > objTop and selfLeft > objRight and selfTop < objBot:
			return True
		if selfRight > objLeft and selfBot < objTop and selfLeft < objRight and selfTop > objBot:
			return True
		if selfRight < objLeft and selfBot < objTop and selfLeft > objRight and selfTop > objBot:
			return True
		return False

	def drawObj(self):
		pygame.draw.circle(screen, BLACK, [int(self.posX), int(self.posY)], self.mass)

# Create objects
objects = []

def init_objects():
	for i in range(random.randint(3, 10)):
		objects.append(Object(random.randint(8, 13), random.randint(10, 900), random.randint(10, 720)))

init_objects()

# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Logic goes here
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_SPACE]:
		del objects[:]
		init_objects()


	for x in objects:
		for y in objects:
			if  x != y:
				x.calcHandle(y)

	# Fill screen
	screen.fill(WHITE)

	# Draw
	for i in objects:
		i.drawObj()

	noMove = False

	# Updates
	pygame.display.flip()

	# 60 FPS
	clock.tick(60)
	
pygame.quit()
