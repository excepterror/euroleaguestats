from kivy.uix.recycleview import RecycleView


class RV(RecycleView):

    """The RecycleView Widget. Used for presenting average and total stats.
    """

    def __init__(self, stats_dict, **kwargs):
        super().__init__(**kwargs)

        self.data = [{'text': str(stat_category) + ' ' * 3 + '[color=FF6600]' + str(data_element) + '[/color]'}
                     for stat_category, data_element in stats_dict.items()]
