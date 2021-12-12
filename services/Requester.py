import requests
from abc import ABC, abstractmethod

class Requester(ABC):
    @abstractmethod
    def fetch():
        '''
        Fetch method to gather data from the URL source
        '''
        pass

class DrinkRequester(Requester):
    def __init__(self, requests: requests):
        self._requests = requests
        self.url = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'

    def fetch(self):
        return self._requests.get(self.url).json()['drinks'][0]

class RequesterFactory:
    requesters = {
        "drink": DrinkRequester
    }
    
    @staticmethod
    def get_requester(type: str, requests):
        if type in RequesterFactory.requesters:
            return RequesterFactory.requesters[type](requests=requests)
        else:
            raise KeyError('Not a valid Requester Type')