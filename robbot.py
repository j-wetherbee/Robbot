import os
import json
import random
import re

import discord
from discord.ext import commands

from dotenv import load_dotenv

from requests.api import get
from util import Bartender


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

    dnd_rolls = _find_dnd_rolls(args_as_str)
    
    # TODO probably replace this with polymorphism
    if dnd_rolls:
        response = _roll_dnd_dice(dnd_rolls)
    else:
        response = str(random.randint(1,100))

    await ctx.send(response)

def _find_dnd_rolls(to_search: str):
    dice_pattern = r'([0-9]*d[0-9]+)(\+[0-9]+)*'
    matches = re.findall(dice_pattern, to_search)
    return matches

def _roll_dnd_dice(roll_descriptions):
    results = [_roll_dnd_die(roll) for roll in roll_descriptions]
    return ''.join(results)

def _roll_dnd_die(roll_description):
    roll_part, offset_part = roll_description  # roll_description doesn't shed any light on what it actually is, a tuple of matching regex groups

    offset = _get_dnd_roll_offset(offset_part)
    num_rolls = _get_dnd_roll_num(roll_part)
    max_roll = _get_dnd_roll_max(roll_part)
    
    result = f'Roll {num_rolls}d{max_roll}+{offset}:    '
    rolls = [random.randint(1, max_roll) for _ in range(num_rolls)]  # the way this stuff is written prevents it from being further decoupled, e.g. a func that rolls once contained in a larger func that rolls all and sums
    roll_sum = sum(rolls) + offset
    result += ' + '.join([str(roll) for roll in rolls]) + f' + {str(offset)} = {str(roll_sum)}\n'  # all this str() business is silly

    return result

def _get_dnd_roll_offset(offset_description):
    offset_parts = offset_description.split('+')
    offset = offset_parts[-1]
    if not offset:
        offset = 0
    return int(offset)

def _get_dnd_roll_num(roll_description):
    roll_parts = roll_description.split('d')
    num_rolls = roll_parts[0]
    if not num_rolls:
        num_rolls = 1
    return int(num_rolls)

def _get_dnd_roll_max(roll_description):
    roll_parts = roll_description.split('d')
    max_roll = roll_parts[-1]
    return int(max_roll)

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