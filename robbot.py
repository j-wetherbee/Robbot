import os
import discord
import json
import random
import re
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
        dice_pattern = r'[0-9]*(d)[0-9]+'  # optional number, d, at least one number, e.g. 2d8, d20, etc

        match = re.search(dice_pattern, message.content)
        if match is not None:
            parts = match.group(0).split('d')
            try:
                num_rolls = int(parts[0])
            except:
                num_rolls = 1
            max_roll = int(parts[1])
            response = f'Roll {num_rolls}d{max_roll}: '
            for i in range(num_rolls):
                response += (str(random.randint(1, max_roll)) + ', ')
            response = response[:-2]
            await message.channel.send(response)
        else:
            await message.channel.send(str(random.randint(1, 100)))


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