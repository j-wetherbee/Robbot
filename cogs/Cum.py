import traceback

import discord
from models.Pin import Pin
from discord.ext import commands
from util.Utility import Channels, Emojis

class Cum(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._cum_channel = Channels.CUM_CHANNEL.value
        self._robbot_testing_channel = Channels.ROBBOT_TESTING.value
        self._emoji = Emojis.NEVERFELTLIKE.value


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            if(message.channel.id != self._cum_channel and message.channel.id != self._robbot_testing_channel):
                return
            
            if(message.content.lower() == 'cum'):
                emoji = self.bot.get_emoji(self._emoji)
                await message.add_reaction(emoji)
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            await message.channel.send(f'Ayo, your code is wack.\n Error: {ex}')
    
def setup(bot):
    bot.add_cog(Cum(bot))