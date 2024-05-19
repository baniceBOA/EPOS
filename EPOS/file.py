from kivymd.color_definitions import colors
#from pprint import pprint
from kivy.properties import ListProperty
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
import random
import os

class CustomColors:
	def __init__(self, rgba_color=[], name=None):
		''' create a customes colors based on material design pattern '''
		self.colors = rgba_color
		self.name = name
		self.customcolor = {}

		self.keys = ['50','100','200','300','400','500','600','700','800','900','A100','A200','A400','A700']
	def generate_colors(self):
		''' generate colors to be mapped to the keys '''
		self.mycolors = {}
		if isinstance(self.colors, (list, tuple)) and len(self.colors) == 4:
			rate = (22/7)
			scale = 1
			for key in self.keys:
				gen_color = []
				for c in self.colors:
					color = self.normalize(c, scale, rate)
					gen_color.append(color)
				gen_color.reverse()
				self.mycolors[key] = get_hex_from_color(gen_color)
				rate = rate**0.5
				scale = scale**3/2
		return self.mycolors

	def normalize(self, value, scale, rate):
		''' prevent the value fro going beyond the expected '''
		color_value = value*scale+rate
		while color_value > 1:
			# we need to normalize the color value 
			color_value *= 0.1
		else:
			return color_value

	def color(self):
		''' give the schema a color code to use '''
		if self.name == None:
			self.name = 'CustomColor'
		self.customcolor[self.name] = self.generate_colors()
		return  self.customcolor



class ViewColorTemplate(MDBoxLayout):
	color = ListProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.custom_theme = CustomColors(rgba_color=self.color, name='Berny').color()
		
		self.scroll = MDScrollView()
		self.color_container = MDBoxLayout(orientation='vertical', adaptive_height=True)
		self.add_widget(self.scroll)
		self.scroll.add_widget(self.color_container)
		dummy = self.custom_theme['Berny']
		color_dict = dummy
		for key, value in color_dict.items():
			theme = get_color_from_hex(value)
			print(theme)
			color_tag = MDFlatButton(text='color', pos_hint={'center_x':0.5})
			color_tag.md_bg_color = theme
			self.color_container.add_widget(color_tag)

class TestColorTheme(MDApp):
	def build(self):
		return ViewColorTemplate(color=[random.random(),random.random(),random.random(),random.random()])

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT

class CustomFontApp(App):
   def build(self):
      # Register the custom font with Kivy
      LabelBase.register(name='CustomFont', fn_regular=os.path.join('fonts','Poppins-Light.ttf'))
      LabelBase.register(name='RegularFont', fn_regular=os.path.join('fonts','Poppins-Regular.ttf'))
      LabelBase.register(name='BoldFont', fn_regular=os.path.join('fonts','Poppins-Bold.ttf'))
      LabelBase.register(name='MediumFont', fn_regular=os.path.join('fonts','Poppins-Medium.ttf'))
      LabelBase.register(name='ThinFont', fn_regular=os.path.join('fonts','Poppins-Thin.ttf'))
      LabelBase.register(name='ItalicFont', fn_regular=os.path.join('fonts','Poppins-Italic.ttf'))
      box = MDBoxLayout(orientation='vertical')
      # Create a label widget and set its font to the custom font
      label = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='CustomFont', font_size='15sp')
      label1 = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='RegularFont', font_size='15sp')
      label2 = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='BoldFont', font_size='15sp')
      label3 = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='MediumFont', font_size='15sp')
      label4 = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='ThinFont', font_size='15sp')
      label5 = Label(text='Tutorialspoint!!! \n Simply easy learning at your fingertips..... ', font_name='ItalicFont', font_size='15sp')
      box.add_widget(label)
      box.add_widget(label1)
      box.add_widget(label2)
      box.add_widget(label3)
      box.add_widget(label4)
      box.add_widget(label5)
      return box




   

	
if __name__ == '__main__':
	'''
	
	color_dict = colors['CustomColor']
	for key, value in color_dict.items():
		theme = get_color_from_hex(value)
		print(len(theme), value)
	#
	'''
	#TestColorTheme().run()
	#mycolors = CustomColors(rgba_color=[1,1,1,0], name='Berny').color()
	#colors['Berny'] = mycolors['Berny']
	#print(colors)
	CustomFontApp().run()
	
		





