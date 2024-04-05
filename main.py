import os
import logging
import json
import threading

from functools import partial

from android.permissions import request_permissions, Permission

from kivy.utils import platform
from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, DictProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.metrics import sp

from Py.standings import fetch_standings
from Py.extract_bio_stats import extract_players_data, download_photos
from Py.fetch_trees import fetch_trees
from Py.extract_game_stats import update_dict
from Py.webview import WebViewInModal

from Widgets.popups import MessagePopup, NotesPopup, DisplayStats
from Widgets.rv_stats import RV
from Widgets.widgets import PlayersImageWithLabel

__version__ = '24.04.0'


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
            self.notification = self.player_tree_data[5]
        except IndexError:
            pass
        else:
            try:
                self.recycle_view_mod.perf_data = self.player_tree_data[4]
            except TypeError as value_error:
                self.remove_widget(self.recycle_view_mod)
                logging.warning('Type error [performance data] occurred [main.py]: {}'.format(value_error))
            try:
                self.text_1 = self.player_tree_data[3]
            except ValueError as value_error:
                self.text_1 = '{Missing data}'
                logging.warning('Value error occurred [missing data] [main.py]: {}'.format(value_error))
            try:
                self.text_2 = self.player_tree_data[2]
            except ValueError as value_error:
                self.text_2 = '{Missing data}'
                logging.warning('Value error occurred [missing data] [main.py]: {}'.format(value_error))
            self.call_this_screen()

    @staticmethod
    def call_this_screen(*args):
        App.get_running_app().root.transition = SlideTransition(duration=.5)
        App.get_running_app().root.current = 'stats'

    def show_stats(self, instance, *args):
        self.display_stats = DisplayStats()
        self.display_stats_title = instance.text + ' for ' + self.player_name
        if instance.text == 'Average Stats':
            try:
                self.rv = RV(update_dict(self.player_tree_data[1]))
            except AttributeError as attribute_error:
                logging.warning('Attribute error [performance data] occurred [main.py]: {}'.format(attribute_error))
                self.open_popup()
        elif instance.text == 'Total Stats':
            try:
                self.rv = RV(update_dict(self.player_tree_data[0]))
            except AttributeError as attribute_error:
                logging.warning('Attribute error [performance data] occurred [main.py]: {}'.format(attribute_error))
                self.open_popup()

    def open_popup(self, *args):
        self.message = MessagePopup(on_open=self.dismiss_text)
        self.message.notification.text = self.notification
        self.message.open()

    def dismiss_text(self, *args):
        Clock.schedule_once(self.message.dismiss, 1.5)

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

    def on_rv(self, *args):
        self.display_stats.content = self.rv
        self.display_stats.title = self.display_stats_title
        self.display_stats.open()

    def restore_recycle_view(self):
        children = self.children
        if self.recycle_view_mod not in children:
            self.add_widget(self.recycle_view_mod)

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Roster(Screen):

    trees = DictProperty({})
    roster = DictProperty({})
    player_name = StringProperty('')
    selection_flag = NumericProperty(0)
    assert_tree_return = ListProperty([])
    notification = StringProperty('')
    message = ObjectProperty(None)
    list_of_players = ListProperty([])
    grid = ObjectProperty(None)
    idx = NumericProperty(0)

    def start_second_thread(self, *args):
        threading.Thread(target=self.extract_trees).start()

    def extract_trees(self, *args):
        t = fetch_trees(self.roster)
        self.trees = t
        '''Check if ThreadPool executor [fetch_trees.py] has thrown a timeout error.'''
        if isinstance(t, str):
            self.time_out_popup(str(t))
        else:
            '''Download photos, if not present. :def: fetch_a_photo [extract_bio_stats] checks if photos are present.'''
            self.list_of_players = download_photos(self.roster)
            self.populate_photos()

    @mainthread
    def populate_photos(self):
        count = 0
        for player in self.list_of_players:
            source = player + '.png'
            if not os.path.isfile('./' + player + '.png'):
                source = 'Images/NoImage.png'
                count += 1
            player_image = PlayersImageWithLabel(player=player, source=source)
            self.grid.add_widget(player_image)
        '''Check if NoImage.png has been used instead of the actual player image, thus :def: fetch_tree [
        fetch_trees.py] and :def: fetch_a_photo [extract_bio_stats.py] have thrown errors.'''
        if count == len(self.roster):
            self.time_out_popup('Error while fetching data!')
            App.get_running_app().root.transition = FadeTransition(duration=.5)
            App.get_running_app().root.current = 'teams'
        else:
            self.call_this_screen()
            self.list_of_players = []

    @staticmethod
    def call_this_screen(*args):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'roster'

    def assert_tree(self, player_name, *args):
        for name, t in self.trees.items():
            if name == player_name:
                player_tree = self.trees[name][0]
                self.assert_tree_return = extract_players_data(player_tree, name)
        if len(self.assert_tree_return) == 0:
            self.time_out_popup('Error while fetching data!')
        else:
            self.selection_flag += 1

    @staticmethod
    def time_out_popup(conn, *args):
        App.get_running_app().root.show_popup(conn)

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Wait(Screen):
    please_wait = ObjectProperty(None)
    anim = ObjectProperty(None)
    team = StringProperty('')

    def animate_please_wait(self, *args):
        self.anim = Animation(opacity=0, duration=1)
        self.anim += Animation(opacity=1, duration=1)
        self.anim.repeat = True
        self.anim.start(self.please_wait)


class Teams(Screen):
    idx = NumericProperty()
    grid_teams = ObjectProperty(None)

    @staticmethod
    def call_please_wait_screen(*args):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'wait'


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
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'standings'

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

    def import_global_values_file(self, *args):
        try:
            import global_values
        except ModuleNotFoundError as error:
            logging.warning('globals.py is missing: {}'.format(error))
        else:
            self.create_dict_with_rosters()

    def create_dict_with_rosters(self, *args):
        with open('roster.json') as json_file:
            data = json.load(json_file)
        self.rosters_reg = data

    def on_rosters_reg(self, *args):
        _standings = fetch_standings()
        if isinstance(_standings, str):
            self.time_out_popup(_standings)
        else:
            self.standings = _standings

    def on_standings(self, *args):
        self.call_menu_screen()

    @staticmethod
    def time_out_popup(conn, *args):
        App.get_running_app().root.show_popup(conn)
        Clock.schedule_once(App.get_running_app().stop, 4)

    @staticmethod
    def call_menu_screen():
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'menu'


class ELSScreenManager(ScreenManager):
    home_screen = ObjectProperty(None)
    teams_screen = ObjectProperty(None)
    wait_screen = ObjectProperty(None)
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
                        App.get_running_app().root.transition = SlideTransition(direction='right')
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
        Window.clearcolor = (0, 0, 0, 1)
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
