from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import TouchRippleButtonBehavior


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
        source = "Assets/notification_important_24dp.png"
        notification_content = "Waiting for {}".format(self.selected_team)
        self.call_notification_popup(source, notification_content, timeout=100)

    def call_notification_popup(self, source, notification_content, timeout, *args):
        teams_screen_instance = self.parent.parent.parent.parent
        teams_screen_instance.notification.ids.image.source = source
        teams_screen_instance.notification.ids.label.text = notification_content
        teams_screen_instance.notification.animate_widget(timeout)


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
                if self.parent.selected_roster == {}:
                    source = "Assets/error_24dp.png"
                    notification_content = "{}\'s roster has not been finalised yet!".format(self.text)
                    teams_screen_instance = self.parent.parent.parent.parent.parent
                    teams_screen_instance.call_notification_popup(source, notification_content, timeout=2)
                else:
                    Clock.schedule_once(self.parent.push_selected_roster, 0)
            except ValueError:
                pass
            return True
        return False
