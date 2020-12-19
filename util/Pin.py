'''
@author: Keeth S.
@dependencies: discord, datetime
@desc: Creates a Pin object from the reply message served from robbot.py
@retunrs: async message back to channel confirming message was pinned
# TODO Make JSON file to save colors for users
       Allow users to customize their pin color 
'''

import discord
import datetime

'''
#Color List
DEFAULT: 0,
AQUA: 1752220,
GREEN: 3066993,
BLUE: 3447003,
PURPLE: 10181046,
GOLD: 15844367,
ORANGE: 15105570,
RED: 15158332,
GREY: 9807270,
DARKER_GREY: 8359053,
NAVY: 3426654,
DARK_AQUA: 1146986,
DARK_GREEN: 2067276,
DARK_BLUE: 2123412,
DARK_PURPLE: 7419530,
DARK_GOLD: 12745742,
DARK_ORANGE: 11027200,
DARK_RED: 10038562,
DARK_GREY: 9936031,
LIGHT_GREY: 12370112,
DARK_NAVY: 2899536,
LUMINOUS_VIVID_PINK: 16580705,
DARK_VIVID_PINK: 12320855
'''

# Dict of Server Member IDs and their coresponding colors
colors = {
    #Brady - Gold
    178851504076095488: 15844367,
    #Carlie - Purple
    323968599687430145: 10181046,
    #James - Grey
    191384926321508353: 9807270,
    #Derick - Blue
    179051738354024449: 3447003,
    #Keeth - Red
    636724139922554893: 15158332,
    #Rob - Orange
    209101464944115713: 15105570,
    #Robbot - Luminous Vivid Pink
    422470851435298818: 16580705
}

class Pin:
    def __init__(self, message):
        self.author = message.author.display_name
        self.id = message.author.id
        self.avatar = message.author.avatar_url
        self.channel = message.channel.name
        formated_date = datetime.date.strftime(message.created_at, "%m/%d/%Y")
        self.posted_date = formated_date
        self.content = message.content
    
    def embed(self):
        pin_embed = discord.Embed(title=self.author, description=f'Posted on {self.posted_date}', color=colors.get(self.id))
        pin_embed.set_thumbnail(url=self.avatar)
        pin_embed.image.width = 300
        pin_embed.image.height = 300
        pin_embed.add_field(name="Channel", value=self.channel, inline=False)
        pin_embed.add_field(name="Message", value=self.content, inline=False)
        return pin_embed

