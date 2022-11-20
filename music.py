import discord
from client import client
import yt_dlp
import os

opts = {
    'format': 'bestaudio',
    'noplaylist': True,
    'outtmpl': 'music/new.mp3',
    'overwrites': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }
    ]
}

def next_song():
    os.remove('music/1.mp3')
    if len(os.listdir('music')) == 0:
        return
    for song in sorted(os.listdir('music')):
        queue_num = int(os.path.splitext(song)[0])
        os.rename('music/' + song, 'music/' + str(queue_num - 1) + os.path.splitext(song)[1])
    voice = client.voice
    player = discord.FFmpegPCMAudio('music/1.mp3')
    voice.play(player, after = lambda e: next_song())
        

@client.slash_command(name='play', description='enter youtube link')
async def play(ctx, link):
    with yt_dlp.YoutubeDL(opts) as ytdl:
        try:
            voice = await ctx.author.voice.channel.connect()
            client.voice = voice
        except discord.errors.ClientException:
            voice = client.voice
        except:
            await ctx.respond('You have to be in voice channel to use that command')
            return
        await ctx.respond('downloading...')
        try:
            ytdl.download(link)
            info = ytdl.extract_info(link, download=False)
            title = ytdl.sanitize_info(info)['title']
        except yt_dlp.utils.DownloadError:
            await ctx.respond("Invalid URL")
            return
        queue_num = len(os.listdir('music'))
        os.rename('music/new.mp3', f'music/{queue_num}.mp3')
        if queue_num == 1:
            await ctx.respond(f'playing {title}')
            player = discord.FFmpegPCMAudio('music/1.mp3')
            voice.play(player, after = lambda e: next_song())
        else:
            await ctx.respond(f'Added {title} to queue')
        
@client.slash_command(name='leave', description='Leaves VC')
async def leave(ctx):
    if ctx.author.voice.channel == client.voice.channel:
        await client.voice.disconnect()
        await ctx.respond('done')
        for file in os.listdir('music'):
            os.remove('music/' + file)
    else:
        await ctx.respond('You have to be in the same voice channel to use that command')

@client.slash_command(name='pause', description='Pause music')
async def pause(ctx):
    if ctx.author.voice.channel == client.voice.channel:
        client.voice.pause()
        await ctx.respond('paused')
    else:
        await ctx.respond('You have to be in the same voice channel to use that command')

@client.slash_command(name='resume', description='Resume music')
async def resume(ctx):
    if ctx.author.voice.channel == client.voice.channel:
        client.voice.resume()
        await ctx.respond('resumed')
    else:
        await ctx.respond('You have to be in the same voice channel to use that command')

@client.slash_command(name='skip', description='Skip song')
async def skip(ctx):
    if ctx.author.voice.channel == client.voice.channel:
        client.voice.stop()
        await ctx.respond('skipped')
    else:
        await ctx.respond('You have to be in the same voice channel to use that command')

