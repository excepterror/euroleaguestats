from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty
from kivy.metrics import sp

class RoundedRectLabelBtn(ButtonBehavior, Label):
    pass


class StandingsLabel(Label):
    pass


class PlayersImageWithLabel(BoxLayout):
    player = StringProperty('')
    source = StringProperty('')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.parent.parent.assert_tree(self.player)
            return super().on_touch_down(touch)
        return None

class StatsLabel(Label):
    pass


class DisplayStatisticsByGameLabel(Label):
    pass


class LoadingMessage(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.labels = []
        self.pos_hint = {'center_x': .5, 'center_y': .58}
        message = 'LOADING!'
        for char in message:
            label = Label(text='[i]' + char + '[/i]', opacity=0, font_size=0, color=(0,0,0,1), font_name='MyriadPro', markup=True)
            self.labels.append(label)
            self.add_widget(label)
        Clock.schedule_once(self.animate_letter, 0.5)

    @staticmethod
    def repeat_animations(label, delay):

        def start_animation(*args):
            anim = Animation(opacity=1, font_size=sp(120), duration=.5) + Animation(font_size=sp(80), duration=.25)
            anim.start(label)

        Clock.schedule_once(start_animation, delay)

    def animate_letter(self, *args):
        delay = 0
        for label in self.labels:
            self.repeat_animations(label, delay)
            delay += .08

class RoundedWidget(Widget):
    corner_radius = 30  # corner radius
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    a = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw_bg, pos=self.draw_bg)
        self.draw_bg()

    def draw_bg(self, *args):
        self.canvas.before.clear()
        cr = self.corner_radius

        with self.canvas.before:
            Color(self.r, self.g, self.b, self.a)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(cr, cr), (cr, cr), 0,0])