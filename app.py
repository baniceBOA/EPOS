''' This is a simple electronic point of sale application '''


from model import Items, session
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable 
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import OneLineIconListItem, OneLineAvatarIconListItem
from kivymd.uix.card import MDCard
from kivymd.toast import toast
from kivy.uix.camera import Camera
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_hex_from_color
from kivy.core.window import Window
from kivymd.uix.snackbar import BaseSnackbar
from string import digits
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock, mainthread
from threading import Thread
from kivymd_extensions import akivymd
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

#import Tools
from tools import LoginUser


kv = '''
#:import Window kivy.core.window.Window
<CircularProgressbar>:
    canvas.before:
        Color:
            rgba:root.bar_color+[0.1]
        Line:
            width:root.bar_width
            ellipse:(self.x, self.y, self.width, self.height, 0, 360)
    canvas.after:
        Color:
            rgb:root.bar_color
        Line:
            width:root.bar_width
            ellipse:(self.x, self.y, self.width, self.height, 0, root.set_value*3.6)
    MDLabel:
        text:root.text
        pos_hint:{'center_x':0.5, 'center_y':0.5}
        font_size:root.text_font_size
        halign:'center'
        color:root.bar_color

<IconListItem>:
	text: root.text
	IconLeftWidget:
		icon:root.icon

<AvatarListItem>:
	text:root.text
	IconLeftWidget:
		icon:root.icon_left
	IconRightWidget:
		theme_icon_color:"Custom"
		icon_color:'red'
		icon:root.icon_right
<Notification>
    padding: dp(10)

    MDLabel:
        text:root.text
        theme_text_color: "Secondary"
        halign: "left"

    MDIconButton:
        id: button
        icon: "close"
        halign: "right"
        valign: "center"
<ErrorDialog>:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: root.title
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: root.message
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Dismiss"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}
<LoginView>:
	username:username
	password:password
	padding:[dp(8), dp(8), dp(8), dp(25)]
    spacing:dp(25)
    radius:dp(25)
    md_bg_color:[1, 1, 1, 1]
	MDBoxLayout:
		orientation:'vertical'
		FitImage:
			source:'assets/face.png'
			radius:[dp(100), dp(100), dp(100), dp(100)]
			size_hint:(None, None)
			size:(dp(200), dp(200))
			pos_hint:{'center_x':0.5}

		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(20)	
		MDLabel:
			text:root.error_text
			size_hint_y:None
			font_size:dp(3)
			font_style:'H2'
			height:dp(5)
			pos_hint:{'center_x':0.5}
		MDTextField:
			id:username
			hint_text:'username'
			helper_text_mode:'on_error'
			pos_hint:{'center_x':0.5}
			mode:'round'
			padding:[0, 0, 0, dp(25)]
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
		MDTextField:
			id:password
			helper_text_mode:'on_error'
			mode:'round'
			hint_text:'password'
			icon_right:'eye'
			password:True
			pos_hint:{'center_x':0.5}
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(20)
		MDFillRoundFlatButton:
			text:'login'
			on_release:app.login(username, password)
			pos_hint:{'center_x':0.5}
		Widget:
<SignUpUser>:
	username:signup_username
	password:signup_password
	repeat_password:repeat_password
	email:signup_email

	spacing:dp(25)
	MDBoxLayout:
		orientation:'vertical'
		MDLabel:
			text:'SIGN UP'
			font_size:dp(5)
			font_style:'H5'
			halign:'center'
		MDTextField:
			id:signup_username
			mode:'round'
			required:True
			hint_text:'username'
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
		MDTextField:
			id:signup_email
			mode:'round'
			required:True
			hint_text:'email'
			validator:'email'
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
		MDTextField:
			id:signup_password
			mode:'round'
			required:True
			hint_text:'password'
			on_text:root.password_strength
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
		MDTextField:
			id:repeat_password
			mode:'round'
			required:True
			hint_text:'repeat password'
			on_text:root.compare_password
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
		MDFillRoundFlatButton:
			id:signup_btn
			text:'sign up'
		




<Sales>:

<ClickableTextFieldRound>:
	size_hint_y: None
	height: text_field.height
	MDTextField:
		id: text_field
		hint_text: root.hint_text
		helper_text:root.helper_text
		helper_text_mode:root.helper_text_mode
		text: root.text
		password: True
		mode:'round'
		icon_left: root.text_field_icon
		on_text_validate:root.validate
	MDIconButton:
		id:password_field_clickable
		icon: root.icon
		pos_hint: {"center_y": .5}
		pos: text_field.width - self.width + dp(8), 0
		theme_text_color: "Hint"
		on_release:root.toggle_eye()
		 

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

<Invetory>:
	orientation:'vertical'
	datatable:datatable
	MDToolbar:
		title:'INVETORY'
	MDRelativeLayout:
		MDIconButton:
			icon:'trash-can'
			text_color:[1,0.2,0.5,1]
			theme_text_color:'Custom'
			pos_hint:{'center_x':0.9, 'center_y':0.9}
		MDIconButton:
			icon:'lead-pencil'
			text_color:[0,1,0,1]
			theme_text_color:'Custom'
			pos_hint:{'center_x':0.8, 'center_y':0.9}
	MDBoxLayout:
		id:datatable

<ViewItems@MDBoxLayout>:
	orientation:'vertical'
	MDTopAppBar:
		left_action_items:[['arrow-left', lambda x:app.return_home()]]
	MDScrollView:
		pos_hint:{'top':0.8}
		MDList:
			id:items_list
			IconListItem
				icon:'bag-carry-on'
				text:'items'

<AdminDashBoard>:
	screen_manager:sm
	MDTopAppBar:
		title:'ADMIN DASHBOARD'
		left_action_items:[['arrow-left', lambda X:app.return_home()]]
		pos_hint:{'top':1}

	MDGridLayout:
		cols:3
		size_hint_y:None
		height:Window.size[1]*.80
        padding:[dp(8),dp(8),dp(8),dp(20)]
        spacing:dp(5)
        pos_hint:{'top':0.9}

		ElementCard:
			orientation:'vertical'
			size_hint_x:None
			width: Window.size[0]*0.25
			size_hint_y:None
			height:Window.size[1]*0.80

			IconListItem:
				icon:'face-man'
				text:'ADMIN'
				on_release:sm.current = 'admin_screen'

			IconListItem:
				icon:'face-man-profile'
				text:'USERS'
				on_release:sm.current = 'user_screen'
			IconListItem:
				icon:'bag-carry-on'
				text:'iTEMS'

			IconListItem:
				icon:'bitcoin'
				text:'SALES'
				on_release:sm.current= 'sales_screen'
			IconListItem:
				icon:'graphql'
				text:'Statistics'
				on_release:sm.current = 'statistics_screen'
			IconListItem:
				icon:'/assets/face.png'
				text:'signup'
				on_release:sm.current = 'signupuser_screen'
			Widget:

		ElementCard:
			orientation:'vertical'
			size_hint_x:None
			width:Window.size[0]*0.60
			size_hint_y:None
			height:Window.size[1]*0.80
			MDScreenManager:
				id:sm
				MDScreen:
					name:'admin_screen'
					MDBoxLayout:
						MDBoxLayout:
							orientation:'vertical'
							size_hint:(None,None)
							width:dp(250)
							height:dp(200)
							pos_hint:{'top':0.82}
							CircularProgressbar:
								bar_color:[0.3, 0.5, 0.2, 0.7]
								test:'SALES'
								bar_width:10
								size_hint:(None, None)
								size:150, 150

							MDLabel:
								text:'Sales per Month'
						MDBoxLayout:
							orientation:'vertical'
							size_hint:(None,None)
							width:dp(300)
							height:dp(200)
							spacing:dp(8)
							IconListItem:
								icon:'face-man'
								text:'ADMIN NAME '
							MDLabel:
								text:'DATE'
								size_hint_y:None
								height:dp(25)
							MDLabel:
								text:'TIME'
								size_hint_y:None
								height:dp(25)
							Widget:

					MDSeparator:
						size_hint_y:None
						height:dp(25)
					MDLabel:
						text:'RECENT ACTIVITIES'
					MDBoxLayout:
						orientation:'vertical'
						MDScrollView:
							id:recent
					Widget:
				MDScreen:
					name:'statistics_screen'
					AKBarChart:
						x_values: [0, 5, 8, 15]
    					y_values: [0, 10, 6, 8]

				MDScreen:
					name:'user_screen'
					MDList:
						id:user_list
				MDScreen:
					name:'sales_screen'
					AKPieChart:
						items:[{"Python": 40, "Java": 30, "C++": 10, "PHP": 8, "Ruby": 12}]
						size_hint:(None, None)
						size:(dp(300), dp(300))
				MDScreen:
					name:'signupuser_screen'
					SignUpUser:
						pos_hint:{'center_y':0.6, 'center_x':0.5}
                		size_hint_y:None
                		height:Window.size[1]*0.90
                		size_hint_x:None
                		width:Window.size[0]*0.40
		ElementCard:
			orientation:'vertical'
			size_hint_x:None
			width:Window.size[0]*0.12
			size_hint_y:None
			height:Window.size[1]*0.80
			MDLabel:
				text:'What is wrong with you'


	ElementCard:
		size_hint_y:None
		height:dp(45)
		pos_hint:{'top':0.082}
		MDLabel:
			text:'ADMIN DASHBOARD'
			halign:'center'
		

<ElementCard@MDCard>:
    md_bg_color:[1, 1, 1, 0.2]
    padding:dp(8)
    spacing:dp(8)
    radius:dp(25)
    ripple_behavior: False 

<MyToolbar@MDTopAppBar>:
	left_action_items:[['arrow-left', lambda X:app.show_screen('home', 'Back')]]

MDScreen:
	MDScreenManager:
		id:screen_manager
		MDScreen:
			name:'login'
			MDBoxLayout:
				orientation:'vertical'
				MyToolbar:
                    title: app.title
                    left_action_items:[["menu" , lambda x: app.open_drawer()]]
                LoginView:
                	pos_hint:{'center_y':0.6, 'center_x':0.5}
                	size_hint_y:None
                	height:Window.size[1]*0.90
                	size_hint_x:None
                	width:Window.size[0]*0.40
                Widget:
        MDScreen:
			name:'home'
			MDBoxLayout:
				orientation:'vertical'
				MyToolbar:
                    title: app.title
                    left_action_items:[["menu" , lambda x: app.open_drawer()]]
                MDBoxLayout:
                	MDLabel:
                		text:f'Welcome'
                		font_style:'H5'
                		halign:'center'

        MDScreen:
        	name:'admin'
        	AdminDashBoard:
        MDScreen:
        	name:'items'
        	ViewItems:
        MDScreen:
        	name:'sales'
        	MDBoxLayout:
        		orientation:'vertical'
        		MDTopAppBar:
        			title:'SALES'
        			left_action_items:[['arrow-left', lambda x:app.return_home()]]
        		Sales:
    MDNavigationDrawer:
        id: navdrawer

        ScrollView:
            
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True

                MDRelativeLayout:
                    size_hint_y: None
                    height: title_box.height

                    FitImage:
                        source: "texture_blur.png"

                    MDBoxLayout:
                        id: title_box
                        adaptive_height: True
                        padding: dp(24)

                        MDLabel:
                            text: "EPOS APP"
                            font_style: "H5"
                            size_hint_y: None
                            height: self.texture_size[1]
                            shorten: True

                MDList:
                    IconListItem:
                    	id:sales_view
                    	icon:'pound'
                    	text:'Sales'
                    	on_release:app.change_screen(sales_view)
                    		

                    IconListItem:
                    	id:item_list
                    	icon:'bag-carry-on'
                    	text:'Items'
                    	on_release:app.change_screen(item_list)
                    		
                    AvatarListItem:
                    	id:notification_view
                    	icon_left:'shield-alert'
                    	icon_right:'numeric-1-circle-outline'
                    	text:'notification'
                    	on_release:app.change_screen(notification_view)

                    IconListItem:
                    	id:admin_view
                    	icon:'shield-lock'
                    	text:'ADMIN'
                    	on_release:app.change_screen(admin_view) 

'''

