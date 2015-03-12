from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.animation import Animation
from kivy.properties import *

from museum import *



class CategoryButton(ListItem):
    category = StringProperty()
    active = BooleanProperty()
    background_normal = StringProperty()
    background_down = StringProperty()

    def on_data(self, *args):
        self.text = self.data['text']

    def on_press(self, *args):
        app = App.get_running_app()
        app.filter_categories(self.parent.children[:])



class TransformLayer(F.ScatterLayout):
    pass


class Photo(F.Scatter):
    photo_type = StringProperty('primary')
    source = StringProperty()
    is_zooming = BooleanProperty(False)

    def on_transform_with_touch(self, touch):
        app = App.get_running_app()
        if self.is_zooming:
            screen = self.parent.parent
            cx, cy = self.center
            trans = Matrix().multiply(self.transform)
            trans.translate(0,1080,0)
            app.photo_transform = trans

    def on_bring_to_front(self, *args):
        self.parent.parent.detail_type = self.photo_type  
        

    def on_scale(self, *args):
        if (self.is_zooming == False) and self.scale > 1.3:
            self.parent.parent.show_photo_zoom()
            self.is_zooming = True



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

