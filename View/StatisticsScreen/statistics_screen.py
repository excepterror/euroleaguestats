from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty, StringProperty, DictProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.app import App

import logging

from PyCoreFiles.extract_game_stats import update_dict
from utils.ui_helpers import adaptive_height


class StatisticsScreenView(Screen):
    player_tree_data = ListProperty([])
    player_name = StringProperty('')
    error_message = StringProperty('')
    recycle_view_mod = ObjectProperty(None)
    float_layout = ObjectProperty(None)
    text_1 = StringProperty('')
    text_2 = StringProperty('')
    games = ObjectProperty(None)
    games_started = ObjectProperty(None)
    combined_dicts = DictProperty({})
    notification = ObjectProperty(None)

    def statistics_options(self, *args):
        try:
            self.error_message = self.player_tree_data[5]
            """This makes sure that the RV widget will be removed if the user picks a player with no data, after having
            viewed another's player data. Otherwise, the player's dataset will be carried to the Statistics Screen of the
            player who has no data."""
            if len(self.error_message) > 0:
                self.float_layout.remove_widget(self.recycle_view_mod)
        except IndexError:
            pass
        else:
            try:
                self.recycle_view_mod.performance_data = self.player_tree_data[4]
            except TypeError as value_error:
                """Remove recycleview widget if :list: player_tree_data is empty."""
                self.float_layout.remove_widget(self.recycle_view_mod)
                logging.warning(f'Type error [performance data] occurred [statistics_screen.py]: {value_error}')
            try:
                self.text_1 = self.player_tree_data[3]
            except ValueError as value_error:
                self.text_1 = '{Missing data}'
                logging.warning(f'Value error occurred [missing data] [statistics_screen.py]: {value_error}')
            try:
                self.text_2 = self.player_tree_data[2]
            except ValueError as value_error:
                self.text_2 = '{Missing data}'
                logging.warning(f'Value error occurred [missing data] [statistics_screen.py]: {value_error}')

    def animate_on_push(self, instance, *args):
        anim = Animation(size_hint_x=.93, height=adaptive_height(scale=0.02, max_height=dp(60), font_scale=App.get_running_app().font_scale), duration=.1)
        anim.bind(on_complete=lambda *args: self.stats_reverse_animate(instance))
        anim.start(instance)

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.98, height=adaptive_height(scale=0.0587, max_height=dp(60), font_scale=App.get_running_app().font_scale), duration=.05)
        anim.bind(on_complete=lambda *args: self.show_statistics(instance))
        anim.start(instance)

    def show_statistics(self, instance, *args):
        dummy_dict, average_stats_dict, total_stats_dict = dict(), dict(), dict()
        if instance.text == 'Average & Total Stats':
            try:
                average_stats_dict = update_dict(self.player_tree_data[1])
                total_stats_dict = update_dict(self.player_tree_data[0])

                """These keys will not be included in :dict: combined_dicts and they will not display in \
                 in the recycleview in :cls: DisplayStats."""
                self.games = total_stats_dict['Games:']
                self.games_started = total_stats_dict['Games Started:']

                """Combine the two dictionaries. Only identical keys are included."""
                dicts = [average_stats_dict, total_stats_dict]
                for key in average_stats_dict.keys():
                    dummy_dict[key] = tuple(d[key] for d in dicts)
                self.combined_dicts = dummy_dict

                Clock.schedule_once(self.call_display_statistics_screen, 0)

            except IndexError as idx_error:
                logging.warning(f'Index error [average_stats_dict] occurred [statistics_screen.py]: {idx_error}')
                self.call_display_statistics_screen()
            except KeyError as key_error:
                logging.warning(f'Key error [self.games] occurred [statistics_screen.py]: {key_error}')
                self.call_display_statistics_screen()
            except AttributeError as attribute_error:
                logging.warning(f'Attribute error [performance data] occurred [statistics_screen.py]: {attribute_error}')
                source = "Assets/error_24dp.png"
                notification_content = self.error_message
                self.call_notification_popup(source, notification_content, timeout=3)

    @staticmethod
    def call_display_statistics_screen(*args):
        App.get_running_app().set_current_screen("display statistics screen")

    def call_notification_popup(self, source, notification_content, timeout, *args):
        self.notification.ids.image.source = source
        self.notification.ids.label.text = notification_content
        self.notification.animate_widget(timeout)

    def restore_recycle_view(self):
        """Restore recycleview if it had previously been removed in :def: statistics_options."""
        if self.recycle_view_mod not in self.float_layout.children:
            self.float_layout.add_widget(self.recycle_view_mod)
