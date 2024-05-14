from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty


class DisplayStatisticsByGameScreenView(Screen):
    player = StringProperty('')
    game_info = StringProperty('')
    recycle_view = ObjectProperty(None)
