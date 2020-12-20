import os
import discord
import json
import random
from dotenv import load_dotenv

SHEBANGS = '.!$'
CFG_FILENAME = 'config.json'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

with open(CFG_FILENAME) as cfg:
    CFG = json.load(cfg)


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
        responses = CFG['8ball_responses']
        rand_i = random.randint(0, len(responses) - 1)
        response = responses[rand_i]
        await message.channel.send(response)

    if cmd == 'roll':
        pass
    if cmd == 'bg':
        await message.channel.send('hey')
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

client.run(TOKEN)