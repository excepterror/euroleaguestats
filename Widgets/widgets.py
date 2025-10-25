from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.properties import NumericProperty
from kivy.metrics import sp, dp
from kivy.app import App

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
            anim = Animation(opacity=1, font_size=App.get_running_app().font_scale * sp(120), duration=.5) + Animation(font_size=App.get_running_app().font_scale * sp(75), duration=.25)
            anim.start(label)

        Clock.schedule_once(start_animation, delay)

    def animate_letter(self, *args):
        delay = 0
        for label in self.labels:
            self.repeat_animations(label, delay)
            delay += .08

class RoundedWidget(Widget):
    r0 = NumericProperty(1)
    g0 = NumericProperty(1)
    b0 = NumericProperty(1)
    a0 = NumericProperty(1)
    r1 = NumericProperty(1)
    g1 = NumericProperty(1)
    b1 = NumericProperty(1)
    a1 = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = None
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()

        with self.canvas.before:
            '''Coloured background.'''
            Color(self.r0, self.g0, self.b0, self.a0)
            radius = [dp(30), dp(30), 0, 0]
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)

        with self.canvas.after:
            '''Dots scaled relative to widget size.'''
            Color(self.r1, self.g1, self.b1, self.a1)

            '''Tweak the number of dots (density).'''
            num_cols = 20
            num_rows = 20

            dot_size = min(self.width / (num_cols * 8), self.height / (num_rows * 8))

            for i in range(num_cols):
                for j in range(num_rows):
                    '''Evenly spaced positions.'''
                    x = self.x + (i + 0.5) * (self.width / num_cols) - dot_size / 2
                    y = self.y + (j + 0.5) * (self.height / num_rows) - dot_size / 2
                    Ellipse(pos=(x, y), size=(dot_size, dot_size))