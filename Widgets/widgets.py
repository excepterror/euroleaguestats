from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.graphics.texture import Texture

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
            anim = Animation(opacity=1, font_size=120, duration=.5) + Animation(font_size=74, duration=.25)
            anim.start(label)

        Clock.schedule_once(start_animation, delay)

    def animate_letter(self, *args):
        delay = 0
        for label in self.labels:
            self.repeat_animations(label, delay)
            delay += .08


class GradientWidgetRedArc(Widget):
    corner_radius = 30  # top corner radius
    steps = 100         # gradient steps

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw_gradient, pos=self.draw_gradient)
        self.draw_gradient()

    def draw_gradient(self, *args):
        self.canvas.before.clear()
        width, height = self.size
        cr = self.corner_radius

        # --- Create vertical gradient texture ---
        tex = Texture.create(size=(1, self.steps), colorfmt='rgb')
        tex_data = bytearray()
        for i in range(self.steps):
            t = min(1.0, i / self.steps * 0.7)
            blue_val = int(90 * (1 - t))
            tex_data += bytes([0, 0, blue_val])
        tex.blit_buffer(bytes(tex_data), colorfmt='rgb', bufferfmt='ubyte')
        tex.wrap = 'clamp_to_edge'    # no repeating
        tex.uvsize = (1, -1)          # stretch vertically

        with self.canvas.before:
            # --- Rounded rectangle with gradient ---
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(cr, cr), (cr, cr), (0, 0), (0, 0)],
                texture=tex
            )

            # --- Red arc ---
            red_rgb = (110 / 255, 20 / 255, 90 / 255)
            arc_radius = height / 1.5
            for i in range(self.steps):
                t = i / self.steps
                Color(*red_rgb, t)
                scaled_radius = arc_radius * (1 - t)
                Line(circle=(width, 0, scaled_radius, 0, -90), width=3)

            # --- Diagonal lines ---
            Color(0, 0, 0, 1)
            dash_length, gap_length = 1, 10
            total = dash_length + gap_length

            for start_y in range(int(self.y - self.height), int(self.y + self.height), total):
                for i in range(0, int(self.width), total):
                    x_start = self.x + i
                    y_start = start_y + i
                    x_end = x_start + dash_length
                    y_end = y_start + dash_length

                    # Clip horizontal to widget
                    if x_end > self.x + self.width:
                        x_end = self.x + self.width

                    # Clip vertical to widget height (including curved corners)
                    if y_end > self.y + self.height:
                        y_end = self.y + self.height
                    if y_start > self.y + self.height:
                        continue  # skip lines starting above widget

                    Line(points=[x_start, y_start, x_end, y_end], width=1)


class GradientWidgetBlueArc(Widget):
    corner_radius = 30  # top corner radius
    steps = 100         # gradient steps

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw_gradient, pos=self.draw_gradient)
        self.draw_gradient()

    def draw_gradient(self, *args):
        self.canvas.before.clear()
        width, height = self.size
        cr = self.corner_radius

        # --- Create vertical gradient texture (now RED gradient) ---
        tex = Texture.create(size=(1, self.steps), colorfmt='rgb')
        tex_data = bytearray()
        for i in range(self.steps):
            t = min(1.0, i / self.steps * 0.7)
            red_val = int(178 * (1 - t))   # was blue, now red
            tex_data += bytes([red_val, 20, 70])  # reddish tones
        tex.blit_buffer(bytes(tex_data), colorfmt='rgb', bufferfmt='ubyte')
        tex.wrap = 'clamp_to_edge'
        tex.uvsize = (1, -1)

        with self.canvas.before:
            # --- Rounded rectangle with RED gradient ---
            Color(1, 1, 1, 1)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[(cr, cr), (cr, cr), (0, 0), (0, 0)],
                texture=tex
            )

            # --- Blue arc ---
            blue_rgb = (0, 0, 90 / 255)
            arc_radius = height / 1.5
            for i in range(self.steps):
                t = i / self.steps
                Color(*blue_rgb, t)
                scaled_radius = arc_radius * (1 - t)
                Line(circle=(width, 0, scaled_radius, 0, -90), width=3)

            # --- Diagonal lines ---
            Color(0, 0, 0, 1)
            dash_length, gap_length = 1, 10
            total = dash_length + gap_length

            for start_y in range(int(self.y - self.height), int(self.y + self.height), total):
                for i in range(0, int(self.width), total):
                    x_start = self.x + i
                    y_start = start_y + i
                    x_end = x_start + dash_length
                    y_end = y_start + dash_length

                    # Clip horizontal to widget
                    if x_end > self.x + self.width:
                        x_end = self.x + self.width

                    # Clip vertical to widget height (including curved corners)
                    if y_end > self.y + self.height:
                        y_end = self.y + self.height
                    if y_start > self.y + self.height:
                        continue

                    Line(points=[x_start, y_start, x_end, y_end], width=1)
