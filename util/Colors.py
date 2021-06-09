from .Configurable import Configurable

class UserColors(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        self._user_color_list = self._get_user_color_list()
        self.brady = self._user_color_list['Brady']
        self.carlie = self._user_color_list['Carlie']
        self.derick = self._user_color_list['Derick']
        self.keeth = self._user_color_list['Keeth']
        self.james = self._user_color_list['James']
        self.rob = self._user_color_list['Rob']
        self.robbot = self._user_color_list['Robbot']
    
    def _get_user_color_list(self):
        user_color_list = {}
        
        for guid, obj in self._file['users'].items():
            user_color_list[obj['name']] = obj['embed_color']
        return user_color_list
    
    def get_user_color(self, guid: str):
        if guid is not None:
            guid = str(guid)
            
        __user_list = self._file['users']
        if guid in __user_list:
            return __user_list[guid]['embed_color']

class Colors(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        self.user_colors = UserColors()
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