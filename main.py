import json, platform, random
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory as F
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import *
from kivy.graphics.transformation import Matrix

from museum import *
from ui import *

Builder.load_file('screens.kv')
Builder.load_file('ui.kv')




DB = json.load(open('data/iowans.json', 'r'))
DB = sorted(DB, key=lambda k: int(k['yearofbirth']))




class OverviewScreen(F.FloatLayout):
    items = ListProperty()



class StartScreen(F.BoxLayout):
    def hide(self):
        def done(*args):
            p = self.parent
            p.add_widget(OverviewScreen())
            p.remove_widget(self)
            
        anim = Animation(opacity=0.0)
        anim.bind(on_complete=done)
        anim.start(self)

    def on_touch_down(self, touch):
        self.hide()




class DetailScreen(F.Widget):
    pass







class WOIApp(App):
    iowans = ListProperty()
    categories = DictProperty()
    selected_iowan = DictProperty()
    photo_transform = ObjectProperty(Matrix())


    def build(self):
        self.load_data()
        #screen = OverviewScreen(items=DB)
        screen = DetailScreen()
        if not "Linux" in platform.system():
            self.viewport = Viewport(size=(1920, 1080*2))
            self.viewport.add_widget(screen)
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


    def select_random_iowan(self):
        self.selected_iowan = random.choice(self.iowans) 

       
    def on_keyboard(self, win, key, scancode, string, modifiers):
        # if key == 49:
        #     self.show_screen('intro')
        # if key ==  50:
        #     self.show_screen('grid')
        # if key == 51:
        #     self.show_screen('list')
        # if key == 52:
        #     self.show_screen('details')
        if key == 32: #space bar
            self.select_random_iowan()



if __name__ == "__main__":        
    app = WOIApp()
    Window.bind(on_keyboard=app.on_keyboard)
    app.run()


