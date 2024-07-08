from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

Builder.load_string("""
<MessagePopup>:
    notification: notification
    title: ''
    title_size: '0sp'
    title_font: 'MyriadPro'
    title_color: 1, .4, 0, 1
    separator_color: 1, .4, 0, 0
    size_hint: .9, .3
    pos_hint: {'center_x': .5, 'center_y': .5}
    overlay_color: 0, 0, 0, .85
    auto_dismiss: True
    Label:
        id: notification
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        font_size: '20dp'
        color: 1, .4, 0, 1
        pos_hint: {'center_x': .5, 'center_y': .6}
""")


class MessagePopup(Popup):
    notification = ObjectProperty(None)
