import pygame, sys
from datetime import datetime, date, time, timedelta
from userevents import SmartSprite, UserEvent

# TimeSprite
class TimeSprite(pygame.sprite.DirtySprite):
	def __init__(self, __delta = 1):
		pygame.sprite.DirtySprite.__init__(self)
		SmartSprite.__init__(self)
		self.clock_font = self.get_font(60);
		self.color = (0,0,0)		

		self.trigger = UserEvent.create_event()
		pygame.time.set_timer(self.trigger, __delta * 1000)

	def update(self):
		pass

	def handle_event(self, event):
		if self.trigger == event.type:
			self.dirty = True

	def get_current_time(self):
		return datetime.now(), self.dirty

	def get_font(self, size):
		return pygame.font.Font("fonts/Roboto-Thin.ttf", size)

	def set_color(self, __color):
		if __color != self.color:
			self.color = __color
			self.dirty = 1

# ClockSprite
class ClockSprite(TimeSprite):
	def __init__(self):
		TimeSprite.__init__(self, 1)

		self.image = self.get_font(60).render("12:00", 1, self.color)
		self.rect = self.image.get_rect(center=(160,60))

	def update(self):
		super(ClockSprite, self).update() #handle default update trigger

		time_now, self.dirty = self.get_current_time()
		if (self.dirty):
			h = time_now.hour
			if h > 12:
				h -=12
			#self.image = self.get_font(60).render(time_now.strftime("%I:%M:%S"), 1, self.color)
			self.image = self.get_font(60).render("{0} uur {1}".format(h, time_now.minute), 1, self.color)
			self.rect = self.image.get_rect(center=(160,60))

# DaySprite
class DaySprite(TimeSprite):
	days_of_week = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
	time_text = [
		{'from_time': (0,0), 'text': "nacht"}, 
		{'from_time': (6,30), 'text': "ochtend"}, 
		{'from_time': (10,00), 'text': "middag"},
		{'from_time': (18,00), 'text':  "avond"},
		{'from_time': (21,00), 'text': "nacht"}
	]

	def __init__(self):
		TimeSprite.__init__(self, 30)

		self.image = self.get_font(32).render("", 1, self.color)
		self.rect = self.image.get_rect(center=(160,120))

	def update(self):
		super(DaySprite, self).update() #handle default update trigger

		time_now, self.dirty = self.get_current_time()

		if (self.dirty):
			time_str = self.days_of_week[time_now.weekday()] + " " + self.get_time_text(time_now)
			self.image = self.get_font(32).render(time_str, 1, self.color)
			self.rect = self.image.get_rect(center=(160,120))

	def get_time_text (self, t):
		for i in range(1, len(self.time_text)):
			if (t.hour, t.minute) < self.time_text[i]['from_time']:
				return self.time_text[i-1]['text']

		return self.time_text[-1]['text']
		