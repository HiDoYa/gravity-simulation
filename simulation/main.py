import pygame
import random
import math

# Basic colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize for program
pygame.init()
pygame.font.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test")
done = False
restart = False

clock = pygame.time.Clock()
random.seed()

# Constants
#GRAV_CONST = 6.67408 * (10 ** (-11))
GRAV_CONST = 6.67408 * (10 ** (1))

# class
class Object:
	def __init__ (self, mass, displacement_x, displacement_y):
		self.mass = mass

		self.displacement_x = displacement_x
		self.displacement_y = displacement_y

		self.acceleration_x = 0
		self.acceleration_y = 0

		self.velocity_x = 0
		self.velocity_y = 0 

	def calculate_new_displacement(self):
		# Velocity is change in displacement
		self.displacement_x += self.velocity_x
		self.displacement_y += self.velocity_y

	def calculate_new_velocity(self, obj):
		# Find angle and force in x and y
		angle = self.calculate_angle(obj)
		force = self.calculate_force(obj)
		force_x = force * math.cos(angle)
		force_y = force * math.sin(angle)

		# F = ma -> a = F / m
		self.acceleration_x = force_x / self.mass
		self.acceleration_y = force_y / self.mass

		# Acceleration is change in velocity
		self.velocity_x += self.acceleration_x
		self.velocity_y += self.acceleration_y

	def calculate_angle(self, obj):
		diff_x = obj.displacement_x - self.displacement_x
		diff_y = obj.displacement_y - self.displacement_y

		if diff_x != 0:
			angle = math.atan(diff_y / diff_x)
		else:
			angle = 0

		if diff_x < 0:
			angle += math.pi

		return angle

	def calculate_force(self, obj):
		# F = G * (m1 * m2 / r^2)
		distance = math.sqrt((self.displacement_x - obj.displacement_x)**2 + (self.displacement_y - obj.displacement_y)**2)
		return GRAV_CONST * (self.mass * obj.mass)/ (distance**2)

	def collision_check(self, obj):
		if self.collision(obj):
			# P = MV
			init_momentum_x = self.velocity_x * self.mass + obj.velocity_x * obj.mass
			init_momentum_y = self.velocity_y * self.mass + obj.velocity_y * obj.mass

			self.velocity_x = ((self.mass - obj.mass) * self.velocity_x)/(self.mass + obj.mass)
			self.velocity_y = ((self.mass - obj.mass) * self.velocity_y)/(self.mass + obj.mass)

	def collision(self, obj):
		self_right = self.displacement_x + self.mass
		self_left = self.displacement_x - self.mass
		self_bot = self.displacement_y + self.mass
		self_top = self.displacement_y - self.mass

		obj_right = obj.displacement_x + obj.mass
		obj_left = obj.displacement_x - obj.mass
		obj_bot = obj.displacement_y + obj.mass
		obj_top = obj.displacement_y - obj.mass

		if self_right > obj_left and self_bot > obj_top and self_left < obj_right and self_top < obj_bot:
			return True
		if self_right < obj_left and self_bot > obj_top and self_left > obj_right and self_top < obj_bot:
			return True
		if self_right > obj_left and self_bot < obj_top and self_left < obj_right and self_top > obj_bot:
			return True
		if self_right < obj_left and self_bot < obj_top and self_left > obj_right and self_top > obj_bot:
			return True
		return False

	def draw_object(self):
		pygame.draw.circle(screen, WHITE, [int(self.displacement_x), int(self.displacement_y)], self.mass)

# Create objects
objects = []

def init_objects():
	for i in range(random.randint(3, 10)):
		objects.append(Object(random.randint(8, 13), random.randint(0, size[0]), random.randint(0, size[1])))

init_objects()

# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Logic goes here
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_SPACE]:
		restart = True

	if restart:
		del objects[:]
		init_objects()
		if not pressed[pyGame.K_SPACE]:
			restart = False



	for i in range(3):
		for x in objects:
			if i == 2:
				# Calculate new position wtih velocities
				x.calculate_new_displacement()
			else:
				for y in objects:
					if  x != y:
						if i == 0:
							# Calculate  velocities for collisions
							x.collision_check(y)
						if i == 1:
							# Calculate new velocities for acceleration and force
							x.calculate_new_velocity(y)

	# Fill screen
	screen.fill(BLACK)

	# Draw
	for i in objects:
		i.draw_object()

	noMove = False

	# Updates
	pygame.display.flip()

	# 60 FPS
	clock.tick(60)
	
pygame.quit()
