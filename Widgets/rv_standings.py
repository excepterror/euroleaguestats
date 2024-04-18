"""RecycleView Widget. Called in :cls: 'Standings' - main.py."""

from kivy.properties import DictProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class StandingsTemplate(RecycleDataViewBehavior, BoxLayout):
    index = 0
    selected_team = ListProperty([])
    rv = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        self.rv = rv
        self.index = index
        super().refresh_view_attrs(rv, index, data)


class RVStandings(RecycleView):
    current_standings = DictProperty({})

    def on_current_standings(self, *args):
        teams_data = [
            {'team_image': team_image, 'ranking': '[color=FF6600]' + group[0] + '[/color]', 'games_played': group[1][0],
             'wins': group[1][1],
             'losses': group[1][2], 'wins_percentage': group[1][3], 'points_plus': group[1][4],
             'points_minus': group[1][5],
             'points_diff': group[1][6]}
            if int(group[0]) in range(1, 7) else
            {'team_image': team_image, 'ranking': '[color=#E69138]' + group[0] + '[/color]', 'games_played': group[1][0], 'wins': group[1][1],
             'losses': group[1][2], 'wins_percentage': group[1][3], 'points_plus': group[1][4],
             'points_minus': group[1][5],
             'points_diff': group[1][6]}
            if int(group[0]) in range(7, 11) else
            {'team_image': team_image, 'ranking': group[0], 'games_played': group[1][0],
             'wins': group[1][1],
             'losses': group[1][2], 'wins_percentage': group[1][3], 'points_plus': group[1][4],
             'points_minus': group[1][5],
             'points_diff': group[1][6]}
            for team_image, group in self.current_standings.items()]
        self.data = teams_data
