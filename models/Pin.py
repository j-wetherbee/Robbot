import datetime
from discord import Embed, Color

'''
Pin Objects
    State is set by the message being pinned. Structure of the
    object is determined 
'''
class Pin:
    def __init__(self, message):
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
            embeds = [self.embed_pin()]
            self.embed = embeds

    def embed_pin(self) -> Embed:
        embed = Embed(title=self.author, description=f'Posted on {self.posted_date}', color=Color.gold().value)
        pin_embed = embed
        pin_embed.set_thumbnail(url=self.avatar)
        pin_embed.add_field(name="Channel", value=self.channel, inline=False)
        if(self.image is not None):
            pin_embed.set_image(url=self.image)
        if(self.content is not None):
            pin_embed.add_field(name="Message", value=f'[{self.content}]({self.url})', inline=False)
        else:
            pin_embed.add_field(name="Message", value='*This pin had no message*', inline=False)
        return pin_embed