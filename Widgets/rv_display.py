"""RecycleView Widget in :cls: DisplayStatisticsScreenView in
DisplayStatisticsScreen.display_statistics_screen.py."""

from kivy.properties import DictProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class DisplayTemplate(RecycleDataViewBehavior, BoxLayout):
    index = 0
    rv = ObjectProperty(None)

    def refresh_view_attrs(self, rv, index, data):
        self.rv = rv
        self.index = index
        super().refresh_view_attrs(rv, index, data)


class RVDisplayStatistics(RecycleView):
    combined_dicts = DictProperty({})

    def on_combined_dicts(self, *args):
        self.data = [
            {'statistical_category': category, 'average_stats': values_tuple[0], 'total_stats': values_tuple[1]}
            for category, values_tuple in self.combined_dicts.items()]
