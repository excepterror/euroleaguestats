from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.metrics import dp

from utils.ui_helpers import adaptive_height

class MenuScreenView(Screen):
    teams = ObjectProperty(None)
    standings = ObjectProperty(None)
    about = ObjectProperty(None)

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint_x=.86, height=adaptive_height(dp_base=30, font_scale=App.get_running_app().font_scale), duration=.1)
        anim.bind(on_complete=lambda *args: self.stats_reverse_animate(instance))
        anim.start(instance)

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.88, height=adaptive_height(dp_base=50, font_scale=App.get_running_app().font_scale), duration=.05)
        anim.bind(on_complete=lambda *args: self.screen_selection(instance))
        anim.start(instance)

    def about_animate_on_push(self, instance):
        anim = Animation(size_hint_x=.38, height=adaptive_height(dp_base=30, font_scale=App.get_running_app().font_scale), duration=.1)
        anim.bind(on_complete=lambda *args: self.about_reverse_animate(instance))
        anim.start(instance)

    def about_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.4, height=adaptive_height(dp_base=50, font_scale=App.get_running_app().font_scale), duration=.05)
        anim.bind(on_complete=lambda *args: self.screen_selection(instance))
        anim.start(instance)

    def screen_selection(self, instance, *args):
        if instance is self.teams:
            App.get_running_app().set_current_screen("teams screen")
        if instance is self.standings:
            App.get_running_app().set_current_screen("standings screen")
        elif instance is self.about:
            App.get_running_app().set_current_screen("welcome screen")
