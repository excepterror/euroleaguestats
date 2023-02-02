from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, DictProperty, NumericProperty
from kivy.animation import Animation


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
    canvas_alpha = NumericProperty(0)

    def on_touch_up(self, touch):
        anim = Animation(x=0, duration=.5)
        self.canvas_alpha = 0
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
            self.canvas_alpha = .8
            self.parent.name = self.label.text
            self.parent.repeated_selection_flag += 1
            return super().on_touch_down(touch)

    def restore_canvas_color(self, *args):
        self.label.color_canvas = (1, 1, 1, .8)
