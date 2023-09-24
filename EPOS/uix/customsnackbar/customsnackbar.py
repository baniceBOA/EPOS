from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
Builder.load_string(
'''
<CustomSnackbar>
	MDIconButton:
		pos_hint: {'center_y': .5}
		icon: root.icon
		opposite_colors: True
	MDLabel:
		id: text_bar
		markup:True
		size_hint_y: None
		height: self.texture_size[1]
		text: root.text
		font_size: root.font_size
		theme_text_color: 'Custom'
		text_color: get_color_from_hex('ffffff')
		shorten: True
		shorten_from: 'right'
		pos_hint: {'center_y': .5}
'''
	)


class CustomSnackbar(BaseSnackbar):
	text = StringProperty(None)
	icon = StringProperty('bell')
	font_size = NumericProperty("15sp")