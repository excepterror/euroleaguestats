import os
import logging
import json

from functools import partial

from android.permissions import request_permissions, Permission

from kivy.utils import platform
from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, DictProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.metrics import sp

from Py.connectivity import connectivity_status
from Py.standings import fetch_standings
from Py.extract_bio_stats import extract_players_data
from Py.fetch_trees import fetch_trees
from Py.extract_game_stats import update_dict
from Py.webview import WebViewInModal

from Widgets.popups import MessagePopup, NotesPopup, DisplayStats
from Widgets.rv_stats import RV

__version__ = '24.01.2'


class Stats(Screen):
    player_tree_data = ListProperty([])
    recycle_view_mod = ObjectProperty(None)
    notification = StringProperty('')
    message = ObjectProperty(None)
    text_1 = StringProperty('')
    text_2 = StringProperty('')
    player_name = StringProperty('')
    player_photo = StringProperty('')
    display_stats = ObjectProperty(None)
    rv = ObjectProperty(None)
    display_stats_title = StringProperty('')

    def on_player_tree_data(self, *args):
        try:
            self.notification = self.player_tree_data[6]
        except IndexError:
            pass
        else:
            if self.notification != '':
                self.open_popup()
            else:
                self.recycle_view_mod.perf_data = self.player_tree_data[5]
                try:
                    self.player_photo = self.player_tree_data[2]
                except ValueError as value_error:
                    logging.warning('Value error occurred [main.py]: {}'.format(value_error))
                try:
                    self.text_1 = self.player_tree_data[0]
                except ValueError as value_error:
                    self.text_1 = '{Missing data}'
                    logging.warning('Value error occurred [main.py]: {}'.format(value_error))
                try:
                    self.text_2 = self.player_tree_data[1]
                except ValueError as value_error:
                    self.text_2 = '{Missing data}'
                    logging.warning('Value error occurred [main.py]: {}'.format(value_error))
                self.call_this_screen()

    @staticmethod
    def call_this_screen(*args):
        App.get_running_app().root.transition = SlideTransition(duration=.5)
        App.get_running_app().root.current = 'stats'

    def open_popup(self, *args):
        self.message = MessagePopup(on_open=self.dismiss_text)
        self.message.notification.text = self.notification
        self.message.open()

    def dismiss_text(self, *args):
        Clock.schedule_once(self.message.dismiss, 1.5)
        Clock.schedule_once(self.reset_text, 1.6)

    def reset_text(self, *args):
        self.notification = ''

    def animate_on_push(self, instance, *args):
        anim = Animation(size_hint_x=.45, font_size=sp(17), duration=.2)
        anim &= Animation(height=sp(40), duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .2))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.47, font_size=sp(20), duration=.1)
        anim &= Animation(height=sp(50), duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.show_stats, instance), .2))

    def show_stats(self, instance, *args):
        if instance.text == 'Average Stats':
            self.display_stats = DisplayStats()
            self.display_stats_title = instance.text + ' for ' + self.player_name
            self.rv = RV(update_dict(self.player_tree_data[3]))
        elif instance.text == 'Total Stats':
            self.display_stats = DisplayStats()
            self.display_stats_title = instance.text + ' for ' + self.player_name
            self.rv = RV(update_dict(self.player_tree_data[4]))

    def on_rv(self, *args):
        self.display_stats.content = self.rv
        self.display_stats.title = self.display_stats_title
        self.display_stats.open()

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Roster(Screen):
    grid_roster = ObjectProperty(None)
    trees = DictProperty({})
    player_name = StringProperty('')
    selection_flag = NumericProperty(0)
    canvas_opacity = NumericProperty(0)
    assert_tree_return = ListProperty([])
    notification = StringProperty('')
    message = ObjectProperty(None)

    def extract_trees(self, *args):
        self.trees = fetch_trees(self.grid_roster)

    def assert_tree(self, *args):
        for name, t in self.trees.items():
            if name == self.player_name:
                player_tree = self.trees[name][0]
                player_url = self.trees[name][1]
                self.assert_tree_return = extract_players_data(player_tree, name, player_url)

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Teams(Screen):
    idx = NumericProperty()
    grid_teams = ObjectProperty(None)

    def call_roster_screen(self, *args):
        conn = connectivity_status()
        if conn is True:
            if len(self.grid_teams.selected_roster) != 0:
                App.get_running_app().root.transition = SlideTransition(direction='left')
                App.get_running_app().root.current = 'roster'
            else:
                message = MessagePopup()
                message.notification.text = 'Roster\'s announcement is pending!'
                message.open()
                Clock.schedule_once(message.dismiss, 2)
        else:
            App.get_running_app().root.show_popup(conn)
            Clock.schedule_once(App.get_running_app().stop, 5)


