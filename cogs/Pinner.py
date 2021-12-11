from re import L
import traceback
from discord.ext import commands
from models.Pin import Pin
from services import Embedder
from util.Utility import Channels

class Pinner(commands.Cog, name='Pinner', description='Used to pin a Message to the Pin Channel'):
    factory_type = 'pin'

    def __init__(self, bot):
        self.bot = bot
        self._embedder = Embedder.EmbedderFactory.get_embedder(Pinner.factory_type)

    @commands.command(name='pin', description='Reply to a message with this command to pin it to the Pin channel', aliases=['this'])
    async def pin(self, ctx: commands.Context):
        try:
            if not ctx.message.reference:
                await ctx.message.channel.send('You have to reply .pin to the message you want pinned.')
                return
            
            pin_channel = self.bot.get_channel(Channels.PINS.value)
            reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)

            pin = Pin(reply, self._embedder)
            for embed in pin.embed:
                await pin_channel.send(embed=embed)

            emoji = '<:bigfoot:468234675622641674>'
            await ctx.message.add_reaction(emoji)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            await ctx.message.channel.send(f'Ayo, your code is wack.\n Error: {ex}')
    
def setup(bot):
    bot.add_cog(Pinner(bot))