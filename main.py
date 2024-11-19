import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
from music import join, leave, play
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

# Music
bot.add_command(join)
bot.add_command(leave)
bot.add_command(play)

# Run the bot
if BOT_TOKEN:
    bot.run(BOT_TOKEN)
else:
    print("Error: BOT_TOKEN not found in .env file")