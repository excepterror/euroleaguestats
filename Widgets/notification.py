from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ObjectProperty

Builder.load_file("Widgets/notification.kv")


class NotificationWidget(RelativeLayout):
    label = ObjectProperty(None)
    image = ObjectProperty(None)

    def animate_widget(self, timeout):
        anim = Animation(pos_hint={'center_x': .5, 'center_y': .9}, duration=1, step=1 / 30, t='out_back')
        anim.start(self)
        anim.on_complete(Clock.schedule_once(self.remove_notification, timeout))

    def remove_notification(self, *args):
        anim = Animation(pos_hint={'center_x': .5, 'center_y': 2}, duration=1, step=1 / 30, t='in_expo')
        anim.start(self)
