from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty


class DisplayStatisticsScreenView(Screen):
    games = ObjectProperty(None)
    games_started = ObjectProperty(None)
    player_name = StringProperty('')
    recycle_view = ObjectProperty(None)
