import discord

from redbot.core import commands


class RedTools(commands.Cog):
    """Some tools for me and giving support."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def docs(self, ctx, *args: str):
        """Get the docs for my cogs."""
        base = "https://kreusadacogs.readthedocs.io/en/latest/"
        if not args:
            return await ctx.send(base)
        cog_header = f"cog_{args[0]}.html"
        if len(args) == 1:
            base += cog_header
            return await ctx.send(base)
        base += cog_header + f"#{args[0]}-command-" + '-'.join([arg for arg in args[1:]])
        await ctx.send(base)