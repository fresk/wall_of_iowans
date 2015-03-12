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
from kivy.factory import Factory as F
from kivy.graphics.transformation import Matrix
from kivy.properties import *

from kivy.utils import interpolate


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
        if not self.layout:
            return
        self.layout.clear_widgets()
        self.selection = []
        for item in self.items:
            w = self.build_item(item)
            self.layout.add_widget(w)



class BoxMask(BoxLayout, StencilView):
    pass




class ScrollList(ListLayout):
    drag_threshold = NumericProperty(20)
    drag_offset = NumericProperty(0)
    total_offset = NumericProperty(0)
    scroll_layer = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScrollList, self).__init__(**kwargs)
        self.drag_touch_id = None
        #Clock.schedule_once(self.load_data)

    def on_drag_offset(self, *args):
        if self.scroll_layer is None:
            return
        tox = self.total_offset
        dox = self.drag_offset
        dx, dy = self.x + tox + dox, self.y
        self.scroll_layer.transform = Matrix().translate(dx, dy, 0)

    def on_total_offset(self, *args):
        if self.scroll_layer is None:
            return
        tox = self.total_offset
        dox = self.drag_offset
        dx, dy = self.x + tox + dox, self.y
        self.scroll_layer.transform = Matrix().translate(dx, dy, 0)

    def on_touch_down(self, touch):
        if self.drag_touch_id != None:
            return False
        if self.collide_point(*touch.pos):
            self.drag_touch_id = touch.uid
            self.velocity = 0
            touch.ud['last_x'] = touch.x
            t = (touch.time_update, touch.x)
            touch.ud['t_update'] = [t,t,t,t]
            touch.ud['move_distance'] = 0
            return True

    def on_touch_move(self, touch):
        if self.drag_touch_id == touch.uid:
            dx = touch.x - touch.ud['last_x']
            touch.ud['last_x'] = touch.x
            touch.ud['move_distance'] += abs(dx)
            t = (touch.time_update, touch.x)
            tupdate = touch.ud['t_update'][1:]
            tupdate.append(t)
            touch.ud['t_update'] = tupdate
            if touch.ud['move_distance'] > self.drag_threshold:
                self.drag_offset += dx
            return True


    def update_velocity(self, *args):
        if abs(self.velocity) == 0.01:
            self.velocity = 0

        min_offset = (1920 - self.layout.width)
        is_too_high = self.total_offset > 0
        is_too_low = self.total_offset < min_offset
        within_bounds = not (is_too_high or is_too_low)

        if self.velocity == 0 and within_bounds:
            return

        if is_too_high:
            self.total_offset = interpolate(self.total_offset, 0)
        if is_too_low:
            self.total_offset = interpolate(self.total_offset, min_offset)

        self.total_offset += self.velocity
        self.velocity = interpolate(self.velocity, 0, 10)
        Clock.schedule_once(self.update_velocity, 1.0/60.0)

    def on_selection(self, *args):

        if len(self.selection):
            App.get_running_app().selected_iowan = self.selection[0]


    
    def on_touch_up(self, touch):
        if self.drag_touch_id == touch.uid:
            dx = touch.x - touch.ud['last_x']
            touch.ud['move_distance'] += abs(dx)
            if touch.ud['move_distance'] > self.drag_threshold:
                self.total_offset += self.drag_offset + dx
                self.drag_offset  = 0

                tup = touch.ud['t_update']
                dura = (tup[3][0] - tup[0][0]) * 100.0
                dist = tup[3][1] - tup[0][1]


                try:
                    self.velocity = 1.8 * (dist/dura)
                except ZeroDivisionError:
                    self.velocity = 1.8 * (dist/100.0)
                Clock.schedule_once(self.update_velocity, 1.0/60.0)
            #if 'mov' in touch.profile:
            #    touch.Y
            else:
                self.drag_offset  = 0
                self.velocity = 0
                if self.layout and len(self.layout.children):
                     x,y = max(min(touch.x - self.total_offset, self.layout.width-1), 0), 10 
                     w = self.layout.children[0].width
                     idx = int(x / w)
                     btn = (self.layout.children[::-1])[idx]
                     app = App.get_running_app()
                     if app.selected_iowan == btn.data:
                        app.sm.current = 'detail'
                     self.selection = [btn.data]

            self.drag_touch_id = None
            return True


def log_scale(v, vmin, vmax):
    logmax = log(vmax / vmin)
    return log(v / vmin) / logmax






