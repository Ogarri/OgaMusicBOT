import discord
from discord.ext import commands
import pytube
import os
import target.config as config

client = commands.Bot(command_prefix='!' , intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Le bot est connecté')

@client.command()
async def play(ctx, url):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice:
        voice = await ctx.author.voice.channel.connect()
    else:
        voice.move_to(ctx.author.voice.channel)
    
    # Télécharger la vidéo
    yt = pytube.YouTube(url)
    yt.streams.filter(only_audio=True).first().download(filename="song.mp3")

    # Lecture de la musique
    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    await ctx.send('Lecture')

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    await ctx.send('Je suis parti')

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
    await ctx.send('Pause')

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
    await ctx.send('Reprise')

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send('Arrêt')

client.run(config.token)