from discord import Embed

class Embedder():
        def __init__(self, title=None, description=None):
                self.title = title
                self.description = description

class DrinkEmbedder(Embedder):

    def __init__(self, drink):
        self.drink = drink
        Embedder.__init__(self, title=drink.name, description='A drink for you, good Bud.')
        self.embed = self.embed_drink(Embed(title=self.title, description=self.description))
        
    def embed_drink(self, embed):
        embed.set_image(url=self.drink.img)
        embed.add_field(name="Name", value=self.drink.name)
        embed.add_field(name="Category", value=self.drink.category)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name="Alcoholic?", value=self.drink.alcoholic)
        embed.add_field(name="Glass Type", value=self.drink.glass)
        embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in self.drink.ingredients:
            ingredient_string += string + '\n'
        embed.add_field(name="Ingredients", value=self.drink.ingredients, inline=False)
        embed.add_field(name="Instructions", value=self.drink.instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed