from kivymd.uix.list import OneLineIconListItem
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivy.lang import Builder
Builder.load_string('''
<IconListItem>:
	text: root.text
	IconLeftWidget:
		icon:root.icon

''')


class IconListItem(OneLineIconListItem, ButtonBehavior):
	icon = StringProperty()
	text = StringProperty()