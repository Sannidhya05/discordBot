import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp

# Get the bot token from the .env file
BOT_TOKEN = os.getenv('TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Command: Join a voice channel
@bot.command()
async def join(ctx):
    if ctx.author.voice:  # Check if the user is in a voice channel
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel.name}!')
    else:
        await ctx.send("You're not in a voice channel!")

# Command: Leave the voice channel
@bot.command()
async def leave(ctx):
    if ctx.voice_client:  # Check if the bot is in a voice channel
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected!")
    else:
        await ctx.send("I'm not in a voice channel!")

# Command: Play audio from YouTube
@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel!")
            return

    try:
        ffmpeg_options = {
            'options': '-vn'  # Disable video processing
        }

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegMetadata'
            }]
        }

        # Fetch the audio stream URL using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        # Play the audio stream using FFmpeg
        source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        ctx.voice_client.stop()  # Stop any currently playing audio
        ctx.voice_client.play(source, after=lambda e: print(f"Finished playing: {e}"))
        await ctx.send(f"Now playing: {info.get('title', 'Unknown')}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

# Run the bot
if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: BOT_TOKEN not found in .env file")
