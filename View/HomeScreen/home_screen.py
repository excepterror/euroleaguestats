import logging
import json

from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty, BooleanProperty, ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from functools import partial
from datetime import datetime


class HomeScreenView(Screen):
    rosters_reg = DictProperty({})
    standings = DictProperty({})
    flag = BooleanProperty(False)
    notification = ObjectProperty(None)

    def schedule_intro_image_display(self, *args):
        Clock.schedule_once(self.import_global_values_file, 0)

    def import_global_values_file(self, *args):
        try:
            from StartupFiles import global_values
        except ImportError as error:
            logging.warning(f'File globals.py is missing: {error}')
            self.critical_error_and_exit(message="Critical file not found!")
        else:
            self.create_dict_with_rosters()

    def create_dict_with_rosters(self, *args):
        try:
            with open('StartupFiles/roster.json') as json_file:
                data = json.load(json_file)
            self.rosters_reg = data
        except FileNotFoundError:
            logging.warning(f'File roster.json is missing!')
            self.critical_error_and_exit()
        except json.JSONDecodeError as error:
            logging.warning(f'Error reading roster.json: {error}')
            self.critical_error_and_exit()

    def on_rosters_reg(self, *args):
        from PyCoreFiles.standings import fetch_standings

        app = App.get_running_app()

        _standings = fetch_standings()
        if isinstance(_standings, str):
            self.critical_error_and_exit(message=_standings)
        elif datetime.today().month in range(6, 10):
            logging.info("Running the app after season, i.e. June onwards.")
            self.standings = _standings
            app.load_kv_files()
            self.call_notification_popup(source="Assets/notification_important_24dp.png",
                                         notification_content="The content is partially unavailable as Euroleague are still making changes to their website!",
                                         timeout=6)
            Clock.schedule_once(partial(app.set_current_screen, "menu screen"), 7)
        else:
            logging.info("Rosters and standings loaded successfully.")
            self.standings = _standings
            app.load_kv_files()
            app.set_current_screen("menu screen")

    def critical_error_and_exit(self, image='Assets/error_24dp.png', message="Critical file not found!", exit_delay=3):
        self.call_notification_popup(image, message, exit_delay)
        Clock.schedule_once(App.get_running_app().stop, exit_delay + 1)

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
        return self.rosters_reg

    def call_notification_popup(self, source, notification_content, timeout, *args):
        self.notification.ids.image.source = source
        self.notification.ids.label.text = notification_content
        self.notification.animate_widget(timeout)
