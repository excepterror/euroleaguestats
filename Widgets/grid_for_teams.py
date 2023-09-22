from kivy.clock import Clock
from kivy.properties import StringProperty, DictProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.gridlayout import GridLayout
from PIL import Image, ImageDraw, ImageFilter
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.behaviors import TouchRippleButtonBehavior


class TeamsLabelGrid(GridLayout):
    rosters = DictProperty({})
    _idx = NumericProperty()
    selected_roster = DictProperty({})

    def on_rosters(self, *args):
        for team, urls in self.rosters.items():
            team_label = TeamsLabel()
            team_label.im.source = 'Images/' + team + '.png'
            self.add_widget(team_label)

    def push_selected_roster(self, *args):
        self._idx += 1


class TeamsLabel(TouchRippleButtonBehavior, Label):
    shadow_texture = ObjectProperty(None)
    shadow_size = ListProperty([0, 0])
    shadow_pos = ListProperty([0, 0])
    team = StringProperty()
    im = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__()

        self.update_shadow = Clock.create_trigger(self.create_shadow)

    def on_size(self, *args, **kwargs):
        self.create_shadow()

    def on_pos(self, *args, **kwargs):
        self.create_shadow()

    def create_shadow(self, *args):
        # Increase blur_radius to increase blur blur_radius
        blur_radius = 25
        # Increase alpha to increase blur intensity
        alpha = .7

        width = self.size[0] + blur_radius * 6.
        height = self.size[1] + blur_radius * 6.
        offset_y = 1

        shadow_texture = self.create_shadow_background(blur_radius, alpha)
        self.shadow_texture = shadow_texture

        self.shadow_size = width, height

        self.shadow_pos = self.x - (width - self.size[0]) / 2.1, self.y - (height - self.size[1]) / 1.9 - offset_y

    def create_shadow_background(self, blur_radius, alpha):
        width = int(self.size[0] + blur_radius * 6.)
        height = int(self.size[1] + blur_radius * 6.)

        # create texture
        texture = Texture.create(size=(width, height), colorfmt='rgba')

        # make a blank image for the text, initialized to transparent text color
        im = Image.new('RGBA', (width, height), color=(1, 1, 1, 0))

        # get a drawing context
        draw = ImageDraw.Draw(im)

        # define the bounding box
        x0, y0 = (width - self.size[0]) / 2., (height - self.size[1]) / 2.
        x1, y1 = x0 + self.size[0] - 1, y0 + self.size[1] - 1
        draw.rectangle((x0, y0, x1, y1), fill=(0, 0, 0, int(255 * alpha)))

        # blurs the image with a sequence of extended box filters, which approximates a Gaussian kernel
        im = im.filter(ImageFilter.GaussianBlur(blur_radius * .25))

        # blit blurred image to texture
        texture.blit_buffer(im.tobytes(), colorfmt='rgba',  bufferfmt='ubyte')

        return texture

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.ripple_show(touch)
            return True
        return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.ripple_fade()
            try:
                for team, dict_with_urls in self.parent.rosters.items():
                    if self.text == team:
                        self.parent.selected_roster = dict_with_urls
            except ValueError:
                pass
            Clock.schedule_once(self.parent.push_selected_roster, .8)
            return True
        return False
