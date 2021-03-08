import pygame, sys, random, time

class Button:
	def __init__(self, screen, _text, color, rect):
		self.screen = screen
		self._text = _text
		self.color = color
		self.rect = rect
		self.pushed = False
		self.click_time = time.time()

	def show(self):
		""" Show button to the screen """
		pygame.draw.rect(self.screen, self.color if not self.pushed else (0, 255,0), self.rect)
		size = self.rect[2] // len(self._text)
		text(self.screen, self._text, (self.rect[0], self.rect[1]), (0, 0, 0), size)

	def check_push(self, reverse=False):
		""" Checked if i pushed the button """
		# check mouse coordinates over button
		if (pygame.mouse.get_pos()[0] > self.rect[0] and 
				pygame.mouse.get_pos()[0] < self.rect[0] + self.rect[2] and
			 	pygame.mouse.get_pos()[1] > self.rect[1] and 
			 	pygame.mouse.get_pos()[1] < self.rect[1] + self.rect[3]):
			self.color = (0, 0, 255)
			# check mouse pressed
			if (pygame.mouse.get_pressed()[0]):
				# if reverse i can turn off 
				if not reverse:
					self.pushed = True
				else:
					# check time last push
					if time.time() - self.click_time > 0.2:
						if not self.pushed:
							self.pushed = True
						else:
							self.pushed = False
						self.click_time = time.time()
		else:
			# color if not pushe and not mouse over
			self.color = (111, 111, 111)

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
hard_mode_roll = random.randint(0, 2)


active_screen = 0 # screen for show

# buttons
buttons = []
buttons.append(Button(screen, "Letters", (111, 111, 111), (0, 450, 100, 30)))
buttons[0].pushed = True
buttons.append(Button(screen, "Notes", (111, 111, 111), (110, 450, 100, 30)))

hard_mode_button = (Button(screen, "Hard", (111, 111, 111), (110, 415, 100, 30)))



def text(screen, text, xy, color, size):
	""" screen, showed text, (x, y), color, size"""
	font = pygame.font.SysFont('Comic Sans MS', size)
	textsurface = font.render(text, False, color)
	screen.blit(textsurface, (xy))


def draw_random_note(screen, note, rect, _hard_mode, roll):
	width_gap = rect[3] // 5
	shift = "FGABCDE".index(note)*-0.5
	if not _hard_mode:
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
	elif _hard_mode:
		pygame.draw.ellipse(screen, (255, 0, 0), 
			(rect[0]+WIDTH/2-50*roll, rect[1]+width_gap*(abs(-0.5+roll*3.5)+shift), 20, 20)
		)

def draw_flat(screen, note, rect):
	width_gap = rect[3] // 5
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

	# draw middle lines
	for i in range(5):
		pygame.draw.line(screen, (0, 0, 0), 
			(rect[0], rect[1]+width_gap*i), 
			(rect[0]+rect[2], rect[1]+width_gap*i), 2
		)

	

while True:
	screen.fill((255, 255, 255))
	
	# check events
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

	for index, button in enumerate(buttons):
		button.show()
		button.check_push()
		if button.pushed and active_screen != index:
			buttons[active_screen].pushed = False
			active_screen = index


	# show fris screen
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
		hard_mode_button.show()
		hard_mode_button.check_push(True)
		if typed_key == notes[random_note]:
			count_right += 1
			random_note = random.randint(0, 6)
			hard_mode_roll = random.randint(0, 2)
		text(screen,  "Right: " + str(count_right), (0, 0), (0, 255, 0), 50)
		draw_flat(screen, notes[random_note], (0, 200, WIDTH, 100))
		draw_random_note(screen, notes[random_note], (0, 200, WIDTH, 100), 
						 hard_mode_button.pushed, hard_mode_roll)

	# update
	pygame.display.update()

		