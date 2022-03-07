from discord import Embed
from discord.colour import Color

#region Embedder
class Embedder():
   
    @staticmethod
    def embed_drink(drink) -> Embed:
        embed = Embed(title= drink.name, description='A drink for you, good Bud.', color=Color.dark_blue().value)
        embed.set_image(url= drink.img)
        embed.add_field(name="Name", value= drink.name)
        embed.add_field(name="Category", value= drink.category)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name="Alcoholic?", value= drink.alcoholic)
        embed.add_field(name="Glass Type", value= drink.glass)
        embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in  drink.ingredients_string:
            ingredient_string += string + '\n'
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(name="Instructions", value= drink.instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed

    @staticmethod
    def embed_pin(pin) -> Embed:
        embed = Embed(title=pin.author, description=f'Posted on {pin.posted_date}', color=Color.gold().value)
        pin_embed = embed
        pin_embed.set_thumbnail(url=pin.avatar)
        pin_embed.add_field(name="Channel", value=pin.channel, inline=False)
        if(pin.image is not None):
            pin_embed.set_image(url=pin.image)
        if(pin.content is not None):
            pin_embed.add_field(name="Message", value=f'[{pin.content}]({pin.url})', inline=False)
        else:
            pin_embed.add_field(name="Message", value='*This pin had no message*', inline=False)
        return pin_embed
#endregion