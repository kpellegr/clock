import pygame
from pygame.locals import *
from backgrounds import *
from clockscene import Scene

class Icon(pygame.sprite.DirtySprite):
	def __init__(self, __iconname):
		pygame.sprite.DirtySprite.__init__(self)
		try:
			self.image = pygame.image.load(os.path.join("icons", __iconname)).convert_alpha()
		except:
			print "Unable to load button icon %s" % (__iconname)
			print pygame.get_error()
			self.image = pygame.Surface((Button.TILE_SIZE, Button.TILE_SIZE))
			self.fill = (0,0,0,0)

		self.rect = self.image.get_rect()

class Button(pygame.sprite.DirtySprite):
	TILE_SIZE = 60
	PADDING = 5

	def __init__(self):
		pygame.sprite.DirtySprite.__init__(self)


class TwoStateButton(Button):
	def __init__(self, __on, __off, __state = False):
		Button.__init__(self)

		self.on  = dict(icon=Icon(__on["icon"]), value = __on["value"])
		self.off = dict(icon=Icon(__off["icon"]), value = __off["value"])

		if __state:
			self.state = self.on
		else:
			self.state = self.off

		self.image = pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)).convert_alpha()
		self.image.fill((250,250,250,100))

		self.rect = self.image.get_rect()
		self.state_bar = pygame.Rect(self.rect.bottomleft, (self.rect.width, -5))
 
	def update(self):
		if not(self.dirty):
			return

		self.blit_icon(self.state["icon"])
		if self.state == self.on:
			pygame.draw.rect(self.image, (250, 250, 0, 255), self.state_bar, 0)
		else:
			pygame.draw.rect(self.image, (250, 250, 250, 255), self.state_bar, 0)

	def blit_icon(self, __icon):
		x = (self.image.get_rect().width - __icon.rect.width - 1) // 2
		y = ((self.image.get_rect().height - __icon.rect.height - 1) // 2) - 3

		self.image.blit(self.image, (0,0), None, BLEND_RGBA_SUB)
		self.image.blit(__icon.image, (x,y))


	def handle_event(self, event):
		if event.type == MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				#print "Released button %d!" % (self.state["value"])
				if self.state == self.on:
					self.state = self.off
					self.dirty = 1
				else:
					self.state = self.on
					self.dirty = 1
				return self.state["value"]
		return False;

class PushButton(TwoStateButton):
	def __init__(self, __icon_file, __value):
		TwoStateButton.__init__(self, dict(value=__value, icon=__icon_file), dict(value=__value, icon=__icon_file))

	def handle_event(self, event):
		if event.type == MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.state = self.on
				self.dirty = 1
				return False
		if event.type == MOUSEBUTTONUP:
			if self.rect.collidepoint(event.pos):
				self.state = self.off
				self.dirty = 1
				return self.state["value"]

		return False;


# =======================================================
# Control center
# =======================================================

class ControlScene(Scene):
	PADDING = 5
	def __init__(self):
		Scene.__init__(self)

		self.image = None
		self.rect = None
		self.background = None
		self.sprite_group = pygame.sprite.LayeredDirty()

		self.max_columns= 320 // (Button.TILE_SIZE + self.PADDING)
		self.max_rows= 240 // (Button.TILE_SIZE + self.PADDING)

		self.button_grid = list()
		self.button_grid.append([])

		self.button_layout()

		self.dirty_rects = []
		self.rect = self.image.get_rect()

	def render(self, screen):
		self.dirty_rects = self.sprite_group.draw(screen)
		#if len(self.dirty_rects) > 0:
			#self.sprite_group.clear(screen, self.clean_background)

	def update(self):
		self.sprite_group.update()
		pygame.display.update(self.dirty_rects)

	def append(self, __button):
		if len(self.button_grid) >= self.max_rows:
			print "Too many button rows"
			return

		if len(self.button_grid[-1]) >= self.max_columns:
			self.button_grid.append([])

		self.button_grid[-1].append(__button)
		
		self.sprite_group.add(__button, layer=1)

		self.button_layout()
		self.dirty = 1

	def button_layout(self):
		number_of_rows = len(self.button_grid)
		button_size = Button.TILE_SIZE + self.PADDING
		box_height = number_of_rows * button_size + 5 * self.PADDING
		padding_left = (320 - self.max_columns * (Button.TILE_SIZE + self.PADDING)) / 2
		padding_top = (240 - box_height) / 2

		self.background = ShadedBackground((255, 255, 255), 320, box_height)
		self.background.rect.move_ip(0, padding_top - 2 * self.PADDING)
		self.sprite_group.add(self.background, layer=0)
		self.image = self.background.image
		self.rect = self.image.get_rect()
		self.clean_background = self.image.copy()

		for r in range(len(self.button_grid)):
			for c in range(len(self.button_grid[r])):
				x = padding_left + c * button_size
				y = padding_top + r * button_size
				self.button_grid[r][c].rect.topleft = (x, y)


	def append_split(self):
		if len(self.button_grid) >= self.max_rows:
			print "Too many button rows"
			return
		self.button_grid.append(list())		

	def activate(self):
		self.background.dirty = 1
		dirty = 1
		return self


	def handle_event(self, event):
		for sprite in self.sprite_group:
			if hasattr(sprite, "handle_event"):
				res = sprite.handle_event(event)
				if res != False:
					return res
		return False
