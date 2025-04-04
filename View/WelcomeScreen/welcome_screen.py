from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

# from PyCoreFiles.webview import WebViewInModal


class WelcomeScreenView(Screen):

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.2)
        anim.start(instance)
        anim.bind(on_complete=self.stats_reverse_animate(instance))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.1)
        anim.start(instance)
        anim.bind(on_complete=self.selection(instance))

    def selection(self, instance, *args):
        if instance is self.privacy_policy:
            self.view_privacy_policy()

    @staticmethod
    def view_privacy_policy(*args):
        view = WebViewInModal()
        view.open_web_view()
