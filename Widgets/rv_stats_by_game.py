"""RecycleView Widget. Called by :cls:. Used for the presentation of per game stats."""

from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.popup import Popup

from Py.stats import update_dict
from Widgets.rv_stats import RV

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection.
    text_size: self.width, None
    font_size: dp(16)
    font_name: 'OpenSans'         
    halign: 'center'
    valign: 'middle'
    color: 1, .4, 0, 1
    canvas.before:
        Color:
            rgba: (0, 0, 0, .5) if self.selected else (0, 0, 0, 1)
        RoundedRectangle:
            segments: 70
            radius: 7,0
            pos: self.pos
            size: self.size
            
<RVMod>:
    viewclass: 'SelectableLabel'
    size_hint: .95, .85
    pos_hint: {'center_x': .5, 'y': .13}
    bar_pos_y: 'right'
    bar_width: dp(2)
    bar_margin: -dp(1)
    bar_color: 1, .4, 0, 1
    
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        size_hint_x: None
        width: root.width
        orientation: 'vertical'
        spacing: 5
        padding: 5
        multiselect: False
        touch_multiselect: False
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """Adds selection and focus behaviour to the view."""

    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Adds selection support to the Label."""

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):

        """Catch and handle the view changes."""

        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):

        """Adds selection on touch down."""

        if super().on_touch_down(touch):
            return True

        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):

        """Respond to the selection of items in the view."""

        self.selected = is_selected
        if is_selected:
            raw_data = rv.perf_data[1]

            k = 5 * (index + 1)
            s1 = raw_data[0][k - 5:k]

            f = 3 * (index + 1)
            s2 = raw_data[1][f - 3:f]
            s3 = raw_data[2][f - 3:f]

            m = 2 * (index + 1)
            s4 = raw_data[3][m - 2:m]
            s5 = raw_data[4][m - 2:m]

            s6 = [raw_data[5][index]]

            stats_per_game = list()
            for s in [s1, s2, s3, s4, s5, s6]:
                stats_per_game.extend(s)

            rv_view = RV(update_dict(stats_per_game))

            display_data_popup = Popup(content=rv_view, size_hint=[.8, .95],
                                       separator_color=(1, 1, 1, .5), separator_height='.5dp',
                                       title=rv.perf_data[2] + ' in ' + self.text, title_align='center',
                                       title_size='18dp', title_font='OpenSans',
                                       title_color=[.2, .6, .8, 1], auto_dismiss=True)
            display_data_popup.open()


class RVMod(RecycleView):
    """The RecycleView Widget. Used for presenting stats by game."""

    perf_data = ListProperty([])
    player_name = StringProperty()

    def __init__(self, perf_data):
        super().__init__()
        self.perf_data = perf_data

    def on_perf_data(self, *args):
        data_rs = [{'text': 'Round ' + num + ':' + ' ' + opp} for num, opp in self.perf_data[0].items()]
        self.data = data_rs
