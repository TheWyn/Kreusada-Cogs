import contextlib
import inspect
import json
import pathlib

import discord
import mystbin
from redbot.core import commands, Config

cli = mystbin.Client()

class Mystbinner(commands.Cog):
    """Automatically upload files/cog files to mystbin."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 9423853940580295, force_registration=True)
        self.config.register_guild(
            channels=[],
        )

    @commands.group()
    async def mystbin(self, ctx):
        """Manually upload/setup mystbin."""

    @mystbin.command(name="cog")
    async def mystbin_cog(self, ctx, cog: str, cog_file: str):
        """Upload the contents of a cog without having to directly upload the file.

        Parameters

        ``cog``: The cog to get the file from.
        ``cog_file``: The filename for the file to upload. 
        Please provide a slash if this file happens to be part of a seperate file.

        **Examples**

        ``[p]mystbin cog Mystbinner mystbinner.py``
        ``[p]mystbin cog Mystbinner folder/file.txt``
        """
        cog_obj = self.bot.get_cog(cog)
        if not cog_obj:
            return await ctx.send(f"Cog '{cog}' not found.")
        cog_file = cog_file.strip("/")
        try:
            await ctx.trigger_typing()
            with open(pathlib.Path(inspect.getfile(cog_obj.__class__)).parent / cog_file, encoding="utf-8") as f:
                file_content = "".join(f.readlines())
                link = await cli.post(file_content, syntax=f.name.split('.')[-1])
            embed = discord.Embed()
            await ctx.send(f"`{cog_file.split('/')[-1]}` uploaded to Mystbin\n> {link}")
        except FileNotFoundError:
            return await ctx.send("Could not resolve a directory for the provided parameters.")
        except UnicodeDecodeError:
            return await ctx.send("This file had weird encoding, and could not be processed.")

    @mystbin.command(name="file", usage="<file>")
    async def mystbin_file(self, ctx):
        """
        Upload the contents of a file to mystbin.
        
        You must provide a file.
        """
        if not ctx.message.attachments:
            return await ctx.send_help()
        attachment = ctx.message.attachments[0]
        file = await attachment.read()
        try:
            link = await cli.post(file.decode(encoding="utf-8"), syntax=attachment.filename.split('.')[-1])
            await ctx.send(f"`{attachment.filename}` uploaded to Mystbin\n> {link}")
        except UnicodeDecodeError:
            return await ctx.send("Failed to decode this file, please provide a valid file type.")

    @mystbin.group(name="channel")
    async def nystbin_channel(self, ctx):
        """Manage the mystbin channels."""

    @nystbin_channel.command(name="add", usage="<channels...>")
    async def mystbin_channel_add(self, ctx, channels: commands.Greedy[discord.TextChannel]):
        """
        Add channels that will automatically upload files to mystbin.

        To provide multiple channels, provide them in a list, seperated by spaces.
        """
        async with self.config.guild(ctx.guild).channels() as config:
            for c in channels:
                if c.id in config:
                    return await ctx.send(f"{c.mention} is already a mystbin channel.")
            config.extend([c.id for c in channels])
        if len(channels) > 1:
            await ctx.send("Channels added as mystbin channels.")
        else:
            await ctx.send("Channel added as a mystbin channel.")

    @nystbin_channel.command(name="remove")
    async def mystbin_channel_remove(self, ctx, channel: discord.TextChannel):
        """
        Remove a channel that is currently listening to files to upload them to mystbin.
        """
        ci = channel.id
        async with self.config.guild(ctx.guild).channels() as config:
            if ci not in config:
                return await ctx.send("This channel was not already a mystbin channel.")
            config.remove(ci)
        await ctx.send("Channel removed as a mystbin listener channel.")

    @nystbin_channel.command(name="list")
    async def mystbin_channel_list(self, ctx):
        """
        List all the mystbin channels.
        """
        async with self.config.guild(ctx.guild).channels() as config:
            if not config:
                return await ctx.send("There are no mystbin channels.")
            for c in config:
                obj = self.bot.get_channel(c)
                if not obj:
                    config.remove(c)
            await ctx.send(", ".join([self.bot.get_channel(c).mention for c in config]))

    @nystbin_channel.command(name="clear")
    async def mystbin_channel_clear(self, ctx):
        """
        Clear the mystbin channels.
        """
        async with self.config.guild(ctx.guild).channels() as config:
            config.clear()
        await ctx.tick()

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        if not message.attachments:
            return
        if message.author.bot:
            return
        async with self.config.guild(message.guild).channels() as config: 
            if not message.channel.id in config:
                return
        with contextlib.suppress(UnicodeDecodeError):
            attachment = message.attachments[0]
            file = await attachment.read()
            link = await cli.post(file.decode(encoding="utf-8"), syntax=attachment.filename.split('.')[-1])
            return await message.channel.send(f"`{attachment.filename}` was automatically uploaded to Mystbin:\n> {link}")
