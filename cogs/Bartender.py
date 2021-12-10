import traceback
from discord.ext import commands
from models.Drink import Drink
from services import Sanitizer
from services import Embedder
from util import Utility

class Bartender(commands.Cog, name='Bartender', description='Used to provide any bud with a delicious, sensual drink'):
    factory_type = 'drink'
    def __init__(self, bot):
        self.bot = bot
        self._request = Utility.Request
        self._sanitizer = Sanitizer.SantizerFactory.get_sanitizer(Bartender.factory_type)
        self._embedder = Embedder.EmbedderFactory.get_embedder(Bartender.factory_type)
    
    @commands.command(name='drink', description='Get a nice, freshing drink from the Bartender',aliases=['drinks', 'cocktail', 'cocktails'])
    async def drink(self, ctx):
        try:
            json = self._request().get_drink_json()
            drink = Drink(json, self._embedder, self._sanitizer)
            await ctx.send(embed = drink.embed)
        except Exception as ex:
            traceback.print_exc()
            await ctx.send(f'Ayo, your code is wack.\n Error: {ex}')
    
def setup(bot):
    bot.add_cog(Bartender(bot))
