from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import ObjectProperty


class MenuScreenView(Screen):
    teams = ObjectProperty(None)
    standings = ObjectProperty(None)
    about = ObjectProperty(None)

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.05)
        anim.bind(on_complete=lambda *args: self.stats_reverse_animate(instance))
        anim.start(instance)

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.05)
        anim.bind(on_complete=lambda *args: self.screen_selection(instance))
        anim.start(instance)

    def about_animate_on_push(self, instance):
        anim = Animation(size_hint=[.38, .04], duration=.05)
        anim.bind(on_complete=lambda *args: self.about_reverse_animate(instance))
        anim.start(instance)

    def about_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.4, .06], duration=.05)
        anim.bind(on_complete=lambda *args: self.screen_selection(instance))
        anim.start(instance)

    def screen_selection(self, instance, *args):
        if instance is self.teams:
            App.get_running_app().set_current_screen("teams screen")
        if instance is self.standings:
            App.get_running_app().set_current_screen("standings screen")
        elif instance is self.about:
            App.get_running_app().set_current_screen("welcome screen")
