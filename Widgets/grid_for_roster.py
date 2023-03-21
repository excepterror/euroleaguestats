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
    r_arrow = ObjectProperty(None)
    l_arrow = ObjectProperty(None)

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
            self.parent.name = self.label.text
            self.parent.repeated_selection_flag += 1
            if touch.x <= self.width * .5:
                self.l_arrow.opacity = 1
                anim_1 = Animation(x=self.width * .1, opacity=0, transition='in_out_quad', duration=.8) \
                    + Animation(x=0, transition='in_out_quad', duration=.05)
                anim_1.start(self.l_arrow)
            elif touch.x >= self.width * .5:
                self.r_arrow.opacity = 1
                anim_2 = Animation(x=self.width * .8, opacity=0, transition='in_out_quad', duration=.8) \
                    + Animation(x=self.width - self.r_arrow.width, transition='in_out_quad', duration=.05)
                anim_2.start(self.r_arrow)
            return super().on_touch_down(touch)
