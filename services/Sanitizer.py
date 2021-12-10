from abc import ABC, abstractmethod
from enum import Enum

#region Sanitizers
'''
@author: Keeth S.
@params: filth: Object which needs to be sanitized
@desc: Parent Sanitizer Class
'''
class Sanitizer(ABC):
    
    @abstractmethod
    def clean_filth(filth):
        ''' Cleans the incoming filth data for the given sanitizer object '''
        pass

'''
@author: Keeth S.
@params: json: dict
@desc: Drink Sanitizer which returns a sanitized version of the drink 
        json passed into it
'''
class DrinkSanitizer(Sanitizer):
    
    def __init__(self, json=None):
        Sanitizer.__init__(self, json)
    
    def clean_filth(self, json: dict):
        drink_dict = {}
        for key in json:
            if(json[key] != None):
                drink_dict[key] = json[key]  

        return drink_dict

'''
@author: Keeth S.
@desc: Sanitizer Factory Object
'''
class SantizerFactory:

    sanitizers = {
        "drink": DrinkSanitizer
    }
    
    @staticmethod
    def get_sanitizer(type: str):
        if type in SantizerFactory.sanitizers:
            return SantizerFactory.sanitizers[type]()
        else:
            raise KeyError('Not a valid Sanitizer Type')
#endregion