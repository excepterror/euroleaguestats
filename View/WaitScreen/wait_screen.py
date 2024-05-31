from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation


class WaitScreenView(Screen):
    please_wait = ObjectProperty(None)
    anim = ObjectProperty(None)
    team_selected = StringProperty('')

    def animate_please_wait_message(self, *args):
        self.anim = Animation(opacity=0, duration=1, step=1/30)
        self.anim += Animation(opacity=1, duration=1, step=1/30)
        self.anim.repeat = True
        self.anim.start(self.please_wait)
