from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, DictProperty, ListProperty
from kivy.clock import mainthread
from kivy.app import App

import threading

from PyCoreFiles.extract_bio_stats import download_photos
from PyCoreFiles.fetch_trees import fetch_trees


class TeamsScreenView(Screen):
    idx = NumericProperty()
    trees = DictProperty({})
    list_of_players = ListProperty([])
    roster_selected = DictProperty({})

    def start_second_thread(self, *args):
        threading.Thread(target=self.extract_trees).start()

    def extract_trees(self, *args):
        roster = self.roster_selected
        t = fetch_trees(roster)
        self.trees = t
        '''Check if ThreadPool executor [fetch_trees.py] has thrown a timeout error.'''
        if isinstance(t, str):
            self.time_out_popup(str(t))
        else:
            '''Download photos, if not present. :def: fetch_a_photo [extract_bio_stats] checks if photos are present.'''
            self.list_of_players = download_photos(roster)

    @mainthread
    def on_list_of_players(self, *args):
        App.get_running_app().set_current_screen("roster screen")

    @staticmethod
    def time_out_popup(conn, *args):
        App.get_running_app().show_popup(conn)
