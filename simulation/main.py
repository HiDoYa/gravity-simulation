import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize
pygame.init()
pygame.font.init()
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Test")
done = False

clock = pygame.time.Clock()

accX = 0
accY = 0
velX = 0
velY = 0
posX = 250
posY = 100

# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	# Logic goes here
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_d]:
		accX += 1
	if pressed[pygame.K_w]:
		accY -= 1
	if pressed[pygame.K_a]:
		accX -= 1
	if pressed[pygame.K_s]:
		accY += 1

	velX += accX
	velY += accY

	if posX + velX > 500:
		posX -= velX
	
	if posX + velX < 0:
		posX -= velX

	if posY + velY > 500:
		posY -= velY

	if posY + velY < 0:
		posY -= velY

	# Fill screen
	screen.fill(WHITE)

	# Draw
	pygame.draw.circle(screen, BLACK, [posX, posY], 50)
	pygame.draw.circle(screen, BLACK, [250, 400], 50)

	noMove = False

	# Updates
	pygame.display.flip()

	# 60 FPS
	clock.tick(60)
	
pygame.quit()
