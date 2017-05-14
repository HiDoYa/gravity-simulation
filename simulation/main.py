import pygame
import random
import math
import sys

# Basic colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize for program
pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gravity Simulation - Hiroya")

clock = pygame.time.Clock()
random.seed()

# Flags
done = False
restart = False

# Constant
GRAV_CONST = 6.67408 * (10 ** (-11))

def string_is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

draw_path = False
draw_color = False
number_of_objects = 20

if len(sys.argv) > 1:
    for i in sys.argv:
        if i == "PATH":
            draw_path = True
        if i == "COLOR":
            draw_color = True
        if string_is_int(i):
            number_of_objects = int(i)
            

# class object
class Object:
	def __init__ (self, mass, position_x, position_y, color):
                # Initialize mass and position 
		self.mass = mass
                self.merged = False
                
                self.color = color

		self.position_x = position_x
		self.position_y = position_y

		self.acceleration_x = 0
		self.acceleration_y = 0

		self.velocity_x = 0
		self.velocity_y = 0

        def calculate_radius(self):
                # Radius is dependent on mass
                # Assumes one unit of mass (1 * 10^11 kg) is equal to one m^2
                self.radius = math.sqrt((self.mass / 10 ** 11) / math.pi)

	def calculate_new_position(self):
		# Velocity is change in position
		self.position_x += self.velocity_x
		self.position_y += self.velocity_y

	def calculate_new_velocity(self, obj):
                # Find angle and force in x and y
                angle = self.calculate_angle(obj)
                force = self.calculate_force(obj)
                force_x = force * math.cos(angle)
                force_y = force * math.sin(angle)

                # Newton's second law
                self.acceleration_x = force_x / self.mass
                self.acceleration_y = force_y / self.mass

                # Acceleration is change in velocity
                self.velocity_x += self.acceleration_x
                self.velocity_y += self.acceleration_y

	def calculate_angle(self, obj):
                # Use trig to get angle between two objects
		diff_x = obj.position_x - self.position_x
		diff_y = obj.position_y - self.position_y

		if diff_x != 0:
			angle = math.atan(diff_y / diff_x)
		else:
			angle = 0

		if diff_x < 0:
			angle += math.pi

		return angle

	def calculate_force(self, obj):
		# Equation for gravity (using big G)
		distance = math.sqrt((self.position_x - obj.position_x)**2 + (self.position_y - obj.position_y)**2)
		return GRAV_CONST * (self.mass * obj.mass)/ (distance**2)

	def collision(self, obj):
                # Gets distance beteween two objects
                difference_x = self.position_x - obj.position_x
                difference_y = self.position_y - obj.position_y
                position = math.sqrt(difference_x ** 2 + difference_y ** 2)

                # If the distance between the two is less than the two object's radii, they collided
                if position <= (self.radius + obj.radius):
                    momentum_x = self.mass * self.velocity_x + obj.mass + obj.velocity_x
                    momentum_y = self.mass * self.velocity_y + obj.mass + obj.velocity_y

                    # Merges to the larger mass
                    if self.mass > obj.mass:
                        self.mass += obj.mass
                        # Using conservation of momentum and assumes perfectly inelastic collision
                        self.velocity_x = momentum_x / self.mass
                        self.velocity_y = momentum_y / self.mass
                        # Merged objects disappear
                        obj.merged = True
                        # Recalculates radius based on new mass
                        self.calculate_radius()
                    else:
                        obj.mass += self.mass
                        obj.velocity_x = momentum_x / obj.mass
                        obj.velocity_y = momentum_y / obj.mass
                        self.merged = True
                        obj.calculate_radius()


	def draw_object(self):
		pygame.draw.circle(screen, self.color, [int(self.position_x), int(self.position_y)], int(self.radius))

# Create objects
objects = []

def init_objects():
	for i in range(number_of_objects):
                mass = random.randint(50 * (10 ** 11), 50 * (10 ** 11))

                position_x = random.randint(0, size[0])
                position_y = random.randint(0, size[1])

                if draw_color:
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                else:
                    color = WHITE

		objects.append(Object(mass, position_x, position_y, color))

                objects[i].calculate_radius()

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
		if not pressed[pygame.K_SPACE]:
			restart = False


        for x in objects:
            x.calculate_new_position()

        for x in objects:
            for y in objects:
                if x != y and not x.merged and not y.merged:
                    x.collision(y)

        for x in objects:
            for y in objects:
                if x != y and not x.merged and not y.merged:
                    x.calculate_new_velocity(y)

	# Fill screen
        if not draw_path:
            screen.fill(BLACK)

	# Draw
	for i in objects:
            if not i.merged:
		i.draw_object()

	noMove = False

	# Updates
	pygame.display.flip()

	# 60 FPS
	clock.tick(60)
	
pygame.quit()
