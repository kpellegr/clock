import pygame

class UserEvent:
	MAX_ID = pygame.locals.USEREVENT
	
	@staticmethod
	def create_event ():
		if UserEvent.MAX_ID >= pygame.locals.NUMEVENTS:
			UserEvent.MAX_ID = pygame.locals.USEREVENT

		UserEvent.MAX_ID+=1
		return UserEvent.MAX_ID

class SmartSprite(object):
	def __init(self):
		pass

	def handle_event(self, event):
		raise NotImplementedError


def calculate_contrast_color (color):
	r = color[0]
	g = color[1]
	b = color[2]
	yiq = ((r*299)+(g*587)+(b*114))//1000
	if yiq >= 128:
		return (0,0,0)
	else:
		return (255, 255, 255)
