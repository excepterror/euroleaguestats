from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from kivy.metrics import sp


Builder.load_file("Widgets/notification.kv")


class NotificationWidget(RelativeLayout):
    label = ObjectProperty(None)
    image = ObjectProperty(None)
    font = NumericProperty(0)

    def animate_widget(self, timeout):
        anim = Animation(size_hint=[.9, .15], duration=1, step=1 / 30, t='out_back')
        anim.start(self)
        Clock.schedule_once(self.set_font, .5)
        anim.on_complete(Clock.schedule_once(self.remove_notification, timeout))

    def set_font(self, *args):
        self.label.font_size = sp(17)
        self.label.color = (0, 0, 0, 1)

    def remove_notification(self, *args):
        anim = Animation(size_hint=[0, 0], duration=1, step=1 / 30, t='out_back')
        Clock.schedule_once(self.reset_font, 0)
        anim.start(self)

    def reset_font(self, *args):
        self.label.color = (0, 0, 0, 0)
        self.label.font_size = sp(0)
