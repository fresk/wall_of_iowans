from kivy.factory import Factgory as F
from kivy.properties import *
from kivy.utils import interpolate

class ScrollList(F.FloatLayout):
    drag_threshold = NumericProperty(20)
    drag_offset = NumericProperty(0)
    total_offset = NumericProperty(0)
    scroll_layer = ObjectProperty(None)
    item_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CountyList, self).__init__(**kwargs)
        self.drag_touch_id = None
        self.anim = None
        Clock.schedule_once(self.load_data)

    def on_drag_offset(self, *args):
        if self.scroll_layer is None:
            return
        toy = self.total_offset
        doy = self.drag_offset
        dx, dy = self.x, self.y + toy + doy
        self.scroll_layer.transform = Matrix().translate(dx, dy, 0)

    def on_total_offset(self, *args):
        if self.scroll_layer is None:
            return
        toy = self.total_offset
        doy = self.drag_offset
        dx, dy = self.x, self.y + toy + doy
        self.scroll_layer.transform = Matrix().translate(dx, dy, 0)

    def on_touch_down(self, touch):
        if self.drag_touch_id != None:
            return False
        if self.collide_point(*touch.pos):
            if self.anim:
                Animation.cancel_all(self, 'total_offset')
                self.anim = None
            self.drag_touch_id = touch.uid
            self.velocity = 0
            touch.ud['last_y'] = touch.y
            t = (touch.time_update, touch.y)
            touch.ud['t_update'] = [t,t,t,t]
            touch.ud['move_distance'] = 0
            return True

    def on_touch_move(self, touch):
        if self.drag_touch_id == touch.uid:
            dy = touch.y - touch.ud['last_y']
            touch.ud['last_y'] = touch.y
            touch.ud['move_distance'] += abs(dy)
            t = (touch.time_update, touch.y)
            tupdate = touch.ud['t_update'][1:]
            tupdate.append(t)
            touch.ud['t_update'] = tupdate
            if touch.ud['move_distance'] > self.drag_threshold:
                self.drag_offset += dy
            return True


    def update_velocity(self, *args):
        if abs(self.velocity) == 0.001:
            self.velocity = 0

        min_offset = (1080 - self.item_list.height)
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
        self.velocity = interpolate(self.velocity, 0, 15)
        Clock.schedule_once(self.update_velocity, 1.0/30.0)

    def selection(self, item):
        App.get_running_app().selected_county = item['name'].replace("-", "_")

    def on_selected_county(self, *args):
        for btn in self.item_list.children:
            n = btn.data['name'].replace("-", "_")
            if n == self.selected_county:
                btn.state="down"
            else:
                btn.state="normal"

    def on_touch_up(self, touch):
        if self.drag_touch_id == touch.uid:
            dy = touch.y - touch.ud['last_y']
            touch.ud['move_distance'] += abs(dy)
            if touch.ud['move_distance'] > self.drag_threshold:
                self.total_offset += self.drag_offset + dy
                self.drag_offset  = 0

                tup = touch.ud['t_update']
                dura = (tup[3][0] - tup[0][0]) * 100.0
                dist = tup[3][1] - tup[0][1]

                self.velocity = 2.5 * (dist/dura)
                Clock.schedule_once(self.update_velocity, 1.0/30.0)
            #if 'mov' in touch.profile:
            #    touch.Y
            else:
                self.drag_offset  = 0
                self.velocity = 0
                x,y = 10, max(0,min(touch.y - self.total_offset, self.item_list.height-1))
                idx = int(y / 80)
                btn = self.item_list.children[idx]
                self.selection(btn.data)

            self.drag_touch_id = None
            return True

    def load_data(self, *args):
        self.counties = App.get_running_app().counties
        for name in sorted(self.counties.keys()):
            county = self.counties[name]
            self.item_list.add_widget(CountyListButton(data=county))

def log_scale(v, vmin, vmax):
    logmax = log(vmax / vmin)
    return log(v / vmin) / logmax