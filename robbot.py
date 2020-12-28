import os
import json
import random
import re

import discord
from discord.ext import commands

from dotenv import load_dotenv

from requests.api import get
from util import Bartender
from util import Rolls


CFG_FILENAME = 'config.json'

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

@bot.command(name='cocktail')
async def get_cocktail(ctx):
    try:
        await ctx.send(embed=Bartender.get_random_drink().embed())
    except Exception as ex:
        print(ex)
        await ctx.send('Ayo, your code is wack.')

@bot.command()
async def drink(ctx):
    await get_cocktail(ctx)

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


bot.run(TOKEN)