class CircularProgressbar(AnchorLayout):
    text = StringProperty('0%')
    bar_color = ListProperty([0, 1, 0])
    bar_width = NumericProperty(5)
    set_value = NumericProperty(50)
    counter = 0
    text_font_size = StringProperty('40sp')
    color_count = NumericProperty(0)
    duration = NumericProperty(1.5)
    value = NumericProperty(45)
    current_value = NumericProperty(0)
    mode = 'free'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.mode == 'free':
            Clock.schedule_once(self.free_mode, 1)
        else:
            Clock.schedule_once(self.animate, 1)
    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter, self.duration/self.value)

    def percent_counter(self, *args):
        if self.counter < self.value:
            self.counter += 1
            self.percent = self.counter/self.value*100
            self.set_value = self.percent
            self.text = f'{int(self.percent)}%'
        else:
            Clock.unschedule(self.percent_counter)
    def on_value(self, instance, value):
        self.set_value = value
        self.text = f'{int(self.value)}%'
    def free_mode(self, *args):
        self.stop = False
        if not self.stop:
            Clock.schedule_once(self.free_fall, 0.2)
        if self.counter == 0:
            Clock.schedule_once(self.free_fall, 0.2)

    def free_fall(self, *args):
        def run():
            from time import sleep
            maximum = 100
            while self.counter < maximum:
                self.counter += 1
                self.free_update(self.counter)
                sleep(0.09)
                self.text = ' '

                if self.counter == 99:
                    self.counter = 0
                if self.stop == True:
                    self.counter = 0
                    break
        Thread(target=run, args=()).start()
    @mainthread
    def free_update(self, counter):

        self.set_value=counter

