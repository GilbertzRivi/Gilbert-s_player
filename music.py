import discord
from client import client
import yt_dlp
import os
from discord import Embed

opts = {
    'format': 'bestaudio',
    'noplaylist': True,
    'outtmpl': 'new/%(title)s.mp3',
    'overwrites': True,
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }
    ]
}

def next_song():
    for song in os.listdir('music'):
        num = int(song.split(';', 1)[0])
        print(song, num)
        if num == 1: break
    os.remove(f'music/{song}')
    if len(os.listdir('music')) == 0:
        return
    for song in sorted(os.listdir('music')):
        queue_num = int(os.path.splitext(song)[0].split(';', 1)[0])
        os.rename('music/' + song, 'music/' + str(queue_num - 1) + ';' + os.path.splitext(song)[0].split(';', 1)[1] + os.path.splitext(song)[1])
    voice = client.voice
    for song in os.listdir('music'):
        num = song.split(';', 1)[0]
        if num == 1: break
    player = discord.FFmpegPCMAudio(f'music/{song}')
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
        queue_num = len(os.listdir('music')) + 1
        song = os.listdir('new')[0]
        os.rename(f'new/{song}', f'music/{queue_num} ; {title}.mp3')
        if queue_num == 1:
            await ctx.respond(f'playing {title}')
            for song in os.listdir('music'):
                num = song.split(';', 1)[0]
                if num == 1: break
            player = discord.FFmpegPCMAudio(f'music/{song}')
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

@client.slash_command(name='q', description='Shows current queue')
async def q(ctx, page=1):
    songs = []
    for song in os.listdir('music'):
        num = os.path.splitext(song)[0].split(';', 1)[0]
        title = os.path.splitext(song)[0].split(';', 1)[1]
        songs.append({'num': num, 'title': title})
    songs.sort(key=lambda s: s['num'])
    songs = songs[10*(page-1):10*page]
    embed = Embed(title='queue')
    for song in songs:
        embed.add_field(name=song['num'], value=song['title'], inline=False)
    await ctx.respond(embed=embed)

@client.slash_command(name='qc', description='Swaps places of two songs')
async def qc(ctx, num1, num2):
    for song in os.listdir('music'):
        if int(song.split(';', 1)[0]) == int(num1):
            song1 = song
            os.rename(f'music/{song}', f'music/swap1.mp3')
        if int(song.split(';', 1)[0]) == int(num2):
            song2 = song
            os.rename(f'music/{song}', f'music/swap2.mp3')
    swaped1 = song1.split(";", 1)[0] + " ; " + song2.split(';', 1)[1]
    swaped2 = song2.split(";", 1)[0] + " ; " + song1.split(';', 1)[1]
    os.rename('music/swap1.mp3', f'music/{swaped1}')
    os.rename('music/swap2.mp3', f'music/{swaped2}')
    await ctx.respond('Done')
