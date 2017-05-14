import math
import pygame
import random
import sys

# Background Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (156, 43, 43)

# Initialize for program
pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gravity Simulation - Hiroya")

# Font and text
pygame.font.init()
text_font = pygame.font.SysFont('Times New Roman', 20)
text_space = text_font.render("Space to Restart", False, WHITE)
text_z = text_font.render("Z for Path", False, WHITE)
text_x = text_font.render("X for Border", False, WHITE)
text_c = text_font.render("C for Color", False, WHITE)

clock = pygame.time.Clock()
random.seed()

# Create objects
objects = []
number_of_objects = 20
start_mass = 30

# Create border
border_thickness = 5
border_right = (0, 0, border_thickness, size[1])
border_left = (size[0] - border_thickness, 0, border_thickness, size[1])
border_top = (0, 0, size[0], border_thickness)
border_down = (0, size[1] - border_thickness, size[0], border_thickness)

# Flags
done = False
pressing = False
draw_path = False
draw_color = True
border = True

# Constant
GRAV_CONST = 6.67408 * (10 ** (-11))

# Returns true if the string is an integer
def string_is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


# Checks for different number of objects
if len(sys.argv) > 1:
    if string_is_int(sys.argv[1]):
        number_of_objects = int(sys.argv[1])
    if len(sys.argv) > 2:
        if string_is_int(sys.argv[2]):
            start_mass = int(sys.argv[2])
            

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

        if border:
            # Check each border for collision
            if self.position_x + self.radius > size[0]:
                # First move the object (to prevent repeated collision)
                self.position_x = size[0] - self.radius
                # Velocity is reversed
                self.velocity_x *= -1
            if self.position_x - self.radius < 0:
                self.position_x = self.radius
                self.velocity_x *= -1
            if self.position_y + self.radius > size[1]:
                self.position_y = size[1] - self.radius
                self.velocity_y *= -1
            if self.position_y - self.radius < 0:
                self.position_y = self.radius
                self.velocity_y *= -1

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
                # Using conservation of momentum and assumes perfectly inelastic collision
                self.mass += obj.mass
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
        if not self.merged:
            if draw_color:
                pygame.draw.circle(screen, self.color, [int(self.position_x), int(self.position_y)], int(self.radius))
            else:
                pygame.draw.circle(screen, WHITE, [int(self.position_x), int(self.position_y)], int(self.radius))


def init_objects():
    # Resets screen regardless of flag draw_path
    screen.fill(BLACK)

    for i in range(number_of_objects):
        # Mass must be in 10^11kg scale (because gravity would be too weak otherwise)
        mass = start_mass * (10 ** 11)
        # Randomized position
        position_x = random.randint(0, size[0])
        position_y = random.randint(0, size[1])
        # Randomized color
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Add the object and calculate radius
        objects.append(Object(mass, position_x, position_y, color))
        objects[i].calculate_radius()

# Starts off 
init_objects()

# Main loop
while not done:
    # Exiting game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Key press
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and not pressing:
        pressing = True
        # Delete objects and reinitialize for new set of objects
        del objects[:]
        init_objects()
    elif pressed[pygame.K_z] and not pressing:
        pressing = True
        draw_path = not draw_path 
    elif pressed[pygame.K_x] and not pressing:
        pressing = True
        border = not border
    elif pressed[pygame.K_c] and not pressing:
        pressing = True
        draw_color = not draw_color

    # Reset key press if all keys aren't pressed
    all_empty = True
    first = True
    for i in pressed:
        # There's a 1 always there for some reason
        if i != 0 and first:
            first = False
        elif i != 0:
            all_empty = False
            break

    # Only allow for new key press if all key's aren't pressed
    if all_empty:
        pressing = False

    # Checks for collision and deletes y if applicable
    for x in objects:
        for y in objects:
            if x != y and not x.merged and not y.merged:
                x.collision(y)

    # Calculates new velocity based on force of gravity
    for x in objects:
        for y in objects:
            if x != y and not x.merged and not y.merged:
                x.calculate_new_velocity(y)

    # Calculates position based on velocity
    for x in objects:
        x.calculate_new_position()

    # Fill screen
    if not draw_path:
        screen.fill(BLACK)

    # Draw
    for i in objects:
        i.draw_object()

    # Instructions
    screen.blit(text_space, (10, size[1] - 100))
    screen.blit(text_z, (10, size[1] - 75))
    screen.blit(text_x, (10, size[1] - 50))
    screen.blit(text_c, (10, size[1] - 25))

    # Border drawing
    if border:
        pygame.draw.rect(screen, DARK_RED, border_right)
        pygame.draw.rect(screen, DARK_RED, border_left)
        pygame.draw.rect(screen, DARK_RED, border_top)
        pygame.draw.rect(screen, DARK_RED, border_down)

    # Updates
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)
	
pygame.quit()
