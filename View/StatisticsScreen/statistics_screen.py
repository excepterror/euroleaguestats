from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty, StringProperty, DictProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import sp, dp
from kivy.app import App

import logging

from functools import partial

from PyCoreFiles.extract_game_stats import update_dict

from Widgets.popups import MessagePopup


class StatisticsScreenView(Screen):
    player_tree_data = ListProperty([])
    player_name = StringProperty('')
    notification = StringProperty('')
    recycle_view_mod = ObjectProperty(None)
    float_layout = ObjectProperty(None)
    text_1 = StringProperty('')
    text_2 = StringProperty('')
    games = ObjectProperty(None)
    games_started = ObjectProperty(None)
    combined_dicts = DictProperty({})
    message = ObjectProperty(None)

    def statistics_options(self, *args):
        try:
            self.notification = self.player_tree_data[5]
        except IndexError:
            pass
        else:
            try:
                self.recycle_view_mod.performance_data = self.player_tree_data[4]
            except TypeError as value_error:
                """Remove recycleview widget if :list: player_tree_data is empty."""
                self.float_layout.remove_widget(self.recycle_view_mod)
                logging.warning('Type error [performance data] occurred [statistics_screen.py]: {}'.format(value_error))
            try:
                self.text_1 = self.player_tree_data[3]
            except ValueError as value_error:
                self.text_1 = '{Missing data}'
                logging.warning('Value error occurred [missing data] [statistics_screen.py]: {}'.format(value_error))
            try:
                self.text_2 = self.player_tree_data[2]
            except ValueError as value_error:
                self.text_2 = '{Missing data}'
                logging.warning('Value error occurred [missing data] [statistics_screen.py]: {}'.format(value_error))

    def animate_on_push(self, instance, *args):
        anim = Animation(size_hint_x=.93, font_size=sp(16), duration=.2)
        anim &= Animation(height=dp(40), duration=.2)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.stats_reverse_animate, instance), .2))

    def stats_reverse_animate(self, instance, *args):
        anim = Animation(size_hint_x=.96, font_size=sp(18), duration=.1)
        anim &= Animation(height=dp(50), duration=.1)
        anim.start(instance)
        anim.on_complete(Clock.schedule_once(partial(self.show_statistics, instance), .2))

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
                logging.warning('Index error [average_stats_dict] occurred [statistics_screen.py]: {}'.format(idx_error))
                self.call_display_statistics_screen()
            except KeyError as key_error:
                logging.warning('Key error [self.games] occurred [statistics_screen.py]: {}'.format(key_error))
                self.call_display_statistics_screen()
            except AttributeError as attribute_error:
                logging.warning('Attribute error [performance data] occurred [statistics_screen.py]: {}'.format(attribute_error))
                self.open_popup()

    @staticmethod
    def call_display_statistics_screen(*args):
        App.get_running_app().set_current_screen("display statistics screen")

    def open_popup(self, *args):
        self.message = MessagePopup(on_open=self.dismiss_text)
        self.message.notification.text = self.notification
        self.message.open()

    def dismiss_text(self, *args):
        Clock.schedule_once(self.message.dismiss, 1.5)

    def restore_recycle_view(self):
        """Restore recycleview if it had previously been removed in :def: statistics_options."""
        if self.recycle_view_mod not in self.float_layout.children:
            self.float_layout.add_widget(self.recycle_view_mod)
