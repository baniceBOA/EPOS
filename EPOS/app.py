''' This is a simple electronic point of sale application '''


from .model import Items, session
from kivymd.app import MDApp, App
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton, MDIconButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable 
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import OneLineIconListItem, OneLineAvatarIconListItem, TwoLineAvatarIconListItem, ThreeLineListItem, ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget, TwoLineAvatarListItem, IRightBodyTouch
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.utils.fitimage import FitImage
from kivymd.toast import toast
from kivy.uix.camera import Camera
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_hex_from_color
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivymd.uix.snackbar import BaseSnackbar
from string import digits
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock, mainthread
from threading import Thread
from kivymd_extensions import akivymd
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog
from kivy.storage.jsonstore import JsonStore

import os
from pathlib import Path
from .tools import LoginUser, check_user_exist

assets = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets')
face_path_png = os.path.join(assets, 'face.png')
kv = '''
#:import Window kivy.core.window.Window

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
<CardContainer>:
	md_bg_color:app.theme_cls.primary_dark
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
			on_release:app.login(username.text, password.text)
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
		size_hint:(None, None)
		width:Window.size[0]
		height:Window.size[1]*0.75
		pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDLabel:
			text:'SIGN UP'
			font_size:dp(5)
			font_style:'H5'
			halign:'center'
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDTextField:
			id:signup_username
			mode:'round'
			required:True
			hint_text:'username'
			on_text:root.check_username()
			size_hint_x:None
			width:Window.size[0]*0.40
			pos_hint:{'center_x':0.5, 'center_y':0.5}

		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDTextField:
			id:signup_email
			mode:'round'
			required:True
			hint_text:'email'
			validator:'email'
			size_hint_x:None
			width:Window.size[0]*0.40
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDTextField:
			id:signup_password
			mode:'round'
			required:True
			hint_text:'password'
			on_text:root.password_strength()
			size_hint_x:None
			width:Window.size[0]*0.40
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDTextField:
			id:repeat_password
			mode:'round'
			required:True
			hint_text:'repeat password'
			on_text:root.compare_password()
			size_hint_x:None
			width:Window.size[0]*0.40
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDSeparator:
			md_bg_color:[0, 0, 0, 0]
			size_hint_y:None
			height:dp(40)
			pos_hint:{'center_x':0.5, 'center_y':0.5}
		MDFillRoundFlatButton:
			id:signup_btn
			text:'sign up'
			on_release:root.signup()
			size_hint_x:None
			width:Window.size[0]*0.40
			pos_hint:{'center_x':0.5, 'center_y':0.5}

<UserEdit>:
	adaptive_height:True
	orientation:'vertical'
	username_id:username_id
	password_id:password_id
	email_id:email_id
	MDTextField:
		id:username_id
		text:root.username
	MDTextField:
		id:password_id
		text:root.password
	MDTextField:
		id:email_id
		text:root.email
<MyAKOnboardingItem@AKOnboardingItem>
    source: ""
    text: ""
    title: ""

    MDFloatLayout:

        Image:
            source: root.source
            pos_hint: {"center_x": .5, "y": .6}
            size_hint: .4, .3

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            adaptive_height: True
            pos_hint: {"center_x": .5, "top": .5}
            spacing: dp(20)
            size_hint_x: .7

            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_dark
                RoundedRectangle:
                    pos: self.pos
                    size: self.size

            MDLabel:
                text: root.title
                bold: True
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "H6"
                halign: "center"
                valign: "center"

            MDLabel:
                size_hint_y: None
                height: self.texture_size[1]
                theme_text_color: "Primary"
                font_style: "Body1"
                halign: "center"
                valign: "center"
                text: root.text		

<Sales>:
<RightLabel>:
<TwoLineAvatar>:

	ImageLeftWidget:
		source:root.source
		radius:[15]
	RightLabel:
		MDLabel:
			font_name:'TIPoppins'
			font_size:'12dp'
			text:root.timestamp

<CartItem>:
	cart_button_icon:cart_button_icon
	ImageLeftWidget:
		source:root.source
	IconRightWidget:
		id:cart_button_icon


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
		
	MDIconButton:
		id:password_field_clickable
		icon: root.icon
		pos_hint: {"center_y": .5}
		pos: text_field.width - self.width + dp(8), 0
		theme_text_color: "Hint"
		
		 

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

<ViewItems>:
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

<AddImage>:
	orientation:'vertical'
	size_hint:(None, None)
	MDIconButton:
		id: add_image_btn_id
		icon:'plus'
	
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
			width: Window.size[0]*0.10
			size_hint_y:None
			height:Window.size[1]*0.80

			MDIconButton:
				icon:'face-man'
			
				on_release:sm.current = 'admin_screen'

			MDIconButton:
				icon:'face-man-profile'
				
				on_release:sm.current = 'user_screen'
			MDIconButton:
				icon:'bag-carry-on'
				
				on_release:sm.current= 'items'

			MDIconButton:
				icon:'bitcoin'
			
				on_release:sm.current= 'sales_screen'
			MDIconButton:
				icon:'graphql'
				
				on_release:sm.current = 'statistics_screen'
			MDIconButton:
				icon:'/assets/face.png'
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
					on_enter:root.launch_admin()
					MDScrollView:
						MDBoxLayout:
							orientation:'vertical'
							adaptive_height:True
							spacing:'5sp'

							MDBoxLayout:
								md_bg_color:app.theme_cls.primary_light
								orientation:'vertical'
								adaptive_height:True
								MDLabel:
									text:'TOP SALES'
									font_name:'BPoppins'
									font_size:'30sp'
									size_hint_y:None
									height:self.texture_size[1]
								MDScrollView:
									size_hint_y:None
									height:dp(230)
									do_scroll_x:True
									MDBoxLayout:
										orientation:'horizontal'
										spacing:'6sp'
										adaptive_width:True
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5



							MDBoxLayout:
								md_bg_color:app.theme_cls.primary_light
								orientation:'vertical'
								adaptive_height:True
								MDLabel:
									text:'TOP SALES'
									font_name:'BPoppins'
									font_size:'30sp'
									size_hint_y:None
									height:self.texture_size[1]
								MDScrollView:
									size_hint_y:None
									height:dp(230)
									do_scroll_x:True
									MDBoxLayout:
										orientation:'horizontal'
										spacing:'6sp'
										adaptive_width:True
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5

							MDBoxLayout:
								md_bg_color:app.theme_cls.primary_light
								orientation:'vertical'
								adaptive_height:True
								MDLabel:
									text:'TOP SALES'
									font_name:'BPoppins'
									font_size:'30sp'
									size_hint_y:None
									height:self.texture_size[1]
								MDScrollView:
									size_hint_y:None
									height:dp(230)
									do_scroll_x:True
									MDBoxLayout:
										orientation:'horizontal'
										spacing:'6sp'
										adaptive_width:True
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5
							MDBoxLayout:
								md_bg_color:app.theme_cls.primary_light
								orientation:'vertical'
								adaptive_height:True
								MDLabel:
									text:'TOP SALES'
									font_name:'BPoppins'
									font_size:'30sp'
									size_hint_y:None
									height:self.texture_size[1]
								MDScrollView:
									size_hint_y:None
									height:dp(230)
									do_scroll_x:True
									MDBoxLayout:
										orientation:'horizontal'
										spacing:'6sp'
										adaptive_width:True
										CardContainer:
											text:'Sugar'
											secondary_text:'50%'
											scale:1.5

							

				MDScreen:
					name:'statistics_screen'
					AKBarChart:
						x_values: [0, 5, 8, 15]
    					y_values: [0, 10, 6, 8]
    			MDScreen:
    				name:'items'
    				on_enter:view_items_id.get_items()
    				ViewItems:
    					id:view_items_id
				MDScreen:
					name:'user_screen'
					on_enter:root.users()
					MDScrollView:
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
						
		ElementCard:
			orientation:'vertical'
			size_hint_x:None
			width:Window.size[0]*0.25
			size_hint_y:None
			height:Window.size[1]*0.80
			MDTopAppBar:
				title:'LOGS'
				right_action_items:[['refresh', lambda x:root.get_logged_activities()]]
			MDScrollViewRefreshLayout:
				id:refresh_activity
				root_layout:logged_activitiy
				refresh_callback:root.logs_refresh
				MDBoxLayout:
					orientation:'vertical'
					adaptive_height:True
					spacing:'3sp'
					id:logged_activitiy


	ElementCard:
		size_hint_y:None
		height:dp(45)
		pos_hint:{'top':0.082}
		MDLabel:
			text:'LOGGED IN AS:' + app.username
			halign:'center'
			font_name:'BPoppins'
			font_size:'12sp'
		

<ElementCard@MDCard>:
    md_bg_color:[1, 1, 1, 0.2]
    padding:dp(8)
    spacing:dp(8)
    radius:dp(25)
    ripple_behavior: False 

<MyToolbar@MDTopAppBar>:
	left_action_items:[['arrow-left', lambda X:app.show_screen('home', 'Back')]]
	right_action_items:[['dots-vertical', lambda X:app.pop_dropdownmenu(X)]]

MDScreen:
	MDScreenManager:
		id:screen_manager
		MDScreen:
			name:'onboarding'
			AKOnboarding:
				on_finish:app.return_home()
				MyAKOnboardingItem:
					source:'assets/icon.png'
					title:'Welcome'
					text:'The Electronic Point of Sale is here to help with your shop management needs'
				AKOnboardingItem:
					SignUpUser:
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
				pos_hint:{'top':1}
				MyToolbar:
                    title: app.title
                    left_action_items:[["menu" , lambda x: app.open_drawer()]]
                MDBoxLayout:
					md_bg_color:app.theme_cls.primary_light
					orientation:'vertical'
					adaptive_height:True
					MDLabel:
						text:'DEALS'
						font_name:'BPoppins'
						font_size:'30sp'
						size_hint_y:None
						height:self.texture_size[1]
					MDScrollView:
						size_hint_y:None
						height:dp(230)
						do_scroll_x:True
						MDBoxLayout:
							orientation:'horizontal'
							spacing:'6sp'
							adaptive_width:True
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
				MDBoxLayout:
					md_bg_color:app.theme_cls.primary_light
					orientation:'vertical'
					adaptive_height:True
					MDLabel:
						text:'New Arrivals'
						font_name:'BPoppins'
						font_size:'30sp'
						size_hint_y:None
						height:self.texture_size[1]
					MDScrollView:
						size_hint_y:None
						height:dp(230)
						do_scroll_x:True
						MDBoxLayout:
							orientation:'horizontal'
							spacing:'6sp'
							adaptive_width:True
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
							CardContainer:
								text:'Sugar'
								secondary_text:' Available at 50% off' 
								scale:1.5
				Widget:

        MDScreen:
        	name:'admin'
        	AdminDashBoard:
        MDScreen:
        	name:'items'
        	on_enter:view_items_id.get_items()
        	ViewItems:
        		id:view_items_id
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



class IconListItem(OneLineIconListItem, ButtonBehavior):
	icon = StringProperty()
	text = StringProperty()

class AvatarListItem(OneLineAvatarIconListItem, ButtonBehavior):
	icon_left = StringProperty()
	icon_right = StringProperty()
	text = StringProperty()

class RightLabel(IRightBodyTouch, MDBoxLayout):
	adaptive_width = True

class AddImage(MDBoxLayout):
	source = StringProperty()
	def on_source(self, *args):
		if self.source:
			self.img = FitImage(source=self.source, radius=[25, 25, 25, 25],   size_hint=(None, None), size=(500, 400))
			self.dialog = MDDialog(title=f'[font_family="BPoppins"]SELECTED[/font_family]: {self.source}', 
									type='custom', 
									content_cls=self.img,
									buttons=[
									MDFlatButton(text='CANCEL', on_release=self.dismiss_dialog), 
									MDRaisedButton(text='OK', on_release=self.set_image)]
				)

			
			self.dialog.open()
	def dismiss_dialog(self, *args):
		self.source = ''
		self.dialog.dismiss()
	def set_image(self, *args):
		#just pass 
		self.dialog.dismiss()

class Notification(BoxLayout):
	text = StringProperty()

class ErrorDialog(BoxLayout):
	title = StringProperty()
	message = StringProperty()


default_image = os.path.join(r'C:\Users\HP\Pictures', '_yibs_ke-20220923-0001.webp')
class CardContainer(MDCard):
	text = StringProperty('')
	secondary_text = StringProperty('')
	source = StringProperty(default_image)
	scale = NumericProperty(1)

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
class CustomSnackbar(BaseSnackbar):
	text = StringProperty(None)
	icon = StringProperty('bell')
	font_size = NumericProperty("15sp")

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

		
class Sales(MDFloatLayout):
	shopping_list = ListProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.view = Scanner(play=False)
		self.view.close_btn.bind(on_release=self.close_scanner)
		self.item_code = ClickableTextFieldRound(hint_text='Item Code', icon='search-web', helper_text='Enter a valid Code')
		self.item_code.ids.text_field.password = False
		self.item_code.bind(on_text=self.perform_match)
		self.item_code.text = self.item_code.ids.text_field.text
		self.item_code.ids.password_field_clickable.bind(on_release=self.search)
		self.item_code.pos_hint = {'center_x':0.45, 'center_y':0.9}
		self.item_code.size_hint_x = None
		self.item_code.width = Window.size[0]*0.7
		self.shopping_cart_button = MDIcon(icon='cart', font_size=40, font_name='BPoppins')
		self.shopping_cart_button.pos_hint = {'center_x':0.9, 'center_y':0.9}
		self.search_scroll = MDScrollView()
		self.search_scroll.pos_hint = {'top':0.85}
		self.search_box = MDBoxLayout(adaptive_height=True, orientation='vertical')
		self.search_scroll.add_widget(self.search_box)
		self.add_widget(self.item_code)
		self.add_widget(self.shopping_cart_button)
		self.add_widget(self.search_scroll)
		self.scanner_button = MDFloatingActionButton(icon='camera')
		self.scanner_button.pos_hint = {'center_x':0.9, 'center_y':0.1}
		self.scanner_button.bind(on_press=self.scan)
		self.add_widget(self.scanner_button)
		Window.bind(on_resize=self._update_size)
		self.search_dropdown = MDDropdownMenu(width_mult=1.2)
	def _update_size(self, *args):
		''' update the size of the widgets '''
		self.item_code.width = Window.size[0]*0.7

	def search(self, *args):
		''' called for the search if the item is not selected in the dropdown '''
		from .tools import item_ids
		search_text = self.item_code.ids.text_field.text
		self.search_box.clear_widgets()
		if search_text:
			for item in item_ids():
				if search_text in str(item.id) or search_text in str(item.name):
					item_view = CartItem(text=item.name, 
											  secondary_text=str(item.id),
											  source=face_path_png, 
											  on_release=lambda x=f'{item.id}': self.make_sale(x))
					if item.id in self.shopping_list:
						item_view.cart_button_icon.icon = 'minus'
					else:
						item_view.cart_button_icon.icon = 'plus'
					item_view.cart_button_icon.bind(on_release = lambda x=item:self.add_to_shopping_list(x))
					self.search_box.add_widget(item_view)
			if self.search_box.children[:]:
				pass
			else:

				error_label = MDLabel(text=f'Item {search_text}  not Found  \n if the problem persist contact admin', 
									  halign='center',
									  font_name='IPoppins', 
									  font_size='18dp',
									  pos_hint={'center_x':0.5, 'center_y':0.3}
									  )
				self.search_box.add_widget(error_label)

	def add_to_shopping_list(self, instance):
		'''
		..	Toggle an Item to shopping list 
			param: instance: <MDIconButton>
				instance of the mdicon button
		'''
		
		item_number = instance.parent.parent.secondary_text
		
		
		
		if item_number in self.shopping_list:
			self.shopping_list.remove(item_number)
			instance.icon = 'plus'
		else: 
			self.shopping_list.append(item_number)
			instance.icon = 'minus' 
		total_items = len(self.shopping_list)
		
		if total_items < 10:
			# create a numeric badge icon
			badge = f'numeric-{total_items}-circle'
			self.shopping_cart_button.badge_font_size = 20
			self.shopping_cart_button.badge_icon = badge

	def perform_match(self, instance, text):
		''' 
		..	perform a match for the items
			param: instance: `kivymd.uix.textfield.MDTextField`
				the calling instance of the class
			param: text: str
				name entered or id that is passed to be viewed 

		'''
		print(instance, text)
		from .tools import item_ids
		for code in item_ids():
			if text in str(code.id) or text in code.name:
				item = {'text':f'{code.name}', 
						'secondary_text':f'{code.id}',
						'source':face_path_png, 
						'viewclass':'CartItem',
						'on_release':lambda x=f'{code.id}': self.make_sale(x),
				}
				self.search_dropdown.items.append(item)

		self.search_dropdown.caller = instance
		self.search_dropdown.open()

	def make_sale(self, item_id):
		''' Callback for making the sale of an item
			opens a confirmation dialog for confirming sale of the item
			param: item_id: str
				the item id is passed as string but later converted to interger during processing of the sale
			returntype: None
		'''
		self.shopping_list.append(item_id.secondary_text)
		self.search_dropdown.dismiss()
		return True
	
	def scan(self, *args):
		''' add the scanner to the window '''
		if self.view in self.children[:]:
			self.close_scanner()

		else:
			self.add_widget(self.view)
			self.view.play = True
			self.view.start_scanner()
			

	def close_scanner(self, *args):
		''' close the scanner '''
		if self.view in self.children[:]:
			self.view.close_scanner()
			self.remove_widget(self.view)


class AddItem(MDBoxLayout):
	''' ..class add items to the invetory '''
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
		''' ..save the items in the database '''
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
		''' ..validate the text of the textfield '''
		if instance.text:
			instance.error = False

		if instance.text == '' or instance.text == ' ':
			instance.error = True
			instance.helper_text = 'this field cannot be blank'
		if len(instance.text) > 32:
			instance.error = True
			instance.helper_text = ' use a shorter name'
		
	def validate_integer(self, instance):
		''' ..validate the integer fields '''
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
		''' ..row data for the datatable '''
		#query the data 
		row_values = []
		datas = session.query(Items).all()
		for data in datas:
			value = [d for d in data.serialized.values()]
			row_values.append(value[0], value[1], value[2], value[4], value[5])

		return row_values

class UserMenuHandler:
	def __init__(self, user_id):
		self.user_id = user_id
		actions = ['edit','delete']
		self.menu_items =[ {
						"text": f"{i}",
						"viewclass": "OneLineListItem",
						"on_release": lambda x=f"{i}": self.menu_callback(x),
						} for i in actions ]
		self.menu = MDDropdownMenu( items=self.menu_items, width_mult=1.5)
		self.initialize_user()
	def initialize_user(self):
		from .tools import query_user
		user = query_user(self.user_id)
		if user:
			self.username = user.username
			self.password = user.password
			self.email = user.email
	def menu_callback(self, func):
		if func == 'edit':
			
			self.open_edit_dialog()
			self.menu.dismiss()
		elif func == 'delete':
			self.open_delete_dialog()
			self.menu.dismiss()

	def open_delete_dialog(self):

		self.delete_dialog = MDDialog(title='Delete',
									  text=f"Are sure you want to permanetly delete [size=24][i][b]{self.username.upper()}[b][/i][/size]", 
									  buttons=[MDFlatButton(text='CANCEL', on_release=self.delete_dialog_dismiss),
									  		   MDRaisedButton(text='DELETE', on_release=self.delete_user_func)])
		self.delete_dialog.open()
	def delete_dialog_dismiss(self, *args):
		''' dismiss the delete dialog box '''
		self.delete_dialog.dismiss()
	def delete_user_func(self, *args):
		self.delete_dialog_dismiss()
		from tools import delete_user
		if delete_user(self.user_id):
			notify_banner('Deleted Succesfully')
		else:
			notify_banner('Failed to delete')


	def open_edit_dialog(self):
		self.useredit = UserEdit(user_id=self.user_id, username=self.username, password=self.password, email=self.email)
		self.edit_dialog = MDDialog(
						  type='custom',
						  title='EDIT USER',
						  content_cls=self.useredit,
						  buttons=[MDFlatButton(text='CANCEL', on_release=self.edit_dialog_dismiss), 
						  		   MDRaisedButton(text='SAVE', on_release=self.save_edit)])

		self.edit_dialog.open()
	def edit_dialog_dismiss(self, *args):
		''' dismiss the edit dialog box '''
		self.edit_dialog.dismiss()
	def save_edit(self, *args):
		''' saves the changes '''
		self.useredit.edit()
		self.edit_dialog_dismiss()
	def __call__(self, instance):
		self.menu.caller = instance
		self.menu.open()


class UserEdit(MDBoxLayout):
	user_id = NumericProperty()
	username = StringProperty()
	password = StringProperty()
	email = StringProperty()
	username_id = ObjectProperty()
	password_id = ObjectProperty()
	email_id = ObjectProperty()


	def edit(self):
		''' perform the edit upon confirmation '''
		from .tools import EditUser
		user = EditUser(self.user_id, self.username_id.text, self.password_id.text, self.email_id.text)
		if user.save():
			notify_banner('Edited Succesfully')
		else:
			notify_banner('Failed to edit')

	def __call__(self):
		return self

class AdminDashBoard(MDFloatLayout):
	''' This display all the functionality of use and all previlliged capabilities in the application '''
	screen_manager = ObjectProperty()
	logs = ListProperty()
	previous = 0
	next = 10

	def users(self, *args):
		from .tools import get_users
		self.ids.user_list.clear_widgets()
		for _user in get_users():
			user = ThreeLineAvatarIconListItem(IconLeftWidget(icon='face-man'), 
												IconRightWidget(icon='dots-vertical', on_release=UserMenuHandler(_user.id)), 
												text=str(_user.username), 
												secondary_text=_user.email, 
												tertiary_text=str(_user.id))
			self.ids.user_list.add_widget(user)
	def get_logged_activities(self):
		'''return the recent logged activities'''
		self.ids.logged_activitiy.clear_widgets()
		from .tools import Log
		self.logs = Log.get_logs()
		self.logs.reverse()
		for log in self.logs[self.previous:self.next]:
			user = log[0]
			action = log[1]
			time = log[2]
			avatar = TwoLineAvatar(text=user, secondary_text=action, timestamp=time)
			self.ids.logged_activitiy.add_widget(avatar)

		self.ids.refresh_activity.refresh_done()
	


	def logs_refresh(self):
		''' update the logs '''
		try:
			if len(self.logs) > self.next:
				self.next += 10
				self.previous += 10
			else:
				self.next = 10 
				self.previous = 0

			self.get_logged_activities()
			

		except IndexError:
			self.next = int(len(self.logs)/2)
			self.get_logged_activities()

	def launch_admin(self):
		''' Process the value for admins widgets'''	
		self.get_logged_activities()




class TwoLineAvatar(TwoLineAvatarIconListItem):
	source = StringProperty(face_path_png)
	timestamp = StringProperty('')

class CartItem(TwoLineAvatarIconListItem):
		source = StringProperty(face_path_png)
		cart_button_icon = ObjectProperty()

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
				
		from tools import PasswordStrength
		strong = PasswordStrength(password_text).validate()
		if strong:
			self.password.error = False
			self.password.helper_text_mode = 'persistent'
			self.password.helper_text_color_normal = [0, 1, 0, 0.8]
			self.password.helper_text = 'Strong password'
		else:
			self.password.error = True
			self.password.helper_text_mode = 'on_error'
			self.password.helper_text = 'Weak password (make sure your password has upper and lowercase , digits and special characters)'



	def compare_password(self, *args):
		if self.password.text != self.repeat_password.text:
			self.repeat_password.helper_text_mode = 'on_error'
			self.repeat_password.error = True
			self.repeat_password.helper_text = "Not a match "
		else:
			self.repeat_password.error = False
			self.repeat_password.helper_text_mode = 'persistent'
			self.repeat_password.helper_text_color_normal = [0, 1, 0, 0.8]
			self.repeat_password.helper_text = 'match'

	def check_username(self):
		if check_user_exist(self.username.text):
			self.username.helper_text_mode = 'on_error'
			self.username.error = True
			self.username.helper_text = f'{self.username.text} name already in use'
		else:
			self.username.error = False

	def signup(self, *args):
		''' Signup the user to the the system '''
		self.compare_password()
		from tools import SignUp

		user = SignUp(self.username.text,self.email.text, self.password.text, self.repeat_password.text)
		user.create_user()
		if user:
			notify_banner(f'welcome {self.username.text}')
			self.username.text = ''
			self.email.text = ''
			self.password.text = ''
			self.repeat_password.text = ''
		else:
			CustomSnackbar(text=f'Failed').open()#
	def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
		if self.repeat_password.focus and keycode == 40:
			self.signup()



class EposApp(MDApp):
	title = 'Electronic Point Of Sale (EPOS)'
	user = BooleanProperty(False)
	data_dir = App().user_data_dir
	store = JsonStore(os.path.join(data_dir, 'storage.json'))
	username = StringProperty('')
	logged_in_timestamp = StringProperty('')
	def build(self):
		font_folder = os.path.join(Path(os.path.abspath(__file__)).parent, 'fonts')
		LabelBase.register(name='IPoppins', fn_regular=os.path.join(font_folder,'Poppins-Italic.ttf'))
		LabelBase.register(name='BPoppins', fn_regular=os.path.join(font_folder, 'Poppins-Bold.ttf'))
		LabelBase.register(name='EBPoppins', fn_regular=os.path.join(font_folder, 'Poppins-ExtraBold.ttf'))
		LabelBase.register(name='TIPoppins', fn_regular=os.path.join(font_folder, 'Poppins-ThinItalic.ttf'))
	
		return Builder.load_string(kv)

	def on_start(self):
		''' perform a preprocessor on start '''
		'''
		self.root.ids.datatable = MDDataTable()
		self.root.ids.datatable.column_data = self.root.column_data()
		self.root.ids.datatable.row_data = self.root.row_data()
		'''
		from kivymd.color_definitions import colors
		

		self.theme_cls.primary_palette = 'Orange'
		self.theme_cls.theme_style = "Dark"
		from .tools import users

		if users():
			#this is not a new sign in 
			#perform a background login for the direct storage
			try: 
				username = self.store.get('credentials')['username']
				password = self.store.get('credentials')['password']
				self.login(username, password)
				self.root.ids.screen_manager.current = 'home'
			except KeyError:
				#user did not set persistences 
				self.root.ids.screen_manager.current = 'login'


		else:
			#load an onboarding before start
			self.root.ids.screen_manager.current = 'onboarding'
		self.menu_items =[ 
						{
						"text":'USER',
						"source":face_path_png,
						"secondary_text":'SIGN IN',
						"timestamp":self.logged_in_timestamp,
						"viewclass": "TwoLineAvatar",
						"on_release":lambda x='login': self.got_to_login(),
						},
						{
						"text":f'{self.username}',
						"source":face_path_png,
						"secondary_text":'SIGN OUT',
						"timestamp":self.logged_in_timestamp,
						"viewclass": "TwoLineAvatar",
						"on_release": lambda x=f'{self.username}': self.logout_callback(),
						},

						]

		self.dropdown = MDDropdownMenu(items=self.menu_items, width_mult=5)
	def got_to_login(self):
		self.root.ids.screen_manager.current = 'login'

	def on_stop(self):
		''' clear all the images in the temp_image folder '''
		parent = os.path.dirname(__file__)
		filepath = os.path.join(parent, 'temp_images')

		for file in os.listdir(filepath):
			filename = os.path.join(filepath, file)
			os.remove(filename)


	def return_home(self):
		self.root.ids.screen_manager.transition.direction = "right"
		self.root.ids.screen_manager.current = 'home'

	def pop_dropdownmenu(self, instance):
		self.dropdown.caller = instance
		self.dropdown.open()
		

	def logout_callback(self):
		'''
		*the function called by the application to perform the logging out of the user 
		'''
		self.logout()
		
		
	def view_items_list(self):
		''' view the items being sold in a list '''
		pass
	def change_screen(self, instance):
		''' 
		*change the screen of the application
		param : instance:
			acts just a place holder to satisfy the object calling the method
			the {instance} is never user in the application
		'''
		if not self.user:
			self.notify_error(title='Login Error', message="Make sure your are logined\n if you don't hava an account contact the admin")
		else:
			self.root.ids.screen_manager.transition.direction = "left"
			self.root.ids.screen_manager.current = instance.text.lower()
			self.root.ids.navdrawer.set_state('close')

	def login(self, user_name, pass_word):
		''' Login the user of the application 
			param: username:
				username of the user
			param: password:
				password of the user
		'''
		import datetime as dt
		
		self.username = user_name
		password = pass_word
		print(f'username:{self.username}\npassword:{password}')
		self.logintool = LoginUser(self.username, password)
		self.user = self.logintool.login()
		if self.user:
			self.logged_in_timestamp = dt.datetime.now().strftime('%H:%M:%S') 
			message=f'Welcome {self.username}'
			self.set_login_cookie(self.username, password)
			self.root.ids.screen_manager.current = 'home'
			self.notify(message)
		else:
			self.notify_error(title='ERROR SIGNIN', message="Couldn't log you in\n makes your you have typed your username and password correctly")
	def set_login_cookie(self, username, password):
		''' 
		*store user credentials localy 
		Enables persistent logging
		param: username:
			username of the user
		param: password:
			password of the user 
		 '''
		self.store.put('credentials', username=username, password=password)

	def logout(self):
		''' Logs out the user of the application '''
		self.logintool.logout
		self.username = ''
		if self.store.exists('credentials'): 
			self.store.delete('credentials')
			notify_banner('Logged Out')

	def notify(self, message):
		''' notify the user of a message  '''
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
		'''
		*Notify the user of an error accompanied with a message 
		 param: title:
		 	The title of the error defaults to erroe
		 param: message:
		 	detailed description of the error
		 returntype: None
		'''
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
		''' Open the drawer of the application '''
		if self.user:
			self.root.ids.navdrawer.set_state("open")
		else:
			self.root.ids.screen_manager.transition.direction = "right"
			self.root.ids.screen_manager.current = 'login'
			self.notify_error(title='Login Error', message="Make sure your are logined.\n if you don't hava an account contact the admin")
def notify_banner(message):
	dialog = AKAlertDialog(
	    header_icon="bell",
	    progress_interval=5,
	    fixed_orientation="landscape",
	    pos_hint={"right": 1, "y": 0.05},
	    dialog_radius=0,
	    opening_duration=5,
	    size_landscape=["350dp", "70dp"],
	    header_width_landscape="70dp",
	)
	dialog.bind(on_progress_finish=dialog.dismiss)
	content = Notification(text=message)
	content.ids.button.bind(on_release=dialog.dismiss)
	dialog.content_cls = content
	dialog.open()

if __name__ == '__main__':
	font_folder = os.path.join(Path(os.path.abspath(__file__)).parent, 'fonts')
	LabelBase.register(name='IPoppins', fn_regular=os.path.join(font_folder,'Poppins-Italic.ttf'))
	LabelBase.register(name='BPoppins', fn_regular=os.path.join(font_folder, 'Poppins-Bold.ttf'))
	LabelBase.register(name='EBPoppins', fn_regular=os.path.join(font_folder, 'Poppins-ExtraBold.ttf'))
	LabelBase.register(name='TIPoppins', fn_regular=os.path.join(font_folder, 'Poppins-ThinItalic.ttf'))
	EposApp().run()