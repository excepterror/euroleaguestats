from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty


class RoundedRectLabelBtn(ButtonBehavior, Label):
    pass


class NullLabel(Label):
    pass


class StandingsLabel(Label):
    pass


class PlayerImage(Image):
    player = StringProperty('')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.parent.assert_tree(self.player)
            return super().on_touch_down(touch)
