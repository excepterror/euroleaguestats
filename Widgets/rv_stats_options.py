"""RecycleView Widget. Called by :cls:. Used for the presentation of per game stats."""
import logging

from kivy.properties import BooleanProperty, StringProperty, ListProperty, DictProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.app import App
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock

from Py.extract_game_stats import update_dict


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """Adds selection and focus behaviour to the view."""
    touch_deselect_last = BooleanProperty(True)


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Adds selection support to the Label."""

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes."""

        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Adds selection on touch down."""

        if super().on_touch_down(touch):
            return True

        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""

        self.selected = is_selected
        if is_selected:
            raw_data = rv.perf_data[1]

            k = 5 * (index + 1)
            s1 = raw_data[0][k - 5:k]

            f = 3 * (index + 1)
            s2 = raw_data[1][f - 3:f]
            s3 = raw_data[2][f - 3:f]

            m = 2 * (index + 1)
            s4 = raw_data[3][m - 2:m]
            s5 = raw_data[4][m - 2:m]

            s6 = [raw_data[5][index]]

            stats_per_game = list()
            for s in [s1, s2, s3, s4, s5, s6]:
                stats_per_game.extend(s)

            stats_by_game = update_dict(stats_per_game)

            rv.stats_by_game = stats_by_game
            rv.player_name = rv.perf_data[2]
            rv.game_info = self.text

            rv.update_game_data()


class RVMod(RecycleView):
    """The RecycleView Widget. Used for presenting stats by game."""

    perf_data = ListProperty([])
    game_info = StringProperty('')
    player_name = StringProperty()
    stats_by_game = DictProperty({})

    def on_perf_data(self, *args):
        try:
            data_rs = [{'text': 'Finals - Game 1' + ': ' + ' ' + opp} if num.startswith('C') else
                       {'text': 'Finals - Game 2' + ': ' + ' ' + opp} if num.startswith('3P') else
                       {'text': 'Semi-finals' + ': ' + ' ' + opp} if num.startswith('S') else
                       {'text': 'Play-off Series ' + num + ': ' + ' ' + opp} if num.startswith('G') else
                       {'text': 'Round ' + num + ': ' + ' ' + opp} for num, opp in self.perf_data[0].items()]
            self.data = data_rs
        except IndexError as idx_error:
            logging.warning('Index error [perf_data] occurred [rv_stats_options.py]: {}'.format(idx_error))

    def update_game_data(self):
        App.get_running_app().root.displaybygame_screen.recycle_view.stats_by_game_dict = self.stats_by_game
        App.get_running_app().root.displaybygame_screen.player = self.player_name
        App.get_running_app().root.displaybygame_screen.game_info = self.game_info
        Clock.schedule_once(self.call_displaybygame_screen, 0)

    @staticmethod
    def call_displaybygame_screen(self):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'displaybygame'
