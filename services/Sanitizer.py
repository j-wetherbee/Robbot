from abc import ABC, abstractmethod
from enum import Enum

#region Sanitizers
class Sanitizer(ABC):
    
    @abstractmethod
    def clean_filth(filth):
        ''' Cleans the incoming filth data for the given sanitizer object '''
        pass

class DrinkSanitizer(Sanitizer):

    @staticmethod    
    def clean_filth(json: dict):
        drink_dict = {}
        for key in json:
            if(json[key] != None):
                drink_dict[key] = json[key]  

        return drink_dict

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