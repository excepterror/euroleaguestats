from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.app import App

from functools import partial


class MenuScreenView(Screen):

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .1))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.screen_selection, instance), .1))

    def about_animate_on_push(self, instance):
        anim = Animation(size_hint=[.38, .04], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.about_reverse_animate, instance), .1))

    def about_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.4, .06], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.screen_selection, instance), .1))

    def screen_selection(self, instance, *args):
        if instance is self.teams:
            App.get_running_app().set_current_screen("teams screen")
        if instance is self.standings:
            App.get_running_app().set_current_screen("standings screen")
        elif instance is self.about:
            App.get_running_app().set_current_screen("welcome screen")
