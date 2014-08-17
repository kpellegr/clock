import pygame, os, random
import bluetooth
from pygame.locals import *
from userevents import *
from backgrounds import ImageBackground
from clockscene import Scene

class RadarSwipe(pygame.sprite.DirtySprite):
	def __init__(self, __color, __width, __step):
		pygame.sprite.DirtySprite.__init__(self)

		color = pygame.Color(__color[0], __color[1], __color[2], 0)
		halfway = (__width + 1) // 2
		alpha_step = 240//(halfway+1)

		self.image = pygame.Surface((__width, 240)).convert_alpha()		
		for i in range(halfway + 1):
			color.a = (i+1)*alpha_step
			pygame.draw.line(self.image, color, (i,0), (i, 240))
			pygame.draw.line(self.image, color, (__width-i,0), (__width-i, 240))
		self.rect = self.image.get_rect()

		self.step = __step

	def update(self):
		self.dirty = 1
		if self.on_edge():
			self.step = -self.step
		self.rect.move_ip(self.step, 0)

	def on_edge(self):
		return (self.rect.x > (319 - self.rect.width)) or (self.rect.x < 0)

class MonsterCounter(pygame.sprite.DirtySprite):
	def __init__(self, __color):
		pygame.sprite.DirtySprite.__init__(self)

		self.number_of_monsters = 0
		self.color = __color
		self.dirty = 1
		self.update()
		self.rect = self.image.get_rect()


	def update(self):
		if not(self.dirty):
			return

		self.image = self.get_font(144).render(str(self.number_of_monsters), 1, self.color)

	def handle_event(self, event):
		if self.trigger == event.type:
			nearby_devices = bluetooth.discover_devices()
			self.number_of_monsters = len(nearby_devices)
			#self.number_of_monsters = random.randint(0,5)
			self.dirty = 1
			self.update()

	def get_font(self, size):
		return pygame.font.Font("fonts/Roboto-Thin.ttf", size)

# =======================================================
# Monster teller
# =======================================================

class MonsterScene(Scene):

	def __init__(self):
		Scene.__init__(self)
		
		monster_color = (180, 180, 240)
		
		self.background = ImageBackground(os.path.join("images", "monster.jpeg"))
		self.image = self.background.image
		self.rect = self.image.get_rect()

		self.radar_swipe = RadarSwipe((250, 0, 0), 16, 4)
		self.monster_counter = MonsterCounter(monster_color)
		self.monster_counter.rect.center = (70, 100)

		self.sprite_group = pygame.sprite.LayeredDirty()
		self.sprite_group.add(self.background, layer=0)
		self.sprite_group.add(self.radar_swipe, layer = 1)
		#self.sprite_group.add(self.monster_counter, layer = 1)

		label = self.monster_counter.get_font(28).render("monsters", 1, (250, 250, 250), (0,0,0))
		self.image.blit(label, (15, 170)) 

		self.dirty_rects = []
		self.clean_background = self.image.copy()
		self.sprite_group.clear(self.image, self.clean_background)

	def render(self, screen, __force = False):
		if __force:
			self.sprite_group.clear(self.image, self.clean_background)

		self.dirty_rects = self.sprite_group.draw(screen)
		if len(self.dirty_rects) > 0:
			self.sprite_group.clear(screen, self.clean_background)
 
	def update(self):
		if (self.radar_swipe.on_edge())
			self.monster_counter.update()
			nearby_devices = bluetooth.discover_devices()
			self.number_of_monsters = len(nearby_devices)

		self.sprite_group.update()
		pygame.display.update(self.dirty_rects)

	def handle_event(self, event):
		for sprite in self.sprite_group.sprites():
			if hasattr(sprite, "handle_event"):
			 sprite.handle_event(event)

	def activate(self):
		self.sprite_group.remove_sprites_of_layer(0)
		self.sprite_group.add(self.background, layer=0)
		dirty = 1
		return self


