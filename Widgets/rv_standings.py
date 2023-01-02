"""RecycleView Widget. Called in :cls: 'Standings' - main.py."""
import re

from kivy.lang import Builder
from kivy.properties import DictProperty, ListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior

Builder.load_string('''
<Template>:
    orientation: 'horizontal'
    team: 'None'
    games_played: 'None'
    wins: 'None'
    losses: 'None'
    wins_percentage: 'None'
    points_plus: 'None'
    points_minus: 'None'
    points_diff: 'None'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        id: team_label
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                size: self.size
                pos: self.pos
        text: '[b]' + root.team + '[/b]' if root.index == 0 else root.team
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .85, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        valign: 'middle'
        markup: True
    Label:   
        text: '[b]' + root.games_played + '[/b]' if root.index == 0 else root.games_played
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .35, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label:          
        text: '[b]' + root.wins + '[/b]' if root.index == 0 else root.wins
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label: 
        text: '[b]' + root.losses + '[/b]' if root.index == 0 else root.losses
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label:        
        text: '[b]' + root.wins_percentage + '[/b]' if root.index == 0 else root.wins_percentage
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label:   
        text: '[b]' + root.points_plus + '[/b]' if root.index == 0 else root.points_plus
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label:  
        text: '[b]' + root.points_minus+ '[/b]' if root.index == 0 else root.points_minus
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True
    Label:  
        text: '[b]' + root.points_diff + '[/b]' if root.index == 0 else root.points_diff
        color: 0, 0, 0, 1
        font_name: 'OpenSans'
        font_size: '16sp'
        size_hint: .2, None
        text_size: self.width, None
        height: '54.5dp'
        halign: 'center'
        markup: True

<RVSt>:
    viewclass: 'Template'
    bar_color: 0, 0, 0, 1
    bar_margin: 3
    scroll_type: ['bars', 'content']
    RecycleBoxLayout:
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                size: self.size
                pos: self.pos  
        default_size: None, dp(60)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


class Template(RecycleDataViewBehavior, BoxLayout):
    index = 0
    selected_team = ListProperty([])
    rv = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        self.rv = rv
        self.index = index
        super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super().on_touch_down(touch):
            return True
        if self.ids.team_label.collide_point(*touch.pos) and self.index > 0:
            selected_team = self.rv.data[self.index]
            data = list(selected_team.values())
            selected_team = data[0].split("[")[0]

            r = re.compile(r"[^\W\d]+")
            selected_team = r.findall(selected_team)
            self.selected_team = selected_team

    def on_selected_team(self, *args):
        self.rv.team_to_visit = ' '.join(self.selected_team)


class RVSt(RecycleView):
    current_standings = DictProperty({})
    team_to_visit = StringProperty('')

    def on_current_standings(self, *args):
        teams_data = [
            {'team': team, 'games_played': group[0], 'wins': group[1],
             'wins_percentage': group[2], 'losses': group[3], 'points_plus': group[4], 'points_minus': group[5],
             'points_diff': group[6]} for team, group in self.current_standings.items()]

        self.data = teams_data
