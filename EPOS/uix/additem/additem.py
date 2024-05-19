from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_hex_from_color


class AddItem(MDBoxLayout):
	''' class add items to the invetory '''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint_y = None
		self.height = 700
		#self.md_bg_color = [120/255, 120/255, 120/255, 1]
		self.scroll = MDScrollView()
		self.box = MDBoxLayout()
		self.box.adaptive_size = True
		self.box.spacing = '2sp'
		self.box.orientation = 'vertical'
		self.item_name = MDTextField(hint_text='Item Name', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_name.bind(on_text=self.validate_strings)
		self.item_quantity = MDTextField(hint_text='Quantity', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_quantity.bind(on_text=self.validate_integer)
		self.item_unit = MDTextField(hint_text='Unit', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_unit.bind(on_text=self.validate_strings)
		self.item_price = MDTextField(hint_text='Price', helper_text_mode='on_error', helper_text='Invalid input')

		self.item_price.bind(on_text=self.validate_integer)
		self.add_image_btn = AddImage()
		self.add_image_btn.ids.add_image_btn_id.bind(on_release=self.choose_image)
		self.save_btn = MDRaisedButton(text='SAVE')
		self.save_btn.bind(on_release=self.save_item)
		self.box.add_widget(self.item_name)
		self.box.add_widget(self.item_quantity)
		self.box.add_widget(self.item_unit)
		self.box.add_widget(self.item_price)
		self.box.add_widget(self.add_image_btn)
		self.box.add_widget(self.save_btn)
		self.scroll.add_widget(self.box)
		self.add_widget(self.scroll)

	def save_item(self, *args):
		''' save the items in the database '''
		from time import time
		item_name = self.item_name.text
		item_quantity = self.item_quantity.text
		item_unit = self.item_unit.text
		item_price = self.item_price.text
		input_fields = [self.item_name,self.item_quantity, self.item_unit,self.item_price]
		self.state = True
		for inpt in input_fields:
			self.validate_otg(inpt)


		if not self.state:
			CustomSnackbar(text='[color='f'{get_hex_from_color([1.0,0.2, 0.2, 0.8])}' ']Make sure all the field as filled[/color]').open()
			self.state = True
		else:
			items = Items( id=int(time()), name=self.item_name.text, quantity=self.item_quantity.text, unit=self.item_unit.text, price=self.item_price.text, description='In stocl')
			session.add(items)
			session.commit()
			for inpt in input_fields:
				self.clean_inputs(inpt)
			CustomSnackbar(text='[color='f'{get_hex_from_color([1.0,0.2, 0.2, 0.8])}'']Saved Succesfully[/color]').open()
	
	def validate_otg(self, instance):
		if not instance.text:
			instance.error = True
			instance.helper_text = 'This field Is required'
			self.state = False
	def clean_inputs(self, instance):
		instance.text = ''

	def choose_image(self, *args):
		from plyer import filechooser
		filechooser.open_file(on_selection=self.selection)
	def selection(self, selection):
		self.image_path = selection[0]
		self.add_image_btn.source = self.image_path
		print(self.image_path)


	def validate_strings(self, instance):
		''' validate the text of the textfield '''
		if instance.text:
			instance.error = False

		if instance.text == '' or instance.text == ' ':
			instance.error = True
			instance.helper_text = 'this field cannot be blank'
		if len(instance.text) > 32:
			instance.error = True
			instance.helper_text = ' use a shorter name'
		
	def validate_integer(self, instance):
		''' validate the integer fields '''
		if instance.text == '' or instance.text == ' ' :
			instance.error = True
			instance.helper_text = 'this field cannot be blank'
		elif instance.text:
			for char in instance.text:
				if char not in digits:
					instance.error = True
					instance.helper_text = 'input number only (0-9)'
					break
			else:
				instance.error = False
		else:
			instance.error = False
