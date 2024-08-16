import logging
import json

from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty, BooleanProperty, ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from PyCoreFiles.standings import fetch_standings

from functools import partial
from datetime import datetime


class HomeScreenView(Screen):
    rosters_reg = DictProperty({})
    standings = DictProperty({})
    flag = BooleanProperty(False)
    notification = ObjectProperty(None)

    def allow_intro_image_display(self, *args):
        Clock.schedule_once(self.import_global_values_file, 0)

    def import_global_values_file(self, *args):
        try:
            from StartupFiles import global_values
        except ModuleNotFoundError as error:
            logging.warning('globals.py is missing: {}'.format(error))
        else:
            self.create_dict_with_rosters()

    def create_dict_with_rosters(self, *args):
        with open('StartupFiles/roster.json') as json_file:
            data = json.load(json_file)
        self.rosters_reg = data

    def on_rosters_reg(self, *args):
        _standings = fetch_standings()
        if isinstance(_standings, str):
            notification_content = _standings
            source = "Assets/error_24dp.png"
            self.call_notification_popup(source, notification_content, timeout=3)
            Clock.schedule_once(App.get_running_app().stop, 4)
        elif datetime.today().month in range(6, 10):
            self.standings = _standings
            App.get_running_app().load_kv_files()
            notification_content = "The content is partially unavailable as Euroleague are still making changes to their website!"
            source = "Assets/notification_important_24dp.png"
            self.call_notification_popup(source, notification_content, timeout=6)
            Clock.schedule_once(partial(App.get_running_app().set_current_screen, "menu screen"), 7)
        else:
            self.standings = _standings
            App.get_running_app().load_kv_files()
            App.get_running_app().set_current_screen("menu screen")

    def data_from_dataset(self):
        """Form data for RVStandings recycleview. Called by :def: set_current_screen in main.py."""
        dataset = [
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
            for team_image, group in self.standings.items()]
        return dataset

    def rosters_of_teams(self):
        rosters_of_teams = self.rosters_reg
        return rosters_of_teams

    def call_notification_popup(self, source, notification_content, timeout, *args):
        self.notification.ids.image.source = source
        self.notification.ids.label.text = notification_content
        self.notification.animate_widget(timeout)
