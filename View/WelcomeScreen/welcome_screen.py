from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock


class WelcomeScreenView(Screen):

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.1)
        anim.bind(on_complete=lambda *a: self.stats_reverse_animate(instance))
        anim.start(instance)

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.05)
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
