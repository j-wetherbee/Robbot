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
    dice_pattern = r'[0-9]*(d)[0-9]+'  # optional number, d, at least one number, e.g. 2d8, d20, etc

    for arg in args:
        match = re.search(dice_pattern, arg)
        if match is not None:
            parts = match.group(0).split('d')
            try:
                num_rolls = int(parts[0])
            except:
                num_rolls = 1
            max_roll = int(parts[1])
            response = f'Roll {num_rolls}d{max_roll}: '
            for _ in range(num_rolls):
                response += (str(random.randint(1, max_roll)) + ', ')
            response = response[:-2]
            await ctx.send(response)
            break  
    else:
        await ctx.send(str(random.randint(1, 100)))

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

    # if not should_respond_msg(message):
    #     return

    cmd = get_msg_cmd(message)
        
    # if cmd == 'drink' or cmd == 'cocktail':
    #     await get_cocktail(message)

    await bot.process_commands(message)
    
    return
  

def should_respond_msg(msg) -> bool:
    if msg.author == bot.user:  # Robbot is the author
        return False
    if msg.content[0] not in SHEBANGS:
        return False
    return True

def get_msg_cmd(msg):
    content = msg.content[1:]
    parts = content.split()
    cmd = parts[0].lower()  # TODO check parts nonempty

    return cmd

async def check_react_ohwow(message):
    if 'oh wow' in message.content.lower():
        for emoji in bot.emojis:
            if emoji.name == 'ohwow':
                await message.add_reaction(emoji)



bot.run(TOKEN)