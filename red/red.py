import discord

from redbot.core import commands


class Red(commands.Cog):
    """Some tools for me and giving support."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def docs(self, ctx, cog: str = None, *, command: str = None):
        """Get the docs for my cogs."""
        base = "https://kreusadacogs.readthedocs.io/en/latest/"
        if not cog or not command:
            return await ctx.send(base)
        if cog:
            base += f"cog_{cog}.html"
        if commmand:
            base += f"#{cog}-command{'-'.join(command)}"
        await ctx.send(base)