'''
@author: Keeth S.
@parms: requests: requests module object
@desc: Object used to get resources outside of the config file
@TODO: Move urls to config file / Make url entries into attributes /
        Abstract Request as Parent classs(?)
'''
class Request:
    def __init__(self, requests):
        self._requests = requests
        self.urls = {
            "cocktail_db_api": 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
        }
    
    def get_drink_json(self):
        return self._requests.get(self.urls['cocktail_db_api']).json()['drinks'][0]   