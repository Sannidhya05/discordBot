import discord
from discord.ext import commands
from tenacity import retry, stop_after_attempt, wait_fixed, sleep
import yt_dlp

# Command: Join a voice channel
@commands.command()
async def join(ctx):
    if ctx.author.voice:  # Check if the user is in a voice channel
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel.name}!')
    else:
        await ctx.send("You're not in a voice channel!")

# Command: Leave the voice channel
@commands.command()
async def leave(ctx):
    if ctx.voice_client:  # Check if the bot is in a voice channel
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected!")
    else:
        await ctx.send("I'm not in a voice channel!")

# Command: Play audio from YouTube
@commands.command()
async def play(ctx, *, query):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not in a voice channel!")
            return

    try:
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'cookiefile': 'cookies.txt',
            'postprocessors': [{'key': 'FFmpegMetadata'}],
            'noplaylist': True
        }

        @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
        def extract_audio_info(ydl, query):
            return ydl.extract_info(query, download=False)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not query.startswith(('http://', 'https://')):
                search_result = extract_audio_info(ydl, f"ytsearch:{query}")
                if not search_result['entries']:
                    await ctx.send("No results found for your query!")
                    return
                audio_info = search_result['entries'][0]
            else:
                audio_info = extract_audio_info(ydl, query)

            audio_url = audio_info['url']
            title = audio_info.get('title', 'Unknown')
            print(f"Audio URL: {audio_url}")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        ctx.voice_client.play(source, after=lambda e: print(f"Finished playing: {e}" if not e else f"Error: {e}"))
        await ctx.send(f"Now playing: {title}")

        # Start a disconnect timer
        await disconnect_timer(ctx)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

async def disconnect_timer(ctx):
    await sleep(300)
    if not ctx.voice_client.is_playing():
        await ctx.voice_client.disconnect()

