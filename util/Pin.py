'''
@author: Keeth S.
@dependencies: discord, datetime
@desc: Creates a Pin object from the reply message served from robbot.py
@retunrs: async message back to channel confirming message was pinned
# TODO Optimize Drink Object.
'''

import discord
import datetime

class Pin:
    def __init__(self, message):
        self.author = message.author.display_name
        self.avatar = message.author.avatar_url
        self.channel = message.channel.name
        formated_date = datetime.date.strftime(message.created_at, "%m/%d/%Y")
        self.posted_date = formated_date
        self.content = message.content
    
    def embed(self):
        pin_embed = discord.Embed(title=self.author, description=f'Posted on {self.posted_date}', color=1146986)
        pin_embed.set_thumbnail(url=self.avatar)
        pin_embed.image.width = 300
        pin_embed.image.height = 300
        pin_embed.add_field(name="Channel", value=self.channel, inline=False)
        pin_embed.add_field(name="Message", value=self.content, inline=False)
        return pin_embed

