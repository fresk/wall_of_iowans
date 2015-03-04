import kivy 
import time

from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scatter import ScatterPlane
from kivy.uix.relativelayout import RelativeLayout
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



    









