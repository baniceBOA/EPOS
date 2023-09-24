from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock, mainthread
from threading import Thread
kv = '''
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

MDFloatLayout:
    CircularProgressbar:
        id:progressbar
        pos_hint:{'center_x':0.5,'center_y':0.5}
        size_hint:(None, None)
        text_font_size:'20sp'
        size:50,50
        bar_width:2
        value:10
        mode:'free'
        bar_color:[1,0.9,0.5]
    MDFlatButton:
        pos_hint:{'center_x':0.5, 'center_y':0.2}
        text:'Cancel'
        on_press:app.cancel()
    MDFlatButton:
        pos_hint:{'center_x':0.5, 'center_y':0.1}
        text:'Start'
        on_press:app.progressbar_start()

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



class MainTest(MDApp):
    def build(self):
        return Builder.load_string(kv)
    def cancel(self):
        progressbar = self.root.ids.progressbar
        progressbar.stop = True
    def progressbar_start(self):
        progressbar = self.root.ids.progressbar
        progressbar.free_mode()
MainTest().run()
