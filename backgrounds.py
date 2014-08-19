import pygame, sys, os
from datetime import datetime, date, time, timedelta
from pygame.locals import *
from collections import deque

class Background(pygame.sprite.DirtySprite):
	def __init__(self, __width = 320, __height = 240):
		pygame.sprite.DirtySprite.__init__(self)

		self.width = __width
		self.height = __height
		self.image = pygame.Surface((self.width, self.height))
		self.rect = self.image.get_rect()

	def update(self):
		pass

class EmptyBackground(Background):
	def __init__(self, __color, __width = 320, __height = 240):
		Background.__init__(self, __width, __height)
		self.image.fill(__color)

class ImageBackground(Background):
	def __init__(self, __image_file, __width = 320, __height = 240):
		Background.__init__(self, __width, __height)
		try:
			self.image = pygame.image.load(__image_file)
		except:
			pass

class ShadedBackground(EmptyBackground):
	def __init__(self, __color, __width = 320, __height = 240, __shade_height = 4):
		EmptyBackground.__init__(self, __color, __width, __height + __shade_height)

		self.image = self.image.convert_alpha()
		self.rect = self.image.get_rect()
		pygame.draw.line(self.image, (196,196,196, 48), (0,0), (__width, 0), 1)

		alpha_step = 1.0 / __shade_height
		for i in range(1, __shade_height + 1):
			pygame.draw.line(self.image, (128, 128, 128, 64 * (1 - alpha_step * i)), (0, __height + i), (__width, __height + i))


class EfimeridesBackground(Background):
	time_slots = [
		{'from_time': (0,0), 'label': "night"},
		{'from_time': (6,30), 'label': "dawn"},
		{'from_time': (11,0), 'label': "day"},
		{'from_time': (18,0), 'label': "dusk"},
		{'from_time': (21,0), 'label': "night"}
	]

	def __init__(self):
		Background.__init__(self)
		self.current_label = ""

	def update(self):
		t = datetime.now()

		label = self.time_slots[-1]['label'] #default to the last label
		bg_name = "gp"

		for i in range(1, len(self.time_slots)):
			if (t.hour, t.minute) > self.time_slots[i]['from_time']:
				label = self.time_slots[i]['label']

		if label <> self.current_label:
			filename = os.path.join("backgrounds", bg_name + "_" + label + ".png.jpg")
			print "Switching to background: %s" % (filename)
			self.image = pygame.image.load(filename)
			self.rect = self.image.get_rect()
			self.current_label = label
			self.dirty = 1

		def load_file_list(self):
			pass # files are always loaded on the spot

class SlideshowBackground(Background):
	file_list = deque()

	def __init__(self, __hourglass = 10, __width = 320, __height = 240):
		Background.__init__(self, __width, __height)

		self.load_file_list();

		self.hourglass = __hourglass
		self.mark = datetime.now() + timedelta(seconds=-1)
		self.update()

	def update(self):
		if len(self.file_list) == 0:
			return

		if datetime.now() > self.mark:
			filename = self.file_list.popleft()
			try:
				self.image = pygame.image.load(filename)
				self.rect = self.image.get_rect()
				self.file_list.append(filename) #put the file back at the end of the list
			except:
				pass # ignore exception, but we're not putting the file back in the list

			self.mark = datetime.now() + timedelta(seconds=self.hourglass)
			self.dirty = 1

		if len(self.file_list) == 0:
			self.load_file_list()

	def load_file_list(self):
		self.file_list.clear()
		for filename in os.listdir ("slideshow"):
			if filename.startswith("."):
				continue

			print "Found background %s" % (filename)
			self.file_list.append(os.path.join("slideshow", filename))
