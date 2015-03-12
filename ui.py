from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.animation import Animation
from kivy.properties import *

from museum import *



class Photo(F.Scatter):
    source = StringProperty()

    def on_transform_with_touch(self, touch):
        app = App.get_running_app()
        trans = self.transform.multiply(Matrix())        
        app.photo_transform = trans.translate(300,800,0)





class ListPhoto(ListItem):
    def on_press(*args):
        pass

class ScrollListView(ScrollList):
    item_class = ListPhoto




class MapMarker(ListItem):
    def on_press(self, *args):
        self.item_layout.position_markers()


class MapView(ListLayout):
    item_class = MapMarker

    def position_markers(self, *args):
        if not self.layout:
            return
        app = App.get_running_app()
        for m in self.layout.children[:]:
            lat, lon = m.data['locationgeo']
            lat, lon = iowa_relative(lat, lon)        
            m.center =   lat * self.layout.width *0.95, lon * self.layout.height * 0.95

    def on_size(self, *args):
        self.position_markers()

    def on_selected_iowan(self, *args):
        self.position_markers()
    
    def on_items(self, *args):
        super(MapView, self).on_items(*args)
        self.position_markers()


def iowa_relative(lat, lon):
    lon = abs(lon)
    lat_min = 40.383333
    lat_max = 43.5
    lon_min = 90.133333
    lon_max = 96.63
    x =  -0.02+ (lon - lon_min) / (lon_max - lon_min)
    y =  0.04+ (lat - lat_min) / (lat_max - lat_min)
    return 1.0-x, y

