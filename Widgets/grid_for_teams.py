from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.app import App

from functools import partial


class TeamsLabelGrid(GridLayout):
    rosters = DictProperty({})
    _idx = NumericProperty(0)
    selected_roster = DictProperty({})
    selected_team = StringProperty('')

    def on_rosters(self, *args):
        for team, urls in self.rosters.items():
            team_label = TeamsLabel()
            team_label.text = team
            team_label.im.source = 'Assets/' + team + '.png'
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
            self.ripple_duration_in = .5
            self.ripple_duration_out = .4
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
                        '''Pass selected roster to the :gridlayout: TeamsLabelGrid.'''
                        self.parent.selected_roster = dict_with_urls
                        '''Pass selected team to the :gridlayout: TeamsLabelGrid.'''
                        self.parent.selected_team = team
            except ValueError:
                pass
            Clock.schedule_once(self.parent.push_selected_roster, 0)
            Clock.schedule_once(partial(App.get_running_app().set_current_screen, "wait screen"), .6)
            return True
        return False
