import pygame, sys, os, random
from datetime import datetime, date, time, timedelta
from pygame.locals import *
import timesprites
from userevents import *
from backgrounds import *

class Scene(object):
	def __init__(self):
		pass

	def activate(self):
		return self

	def render(self, screen):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def handle_event(self, event):
		raise NotImplementedError

	def set_background(self, background):
		raise NotImplementedError

class ClockScene(Scene):
	def __init__(self, __background):
		Scene.__init__(self)
		self.clock_sprite = timesprites.ClockSprite()
		self.day_sprite = timesprites.DaySprite()
		self.sprite_group = pygame.sprite.LayeredDirty()
		
		self.sprite_group.add([self.clock_sprite, self.day_sprite], layer=1)
		self.set_background(__background)
		self.image = __background.image

		self.rect = self.image.get_rect()
		self.dirty_rects = []
		self.clean_background = self.image.copy()
		self.sprite_group.clear(self.image, self.clean_background)
		
	def render(self, screen):
		self.dirty_rects = self.sprite_group.draw(screen)
		if len(self.dirty_rects) > 0:
			self.sprite_group.clear(screen, self.clean_background)
		
	def update(self):
		__background = self.sprite_group.get_sprites_from_layer(0)[0]

		avg_color = pygame.transform.average_color(__background.image, self.clock_sprite.rect)
		self.clock_sprite.set_color(calculate_contrast_color(avg_color))

		avg_color = pygame.transform.average_color(__background.image, self.day_sprite.rect)
		self.day_sprite.set_color(calculate_contrast_color(avg_color))

		self.sprite_group.update()
		pygame.display.update(self.dirty_rects)

	def handle_event(self, event):
		for sprite in self.sprite_group.sprites():
			if hasattr(sprite, "handle_event"):
			 sprite.handle_event(event)

	def set_background(self, __background):
		self.sprite_group.remove_sprites_of_layer(0)
		self.sprite_group.add(__background, layer=0)
		dirty = 1

