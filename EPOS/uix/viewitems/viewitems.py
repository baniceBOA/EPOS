from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton

Builder.load_string('''<ViewItems>:
	orientation:'vertical'
	MDTopAppBar:
		left_action_items:[['arrow-left', lambda x:app.return_home()]]
		right_action_items:[['refresh', lambda x:root.get_items()]]
	MDScrollView:
		pos_hint:{'top':0.8}
		MDList:
			id:items_list
			IconListItem
				icon:'bag-carry-on'
				text:'items'
	MDFloatingActionButton:
		icon:'plus'
		pos_hint:{'center_x':0.9, 'center_y':0.89}
		on_release:root.add_item()

''')
class ViewItems(MDBoxLayout):
	dialog = None

	def get_items(self):
		from .tools import get_invetory
		items = get_invetory()
		for v in self.ids.items_list.children[:]:
			self.ids.items_list.remove_widget(v)
		for item in items:
			i = ThreeLineListItem(text='code:'+str(item['id']), secondary_text='name:'+ item['name'], tertiary_text='price:'+str(item['price']) )
			self.ids.items_list.add_widget(i)
	def add_item(self):
		self.dialog = MDDialog(
				title='ADD ITEM',
				type = 'custom',
				content_cls = AddItem(),
				buttons = [MDFlatButton(text='Cancel', on_release=self.close)]

			)
		self.dialog.open()
	def close(self, *args):
		self.dialog.dismiss() 