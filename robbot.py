import os
import json
import random
import re

import discord
from discord.ext import commands

from dotenv import load_dotenv

from requests.api import get
from util import Bartender

SHEBANGS = '.!$'
CFG_FILENAME = 'config.json'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open(CFG_FILENAME) as cfg:
    CFG = json.load(cfg)


bot = commands.Bot(command_prefix='.')

@bot.command(name='8ball')
async def shake_8ball(ctx):
    responses = CFG['8ball_responses']
    rand_i = random.randint(0, len(responses) - 1)
    response = responses[rand_i]
    await ctx.send(response)

@bot.command(name='roll')
async def roll(ctx, *args):
    dice_pattern = r'([0-9]*d[0-9]+)(\+[0-9]+)*'  # optional number, d, at least one number, e.g. 2d8, d20, etc

    matches = re.findall(dice_pattern, ' '.join(args))

    response = ''
    if len(matches) > 0:
        for match in matches:
            roll_part, offset_part = match

            if '+' in offset_part:
                _, offset = offset_part.split('+')
                offset = int(offset)
            else:
                offset = 0
            
            num_rolls, max_roll = roll_part.split('d')
            try:
                num_rolls = int(num_rolls)
            except:
                num_rolls = 1
            max_roll = int(max_roll)

            response += f'Roll {num_rolls}d{max_roll}+{offset}:    '

            rolls = [random.randint(1, max_roll) for _ in range(num_rolls)]
            roll_sum = sum(rolls) + offset
            roll_str = ' + '.join([str(roll) for roll in rolls]) + f' + {str(offset)} = {str(roll_sum)}\n'  # all this str() business is silly
            response += roll_str
    else:
        response = str(random.randint(1,100))

    await ctx.send(response)

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