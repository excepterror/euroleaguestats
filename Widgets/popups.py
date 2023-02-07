from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

Builder.load_string("""
<MessagePopup>:
    notification: notification
    title: ''
    title_size: '0sp'
    title_font: 'OpenSans'
    title_color: 1, .4, 0, 1
    separator_color: 1, .4, 0, 0
    size_hint: .6, .3
    pos_hint: {'center_x': .5, 'center_y': .5}
    overlay_color: 0, 0, 0, .85
    auto_dismiss: False
    Label:
        id: notification
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        font_size: '18sp'
        color: 1, .4, 0, 1
        pos_hint: {'center_x': .5, 'center_y': .6}
""")

Builder.load_string("""
<DisplayStats>:
    size_hint: .8, .95
    title_size: '18dp'
    title_font: 'OpenSans'
    title_color: .2, .6, .8, 1
    title_align: 'center'
    separator_color: 1, 1, 1, .5
    separator_height: '.5dp'
    auto_dismiss: True
""")

Builder.load_string("""
<NotesPopup>:
    title: 'A few reminders'
    title_size: '18sp'
    title_font: 'OpenSans'
    title_color: 1, .4, 0, 1
    separator_color: 1, 1, 1, .5
    separator_height: '.5dp'
    size_hint: .95, .6
    pos_hint: {'center_x': .5, 'center_y': .5}
    auto_dismiss: True
    FloatLayout:
        Label:
            text: root.text_1
            font_size: '18sp'
            color: 1, 1, 1, 1
            size_hint: .95, None
            text_size: self.width, None
            height: self.texture_size[1]
            halign: 'justify'
            valign: 'center'
            pos_hint: {'center_x': .5, 'center_y': .75}
        Label:
            text: root.text_2
            font_size: '18sp'
            color: 1, 1, 1, 1
            size_hint: .95, None
            text_size: self.width, None
            height: self.texture_size[1]
            halign: 'justify'
            valign: 'center'
            pos_hint: {'center_x': .5, 'center_y': .3}
""")


class DisplayStats(Popup):
    pass


class MessagePopup(Popup):
    notification = ObjectProperty(None)


class NotesPopup(Popup):
    text_1 = StringProperty(
        'Slide a player\'s label to the right to access average and total statistics. Slide it to '
        'the left to access statistics for each game he played.')
    text_2 = StringProperty(
        'Just press a player\'s label to access his statistics when you are viewing past competitions.')
