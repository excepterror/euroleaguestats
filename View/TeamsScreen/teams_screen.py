import logging
import threading

from functools import partial

from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, DictProperty, ListProperty, ObjectProperty
from kivy.app import App
from kivy.clock import Clock

from PyCoreFiles.extract_bio_stats import download_photos
from PyCoreFiles.fetch_trees import fetch_trees


class TeamsScreenView(Screen):
    idx = NumericProperty()
    trees = DictProperty({})
    list_of_players = ListProperty([])
    roster_selected = DictProperty({})
    notification = ObjectProperty(None)

    def extract_trees_photos_on_thread(self, *args):
        threading.Thread(target=self.extract_trees, daemon=True).start()

    def extract_trees(self, *args):
        try:
            roster = self.roster_selected
            trees = fetch_trees(roster)
            '''Check if ThreadPool executor [fetch_trees.py] has thrown a timeout error.'''
            if not trees:
                raise ValueError("No trees were fetched.")
            self.trees = trees
            '''Download photos, if not present. :def: fetch_a_photo [extract_bio_stats] checks if photos are present.'''
            self.list_of_players = download_photos(roster)
        except ValueError as val_error:
            logging.warning(f"[teams_screen.py] Value error occurred. ThreadPool executor [fetch_trees.py] has thrown a timeout error: {val_error}")
            """Update message and go to menu screen."""
            self.notification.ids.label.text = "Response is taking too long!"
            Clock.schedule_once(self.notification.remove_notification, 2)
            Clock.schedule_once(partial(App.get_running_app().set_current_screen, "menu screen"), 3)

    def on_list_of_players(self, *args):
        if App.get_running_app().root.current != "roster screen":
            self.notification.remove_notification()
            Clock.schedule_once(partial(App.get_running_app().set_current_screen, "roster screen"), 1.1)

    def call_notification_popup(self, source, notification_content, timeout, *args):
        self.notification.ids.image.source = source
        self.notification.ids.label.text = notification_content
        self.notification.animate_widget(timeout)
