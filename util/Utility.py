import json
import requests    
from enum import Enum
from discord import Embed

#region Configuration
'''
@author: Keeth S.
@desc: Parent Configuration object used to store the config file
'''
class Configurable():
    def __init__(self):
        self._file = self._get_config_file()
    
    def _get_config_file(self):
        CFG_FILENAME = './config.json'
        with open(CFG_FILENAME) as cfg:
            CFG = json.load(cfg)
        return CFG
#endregion

#region Request
'''
@author: Keeth S.
@parms: requests: requests module object
@desc: Object used to get resources outside of the config file
@TODO: Move urls to config file / Make url entries into attributes /
        Abstract Request as Parent classs(?)
'''
class Request:
    def __init__(self):
        self._requests = requests
        self.urls = {
            "cocktail_db_api": 'https://www.thecocktaildb.com/api/json/v1/1/random.php',
        }
    
    def get_drink_json(self):
        return self._requests.get(self.urls['cocktail_db_api']).json()['drinks'][0]
#endregion

#region Formatter
'''
@author: Keeth S.
@params: arg: Object passed in to be formatted
@desc: Parent Formatter Class
'''
class Formatter():
    
    def __init__(self, arg):
        self.arg = arg


    def get_filth_type(self):
        return f'Type: {str(type(self.arg))}'


'''
@author: Keeth S.
@params: json: dict
@desc: Drink Formatter which formats the ingredient's
        and measurments of a drink
'''
class DrinkFormatter(Formatter):

    def __init__(self, json: dict):
        if(isinstance(json, dict) != True):
            raise TypeError('The argument must be of type dict')
        Formatter.__init__(self, json)
        self.ingredients_string = self.make_ingredients_string(self.arg)

    def make_ingredients_string(self, json):
        ingredients = [json.get(ing) for ing in json if 'Ingredient' in ing and json.get(ing) is not None]
        measurements = [json.get(measure) for measure in json if 'Measure' in measure and json.get(measure) is not None]
        
        if(len(measurements) == 0):
            return ingredients
        
        ingredient_list = []
        for i in range(len(ingredients)):
            if(i < len(measurements)):
                ingredient_list.append(measurements[i].strip() + " " + ingredients[i])
            elif(ingredients[i] == ' '):
                pass
            else:
                ingredient_list.append(ingredients[i])
        return ingredient_list
#endregion

#region Colors
'''
@author: Keeth S.
@desc: Configuration Child Object which stores the color values for each 
        user in the server
'''
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


'''
@author: Keeth S.
@desc: Configuration Child which stores the values of 
        colors which can be accessed globally.
'''
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
#endregion

#region Channels
'''
@author: Keeth S.
@desc: Enum of all Channel ids
'''
class Channels(Enum):
        JERIFISSHU = 208694891486773248
        NSFW = 324699837297721344
        JAZZ_ZONE = 335923711662227456
        GAME_IDEAS = 842496144603873291
        SHITPOST = 413881959857520640
        DND = 790011375220162590
        SET_AND_BETS = 580583079597572096
        BUDS_N_CRAFT = 804897670065815552
        BUD_COURT = 796190794334732298
        NEW_CHANEL_OLD = 796187591162069003
        CUM_CHANNEL = 819458956606439424
        NEW_CHANNEL = 872613001709113414
        MUSIC_QUEUE = 741139638072246323
        GAMING_ZONE = 380181785390088203
        DEBATE_ZONE = 786065089367113728
        AFK = 291414646189981696
        PINS = 789771971532947486
        HALL_OF_FAME = 833063954602786836
        ROBBOT_TESTING = 789662489092030494
#endregion

#region Channels
'''
@author: Keeth S.
@desc: Enum of all Role ids
'''
class Roles(Enum):
    PATRIARCH = 290567553510539264
    CAPTAIN = 290566787580428288
    DEV = 789929955743236106
    LIEUTENANT = 290566792760262656
    FUCKBOY = 323617141054111756
#endregion

#region Emojis
'''
@author: Keeth S.
@desc: Enum of all Emoji ids
'''
class Emojis(Enum):
    HEEHO = 324008832735117312
    RISE = 324010369267793930
    NEVERFELTLIKE = 324011042890055680
    NOTLIKETHIS = 324012625342103552
    AIGIS = 324013626253901836
    FRANCISYORKMORGAN = 324013824338427905
    HATSUNEMIKU = 324023809374158848
    BLASTED = 324023892786151425
    POSITIVETHINKING = 324023913946284035
    EVERYDAY = 324694469150638093
    STOP = 324694491510472704
    OHWOW = 324694529733296128
    KOROMARU = 324694541871480832
    ORLANDO = 324694553200427009
    SPEED = 324694586855391244
    SUPERNUT = 324694596397432833
    TIFA = 324694604903481344
    VINCENT = 324694614823010314
    BUTTHETEACHINGS = 324694624708984832
    ZILTOID = 324694636972998657
    AUTISTICSCREECHING = 324694662759841792
    DERICK = 324695421639196672
    HURR = 324696431904686090
    CRAWLING = 324699598914453504
    THATSRAD = 324706382781743105
    STUPID_IDIOT = 324724786557353984
    SMUGTEACHER = 324745655878811648
    DDOG = 324750990630846474
    SAKEGREMLIN = 324752939904270336
    Q_ = 325104825882902538
    DOTHEYSMUGEVERYTIME = 325105720121098240
    HAHAA = 325106039345381376
    KIRYU = 325106393701023744
    LOLOL = 325107124931788800
    LETSNOTDOTHATTODAY = 336164623453650944
    RIBBERTSTIBBERT = 399288392321335307
    HMMM = 399302648169496577
    HMMMMM = 399304587745689600
    YOTSUBATUNES = 399311065416204288
    NOWIMMOTIVATED = 458107334926008331
    BIGFOOT = 468234675622641674
    BIGBOSSU = 468564992334233600
    OHJEEZ = 543988083306266624
    PERSONA = 543996812160401408
    SMIRK = 734835488166379550
    HMM = 791116665202016256
    UM = 791118149063147560
    EDGYSMILE = 796455827556270120
    CRINGESHOCK = 796455847127416882
    HEH = 803777598877597736
    DROOL = 804524633998622740
    SAYHUH = 832708202852253706
#endregion