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

class FormatterFactory:
    embedders = {
        "drink": DrinkFormatter
    }
    
    @staticmethod
    def get_sanitizer(type: str):
        if type in Formatter.embedders:
            return Formatter.embedders[type]()
        else:
            raise KeyError('Not a valid Formatter Type')
#endregion