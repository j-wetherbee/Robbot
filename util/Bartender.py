# coding: utf-8
'''
@author: Keeth S.
@dependencies: requests, discord
@desc: Calls API and fills a Drink object to be served to robbot.py
@retunrs: Drink object with embed method
@TODO Account for ingredients that do not have corresponding measurements
'''
# In[180]:

import requests
import discord

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
    
    '''
    # Creates the formated embed when called. 
    # Iterates through ingredients and adds them to a field
    '''
    def embed(self):
        drink_embed = discord.Embed(title='Buds Bartender', description='A drink for you, dear bud.', color=1146986)
        drink_embed.set_image(url=self.img)
        drink_embed.add_field(name="Name", value=self.name)
        drink_embed.add_field(name="Category", value=self.category)
        drink_embed.add_field(name="\u200b", value='\u200b')
        drink_embed.add_field(name="Alcoholic?", value=self.alcoholic)
        drink_embed.add_field(name="Glass Type", value=self.glass)
        drink_embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in self.ingredients:
            ingredient_string += string + '\n'
        drink_embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        drink_embed.add_field(name="Instructions", value=self.instructions, inline=False)
        drink_embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return drink_embed
        


# In[194]:

'''
# Gets drink data from the API
# Removes empty fields
# Returns a Drink object 
'''
def get_random_drink():
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
