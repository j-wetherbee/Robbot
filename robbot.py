import os
import json
import random
import re
import requests
from discord.ext import commands
from dotenv import load_dotenv
from funcs.Bartender import Drink
from funcs.Pin import Pin
from util.Request import Request
from util.Sanitizer import DrinkJsonSanitizer
from util.Formatter import DrinkFormatter
from util.Embedder import DrinkEmbedder, PinEmbedder
from util import Rolls

CFG_FILENAME = 'config.json'
request = Request(requests)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open(CFG_FILENAME) as cfg:
    CFG = json.load(cfg)


bot = commands.Bot(command_prefix='.')

@bot.command(name='8ball')
async def shake_8ball(ctx):
    responses = CFG['8ball_responses']
    response = random.choice(responses)
    await ctx.send(response)

@bot.command(name='roll')
async def roll(ctx, *args):
    args_as_str = ' '.join(args)

    roll = Rolls.rolls_from_args(args_as_str)
    await ctx.send(roll, tts=True)

'''
@author: Keeth S.
@desc: Returns a random drink embedded from the Drink object's  embed method
@retunrs: async message back to channel
'''
@bot.command()
async def drink(ctx):
    try:
        drink_json = request.get_drink_json()
        drink = Drink(drink_json, DrinkJsonSanitizer, DrinkFormatter, DrinkEmbedder)
        await ctx.send(embed = drink.embed)
    except Exception as ex:
        print(ex)
        await ctx.send('Ayo, your code is wack.')

@bot.command()
async def cocktail(ctx):
    await drink(ctx)

'''
@author: Keeth S.
@desc: Sends a embed to the Pin channel when a user reply's to a message with .pin
@retunrs: async message back to channel confirming message was pinned
'''
@bot.command()
async def pin(ctx):
    try:
        if not ctx.message.reference:
            await ctx.message.channel.send('You have to reply .pin to the message you want pinned.')
            return
        reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        pin = Pin(reply, PinEmbedder)
        pin_channel = bot.get_channel(789771971532947486)
        await pin_channel.send(embed=pin.embed)
        await ctx.message.channel.send('You got it, bud.')
    except Exception as ex:
        print(ex)
        await ctx.message.channel.send(f'Ayo, your code is wack.\n Error: {ex}')

@bot.command()
async def test(ctx):
    await ctx.send('.test')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    await check_react_ohwow(message)

    await bot.process_commands(message)
    
    return

async def check_react_ohwow(message):
    if 'oh wow' in message.content.lower():
        for emoji in bot.emojis:
            if emoji.name == 'ohwow':
                await message.add_reaction(emoji)


async def get_cocktail(msg):

    pass

bot.run(TOKEN)