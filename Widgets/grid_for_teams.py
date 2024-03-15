from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import TouchRippleButtonBehavior


class TeamsLabelGrid(GridLayout):
    rosters = DictProperty({})
    _idx = NumericProperty(0)
    selected_roster = DictProperty({})

    def on_rosters(self, *args):
        for team, urls in self.rosters.items():
            team_label = TeamsLabel()
            team_label.text = team
            team_label.im.source = 'Images/' + team + '.png'
            self.add_widget(team_label)

    def push_selected_roster(self, *args):
        self._idx += 1


class TeamsLabel(TouchRippleButtonBehavior, Label):
    shadow_texture = ObjectProperty(None)
    shadow_size = ListProperty([0, 0])
    shadow_pos = ListProperty([0, 0])
    team = StringProperty()
    im = ObjectProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            try:
                for team, dict_with_urls in self.parent.rosters.items():
                    if self.text == team:
                        self.parent.selected_roster = dict_with_urls
            except ValueError:
                pass
            Clock.schedule_once(self.parent.push_selected_roster, .8)
            return True
        return False
