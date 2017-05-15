'''
Gravity Simulation
---------------------
By Hiroya Gojo
---------------------
Use two number arguments to set screen resolution.
Use keyboard instructions on screen to manipulate simulation.
Idea: Arrows showing direction of force/acceleration/velocity/etc
Idea: Presets with set amount of velocity or position of objects (store in file) to show examples
Idea: Can store examples in files and make simulations

'''
import math
import pygame
import random
import sys

# Returns true if the string is an integer
def string_is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

width = 1280
height = 720
# Checks for different number of objects
if len(sys.argv) > 1:
    if string_is_int(sys.argv[1]):
        width = int(sys.argv[1])
    if len(sys.argv) > 2:
        if string_is_int(sys.argv[2]):
            height = int(sys.argv[2])
 
# Background Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARK_RED = (156, 43, 43)

# Initialize for program
pygame.init()
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Gravity Simulation - Hiroya")

# Font and text
pygame.font.init()
font_type = "Times New Roman"
text_font = pygame.font.SysFont(font_type, 15)
text_font_small = pygame.font.SysFont(font_type, 13)

text_space = text_font.render("Space to Restart", False, WHITE)
text_z = text_font.render("Z for path", False, WHITE)
text_x = text_font.render("X for border", False, WHITE)
text_c = text_font.render("C for color", False, WHITE)
text_s = text_font.render("Q/W to speed up", False, WHITE)
text_a = text_font.render("A/S to slow down", False, WHITE)
text_d = text_font.render("E/R for more mass", False, WHITE)
text_f = text_font.render("D/F for less mass", False, WHITE)
text_g = text_font.render("T/Y for more objects", False, WHITE)
text_h = text_font.render("G/H for less objects", False, WHITE)
text_p = text_font.render("P to pause/unpause", False, WHITE)
text_m = text_font_small.render("M for antigravity (FOR FUN)", False, GRAY)

clock = pygame.time.Clock()
random.seed()

# Create objects
objects = []
number_of_objects = 5
start_mass = 110
game_speed = 1

# Create border
border_thickness = 5
border_right = (0, 0, border_thickness, size[1])
border_left = (size[0] - border_thickness, 0, border_thickness, size[1])
border_top = (0, 0, size[0], border_thickness)
border_down = (0, size[1] - border_thickness, size[0], border_thickness)

# Flags
done = False
pressing = False
pause = False
draw_path = False
draw_color = True
border = True

# Constant
GRAV_CONST = 6.67408 * (10 ** (-11))

