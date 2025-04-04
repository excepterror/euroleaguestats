from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.app import App

import os
import logging

from PyCoreFiles.extract_bio_stats import extract_players_data

from Widgets.widgets import PlayersImageWithLabel


class RosterScreenView(Screen):
    trees = DictProperty({})
    roster_selected = DictProperty({})
    selection_flag = NumericProperty(0)
    assert_tree_return = ListProperty([])
    grid = ObjectProperty(None)

    def populate_photos(self):
        count = 0
        roster = self.roster_selected
        for player in self.list_of_players:
            source = player + '.png'
            if not os.path.isfile('./' + player + '.png'):
                source = 'Assets/NoImage.png'
                count += 1
            player_image = PlayersImageWithLabel(player=player, source=source)
            self.grid.add_widget(player_image)
        '''Check if NoImage.png has been used instead of the actual player image, thus :def: fetch_tree [
        fetch_trees.py] and :def: fetch_a_photo [extract_bio_stats.py] have thrown errors.'''
        if count == len(roster):
            logging.warning("Counter value is not equal to length of  :dict: roster in :def: populate_photos"
                            " [roster_screen.py]")
            self.call_notification_popup()

    def assert_tree(self, player_name, *args):
        """Called from :def: on_touch_down in :cls: PlayersImageWithLabel in Widgets.widgets.py."""
        for name, t in self.trees.items():
            if name == player_name:
                player_tree = self.trees[name][0]
                self.assert_tree_return = extract_players_data(player_tree, name)
        if len(self.assert_tree_return) == 0:
            self.call_notification_popup()
        else:
            self.selection_flag += 1

    @staticmethod
    def on_selection_flag(*args):
        App.get_running_app().set_current_screen("statistics screen")

    def call_notification_popup(self,*args):
        self.notification.ids.image.source = "Assets/error_24dp.png"
        self.notification.ids.label.text = "Error while fetching data!"
        self.notification.animate_widget(timeout=3)

    def on_enter(self, *args):
        App.get_running_app().root.get_screen("teams screen").list_of_players = []
