import os
import requests
import concurrent.futures
import logging
import json

from functools import partial
from lxml import etree
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
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
from Py.stats import update_dict, access_per_game_stats
from Py.webview import WebViewInModal

from Widgets.popups import MessagePopup, DisplayStats, NotesPopup
from Widgets.rv_stats import RV

__version__ = '23.03.4'


class StatsByGame(Screen):
    player_name = StringProperty('')
    player_tree = DictProperty({})
    recycle_view_mod = ObjectProperty(None)
    data = ListProperty([])
    opponents = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = MessagePopup()
        self.message.auto_dismiss = True

    def extract_player_games(self):
        self.opponents = self.player_tree.xpath('//div[@class="stats-table_table__2BoHU"]')
        if len(self.opponents) != 0:
            data = access_per_game_stats(self.player_tree, self.player_name)
            self.data = data
        else:
            self.message.notification.text = 'No games played by ' + self.player_name + ' yet!'
            self.message.open()

    def on_data(self, *args):
        self.recycle_view_mod.perf_data = self.data

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Stats(Screen):
    player_tree = DictProperty({})
    player_name = StringProperty('')
    player_url = StringProperty()
    player_photo = StringProperty('Images/NoImage.jpg')
    text_1 = StringProperty('')
    text_2 = StringProperty('')
    stats = ListProperty([])
    rv = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_stats = DisplayStats()
        self.message = MessagePopup()
        self.message.auto_dismiss = True

    def extract_players_data(self):
        pos = self.player_tree.xpath(
            '//div[@class="player-hero_inner__1-bR2 side-gaps_sectionSideGaps__1ylL0"]'
            '//div[@class="hero-info_position__1uHKl"]/text()')
        info_1 = self.player_tree.xpath(
            '//div[@class="player-hero_inner__1-bR2 side-gaps_sectionSideGaps__1ylL0"]'
            '//ul[@class="hero-info_dataList__2BmgP"]//li[@class="hero-info_dataItem__cOtmj"]'
            '//span[@class="hero-info_key__1nddj"]/text()')
        info_2 = self.player_tree.xpath(
            '//div[@class="player-hero_inner__1-bR2 side-gaps_sectionSideGaps__1ylL0"]'
            '//ul[@class="hero-info_dataList__2BmgP"]//li[@class="hero-info_dataItem__cOtmj"]'
            '//b[@class="hero-info_value__2U8j_"]/text()')

        info = list()
        for i, j, in zip(info_1, info_2):
            s = i + ': ' + j
            info.append(s)

        try:
            '''Check if photo already exists.'''
            if self.player_photo.strip('.png') == self.player_name:
                pass
            elif len(self.player_url) != 0:
                try:
                    session = requests.Session()
                    retry = Retry(connect=3, backoff_factor=0.5)
                    adapter = HTTPAdapter(max_retries=retry)
                    session.mount('http://', adapter)
                    session.mount('https://', adapter)
                    response = session.get(self.player_url)
                    player_photo = self.player_name + '.png'
                    with open(player_photo, 'wb') as f:
                        f.write(response.content)
                    self.player_photo = self.player_name + '.png'
                except requests.exceptions.ConnectTimeout as conn_timeout:
                    logging.warning('Connection timed-out: {}'.format(conn_timeout))
                except Exception as e:
                    logging.warning(e)
            else:
                self.player_photo = 'Images/NoImage.jpg'
        except requests.exceptions.RequestException as request_exceptions:
            logging.warning('Requests exceptions occurred: {}'.format(request_exceptions))

        try:
            self.text_1 = pos[0]
            self.text_2 = '\n' + info[0] + '\n\n' + info[1] + '\n\n' + info[2]
        except IndexError as index_error:
            logging.warning('Index error occurred: {}'.format(index_error))

    def select_stats(self, instance, *args):
        if instance.text == 'Average Stats':
            average_stats = self.player_tree.xpath(
                '//div[@class="tab-season_seasonTableWrap__2BvIN"]//div[@class="stats-table_table__2BoHU"]'
                '//div[@class="stats-table_row__ymPKW"][3]//div[@class="stats-table_cell__RKRoT"]/text()')
            if len(average_stats) != 0:
                self.show_stats.title = 'Average Stats for ' + self.player_name
                self.rv = RV(update_dict(average_stats))
            else:
                self.message.notification.text = 'No games played by ' + self.player_name + ' yet!'
                self.message.open()
        elif instance.text == 'Total Stats':
            total_stats = self.player_tree.xpath(
                '//div[@class="tab-season_seasonTableWrap__2BvIN"]//div[@class="stats-table_table__2BoHU"]'
                '//div[@class="stats-table_row__ymPKW"][2]//div[@class="stats-table_cell__RKRoT"]/text()')
            if len(total_stats) != 0:
                self.show_stats.title = 'Total Stats for ' + self.player_name
                self.rv = RV(update_dict(total_stats))
            else:
                self.message.notification.text = 'No games played by ' + self.player_name + ' yet!'
                self.message.open()

    def on_rv(self, *args):
        self.show_stats.content = self.rv
        self.show_stats.open()

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint_x=.68, duration=.2)
        anim &= Animation(height=sp(70), duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .2))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.7, duration=.1)
        anim &= Animation(height=sp(80), duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.select_stats, instance), .2))

    @staticmethod
    def call_teams_screen(*args):
        del App.get_running_app().root.screens_visited[1:]
        App.get_running_app().root.transition = FadeTransition(duration=.5)
        App.get_running_app().root.current = 'teams'