class Standings(Screen):
    standings = DictProperty({})
    recycle_view = ObjectProperty(None)


class Menu(Screen):
    current = ObjectProperty(None)
    standings = ObjectProperty(None)
    about = ObjectProperty(None)

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .1))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.selection, instance), .1))

    def about_animate_on_push(self, instance):
        anim = Animation(size_hint=[.38, .04], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.about_reverse_animate, instance), .1))

    def about_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.4, .06], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.selection, instance), .1))

    def selection(self, instance, *args):
        if instance is self.current:
            self.call_teams_screen()
        elif instance is self.standings:
            self.call_standings_screen()
        elif instance is self.about:
            self.call_changelog_screen()

    @staticmethod
    def call_teams_screen(*args):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'teams'

    @staticmethod
    def call_standings_screen(*args):
        conn = connectivity_status()
        if conn is True:
            App.get_running_app().root.transition = SlideTransition(direction='left')
            App.get_running_app().root.current = 'standings'
        else:
            App.get_running_app().root.show_popup(conn)
            Clock.schedule_once(App.get_running_app().stop, 3)

    @staticmethod
    def call_changelog_screen(*args):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'changelog'


class Changelog(Screen):
    notes = ObjectProperty(None)
    privacy_policy = ObjectProperty(None)

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .2))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.selection, instance), .2))

    def selection(self, instance, *args):
        if instance is self.notes:
            self.view_notes()
        elif instance is self.privacy_policy:
            self.view_privacy_policy()

    @staticmethod
    def view_notes():
        notes = NotesPopup()
        notes.open()

    @staticmethod
    def view_privacy_policy(*args):
        view = WebViewInModal()
        view.open_web_view()


class Home(Screen):
    welcome = ObjectProperty(None)
    rosters_reg = DictProperty({})
    standings = DictProperty({})

    def allow_intro_image_display(self, *args):
        Clock.schedule_once(self.import_global_values_file, .1)

    def create_dict_with_rosters(self, *args):
        with open('roster.json') as json_file:
            data = json.load(json_file)
        self.rosters_reg = data

    def import_global_values_file(self, *args):
        try:
            import global_values
        except ModuleNotFoundError as error:
            logging.warning('globals.py is missing: {}'.format(error))
        else:
            self.create_dict_with_rosters()

    @staticmethod
    def time_out_popup(conn, *args):
        App.get_running_app().root.show_popup(conn)
        Clock.schedule_once(App.get_running_app().stop, 4)

    def on_rosters_reg(self, *args):
        self.standings = fetch_standings()

    def on_standings(self, *args):
        self.call_menu_screen()

    @staticmethod
    def call_menu_screen():
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'menu'


class ELSScreenManager(ScreenManager):
    home_screen = ObjectProperty(None)
    teams_screen = ObjectProperty(None)
    roster_screen = ObjectProperty(None)
    standing_screen = ObjectProperty(None)
    stats_screen = ObjectProperty(None)
    screens_visited = ListProperty([])

    def __init__(self):
        super().__init__()

        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        screens_resolution_order = (('teams', 'menu'), ('standings', 'menu'), ('changelog', 'menu'),
                                    ('roster', 'teams'), ('stats', 'roster'))

        if key in (27, 1001):
            if self.screens_visited[-1] not in 'menu':
                for scr_name, instance in screens_resolution_order:
                    if self.screens_visited[-1] == scr_name:
                        App.get_running_app().root.current = instance
                        del self.screens_visited[-1]
                        return True
            else:
                Clock.schedule_once(self.exit_app, .5)
                return True

    def check_in_names(self, screen_name):
        if screen_name in self.screens_visited:
            pass
        else:
            self.screens_visited.append(screen_name)

    @staticmethod
    def show_popup(text_to_display):
        message = MessagePopup()
        message.notification.text = text_to_display
        message.open()

    @staticmethod
    def exit_app(*args):
        App.get_running_app().stop()


class EuroLeagueStatsApp(App):
    def build(self):
        return ELSScreenManager()

    def on_stop(self):
        suffixes = '.png'
        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith(suffixes):
                try:
                    os.remove(file_name)
                except OSError as os_error:
                    logging.warning('OS error occurred: {}'.format(os_error))


if __name__ == '__main__':
    if platform == "android":
        request_permissions(
            [Permission.READ_EXTERNAL_STORAGE, Permission.INTERNET, Permission.ACCESS_NETWORK_STATE])
    LabelBase.register(name='MyriadPro', fn_regular='Fonts/MyriadPro-Regular.ttf',
                       fn_bold='Fonts/MyriadPro-BoldCondensedItalic.ttf',
                       fn_italic='Fonts/MyriadPro-BlackCondensedItalic.ttf')
    EuroLeagueStatsApp().run()
