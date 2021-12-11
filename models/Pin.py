import datetime
from abc import ABC, abstractmethod
from discord import Message
from services.Embedder import PinEmbedder

'''
Pin Objects
    State is set by the message being pinned. Structure of the
    object is determined 
'''
class Pin:
    def __init__(self, message, embedder: PinEmbedder):

        self.author = message.author.display_name
        self.id = message.author.id
        self.avatar = message.author.avatar_url
        self.channel = message.channel.name
        formated_date = datetime.date.strftime(message.created_at, "%m/%d/%Y")
        self.posted_date = formated_date
        self.content = message.content
        self.url = message.jump_url
        
        self.image = None
        if(len(message.attachments) > 0):
            self.image = message.attachments[0].url
        if len(message.embeds) > 0:
            self.embed = message.embeds
        else:
            embeds = [embedder.embed(self)]
            self.embed = embeds