import json 
import random

from kivy.app import App
from kivy.lang import Builder as B
from kivy.factory import Factory as F
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import *
from kivy.core.window import Window

from museum import Viewport, ListLayout, ListItem




class IntroScreen(Screen):
    pass

class ListScreen(Screen):
    pass

class GridScreen(Screen):
    pass

class DetailsScreen(Screen):
    iowan = DictProperty()
    photo_tray = ObjectProperty()

    top_image = StringProperty()
    top_title = StringProperty()
    top_subtitle = StringProperty()
    top_category = StringProperty()
    top_text = StringProperty()
    bottom_title = StringProperty()
    bottom_text = StringProperty()

    
    def on_iowan(self, *args):
        born_text = self.iowan['yearofbirth'] or ""
        
        died_on = self.iowan['yearofdeath'] or ""
        if died_on:
            born_text += " - "+ died_on


        self.top_image = self.iowan['image']['file']
        self.top_title = self.iowan['title'] or "" 
        self.top_subtitle = born_text
        self.top_category = (",".join(self.iowan['categories']).replace("&amp;", "&"))
        self.top_text = self.iowan['overview'] or ""
        
        self.bottom_title = self.iowan['title'] or ""
        self.bottom_text = self.iowan['bio'] or ""

        if self.photo_tray:
            self.photo_tray.clear_widgets()
            self.add_photos()

    def add_photos(self, *args):

        
        if self.iowan['artifactimg']:
            self.add_photo(
                self.iowan['artifactimg']['file'],
                self.iowan['artifact'] or "",
                "",
                self.iowan['artifactshort'] or "",
                self.iowan['artifactlong'] or "",
                (150, 0))

        if self.iowan['locationimg']:
            self.add_photo(
                self.iowan['locationimg']['file'],
                self.iowan['location'] or "",
                "",
                self.iowan['locationshort'] or "",
                self.iowan['locationlong'] or "",
                (0, -250)
            )
        
        born_text = self.iowan['yearofbirth'] or ""
        
        died_on = self.iowan['yearofdeath'] or ""
        if died_on:
            born_text += " - "+ died_on

        main_photo = self.add_photo(
            self.iowan['image']['file'],
            self.iowan['title'] or "",
            born_text,
            self.iowan['overview'] or "",
            self.iowan['bio'] or "",
            (-200, 0))


    def add_photo(self, fname, title, subtitle,  short_text, long_text, offset):
        
        p = Photo(screen=self, source=fname, title=title, subtitle=subtitle, short_text=short_text, long_text=long_text)
        self.photo_tray.add_widget(p)
        x,y = 500,550 #p.parent.center
        p.center = x + offset[0], y + offset[1]
        p.rotation = (  random.random()-0.5) *35
        return p
        


class Photo(F.Scatter):
    screen = ObjectProperty()
    source = StringProperty()
    title = StringProperty()
    subtitle = StringProperty()
    short_text = StringProperty()
    long_text = StringProperty()

    def on_bring_to_front(self, *args):
        app = App.get_running_app()
        print "BRING TO FRONT"
        self.screen.top_image = self.source
        self.screen.top_title = self.title
        self.screen.top_text = self.short_text
        self.screen.top_subtitle = self.subtitle

        self.screen.bottom_title = self.title
        self.screen.bottom_text = self.long_text











class ListPhoto(ListItem):
    photo_source = StringProperty()
    def on_data(self, *args):
        if self.data and self.data['image_alt']:
            self.photo_source = self.data['image_alt']['file']
        else:
            self.photo_source = "img/anon.jpg"

    def on_press(self, *args):
        app = App.get_running_app()
        if (app.selected_iowan == self.data):
            return app.show_screen('details')
        app.selected_iowan = self.data


class ScrollListView(ListLayout):
    item_class = ListPhoto





class GridPhoto(ListItem):
    photo_source = StringProperty()
    def on_data(self, *args):
        if self.data and self.data['image_alt']:
            self.photo_source = self.data['image_alt']['file']
        else:
            self.photo_source = "img/anon.jpg"


class GridView(ListLayout):
    item_class = GridPhoto
    




class CategoryButton(ListItem):
    text = StringProperty()
    active = BooleanProperty()

    def on_data(self, *args):
        self.text = self.data['text']

    def on_press(self, *args):
        app = App.get_running_app()
        app.filter_categories(self.parent.children[:])


class FilterView(ListLayout):
    item_class = CategoryButton




   
class MapMarker(ListItem):
    def on_press(self, *args):
        app = App.get_running_app()
        if (app.selected_iowan == self.data):
            return app.show_screen('details')
        app.selected_iowan = self.data
        self.parent.position_markers()


class MapView(ListLayout):
    item_class = MapMarker

    def position_markers(self, *args):
        if not self.layout:
            return
        app = App.get_running_app()
        for m in self.layout.children[:]:
            if (m.data == app.selected_iowan):
                m.opacity = 1.0
            else:
                m.opacity = 0.5
        
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
    x =  (lon - lon_min) / (lon_max - lon_min)
    y =  (lat - lat_min) / (lat_max - lat_min)
    return 1.0-x, y

    




class MuseumApp(App):
    iowans = ListProperty()
    categories = DictProperty()
    filtered_iowans = ListProperty()
    selected_iowan = DictProperty()
    screen_manager = ObjectProperty()


    def build(self):
        self.load_data()

        self.screen_manager = F.ScreenManager()
        self.screen_manager.add_widget(IntroScreen(name='intro'))
        self.screen_manager.add_widget(GridScreen(name='grid'))
        self.screen_manager.add_widget(ListScreen(name='list'))
        self.screen_manager.add_widget(DetailsScreen(name='details'))
        self.screen_manager.current = 'intro'

        self.viewport = Viewport(size=(1920, 1080*2))
        self.viewport.add_widget(self.screen_manager)
        return self.viewport

    def load_data(self):
        iowans = json.load(open('data/iowans.json', 'r'))
        self.iowans = sorted(iowans, key=lambda k: int(k['yearofbirth'])) 
        self.filtered_iowans = self.iowans[:]
        self.selected_iowan = self.iowans[0]

        #assign iowans to their category
        for iowan in self.iowans:
            for cat in iowan['categories']:
                cat_list = self.categories.get(cat, [])
                cat_list.append(iowan)
                self.categories[cat] = cat_list

        self.select_random_iowan()

    def on_keyboard(self, win, key, scancode, string, modifiers):
        if key == 49:
            self.show_screen('intro')
        if key ==  50:
            self.show_screen('grid')
        if key == 51:
            self.show_screen('list')
        if key == 52:
            self.show_screen('details')
        if key == 32: #space bar
            self.select_random_iowan()

    def on_selected_iowan(self, *args):
        print "selected", self.selected_iowan['title']

    def show_screen(self, screen_name):
        print "show screen:", screen_name
        self.screen_manager.current = screen_name

    def filter_categories(self, category_buttons):
        filtered = []
        active_buttons = [b for b in category_buttons if b.active]
        for b in active_buttons:
            filtered.extend(self.categories[b.text])
        if len(active_buttons) == 0:
            filtered = self.iowans[:]
        self.filtered_iowans = filtered


    def select_random_iowan(self):
        self.selected_iowan = random.choice(self.iowans) 
       


if __name__ == '__main__':
    APP = MuseumApp()
    Window.bind(on_keyboard=APP.on_keyboard)
    APP.run()

