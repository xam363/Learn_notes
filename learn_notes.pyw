import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Learn notes")

typed_key = ""
notes = "ABCDEFG"
showed_text = ""
random_note = random.randint(0, 6)
shift_note = random.choice([-3, -2, -1, 1, 2, 3])
target_note = (random_note + shift_note) % 7
count_right = 0

# screens
active_screen = 0

def text(screen, text, xy, color, size):
	""" screen, showed text, (x, y), color, size"""
	font = pygame.font.SysFont('Comic Sans MS', size)
	textsurface = font.render(text, False, color)
	screen.blit(textsurface, (xy))

def button(screen, _text, color, rect):
	pygame.draw.rect(screen, color, rect)
	size = rect[2] // len(_text)
	text(screen, _text, (rect[0], rect[1]), (0, 0, 0), size)

def note_flat(screen, note, rect):
	width_gap = rect[3] // 5
	def draw_note(shift):
		# bottom note
		pygame.draw.ellipse(screen, (255, 0, 0), 
			(rect[0]+WIDTH/2-100, rect[1]+width_gap*(6.5+shift), 20, 20)
		)
		# middle note
		pygame.draw.ellipse(screen, (255, 0, 0), 
			(rect[0]+WIDTH/2-50, rect[1]+width_gap*(3+shift), 20, 20)
		)
		# top note
		pygame.draw.ellipse(screen, (255, 0, 0), 
			(rect[0]+WIDTH/2, rect[1]-width_gap*(0.5 - shift), 20, 20)
		)

		# bottom lines
		for i in range(3):
			pygame.draw.line(screen, (0, 0, 0), 
				(rect[0]+WIDTH/2-100-15, rect[1]+width_gap*(4.5+i)+10), 
				(rect[0]+WIDTH/2-100+30, rect[1]+width_gap*(4.5+i)+10), 2
			)

		# top lines
		for i in range(3):
			pygame.draw.line(screen, (0, 0, 0), 
				(rect[0]+WIDTH/2-15, rect[1]-width_gap*(1.5+i)+10), 
				(rect[0]+WIDTH/2+30, rect[1]-width_gap*(1.5+i)+10), 2
			)

	# draw lines
	for i in range(5):
		pygame.draw.line(screen, (0, 0, 0), 
			(rect[0], rect[1]+width_gap*i), 
			(rect[0]+rect[2], rect[1]+width_gap*i), 2
		)

	if note == "F":
		draw_note(0)
	elif note == "G":
		draw_note(-0.5)
	elif note == "A":
		draw_note(-1)
	elif note == "B":
		draw_note(-1.5)
	elif note == "C":
		draw_note(-2)
	elif note == "D":
		draw_note(-2.5)
	elif note == "E":
		draw_note(-3)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				typed_key = "A"
			elif event.key == pygame.K_b:
				typed_key = "B"
			elif event.key == pygame.K_c:
				typed_key = "C"
			elif event.key == pygame.K_d:
				typed_key = "D"
			elif event.key == pygame.K_e:
				typed_key = "E"
			elif event.key == pygame.K_f:
				typed_key = "F"
			elif event.key == pygame.K_g:
				typed_key = "G"

		if (pygame.mouse.get_pressed()[0] and 
				pygame.mouse.get_pos()[0] > 0 and 
				pygame.mouse.get_pos()[0] < 100 and 
				pygame.mouse.get_pos()[1] > 450 and
				pygame.mouse.get_pos()[1] < 480):
			active_screen = 0
			count_right = 0

		if (pygame.mouse.get_pressed()[0] and 
				pygame.mouse.get_pos()[0] > 110 and 
				pygame.mouse.get_pos()[0] < 210 and 
				pygame.mouse.get_pos()[1] > 450 and
				pygame.mouse.get_pos()[1] < 480):
			active_screen = 1
			count_right = 0

	screen.fill((0, 100, 255))

	# buttoms and active color
	if active_screen == 0:
		button(screen, "Letters", (0, 255, 0), (0, 450, 100, 30))
	else:
		button(screen, "Letters", (111, 111, 111), (0, 450, 100, 30))
	if active_screen == 1:
		button(screen, "Notes", (0, 255, 0), (110, 450, 100, 30))
	else:
		button(screen, "Notes", (111, 111, 111), (110, 450, 100, 30))

	# show notes letter
	if active_screen == 0:
		if typed_key == notes[target_note]:
			count_right += 1
			random_note = random.randint(0, 6)
			shift_note = random.choice([-3, -2, -1, 1, 2, 3])
			target_note = (random_note + shift_note) % 7
		if shift_note > 0:
			showed_text = notes[random_note] + ("+" * shift_note)
		else:
			showed_text = "-" * abs(shift_note) + notes[random_note]
		text(screen, showed_text, (WIDTH/2-100, HEIGHT/2-100), (0, 0, 0), 100)
		text(screen,  "Right: " + str(count_right), (0, 0), (0, 255, 0), 50)

	# show second screen	
	elif active_screen == 1:
		if typed_key == notes[random_note]:
			count_right += 1
			random_note = random.randint(0, 6)
		text(screen,  "Right: " + str(count_right), (0, 0), (0, 255, 0), 50)
		note_flat(screen, notes[random_note], (0, 200, WIDTH, 100))

	# update
	pygame.display.update()