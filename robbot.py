import os
import discord
from requests.api import get
from util import Bartender
from dotenv import load_dotenv

SHEBANGS = '.!$'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await check_react_ohwow(message)

    if not should_respond_msg(message):
        return

    cmd = get_msg_cmd(message)

    if cmd == '8ball':
        pass
    if cmd == 'roll':
        pass
    if cmd == 'bg':
        await message.channel.send('hey')
    if cmd == 'drink' or cmd == 'cocktail':
        await get_cocktail(message)
    
    return



def should_respond_msg(msg) -> bool:
    if msg.author == client.user:  # Robbot is the author
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
        for emoji in client.emojis:
            if emoji.name == 'ohwow':
                await message.add_reaction(emoji)

'''
@author: Keeth S.
@dependencies: util/Bartender.py
@desc: Declares, fills and formats a discord embed object with drink info
@retunrs: async message back to channgel
# TODO Optimize Drink Object. Create Embed method?
'''
async def get_cocktail(msg):
    try:
        drink = Bartender.get_drink()
        embed_var = discord.Embed(title='Buds Bartender', description='A drink for you, dear bud.', color=1146986)
        embed_var.set_image(url=drink.img)
        embed_var.add_field(name="Name", value=drink.name)
        embed_var.add_field(name="Category", value=drink.category)
        embed_var.add_field(name="\u200b", value='\u200b')
        embed_var.add_field(name="\Alcoholic?", value=drink.alcoholic)
        embed_var.add_field(name="Glass Type", value=drink.glass)
        embed_var.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in drink.ingredients:
            ingredient_string += string + '\n'
        embed_var.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed_var.add_field(name="Instructions", value=drink.instructions, inline=False)
        embed_var.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")

        await msg.channel.send(embed=embed_var)
    
    except Exception as ex:
        print(ex)
        await msg.channel.send('Ayo, your code is wack.')



client.run(TOKEN)