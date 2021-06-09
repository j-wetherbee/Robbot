from .Configurable import Configurable

class Colors(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        self._color_list = self._file['colors']
        self.aqua = self._get_color('AQUA')
        self.green = self._get_color('GREEN')
        self.blue = self._get_color('BLUE')
        self.purple = self._get_color('PURPLE')
        self.gold = self._get_color('GOLD')
        self.orange = self._get_color('ORANGE')
        self.red = self._get_color('RED')
        self.grey = self._get_color('GREY')
        self.light_grey = self._get_color('LIGHT_GREY')
        self.navy = self._get_color('NAVY')
        self.dark_aqua = self._get_color('DARK_AQUA')
        self.dark_green = self._get_color('DARK_GREEN')
        self.dark_blue = self._get_color('DARK_BLUE')
        self.dark_purple = self._get_color('DARK_PURPLE')
        self.dark_gold = self._get_color('DARK_GOLD')
        self.dark_orange = self._get_color('DARK_ORANGE')
        self.dark_red = self._get_color('DARK_RED')
        self.dark_grey = self._get_color('DARK_GREY')
        self.darker_grey = self._get_color('DARKER_GREY')
        self.dark_navy = self._get_color('DARK_NAVY')
        self.vivid_pink = self._get_color('LUMINOUS_VIVID_PINK')
        self.dark_vivd_pink = self._get_color('DARK_VIVID_PINK')

    def _get_color(self, color):
        return self._color_list[color]