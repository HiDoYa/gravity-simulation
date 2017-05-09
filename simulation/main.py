import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize
pygame.init()
pygame.font.init()
size = (960, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test")
done = False

clock = pygame.time.Clock()


# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Logic goes here
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_s]:

	# Fill screen
	screen.fill(WHITE)

	# Draw
	pygame.draw.circle(screen, BLACK, [250, 400], 50)

	noMove = False

	# Updates
	pygame.display.flip()

	# 60 FPS
	clock.tick(60)
	
pygame.quit()
