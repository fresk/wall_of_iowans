import json, platform, random
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics.transformation import Matrix
from kivy.uix.screenmanager import ScreenManager, Screen

from museum import *
from ui import *

Builder.load_file('ui.kv')
Builder.load_file('screens.kv')





DB = json.load(open('data/iowans.json', 'r'))
DB = sorted(DB, key=lambda k: int(k['yearofbirth']))




def animate(widget, **kwargs):
    if not widget:
        retuen
    Animation.cancel_all(widget)
    a = Animation(**kwargs)
    a.start(widget)




class OverviewScreen(Screen):
    items = ListProperty()
    selection = ObjectProperty()
    scroll_list = ObjectProperty()



class MapScreen(Screen):
    items = ListProperty()
    selection = ObjectProperty()




class IntroScreen(Screen):
    def hide(self):
        def done(*args):
            p = self.parent
            p.add_widget(OverviewScreen())
            p.remove_widget(self)
            
        anim = Animation(opacity=0.0)
        anim.bind(on_complete=done)
        anim.start(self)

    def on_touch_down(self, touch):
        app = App.get_running_app()
        app.sm.current = 'overview'




class DetailScreen(Screen):
    title_text = StringProperty()
    lifetime_text = StringProperty()
    excerpt_text = StringProperty()
    detail_text = StringProperty()
    detail_type = StringProperty()
    featured_photo = StringProperty()
    inactivity_timer = NumericProperty()
    backdrop_alpha = NumericProperty(0.0)
    zoom_photo = ObjectProperty()
    photo_tray = ObjectProperty()



    def on_inactivity_timer(self, *args):
        if self.inactivity_timer == 3:
            print "hide photo zoom"
            self.hide_photo_zoom()


    def on_touch_move(self, *args):
        app = App.get_running_app()
        app.inactivity_timer = 0
        super(DetailScreen, self).on_touch_move(*args)

    def on_detail_type(self, *args):
        if self.detail_type == 'primary':
            self.show_primary_info()
        if self.detail_type == 'artifact':
            self.show_artifact_info()
        if self.detail_type == 'location':
            self.show_location_info()
        
    def show_photo_zoom(self, *args):
        animate(self, backdrop_alpha=0.9)
        #animate(self.zoom_photo, y=0, t='in_back')



    def hide_photo_zoom(self, *args):
        animate(self, backdrop_alpha=0.0)
        animate(self.zoom_photo, y=-3000, t='in_back')

        animate(self.photo_tray.children[0], pos=(250,50), scale=1 )
        animate(self.photo_tray.children[1], pos=(350,400), scale=1)
        animate(self.photo_tray.children[2], pos=(50,380), scale=1)

        def stop_zooming(*args):
            self.photo_tray.children[0].is_zooming = False
            self.photo_tray.children[1].is_zooming = False
            self.photo_tray.children[2].is_zooming = False


        Clock.schedule_once(stop_zooming, 1.1)

    def show_primary_info(self, *args):
        app = App.get_running_app()
        #self.show_photo_zoom()
        self.title_text = app.selected_iowan['title']
        self.lifetime_text = str(app.selected_iowan['birth_to_death'])
        self.excerpt_text = app.selected_iowan['overview']
        self.detail_text = app.selected_iowan['bio']
        self.featured_photo = app.selected_iowan['image_source']

    def show_artifact_info(self, *args): 
        app = App.get_running_app()
        #self.show_photo_zoom()
        self.title_text = app.selected_iowan['artifact']
        self.lifetime_text = ""
        self.excerpt_text = app.selected_iowan['artifactshort']
        self.detail_text = app.selected_iowan['artifactlong']
        self.featured_photo = app.selected_iowan['artifactimg_source']

    def show_location_info(self, *args): 
        app = App.get_running_app()
        #self.show_photo_zoom()
        self.title_text = app.selected_iowan['location']
        self.lifetime_text = ""
        self.excerpt_text = app.selected_iowan['locationshort']
        self.detail_text = app.selected_iowan['locationlong']
        self.featured_photo = app.selected_iowan['locationimg_source']


class WOIApp(App):
    detail_type = StringProperty()
    iowans = ListProperty()
    filtered_iowans = ListProperty()
    categories = DictProperty()
    selected_iowan = DictProperty()
    photo_transform = ObjectProperty(Matrix().translate(0,-3000,0))
    inactivity_timer = NumericProperty()


    def tick_timer(self, *args):
        self.inactivity_timer = self.inactivity_timer + 1

    def build(self):
        self.load_data()
        Clock.schedule_interval(self.tick_timer, 1)
        #self.screen = OverviewScreen(items=DB)

        self.sm = ScreenManager()
        self.intro = IntroScreen(name='intro')
        self.overview = OverviewScreen(name='overview', items=DB)
        self.detail = DetailScreen(name='detail')
        self.map = MapScreen(name='map')
        self.sm.add_widget(self.intro)
        self.sm.add_widget(self.overview)
        self.sm.add_widget(self.detail)
        self.sm.add_widget(self.map)
        self.sm.current = 'intro'
        #screen = DetailScreen()
        if not "Linux" in platform.system():
            self.viewport = Viewport(size=(1920, 1080*2))
            self.viewport.add_widget(self.sm)
            return self.viewport
        else:
            return screen
        

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


    def filter_categories(self, category_buttons):
        filtered = []
        active_buttons = [b for b in category_buttons if b.active]
        for b in active_buttons:
            filtered.extend(self.categories[b.category])
        if len(active_buttons) == 0:
            filtered = self.iowans[:]
        print "FILTERED", filtered
        self.filtered_iowans = filtered



    def select_random_iowan(self):
        self.selected_iowan = random.choice(self.iowans) 

       
    def on_keyboard(self, win, key, scancode, string, modifiers):
        if key == 32: #space bar
            self.select_random_iowan()



if __name__ == "__main__":        
    app = WOIApp()
    Window.bind(on_keyboard=app.on_keyboard)
    app.run()


