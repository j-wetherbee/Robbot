import asyncio
import discord
import youtube_dl

# This shit all comes from the basic voice example (https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py) and I don't know what half of it does tbh
youtube_dl.utils.bug_reports_message = lambda: ''

# might wanna throw this in config file
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'cookiefile': './util/Music/youtube.com_cookies.txt' # circumvent age restriction by supplying cookies from an age verified account
}

ffmpeg_options = {
    'options': '-vn'
}

try:
    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
except Exception as err:
    print(type(err))
    print(err.__str__())


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)