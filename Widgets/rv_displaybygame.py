"""RecycleView Widget. Called in :cls: 'DisplayByGame' - main.py."""

from kivy.properties import DictProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class DisplayByGameTemplate(RecycleDataViewBehavior, BoxLayout):
    index = 0
    rv = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        self.rv = rv
        self.index = index
        super().refresh_view_attrs(rv, index, data)


class RVDisplayByGame(RecycleView):
    stats_by_game_dict = DictProperty({})

    def on_stats_by_game_dict(self, *args):
        self.data = [
            {'statistical_category': category, 'game_stat': value}
            for category, value in self.stats_by_game_dict.items()]
