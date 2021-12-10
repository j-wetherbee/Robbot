from services.Embedder import DrinkEmbedder
from services.Sanitizer import DrinkSanitizer

'''
Drink Object
    Processes json data retrieved from the request object and
    stores a Discord.Embed object

    TODO: Consider rewriting this as a functional module vs a Class
'''
class Drink():

    def __init__(self, drink_json: dict, embedder: DrinkEmbedder, sanitizer: DrinkSanitizer):
        _json = sanitizer.clean_filth(drink_json)
        self._img = _json.get('strDrinkThumb')
        self._name = _json.get('strDrink')
        self._category = _json.get('strCategory')
        self._alcoholic = _json.get('strAlcoholic')
        self._glass = _json.get('strGlass')
        self._ingredients_string = self.__get_ingredient_string(_json)
        self._instructions = _json.get('strInstructions')
        self.embed = embedder.embed(self)

    def __get_ingredient_string(self, json) -> list:
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
        
        
    def __repr__(self):
        new_line='\n'
        tab = '\t'
        bracket = '{}'
        rerp_string = f'Drink{bracket[0]}{new_line}{tab}name: {self._name},{new_line}{tab}category: {self._category},{new_line}{tab}alcoholic: {self._alcoholic},'
        rerp_string += f'{new_line}{tab}glass: {self._glass},{new_line}{tab}ingredients: {self.ingredients__string},{new_line}{tab}instructions: {self._instructions},'
        rerp_string += f'{new_line}{tab}image: {self._img},{new_line}{tab}embed: {self.embed},{new_line}{tab}{new_line}{tab}sanitzier: {self._sanitizer},'
        rerp_string += f'{new_line}{tab}{new_line}{tab}formatter: {self._formatter},{new_line}{tab}{bracket[1]}'  
        return rerp_string 