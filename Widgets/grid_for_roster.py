from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, DictProperty, NumericProperty
from kivy.clock import Clock


class SlidingLabelGrid(GridLayout):
    roster = DictProperty()
    name = StringProperty('')
    selection_flag = NumericProperty(0)

    def on_roster(self, *args):
        for name, link in self.roster.items():
            label = SlidingLabel(name=name)
            self.add_widget(label)


class SlidingLabel(RelativeLayout):
    name = StringProperty('')
    label = ObjectProperty(None)
    r = NumericProperty(1)
    g = NumericProperty(1)
    b = NumericProperty(1)
    a = NumericProperty(.9)

    def on_touch_up(self, touch):
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.r, self.g, self.b, self.a = 1, .4, .0, 1
            Clock.schedule_once(self.select_player, 0)
            return super().on_touch_down(touch)

    def select_player(self, *args):
        self.parent.name = self.label.text
        self.parent.parent.parent.assert_tree()
        self.parent.selection_flag += 1
        Clock.schedule_once(self.restore_background_color, .5)

    def restore_background_color(self, *args):
        self.r, self.g, self.b, self.a = 1, 1, 1, .9
