from discord import Embed
from .Colors import Colors

class DrinkEmbedder():

    def __init__(self, drink):
        self.drink = drink
        embed = Embed(title=self.drink.name, description='A drink for you, good Bud.', color=Colors().dark_navy)
        self.embed = self.embed_drink(embed)
        
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
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(name="Instructions", value=self.drink.instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed

class PinEmbedder():
    def __init__(self, pin):
        self.pin = pin
        embed = Embed(title=self.pin.author, description=f'Posted on {self.pin.posted_date}', color=int(Colors().user_colors.get_user_color(self.pin.id)))
        self.embed = self.embed_pin(embed)

    def embed_pin(self, embed):
        pin_embed = embed
        pin_embed.set_thumbnail(url=self.pin.avatar)
        pin_embed.add_field(name="Channel", value=self.pin.channel, inline=False)
        if(self.pin.image is not None):
            pin_embed.set_image(url=self.pin.image)
        if(self.pin.content is not None):
            pin_embed.add_field(name="Message", value=f'[{self.pin.content}]({self.pin.url})', inline=False)
        else:
            pin_embed.add_field(name="Message", value='*This pin had no message*', inline=False)
        return pin_embed