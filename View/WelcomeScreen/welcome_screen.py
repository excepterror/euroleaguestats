from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.app import App

from utils.ui_helpers import adaptive_height

class WelcomeScreenView(Screen):

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint_x=.86, height=adaptive_height(scale=0.06, max_height=dp(80), font_scale=App.get_running_app().font_scale), duration=.1)
        anim.bind(on_complete=lambda *a: self.stats_reverse_animate(instance))
        anim.start(instance)

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.88, height=adaptive_height(scale=0.08, max_height=dp(80), font_scale=App.get_running_app().font_scale), duration=.05)
        anim.bind(on_complete=lambda *a: self.selection(instance))
        anim.start(instance)

    def selection(self, instance, *args):
        if instance is self.privacy_policy:
            Clock.schedule_once(self.view_privacy_policy, .06)

    @staticmethod
    def view_privacy_policy(*args):
        from PyCoreFiles.webview import WebViewInModal
        view = WebViewInModal()
        view.open_web_view()