# class object
class Object:
    def __init__ (self, mass, position_x, position_y, color):
        # Initialize mass and position 
        self.mass = mass
        self.merged = False
        self.selected = False
        self.store_force_x = 0
        self.store_force_y = 0
                
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

        # Adds the force to the stored force
        self.store_force_x += force_x
        self.store_force_y += force_y

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
            momentum_x = self.mass * self.velocity_x + obj.mass * obj.velocity_x
            momentum_y = self.mass * self.velocity_y + obj.mass * obj.velocity_y

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
            # If an object is selected, draw an outline around them
            if self.selected:
                pygame.draw.circle(screen, DARK_RED, [int(self.position_x), int(self.position_y)], int(self.radius) + 4)

            # Draw objects. If/else for diff color modes
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

    # Path
    elif pressed[pygame.K_z] and not pressing:
        pressing = True
        draw_path = not draw_path 

    # Border
    elif pressed[pygame.K_x] and not pressing:
        pressing = True
        border = not border
        # Border needs to disappear
        screen.fill(BLACK)

    # Color
    elif pressed[pygame.K_c] and not pressing:
        pressing = True
        draw_color = not draw_color

    # Game speed +
    elif pressed[pygame.K_q] and not pressing:
        pressing = True
        game_speed += 1
    elif pressed[pygame.K_w] and not pressing:
        pressing = True
        game_speed += 10

    # Game speed -
    elif pressed[pygame.K_a] and not pressing:
        pressing = True
        if game_speed > 1:
            game_speed -= 1
    elif pressed[pygame.K_s] and not pressing:
        pressing = True
        if game_speed > 10:
            game_speed -= 10

    # Mass +
    elif pressed[pygame.K_e] and not pressing:
        pressing = True
        start_mass += 1
    elif pressed[pygame.K_r] and not pressing:
        pressing = True
        start_mass += 10

    # Mass -
    elif pressed[pygame.K_d] and not pressing:
        pressing = True
        if start_mass > 1:
            start_mass -= 1
    elif pressed[pygame.K_f] and not pressing:
        pressing = True
        if start_mass > 11:
            start_mass -= 10

    # Num +
    elif pressed[pygame.K_t] and not pressing:
        pressing = True
        number_of_objects += 1
    elif pressed[pygame.K_y] and not pressing:
        pressing = True
        number_of_objects += 10

    # Num -
    elif pressed[pygame.K_g] and not pressing:
        pressing = True
        if number_of_objects > 1:
            number_of_objects -= 1
    elif pressed[pygame.K_h] and not pressing:
        pressing = True
        if number_of_objects > 11:
            number_of_objects -= 10

    # Pause
    elif pressed[pygame.K_p] and not pressing:
        pressing = True
        pause = not pause

    # Wtf
    elif pressed[pygame.K_m] and not pressing:
        pressing = True
        GRAV_CONST *= -1

    # Check if player clicked on an object
    if pygame.mouse.get_pressed()[0]:
        # To check whether to deselect item
        for i in objects:
            # Deselect all other objects
            i.selected = False
            # Find distance between mouse and object
            mouse_pos = pygame.mouse.get_pos()
            distance = math.sqrt((mouse_pos[0] - i.position_x)**2 + (mouse_pos[1] - i.position_y)**2)
            # If the distance is smaller than the radius, the mouse is in the object and is selected
            if i.radius > distance:
                # Current object is selected
                i.selected = True
                break

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

    # If paused, don't need to run code
    if not pause:
        # Run multiple times for larger game_speed
        for num in range(game_speed):
            # Checks for collision and deletes y if applicable
            for x in objects:
                for y in objects:
                    if x != y and not x.merged and not y.merged:
                        x.collision(y)

            # Zeroes out acceleration and old gravitational force
            for x in objects:
                x.acceleration_x = 0
                x.acceleration_y = 0
                x.store_force_x = 0
                x.store_force_y = 0

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

    # Rectangle for top bar
    pygame.draw.rect(screen, (40, 40, 40), (0, 0, size[0], 40))

    # If an object is selected, display its information
    for i in objects:
        if i.selected and not i.merged:
            object_information_x = "X  Position: " + str(round(i.position_x, 2))
            object_information_y = "Y  Position: " + str(round(i.position_y, 2))
            object_information_vel_x = "X  Velocity: "  + str(round(i.velocity_x, 3)) + "m/s"
            object_information_vel_y = "Y  Velocity: "  + str(round(i.velocity_y, 3)) + "m/s"
            object_information_acc_x = "X  Acceleration: " + str(round(i.acceleration_x, 5)) + "m/s^2"
            object_information_acc_y = "Y  Acceleration: " + str(round(i.acceleration_y, 5)) + "m/s^2"
            object_information_force_x = "X  Force: " + str('%.3e' % i.store_force_x) + "N"
            object_information_force_y = "Y  Force: " + str('%.3e' % i.store_force_y) + "N"
            # Display the text
            text_display_x = text_font_small.render(object_information_x, False, WHITE)
            text_display_y = text_font_small.render(object_information_y, False, WHITE)
            text_display_vel_x = text_font_small.render(object_information_vel_x, False, WHITE)
            text_display_vel_y = text_font_small.render(object_information_vel_y, False, WHITE)
            text_display_acc_x = text_font_small.render(object_information_acc_x, False, WHITE)
            text_display_acc_y = text_font_small.render(object_information_acc_y, False, WHITE)
            text_display_force_x = text_font_small.render(object_information_force_x, False, WHITE)
            text_display_force_y = text_font_small.render(object_information_force_y, False, WHITE)
            screen.blit(text_display_x, (600, 4))
            screen.blit(text_display_y, (600, 25))
            screen.blit(text_display_vel_x, (760, 4))
            screen.blit(text_display_vel_y, (760, 25))
            screen.blit(text_display_acc_x, (900, 4))
            screen.blit(text_display_acc_y, (900, 25))
            screen.blit(text_display_force_x, (1100, 4))
            screen.blit(text_display_force_y, (1100, 25))

    # Game speed change
    text_speed = text_font.render("Speed: " + str(game_speed) + "x", False, WHITE)
    screen.blit(text_speed, (10, 14))
    screen.blit(text_s, (10, 40))
    screen.blit(text_a, (10, 55))
    screen.blit(text_p, (10, 70))

    # Mass Change
    text_mass = text_font.render("Init Mass: " + str(start_mass) + "*10^11 kg", False, WHITE)
    screen.blit(text_mass, (190, 14))
    screen.blit(text_d, (190, 40))
    screen.blit(text_f, (190, 55))

    # Number change
    text_number = text_font.render("Init Number: " + str(number_of_objects), False, WHITE)
    screen.blit(text_number, (400, 14))
    screen.blit(text_g, (400, 40))
    screen.blit(text_h, (400, 55))
    
    # Instructions
    screen.blit(text_space, (10, size[1] - 100))
    screen.blit(text_z, (10, size[1] - 75))
    screen.blit(text_x, (10, size[1] - 50))
    screen.blit(text_c, (10, size[1] - 25))

    screen.blit(text_m, (size[0] - 160, size[1] - 20))

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
