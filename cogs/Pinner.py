import traceback
from discord.ext import commands
from models.Pin import Pin


class Pinner(commands.Cog, name='Pinner', description='Used to pin a Message to the Pin Channel'):
    PIN_CHANNEL_ID = 789771971532947486
    PIN_REACTION = '<:bigfoot:468234675622641674>'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pin', description='Reply to a message with this command to pin it to the Pin channel', aliases=['this'])
    async def pin(self, ctx: commands.Context):
        try:
            if not ctx.message.reference:
                await ctx.message.channel.send('You have to reply .pin to the message you want pinned.')
                return

            pin_channel = self.bot.get_channel(Pinner.PIN_CHANNEL_ID)
            reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            pin = Pin(reply)

            for embed in pin.embed:
                await pin_channel.send(embed=embed)
            await ctx.message.add_reaction(Pinner.PIN_REACTION)
            
        except Exception as ex:
            traceback.print_exc()
            await ctx.message.channel.send(f'Ayo, your code is wack.\n Error: {ex}')
    

def setup(bot):
    bot.add_cog(Pinner(bot))