class IconListItem(OneLineIconListItem, ButtonBehavior):
	icon = StringProperty()
	text = StringProperty()

class AvatarListItem(OneLineAvatarIconListItem, ButtonBehavior):
	icon_left = StringProperty()
	icon_right = StringProperty()
	text = StringProperty()

class Notification(BoxLayout):
	text = StringProperty()

class ErrorDialog(BoxLayout):
	title = StringProperty()
	message = StringProperty()

class ClickableTextFieldRound(MDRelativeLayout):
	text = StringProperty()
	hint_text = StringProperty()
	helper_text = StringProperty()
	helper_text_mode = StringProperty('on_error')
	icon = StringProperty('android')
	text_field_icon = StringProperty('lead-pencil')

	def validate(self, instance):
		'''validate the text that is enter 
			This method is implemetend by the inhereting class
		'''
	def toggle_eye(self):
		if self.ids.password_field_clickable.icon == 'eye':
			self.ids.text_field.password = False
			self.ids.password_field_clickable.icon = 'eye-off'
		else:
			self.ids.password_field_clickable.icon = 'eye'
			self.ids.text_field.password = True


class CustomSnackbar(BaseSnackbar):
	text = StringProperty(None)
	icon = StringProperty('bell')
	font_size = NumericProperty("15sp")

