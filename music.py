import pygame, os

class MusicPlayer:
	file_list = []
	current_song_index = -1

	def __init__(self):
		self.load_file_list()
		if len(self.file_list) >= 1:
			self.current_song_index = 0
		self.playing = False

	def play(self):
		if not(self.playing):
			self.load_song()
			pygame.mixer.music.play()
		else:
			pygame.mixer.music.unpause()
		self.playing = True

	def is_playing(self):
		return self.playing

	def stop(self):
		pygame.mixer.music.stop()
		self.playing = False

	def pause(self):
		pygame.mixer.music.pause()

	def unpause(self):
		if self.playing:
			pygame.mixer.music.unpause()
		else:
			self.play()

	def toggle_audio(self):
		if pygame.mixer.music.get_volume() > 0.0:
			pygame.mixer.music.set_volume(0.0)
		else:
			pygame.mixer.music.set_volume(1.0)

	def next(self):
		self.stop()
		self.current_song_index += 1
		if self.current_song_index >= len(self.file_list):
			self.current_song_index = 0
		self.play()

	def previous(self):
		self.stop()
		self.current_song_index -= 1
		if (self.current_song_index < 0) and (len(self.file_list) >= 1):
			self.current_song_index = len(self.file_list) - 1
		self.play()

	def load_song(self):
		if len(self.file_list) > 0:
			print "Loading song %s" % (self.file_list[self.current_song_index])
			pygame.mixer.music.load(self.file_list[self.current_song_index])


	def load_file_list(self):
		self.file_list = []
		for filename in os.listdir ("music"):
			if filename.startswith("."):
				continue

			print "Found song %s" % (filename)
			self.file_list.append(os.path.join("music", filename))

