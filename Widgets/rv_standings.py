"""RecycleView Widget in :cls: 'StandingsScreenView' - StandingsScreen.standings_screen.py."""

from kivy.properties import ListProperty, ObjectProperty
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
    pass
