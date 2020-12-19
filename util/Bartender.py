# coding: utf-8

# In[180]:

import requests

# In[193]:

# Drink Class - Holds all the info needed to display a random drink
class Drink():
    def __init__(self, drink_dic, ingredients, measurements):
        self.img = drink_dic.get('strDrinkThumb')
        self.name = drink_dic.get('strDrink')
        self.category = drink_dic.get('strCategory')
        self.alcoholic = drink_dic.get('strAlcoholic')
        self.glass = drink_dic.get('strGlass')
        self.ingredients = self.make_ingredients_string(ingredients, measurements)
        self.instructions = drink_dic.get('strInstructions')
    
    '''
    # Combines the ingredient and measurment string lists together
    # Note: Some ingredients do not have corresponding measurements and will not be 
            added to the list with the following logic
    # TODO Account for ingredients that do not have corresponding measurements
    '''
    def make_ingredients_string(self, ingredients, measurements):
        ingredient_list = []
        for i in range(len(measurements)):
            ingredient_list.append(str(measurements[i]) + str(ingredients[i]))
        return ingredient_list
    
    def __str__(self):
        string = 'Name: ' + self.name + '\n' + 'Category: ' + self.category + '\n' + 'Alcoholic?: ' + self.alcoholic + '\n' + 'Ingredients: \n'
        for element in self.ingredients:
            string += '\t' + element + '\n'
        string += 'Instructions: ' + self.instructions
        return string
        


# In[194]:

'''
# Gets drink data from the API, removes empty fields and returns a 
'''
def get_drink():
    res = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    temp = (res.json())['drinks'][0]    
    
    # 
    ingredient = [temp.get(x) for x in temp if 'Ingredient' in x and temp.get(x) is not None]
    measure = [temp.get(x) for x in temp if 'Measure' in x and temp.get(x) is not None]
    drink_dic = {}
    for key in temp:
        if(temp[key] != None):
            drink_dic[key] = temp[key]    
    return Drink(drink_dic, ingredient, measure)
