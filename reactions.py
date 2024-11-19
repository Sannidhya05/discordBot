from discord.ext import commands

def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        if message.content.lower().startswith("react ") or message.content.lower() == "react":
            await message.add_reaction("👍")  # Add thumbs-up emoji
            await message.add_reaction("🎉")  # Add party popper emoji

        if message.content.lower().startswith("hello ") or message.content.lower() == "hello":
            await message.add_reaction("👋")  # Add greet emoji

        if message.content.lower().startswith("hi ") or message.content.lower() == "hi":
            await message.add_reaction("👋")  # Add greet emoji

        if message.content.lower().startswith("heya ") or message.content.lower() == "heya":
            await message.add_reaction("👋")  # Add greet emoji

        if message.content.lower() == "good puppy":
            await message.add_reaction("🐶")  # Add dog emoji
