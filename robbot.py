import os
import json
import random
import discord
import requests
import traceback
from discord.ext import commands
from dotenv import load_dotenv
from models.Pin import Pin
from util import Utility
from util import Rolls

CFG_FILENAME = 'config.json'
request = Utility.Request()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open(CFG_FILENAME) as cfg:
    CFG = json.load(cfg)


bot = commands.Bot(command_prefix='.')

'''
    Cog Functions & Commands
'''
def load_cogs():
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):              
            bot.load_extension(f'cogs.{files[:-3]}')
            print(f'{files[:-3]} extension loaded')

def unload_cogs():
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):              
            bot.unload_extension(f'cogs.{files[:-3]}')
            print(f'{files[:-3]} extension unloaded')

@bot.command(name='refresh', description='Reloads all cogs', alais=['refresh, reload'])
async def refresh(ctx: commands.Context):
    print('Reloading Cogs...\n')
    unload_cogs()
    load_cogs()
    print('Cogs reloaded successfully')
    reaction = '👍'
    await ctx.message.add_reaction(reaction)


'''
    TODO: Create Cogs for the follow commands
'''
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


load_cogs()
bot.run(TOKEN)