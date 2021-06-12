'''
@author: Keeth S.
@params: filth: Object which needs to be sanitized
@desc: Parent Sanitizer Class
'''
class Sanitizer:
    

    def __init__(self, filth):
        self.filth = filth


'''
@author: Keeth S.
@params: json: dict
@desc: Drink Sanitizer which returns a sanitized version of the drink 
        json passed into it
'''
class DrinkJsonSanitizer(Sanitizer):
    

    def __init__(self, json: dict):
        Sanitizer.__init__(self, json)
    

    def clean_json(self):
        drink_dict = {}
        for key in self.filth:
            if(self.filth[key] != None):
                drink_dict[key] = self.filth[key]  

        return drink_dict