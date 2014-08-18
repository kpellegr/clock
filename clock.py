import pygame, sys, os, time, platform
from pygame.locals import *
from userevents import *
from clockscene import ClockScene
from backgrounds import Background, EmptyBackground, SlideshowBackground, EfimeridesBackground
from controlcenter import TwoStateButton, PushButton, ControlScene
from monsterscene import MonsterScene
from music import MusicPlayer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LEFT_BUTTON = 1

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240


def on_raspberry():
	return platform.uname()[4].startswith("arm")

def set_transparant_cursor():
	transparant_cursor = (
		"        ",
		"        ",
		"        ",
		"        ",
		"        ",
		"        ",
		"        ",
		"        ")
	cursor, mask = pygame.cursors.compile(transparant_cursor)
	pygame.mouse.set_cursor((8,8), (4,4), cursor, mask)

class PiTFT(object):
	backlight_status = True
	backlight_path = "/sys/class/gpio/gpio252/value"

	def __init__(self):
		self.set_backlight(True)

	def set_backlight(self, __status):
		self.backlight_status = __status
		if not(on_raspberry()):
			return
		try:
			with open(self.backlight_path, "w") as bfile:
				bfile.write("%d" % (bool(__status)))
		except:
			pass

	def get_backlight(self):
		return self.backlight_status


# =========================
# MAIN LOOP
# =========================

pygame.init()
FPS = 10 # frames per second setting
SLEEP_TIMEOUT = 300 # 5 minutes
fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)
if on_raspberry():
	pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	set_transparant_cursor()

pygame.display.set_caption('Clock')
tft = PiTFT()

background = pygame.Surface(screen.get_size())
efimerides_background = EfimeridesBackground();
slideshow_background = SlideshowBackground(20);
clock_scene = ClockScene(efimerides_background)
monster_scene = MonsterScene()
music_player = MusicPlayer()

BTN_LIGHT      = 101
BTN_SOUND      = 102
BTN_EFIMERIDES = 103
BTN_SLIDESHOW  = 104
BTN_MONSTER    = 105
BTN_MUSIC      = 106
BTN_SOUNDON    = 107
BTN_SOUNDOFF   = 108

BTN_PLAY  = 201
BTN_PAUSE = 202
BTN_PREV  = 203
BTN_NEXT  = 204

control_scene = ControlScene()
control_scene.append(TwoStateButton(dict(value=BTN_LIGHT, icon="371.png"), dict(value=BTN_LIGHT, icon="371.png"), True))

control_scene.append(PushButton("318.png", BTN_EFIMERIDES))
control_scene.append(PushButton("126.png", BTN_SLIDESHOW))
control_scene.append(PushButton("325.png", BTN_MONSTER))

control_scene.append_split();

control_scene.append(TwoStateButton(dict(value=BTN_SOUND, icon="074.png"), dict(value=BTN_SOUND, icon="076.png"), True))
control_scene.append(TwoStateButton(dict(value=BTN_PLAY, icon="115.png"), dict(value=BTN_PAUSE, icon="113.png")))
control_scene.append(PushButton("122.png", BTN_PREV))
control_scene.append(PushButton("120.png", BTN_NEXT))

# ---------
# Game loop
# ---------

running = True;
current_scene = clock_scene

SLEEP_TRIGGER = UserEvent.create_event()
pygame.time.set_timer(SLEEP_TRIGGER, SLEEP_TIMEOUT * 1000)

while running:
	for event in pygame.event.get():
		event_handled = False

		if event.type == QUIT:
			running = False
		if event.type == SLEEP_TRIGGER:
			#print "Turning off backlight"
			tft.set_backlight(False)
			event_handled = True
		if (event.type == MOUSEBUTTONUP):
			pygame.time.set_timer(SLEEP_TRIGGER, SLEEP_TIMEOUT * 1000)
			if tft.get_backlight(): # screen is already active
				if (current_scene != control_scene):
					current_scene = control_scene.activate()
					event_handled = True
			else: # just turn on backlight and nothing else
				#print "Turning on backlight"
				tft.set_backlight(True)
				event_handled = True
		
		# FOR DEBUGGING ONLY
		if event.type == KEYDOWN:
			pygame.time.set_timer(SLEEP_TRIGGER, SLEEP_TIMEOUT * 1000)
			if event.key == K_ESCAPE:
				running = False
				event_handled = True
			if event.key == K_s:
				#Slideshow
				print "Going to slideshow"
				current_scene = clock_scene.activate()
				clock_scene.set_background(slideshow_background)
				event_handled = True
			elif event.key == K_e:
				#Efimeriden
				print "Going to efimerides"
				current_scene = clock_scene.activate()
				clock_scene.set_background(efimerides_background)
				event_handled = True
			elif event.key == K_l:
				#Licht in de gang aan/uit
				event_handled = True
			elif event.key == K_m:
				#Monsterteller
				print "Going to monster scene"
				current_scene = monster_scene.activate()
				event_handled = True
			elif event.key == K_c:
				#Monsterteller
				print "Going to control scene"
				current_scene = control_scene.activate()
				event_handled = True
			else:
				event_handled = False

		if not(event_handled):
			#print "Event not handled"
			res = current_scene.handle_event(event)
			if res == BTN_LIGHT:
				#print "Toggeling light"
				event_handled = True;
			elif res == BTN_EFIMERIDES:
				#print "To efemerides"
				current_scene = clock_scene.activate()
				clock_scene.set_background(efimerides_background)
				event_handled = True
			elif res == BTN_SLIDESHOW:
				#print "To slideshow"
				current_scene = clock_scene.activate()
				clock_scene.set_background(slideshow_background)
				event_handled = True
			elif res == BTN_MONSTER:
				#print "To monster"
				current_scene = monster_scene.activate()
				event_handled = True
			elif res == BTN_PLAY:
				#print "Start playing music"
				music_player.play()
				event_handled = True
			elif res == BTN_PAUSE:
				#print "Pause music"
				music_player.pause()
				event_handled = True
			elif res == BTN_PREV:
				#print "Previous song"
				music_player.previous()
				event_handled = True
			elif res == BTN_NEXT:
				#print "Next song"
				music_player.next()
				event_handled = True
			elif res == BTN_SOUND:
				#print "Toggle audio"
				music_player.toggle_audio()
				event_handled = True
			else:
				event_handled = True

	current_scene.update()
	current_scene.render(screen)

	fpsClock.tick(FPS)

# End of game loop (running = False)
tft.set_backlight(True)
pygame.quit()

