from services.Embedder import Embedder

'''
Drink Object
    Processes json data retrieved from the request object and
    stores a Discord.Embed object
'''
class Drink():
    def __init__(self, drink_json: dict):
        drink_json = self.sanitize_json(drink_json)
        self.img = drink_json.get('strDrinkThumb')
        self.name = drink_json.get('strDrink')
        self.category = drink_json.get('strCategory')
        self.alcoholic = drink_json.get('strAlcoholic')
        self.glass = drink_json.get('strGlass')
        self.ingredients_string = self.get_ingredient_string(drink_json)
        self.instructions = drink_json.get('strInstructions')
        self.embed = Embedder.embed_drink(self)

    
    def sanitize_json(self, json: dict):
        drink_dict = {}
        for key in json:
            if(json[key] != None):
                drink_dict[key] = json[key]  

        return drink_dict  
    
    
    def get_ingredient_string(self, json) -> list:
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