import kivy 
import time

from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scatter import ScatterPlane
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import *


class Viewport(ScatterPlane):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (1920, 1080))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_rotation', False)
        super(Viewport, self).__init__( **kwargs)
        Window.bind(system_size=self.on_window_resize)
        Clock.schedule_once(self.fit_to_window, -1)

    def on_window_resize(self, window, size):
        self.fit_to_window()


    def fit_to_window(self, *args):
        self.scale = Window.width/float(self.width)
        self.center = Window.center

        for c in self.children:
            c.size = self.size

    def add_widget(self, w, *args, **kwargs):
        super(Viewport, self).add_widget(w, *args, **kwargs)
        w.size = self.size




class TouchTransform(BoxLayout):
    pos_pre = ListProperty([0,0])
    pos_post = ListProperty([0,0])

    def on_touch_down(self, touch):
        print("DOWN")
        def transform(x, y):
            return x, y/2
        self.pos_pre = [touch.x, touch.y]
        touch.push()
        touch.apply_transform_2d(transform)
        self.pos_post = [touch.x, touch.y]
        status = super(TouchTransform, self).on_touch_down(touch)
        touch.pop()
        return status

    def on_touch_move(self, touch):
        print("MOVE")
        def transform(x, y):
            return x, y/2
        self.pos_pre = [touch.x, touch.y]
        touch.push()
        touch.apply_transform_2d(transform)
        self.pos_post = [touch.x, touch.y]
        status = super(TouchTransform, self).on_touch_move(touch)
        touch.pop()
        return status


    def on_touch_down(self, touch):
        def transform(x, y):
            return x, y/2
        self.pos_pre = [touch.x, touch.y]
        touch.push()
        touch.apply_transform_2d(transform)
        self.pos_post = [touch.x, touch.y]
        status = super(TouchTransform, self).on_touch_up(touch)
        touch.pop()
        return status





class ListItem(RelativeLayout):
    data = DictProperty()
    item_layout = ObjectProperty()


class ListLayout(RelativeLayout):
    items = ListProperty([])
    selection = ListProperty()
    layout = ObjectProperty()
    item_class = ListItem

    def build_item(self, data):
        klass = self.__class__.item_class
        return klass(data=data, item_layout=self)

    def on_items(self, *args):
        self.layout.clear_widgets()
        self.selection = []
        for item in self.items:
            w = self.build_item(item)
            self.layout.add_widget(w)



class BoxMask(BoxLayout, StencilView):
    pass









