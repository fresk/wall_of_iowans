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
        app.filter_categories(self.category)



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



class GridItem(ListItem):
    pass

class GridView(ListLayout):
    item_class=GridItem





class MapMarker(ListItem):
    def on_press(self, *args):
        print "SELECTED"
        app = App.get_running_app()
        app.selected_iowan = self.data
        app.from_screen = 'map'
        app.show_detail()

        


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
        Clock.schedule_once(self.position_markers)
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


'''
FBO example
===========

This is an example of how to use FBO (Frame Buffer Object) to speedup graphics.
An Fbo is like a texture that you can draw on it.

By default, all the children are added in the canvas of the parent.
When you are displaying thousand of widget, you'll do thousands of graphics
instructions each frame.
The idea is to do this drawing only one time in a Fbo, and then, draw the Fbo
every frame instead of all children's graphics instructions.

We created a FboFloatLayout that create his canvas, and a Fbo.
After the Fbo is created, we are adding Color and Rectangle instruction to
display the texture of the Fbo itself.
The overload of on_pos/on_size are here to update size of Fbo if needed, and
adapt the position/size of the rectangle too.

Then, when a child is added or removed, we are redirecting addition/removal of
graphics instruction to our Fbo. This is why add_widget/remove_widget are
overloaded too.

.. note::

    This solution can be helpful but not ideal. Multisampling are not available
    in Framebuffer. We will work to add the support of it if the hardware is
    capable of, but it could be not the same.

'''


# needed to create Fbo, must be resolved in future kivy version
from kivy.core.window import Window

from kivy.graphics import Color, Rectangle, Canvas
from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty


class FboFloatLayout(FloatLayout):

    texture = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        self.canvas = Canvas()
        with self.canvas:
            self.fbo = Fbo(size=self.size)
            Color(1, 1, 1)
            self.fbo_rect = Rectangle()

        # wait that all the instructions are in the canvas to set texture
        self.texture = self.fbo.texture
        super(FboFloatLayout, self).__init__(**kwargs)

    def add_widget(self, *largs):
        # trick to attach graphics instructino to fbo instead of canvas
        canvas = self.canvas
        self.canvas = self.fbo
        ret = super(FboFloatLayout, self).add_widget(*largs)
        self.canvas = canvas
        return ret

    def remove_widget(self, *largs):
        canvas = self.canvas
        self.canvas = self.fbo
        super(FboFloatLayout, self).remove_widget(*largs)
        self.canvas = canvas

    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

F.register('FboFloatLayout', FboFloatLayout)

