from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, DictProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock

Builder.load_string("""
   
<SlidingLabel>:
    pos: self.pos
    scatter_: scatter_
    label: label
    canvas.before:
        Color:
            rgba: .2, .4, .6, .8
        RoundedRectangle:
            size: self.width / 2, dp(60)
            segments: 70
            radius: 7, 0, 0, 7
        Color:
            rgba: .8, .2, .2, .8
        RoundedRectangle:
            size: self.width / 2, dp(60)
            pos: self.width / 2, 0
            segments: 70
            radius: 0, 7, 7, 0
    Scatter:
        id: scatter_
        do_translation_y: False
        do_scale: False
        do_rotation: False
        Label:
            id: label
            color_canvas: 1, 1, 1, 1
            text: root.name
            font_name: 'OpenSans'
            font_size: '18sp'
            color: 0, 0, 0, 1
            size_hint: None, None
            size: self.parent.width, dp(60)
            text_size: self.width, None
            halign: 'center'
            valign: 'middle'
            canvas.before:
                Color:
                    rgba: self.color_canvas
                RoundedRectangle:
                    size: self.size
                    segments: 70
                    radius: 7, 7, 7, 7
""")


class SlidingLabelGrid(GridLayout):
    stats_option = BooleanProperty(False)
    stats_by_game_option = BooleanProperty(False)
    roster = DictProperty()
    name = StringProperty()
    repeated_selection_flag = NumericProperty(0)

    def on_roster(self, *args):
        for name, link in self.roster.items():
            label = SlidingLabel(name=name)
            self.add_widget(label)


class SlidingLabel(RelativeLayout):
    name = StringProperty()
    scatter_ = ObjectProperty(None)
    label = ObjectProperty(None)

    def on_touch_up(self, touch):
        anim = Animation(x=0, duration=.5)
        if self.collide_point(*touch.pos):
            self.scatter_.do_translation_x = True
            if self.scatter_.pos[0] >= self.width / 4:
                self.parent.stats_option = True
                anim.start(self.scatter_)
            if self.scatter_.pos[0] <= - self.width / 4:
                self.parent.stats_by_game_option = True
                anim.start(self.scatter_)
            if self.scatter_.pos[0] < self.width / 4:
                anim.start(self.scatter_)
            return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and (self.scatter_.pos[0] >= self.width / 4
                                               or self.scatter_.pos[0] <= - self.width / 4):
            self.scatter_.do_translation_x = False
            return super().on_touch_move(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.label.color_canvas = (1, .4, 0, 1)
            self.parent.name = self.label.text
            self.parent.repeated_selection_flag += 1

            Clock.schedule_once(self.restore_canvas_color, 1)
            return super().on_touch_down(touch)

    def restore_canvas_color(self, *args):
        self.label.color_canvas = (1, 1, 1, 1)