class Roster(Screen):
    grid_roster = ObjectProperty(None)
    trees = DictProperty({})
    player_name = StringProperty()
    repeated_selection_flag = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = MessagePopup()
        self.message.notification.text = 'Almost there...'

    def assert_tree(self, *args):
        for name, t in self.trees.items():
            if name == self.player_name:
                Stats.player_tree = self.trees[name][0]
                Stats.player_url = self.trees[name][1]
                StatsByGame.player_tree = self.trees[name][0]
                StatsByGame.player_name = name

    @staticmethod
    def fetch_tree(url):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(url)
        t = etree.HTML(response.content)
        return t

    def fetch_trees(self, *args):
        temp_dict = dict()
        roster_keys = self.grid_roster.roster.keys()
        roster_values = self.grid_roster.roster.values()

        names = list(roster_keys)
        roster_values = list(roster_values)

        players_urls = list()
        photo_urls = list()
        for _tuple in roster_values:
            players_urls.append(_tuple[0])
            photo_urls.append(_tuple[1])

        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                trees = executor.map(self.fetch_tree, players_urls)
        except TimeoutError as timeout_error:
            logging.warning('Timeout error occurred: {}'.format(timeout_error))

        for name, tree, url in zip(names, trees, photo_urls):
            if name in temp_dict:
                temp_dict[name] = name
            else:
                temp_dict[name] = tree, url

        self.trees = temp_dict
        self.grid_roster.roster = dict()

    def call_stats(self):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'stats'
        self.grid_roster.stats_option = False

    def call_stats_by_game(self):
        App.get_running_app().root.transition = SlideTransition(direction='left')
        App.get_running_app().root.current = 'stats_by_game'
        self.grid_roster.stats_by_game_option = False

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

    def on_standings(self, *args):
        self.recycle_view.current_standings = self.standings


class Menu(Screen):
    current = ObjectProperty(None)
    standings = ObjectProperty(None)
    about = ObjectProperty(None)

    def stats_animate_on_push(self, instance):
        anim = Animation(size_hint=[.86, .06], duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .2))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.88, .08], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.selection, instance), .2))

    def about_animate_on_push(self, instance):
        anim = Animation(size_hint=[.38, .04], duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.about_reverse_animate, instance), .2))

    def about_reverse_animate(self, instance, *args):
        anim = Animation(size_hint=[.4, .06], duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.selection, instance), .2))

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

    def on_enter(self, *args):
        Clock.schedule_once(self.create_dict_with_rosters, 3)

    def create_dict_with_rosters(self, *args):
        conn = connectivity_status()
        if conn is True:
            with open('roster.json') as json_file:
                data = json.load(json_file)
            self.rosters_reg = data
        else:
            Clock.schedule_once(partial(self.hold, conn), 1)

    @staticmethod
    def hold(conn, *args):
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
                                    ('roster', 'teams'), ('stats', 'roster'), ('stats_by_game', 'roster'))

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
        for file_name in os.listdir(os.getcwd()):
            if file_name.endswith('.png') and file_name not in ('Court.jpg', 'NoImage.jpg'):
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
