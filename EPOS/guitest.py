from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivy.uix.carousel import Carousel
from kivymd.theming import ThemableBehavior
from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.metrics import dp

from kivy.core.text import LabelBase
import os
kv = '''

<CardContainer>:
	md_bg_color:[0, 0.5, 0, 0.5]
	pos_hint:{'center_x':0.5, 'center_y':0.5}
	orientation:'vertical'
	size_hint_y:None
	height:self.minimum_height
	size_hint_x:None
	width:dp(150)*root.scale
	radius:[int(25*root.scale/4)]

	FitImage:
		source:root.source
		size_hint_x:None
		size_hint_y:None
		width:dp(150)*root.scale
		height:dp(100)*root.scale
		radius:[int(25*root.scale/4), int(25*root.scale/4), 0, 0]
	
	MDLabel:
		font_name:'BPoppins'
		font_size:'25dp'
		size_hint_y:None
		height:self.texture_size[1]
		text:root.text
		halign:'center'
		
		
	MDLabel:
		font_name:'IPoppins'
		font_size:'15dp'
		size_hint_y:None
		height:self.texture_size[1]
		text:root.secondary_text
		halign:'center'

<ItemCircle>:
	size_hint_x:None
	canvas.before:
		Color:
			rgba:root._circle_color 
		Line:
            circle: [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2, self.width / 2]
            width: dp(1)

<CustomCarouselItem>:

<CustomCarousel>:
	orientation:'vertical'

	MyCarousel:
		auto:root.auto
		id:carousel
	MDFloatLayout:
		id:rounded_box
		size_hint_y:None
		height:circle_box.y + circle_box.height*2

	GhostCircle:
		id:ghost_circle
	MDBoxLayout:
		id:circle_box
		pos: rounded_box.width / 2 - self.width / 2, rounded_box.height / 2 - self.height / 2
		size_hint: None,None
		size: self.minimum_width, root.circles_size
		spacing: root.circles_size / 2




<GhostCircle@Widget>:
	size_hint:(None, None)
	size:dp(20),dp(20)
	canvas.before:
		Color:
			rgba:app.theme_cls.primary_color
		Ellipse:
			pos:self.pos
			size:self.size




MDBoxLayout:
	orientation:'vertical'
	CustomCarousel:
		auto:True
		id:anim_carousel
						
	'''

class ItemCircle(ThemableBehavior, Widget):
	_circle_color = ListProperty()


class CustomCarouselItem(MDBoxLayout):
	pass

class CustomCarousel(ThemableBehavior, MDBoxLayout, EventDispatcher):
	circles_size = NumericProperty(dp(20))
	circle_color = ListProperty()
	auto = BooleanProperty(False)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(lambda x: self._update())

	def _update(self):
		self.ids.ghost_circle.size = [self.circles_size, self.circles_size]

	def on_size(self, *args):
		self.ids.carousel.size = self.size

	def add_widget(self, widget, index=0, canvas=None):
		if issubclass(widget.__class__, CustomCarouselItem):
			self.ids.carousel.add_widget(widget)
		else:
			super().add_widget(widget, index=index, canvas=canvas)


class MyCarousel(ThemableBehavior, Carousel):
	auto = BooleanProperty(False)
	''' auto 
			``BooleanProperty``
				make the loading of next carousel automatic defaults to **FALSE**
	'''

	def __init__(self, **kwargs):
		'''
		This is a custom carousel that when moved in moves with a circle below it 
		to show it's position

		'''
		super(MyCarousel, self).__init__(**kwargs)
		Clock.schedule_once(lambda x: self.add_circle())


	def add_circle(self):
		''' 
		*Add Circle to the the layout to signify the current carousel 
		returntype: return None
		'''
		self.total_circle = len(self.slides)-1
		if self.parent.circle_color:
			circle_color =self.parent.circle_color
		else:
			circle_color = self.theme_cls.primary_color
		for _ in range(self.total_circle+1):
			self.parent.ids.circle_box.add_widget(ItemCircle(
				width=self.parent.circles_size,
				_circle_color=circle_color))
			self._current_circle = self.total_circle
		Clock.schedule_once(lambda x: self.set_current_circle())

	def set_current_circle(self, mode=None):
		''' 
		* Place the ghost circel above the item circel in the circel_box.
		The effect of this will make the ItemCircle to look highlighted
		the **index** here refers to the slide of the that is in current view
		'''
		if mode == 'next':
			self.parent.ids.ghost_circle.pos = self.parent.ids.circle_box.children[self._current_circle].pos
			self._current_circle -= 1
			if self._current_circle < 0:
				self.reset()
		if mode == 'previous':
			self.parent.ids.ghost_circle.pos = self.parent.ids.circle_box.children[self._current_circle].pos
			self._current_circle += 1
			if self._current_circle > self.total_circle:
				self.reset()
		if mode == None:
			self.parent.ids.ghost_circle.pos = self.parent.ids.circle_box.children[max(self.index, self.total_circle)].pos


			

	def reset(self):
		self.load_slide(self.slides[0])
		self._current_circle = self.total_circle
	def on_touch_up(self, touch):
		if abs(self._offset) > self.width*self.min_move:

			if self._offset > 0:
				self.set_current_circle('previous')
			if self._offset < 0:
				self.set_current_circle('next')
		return super().on_touch_up(touch)

	def on_auto(self, *args):
		''' Trigger the automation of slide moving '''
		self.loop = True
		Clock.schedule_interval(self.automate,3)

	def automate(self, interval):
		''' Implements the automatio of slides after a time interval '''

		self.load_next(mode='next')
		index =abs(self.total_circle-self.index)
		self.set_current_circle_auto(index)


	def set_current_circle_auto(self, index):
		''' set the circle after every automation '''

		anim = Animation(pos=self.parent.ids.circle_box.children[index].pos, t="out_quad", duration=0.6)
		anim.start(self.parent.ids.ghost_circle)
		#self.parent.ids.ghost_circle.pos = self.parent.ids.circle_box.children[index].pos









default_image = os.path.join(r'C:\Users\HP\Pictures', '_yibs_ke-20220923-0001.webp')

class CardContainer(MDCard):
	text = StringProperty('')
	secondary_text = StringProperty('')
	source = StringProperty(default_image)
	scale = NumericProperty(1.5)


class TestApp(MDApp):
	def build(self):
		return Builder.load_string(kv)

	def on_start(self):
		for i in range(10):
			carouselitem = CustomCarouselItem()
			carouselitem.pos_hint = {'center_x':0.5, 'center_y':0.5}
			card = CardContainer(text='MILK', secondary_text='15% off', scale=3.5, pos_hint={'x':0.5})
			carouselitem.add_widget(card)
			self.root.ids.anim_carousel.add_widget(carouselitem)



if __name__ == '__main__':
	LabelBase.register(name='IPoppins', fn_regular=os.path.join('fonts','Poppins-Italic.ttf'))
	LabelBase.register(name='BPoppins', fn_regular=os.path.join('fonts', 'Poppins-Bold.ttf'))
	LabelBase.register(name='EBPoppins', fn_regular=os.path.join('fonts', 'Poppins-ExtraBold.ttf'))
	LabelBase.register(name='TIPoppins', fn_regular=os.path.join('fonts', 'Poppins-ThinItalic.ttf'))

	TestApp().run()