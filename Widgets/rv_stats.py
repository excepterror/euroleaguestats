from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

Builder.load_string('''
<RV>:
    viewclass: 'StatisticsLabel'
    RecycleBoxLayout:
        default_size: None, dp(46)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        size_hint_x: None
        width: root.width
        orientation: 'vertical'
        bar_pos_y: 'right'
        bar_color: .2, .6, .8, 1
        bar_margin: -dp(6)
        bar_width: dp(2)

<StatisticsLabel@Label>:
    text_size: self.width, None 
    font_name: 'OpenSans' 
    font_size: dp(16)        
    halign: 'center'
    valign: 'middle'
    markup: True
''')


class RV(RecycleView):

    """The RecycleView Widget. Used for presenting average and total stats.
    """

    def __init__(self, stats_dict, **kwargs):
        super().__init__(**kwargs)

        self.data = [{'text': str(stat_category) + ' ' * 3 + '[color=FF6600]' + str(data_element) + '[/color]'}
                     for stat_category, data_element in stats_dict.items()]
