import os
import logging

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import FallOutTransition
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.utils import platform
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import __version__ as kivy_version

from View.screens import screens
from utils.ui_helpers import get_screen_diagonal_in, compute_font_scale, print_display_metrics_and_size

__version__ = "25.11.1"

logging.info(f"[main.py     ] App version {__version__}, Kivy {kivy_version}")

font_scale = 1.0

class ScreenManagement(ScreenManager):
    def __init__(self):
        super().__init__()

        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key in (27, 1001):
            if self.current == "menu screen":
                Clock.schedule_once(self.exit_app, .5)
                return True
            else:
                name = screens[self.current]["on back-click screen transition"]
                if name is None:
                    pass
                else:
                    App.get_running_app().set_current_screen(name)
                return True
        return self.current != "menu screen"

    @staticmethod
    def exit_app(*args):
        App.get_running_app().stop()


class EuroLeagueStatsApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = ScreenManagement()
        self.set_current_screen(name="home screen")

    def on_start(self):
        global font_scale

        diagonal_in = get_screen_diagonal_in()
        font_scale = compute_font_scale(diagonal_in)
        print_display_metrics_and_size(61.7)

        '''Lock portrait on phones.'''
        if platform == "android":
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            if diagonal_in <= 7:
                '''Treat as phone: portrait.'''
                activity.setRequestedOrientation(1)
            else:
                '''Treat as tablet/foldable: auto-rotate.'''
                activity.setRequestedOrientation(-1)
        logging.info(f"[main.py] Screen diagonal in inches is {round(diagonal_in,3)} and font_scale is {round(font_scale,3)}.")

    @property
    def font_scale(self):
        return font_scale

    def load_kv_files(self, *args):
        """Load kv files for Standings, Teams and Roster screen and add their classes."""
        if not self.root.has_screen("standings screen"):
            Builder.load_file(screens["standings screen"]["kv"])
            self.root.add_widget(screens["standings screen"]["view"]())
            self.root.get_screen("standings screen").recycle_view.data = self.root.get_screen(
                "home screen").data_from_dataset()
        if not self.root.has_screen("teams screen"):
            Builder.load_file(screens["teams screen"]["kv"])
            self.root.add_widget(screens["teams screen"]["view"]())
            self.root.get_screen("teams screen").grid_teams.rosters = self.root.get_screen(
                "home screen").rosters_of_teams()
        if not self.root.has_screen("roster screen"):
            Builder.load_file(screens["roster screen"]["kv"])
            self.root.add_widget(screens["roster screen"]["view"]())

    def set_current_screen(self, name, *args):
        if not self.root.has_screen(name):
            Builder.load_file(screens[name]["kv"])
            self.root.add_widget(screens[name]["view"]())
        if name == "roster screen":
            self.root.get_screen(name).list_of_players = self.root.get_screen("teams screen").list_of_players
            self.root.get_screen(name).trees = self.root.get_screen("teams screen").trees
            self.root.get_screen(name).roster_selected = self.root.get_screen("teams screen").roster_selected
        if name == "statistics screen":
            self.root.get_screen(name).player_tree_data = self.root.get_screen("roster screen").assert_tree_return
            self.root.get_screen(name).player_name = self.root.get_screen("roster screen").assert_tree_return[6]
        if name == "display statistics screen":
            self.root.get_screen(name).games = self.root.get_screen("statistics screen").games
            self.root.get_screen(name).games_started = self.root.get_screen("statistics screen").games_started
            self.root.get_screen(name).recycle_view.combined_dicts = self.root.get_screen(
                "statistics screen").combined_dicts
            self.root.get_screen(name).player_name = self.root.get_screen("statistics screen").player_name
        if name == "display statistics by game screen":
            self.root.get_screen(name).recycle_view.statistics_by_game_dict = self.root.get_screen(
                "statistics screen").recycle_view_mod.statistics_by_game
            self.root.get_screen(name).player = self.root.get_screen("statistics screen").recycle_view_mod.player_name
            self.root.get_screen(name).game_info = self.root.get_screen("statistics screen").recycle_view_mod.game_info
        self.root.transition = FallOutTransition()
        self.root.current = name

    def on_stop(self):
        suffixes = '.png'
        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith(suffixes):
                try:
                    os.remove(file_name)
                    logging.info('Image {} removed'.format(file_name))
                except OSError as os_error:
                    logging.warning('OS error occurred: {}'.format(os_error))


if __name__ == '__main__':
    if platform == "android":
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE
        ])
    LabelBase.register(name='MyriadPro', fn_regular=os.path.join('Fonts', 'MyriadPro-Regular.ttf'),
                       fn_bold=os.path.join('Fonts', 'MyriadPro-BoldCondensedItalic.ttf'),
                       fn_italic=os.path.join('Fonts', 'MyriadPro-BlackCondensedItalic.ttf'))
    EuroLeagueStatsApp().run()