class Scanner(MDFloatLayout):
	play = BooleanProperty(False)
	close_btn = ObjectProperty()
	def __init__(self, **kwargs):
		''' scan the qrcode for the item '''
		super().__init__(**kwargs)
		self.size_hint = (None,None)
		self.width = Window.size[0]*0.55
		self.height = Window.size[1]*0.52
		self.camera = Camera( index=-1,  size_hint=(None, None), width=Window.size[0]/2, height=Window.size[1]/2)
		#self.camera.resolution = (dp(Window.size[0]), dp(Window.size[1]))
		self.close_btn = MDFloatingActionButton(icon='close')
		self.close_btn.pos_hint = {'center_x':0.9, 'center_y':0.9}
		self.camera.play = self.play
		self.camera.pos_hint = {'center_x':0.5, 'center_y':0.5}
		self.add_widget(self.camera)
		self.add_widget(self.close_btn)
		self.md_bg_color = (0,1,0,1)
		self.pos_hint = {'center_x':0.5, 'center_y':0.5}

	def close_scanner(self, *args):
		''' close the scanner and also the camera'''
		self.camera.play = False
		

		
class Sales(MDFloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.view = Scanner(play=False)
		self.view.close_btn.bind(on_release=self.close_scanner)
		self.item_code = ClickableTextFieldRound(hint_text='Item Code', icon='search-web', helper_text='Enter a valid text')
		self.item_code.pos_hint = {'center_x':0.5, 'center_y':0.5}
		self.item_code.size_hint_x = None
		self.item_code.width = Window.size[0]/2
		self.add_widget(self.item_code)
		self.scanner_button = MDFloatingActionButton(icon='camera')
		self.scanner_button.pos_hint = {'center_x':0.9, 'center_y':0.1}
		self.scanner_button.bind(on_press=self.scan)
		self.add_widget(self.scanner_button)


	def scan(self, *args):
		''' add the scanner to the window '''
		if self.view in self.children[:]:
			self.remove_widget(self.view)
		else:
			self.add_widget(self.view)
		self.view.play = True

	def close_scanner(self, *args):
		''' close the scanner '''
		if self.view in self.children[:]:
			self.remove_widget(self.view)



class AddItem(MDBoxLayout):
	''' class add items to the invetory '''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.item_name = MDTextField(hint_text='Item Name', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_name.bind(on_text_validate=self.validate_strings)
		self.item_quantity = MDTextField(hint_text='Quantity', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_quantity.bind(on_text_validate=self.validate_integer)
		self.item_quantity.bind(on_text=self.validate_integer)
		self.item_unit = MDTextField(hint_text='Unit', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_unit.bind(on_text_validate=self.validate_strings)
		self.item_price = MDTextField(hint_text='Price', helper_text_mode='on_error', helper_text='Invalid input')
		self.item_price.bind(on_text_validate=self.validate_integer)
		self.item_price.bind(on_text=self.validate_integer)
		self.save_btn = MDFlatButton(text='SAVE')
		self.save_btn.bind(on_release=self.save_item)
		self.add_widget(self.item_name)
		self.add_widget(self.item_quantity)
		self.add_widget(self.item_unit)
		self.add_widget(self.item_price)
		self.add_widget(self.save_btn)

	def save_item(self, *args):
		''' save the items in the database '''
		item_name = self.item_name.text
		item_quantity = self.item_quantity.text
		item_unit = self.item_unit.text
		item_price = self.item_price.text

		if not item_name or item_quantity or item_unit or item_price:
			CustomSnackbar(text='[color='f'{get_hex_from_color([1.0,0.2, 0.2, 0.8])}' ']Make sure all the field as filled[/color]').open()
		else:
			items = Items(name=item_name, quantity=item_quantity, unit=item_unit, price=item_price)
			session.add(items)
			session.commit()
			CustomSnackbar(text='[color='f'{get_hex_from_color([1.0,0.2, 0.2, 0.8])}'']Saved Succesfully[/color]').open()

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

class Invetory(MDBoxLayout):
	datatable = ObjectProperty()

	def column_data(self):
		''' arrange the data in a row '''
		column = [
		('ID', dp(10)),
		('NAME', dp(10)),
		('QUANTITY', dp(10)),
		('UNIT', dp(10)), 
		('PRICE', dp(15)),
		('DESCRIPTION', dp(30))
		]

		return column

	def row_data(self):
		''' row data for the datatable '''
		#query the data 
		row_values = []
		datas = session.query(Items).all()
		for data in datas:
			value = [d for d in data.serialized.values()]
			row_values.append(value[0], value[1], value[2], value[4], value[5])

		return row_values


class AdminDashBoard(MDFloatLayout):
	''' This display all the functionality of use and all previlliged capabilities in the application '''
	screen_manager = ObjectProperty()


class LoginView(MDCard):
	''' Logins the user of the application '''
	username = ObjectProperty()
	password = ObjectProperty()
	error_text = StringProperty()
class SignUpUser(MDCard):
	username = ObjectProperty()
	password = ObjectProperty()
	email = ObjectProperty()
	repeat_password = ObjectProperty()

	def password_strength(self, *args):
		''' Check the strength of the password '''
		password_text = self.password.text
		if len(password_text) < 8:
			self.password.error = True
			self.password.helper_text_mode = 'on_error'
			self.password.helper_text = 'Weak password'
			
		from tools import PasswordStrength
		strong = PasswordStrength(password_text)
		if strong:
			self.password.helper_text_mode = 'persistent'
			self.password.helper_text_color_normal = [0, 1, 0, 0.8]
			self.password.helper_text = 'Strong password'

	def compare_password(self, *args):
		if self.password.text != self.repeat_password.text:
			self.repeat_password.helper_text_mode = 'on_error'
			self.repeat_password.error = True
			self.repeat_password.helper_text = "Not a match "
		else:
			self.repeat_password.helper_text_mode = 'persistent'
			self.repeat_password.helper_text_color_normal = [0, 1, 0, 0.8]
			self.repeat_password.helper_text = 'match'

	def signup(self, *args):
		''' Signup the user to the the system '''
		from tools import SignUp

		user = SignUp(self.username.text,self.email.text, self.password.text, self.repeat_password.text)
		user.create_user()
		if user:
			CustomSnackbar(text=f'Welcome {self.username}').open()




class EposApp(MDApp):
	title = 'Electronic Point Of Sale (EPOS)'
	user = BooleanProperty(False)
	def build(self):

		return Builder.load_string(kv)

	def on_start(self):
		''' perform a preprocessor on start '''
		'''
		self.root.ids.datatable = MDDataTable()
		self.root.ids.datatable.column_data = self.root.column_data()
		self.root.ids.datatable.row_data = self.root.row_data()
		'''
		self.username = None




	def return_home(self):
		self.root.ids.screen_manager.transition.direction = "right"
		self.root.ids.screen_manager.current = 'home'
	def view_items_list(self):
		''' view the items being sold in a list '''
		pass
	def change_screen(self, instance):
		''' change the screen of the application'''
		if not self.user:
			self.notify_error(title='Login Error', message="Make sure your are logined\n if you don't hava an account contact the admin")
		else:
			self.root.ids.screen_manager.transition.direction = "left"
			self.root.ids.screen_manager.current = instance.text.lower()
			self.root.ids.navdrawer.set_state('close')

	def login(self, user_name, pass_word):
		''' Login the user of the application '''
		self.username = user_name.text
		password = pass_word.text
		print(f'username:{self.username}\npassword:{password}')
		self.user = LoginUser(self.username, password).login()
		if self.user:
			message=f'Welcome {self.username}'
			self.root.ids.screen_manager.current = 'home'
			self.notify(message)
		else:
			self.notify_error(title='ERROR SIGNIN', message="Couldn't log you in\n makes your you have typed your username and password correctly")

	def notify(self, message):
		''' notify the user of a message to be passed along '''
		dialog = AKAlertDialog(
            header_icon="bell",
            progress_interval=5,
            fixed_orientation="landscape",
            pos_hint={"center_x": 0.5, "top": 0.95},
            dialog_radius=0,
            size_landscape=["300dp", "70dp"],
            header_font_size="40dp",
            header_width_landscape="50dp",
            progress_color=[0.4, 0.1, 1, 1],
        )

		dialog.bind(on_progress_finish=dialog.dismiss)
		content = Notification(text=message)
		content.ids.button.bind(on_release=dialog.dismiss)
		dialog.content_cls = content
		dialog.open()

	def notify_error(self, title='Error', message=''):
		if message == '':
			message = 'An error occured while trying to process your request'
		dialog = AKAlertDialog(
		    header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
		)
		content = ErrorDialog(title=title, message=message)
		content.ids.button.bind(on_release=dialog.dismiss)
		dialog.content_cls = content
		dialog.open()

	def open_drawer(self):
		if self.user:
			self.root.ids.navdrawer.set_state("open")
		else:
			self.notify_error(title='Login Error', message="Make sure your are logined.\n if you don't hava an account contact the admin")


if __name__ == '__main__':
	EposApp().run()