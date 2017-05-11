import pygame
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
begin = False

clock = pygame.time.Clock()

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
		self.accX = forceX / self.mass
		self.accY = forceY / self.mass

		self.velX += self.accX
		self.posX += self.velX

		self.velY += self.accY
		self.posY += self.velY

	def calcAngle(self, obj):
		diffX = self.posX - obj.posX
		diffY = self.posY - obj.posY
		if self.
		return math.atan(diffY/diffX)

	def calcGrav(self, obj):
		distance = math.sqrt((self.posX - obj.posX)**2 + (self.posY - obj.posY)**2)
		return GRAV_CONST * (self.mass * obj.mass) / (distance**2)

	def calcHandle(self, obj):
		angle = self.calcAngle(obj)
		force = self.calcGrav(obj)
		x.calcNewPos(force*math.cos(angle), force*math.sin(angle))

	def drawObj(self):
		pygame.draw.circle(screen, BLACK, [int(self.posX), int(self.posY)], self.mass)

# Create
objects = [Object(10, 100, 100), Object(10, 10, 10)]
print objects[0].mass

# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Logic goes here
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_SPACE]:
		begin = True

	if begin:
		print "hello"
	
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
