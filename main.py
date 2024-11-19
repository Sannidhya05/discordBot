import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
import reactions

# Get the bot token from the .env file
BOT_TOKEN = os.getenv('TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Event : Errors
@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")

# Event : Member joining
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")  # Replace with the role name
    channel = bot.get_channel(1208757573885624355) # Replace with your channel id
    if role:
        await member.add_roles(role)
    if channel:
        await channel.send(f"Welcome {member.mention}! You have been given the {role.name} role.")

# Event : Member leaving
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1208757573885624355) # Replace with your channel id
    if channel:
        await channel.send(f"Sadly {member.mention}  left us :(")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Reactions
reactions.setup(bot)

# Command: Commands
@bot.command()
async def commands(ctx):
    await ctx.send('''Commands:
ping - to ping the bot.
greet {name} - to greet someone.
commands - display all the commands.
join - to make it hop onto the vc you are in.
play {url} - makes it play the yt url you pasted.
stop - stops playing music.
leave - leaves the vc.''')

# Command : Say
@bot.command()
async def say(ctx, content):
    await ctx.send(f'{content}')

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