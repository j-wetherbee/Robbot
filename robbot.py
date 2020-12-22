import os
import json
import random
import re
import requests
from discord.ext import commands
from dotenv import load_dotenv
from util.Request import Request
from util.Bartender import Drink
from util.Sanitizer import DrinkJsonSanitizer
from util.Formatter import DrinkFormatter
from util.Embedder import DrinkEmbedder
from util.Pin import Pin


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

@bot.command()
async def drink(ctx):
    try:
        drink_json = request.get_drink_json()
        drink = Drink(drink_json, sanitizer=DrinkJsonSanitizer, formatter=DrinkFormatter, embedder=DrinkEmbedder)
        await ctx.send(embed = drink.embed)
    except Exception as ex:
        print(ex)
        await ctx.send('Ayo, your code is wack.')

@bot.command()
async def test(ctx):
    await ctx.send('.test')

@bot.command()
async def cocktail(ctx):
    await drink(ctx)

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

'''
@author: Keeth S.
@dependencies: util/Bartender.py
@desc: Returns a random drink embedded from the Drink object's  embed method
@retunrs: async message back to channel
# TODO Optimize Drink Object.
'''
async def get_cocktail(msg):

    pass

'''
@author: Keeth S.
@dependencies: util/Pin.py
@desc: Sends a embed to the Pin channel when a user reply's to a message with .pin
@retunrs: async message back to channel confirming message was pinned
# TODO Optimize Drink Object.
'''
# async def pin_message(msg):
#     try:
#         if not msg.reference:
#             await msg.channel.send('Sorry, bud. Just can\'t do it.')
#             return
#         reply = await msg.channel.fetch_message(msg.reference.message_id)
#         pin_embed = Pin(reply)
#         pin_channel = client.get_channel(789771971532947486)
#         await pin_channel.send(embed=pin_embed.embed())
#         await msg.channel.send('You got it, bud.')
#     except Exception as ex:
#         print(ex)
#         await msg.channel.send('Ayo, your code is wack.')

bot.run(TOKEN)