from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.camera import Camera
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
import os

class Scanner(MDFloatLayout):
	play = BooleanProperty(False)
	close_btn = ObjectProperty()
	images = ListProperty()
	camera = ObjectProperty()
	def __init__(self, **kwargs):
		''' scan the qrcode for the item '''
		super().__init__(**kwargs)
		self.size_hint = (None,None)
		self.width = Window.size[0]*0.55
		self.height = Window.size[1]*0.52
		
		#self.camera.resolution = (dp(Window.size[0]), dp(Window.size[1]))
		self.close_btn = MDFloatingActionButton(icon='close')
		self.close_btn.pos_hint = {'center_x':0.9, 'center_y':0.9}
		
		
		
		self.pos_hint = {'center_x':0.5, 'center_y':0.5}
		Clock.schedule_once(self.prepopulate)

		Clock.schedule_interval(self.cache_management, 1/0.5)

	def close_scanner(self, *args):
		''' close the scanner and also the camera'''
		self.camera.play = False
		if self.close_btn in self.children[:]:
			self.remove_widget(self.close_btn)
		if self.thread.is_alive():
			self.thread.join(timeout=0.001)
		

	def start_scanner(self):
		''' start the scanner of the application '''
		def starter():
			self.create_camera()
		self.thread = Thread(target=starter, args=( ))

		self.thread.start()

	@mainthread
	def update(self, instance):
		if instance in self.children[:] and self.close_btn in self.children[:]:
			pass
		else:
			self.add_widget(instance)
		if self.close_btn in self.children[:]:
			self.remove_widget(self.close_btn)
			self.add_widget(self.close_btn)
	@mainthread
	def create_camera(self):
		self.camera = Camera(index=-1, resolution=(dp(Window.size[0]/2), dp(Window.size[1]/2)), size_hint=(None, None), width=Window.size[0]/2, height=Window.size[1]/2)
		self.camera.play = True
		self.camera.pos_hint = {'center_x':0.5, 'center_y':0.5}
		self.start_scanning()
		self.update(self.camera)

	def scan(self, image):
		''' scan the image for the codes '''
		from .tools import CodeScanner

		codescanner = CodeScanner(image)
		codescanner.scan()
	def on_images(self, *args):
		pic = self.images[-1]
		self.scan(pic)

	@mainthread
	def capture_image(self, interval):
		''' capture the image as the camera see it'''
		from time import time
		import os
		parent = os.path.dirname(__file__)
		filepath = os.path.join(parent, 'temp_images')
		if os.path.isdir(filepath):
			pass
		else:
			#make the dir
			os.makedirs(os.path.join(parent, 'temp_images'))
		file_name = str(time()).replace('.', '_') + '.png'
		filename = os.path.join(filepath, file_name)
		if self.camera in self.children[:]:
			self.camera.export_to_png(filename)
			self.images.append(filename)

	def start_scanning(self):
		if self.camera.play == True:
			Clock.schedule_interval(self.capture_image, 0.5)
		else:
			Clock.unschedule(self.capture_image)

	def cache_management(self, interval):
		''' prevent from making too many images '''
		parent = os.path.dirname(__file__)
		filepath = os.path.join(parent, 'temp_images')
		if  len(os.listdir(filepath)) > 20:
			for file in os.listdir(filepath)[:len(os.listdir(filepath))-20]:
				filename = os.path.join(filepath, file)
				os.remove(filename)

	def prepopulate(self, interval):
		''' load previous images from the temp file '''
		parent = os.path.dirname(__file__)
		filepath = os.path.join(parent, 'temp_images')
		for file in os.listdir(filepath):
			filename = os.path.join(filepath, file)
			self.images.append(filename)
