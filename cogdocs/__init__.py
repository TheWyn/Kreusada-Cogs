import asyncio
import datetime
import io

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify

footer = """
----------------------
Additional Information
----------------------

This cog has been vetted by the Red-DiscordBot QA team as approved.
For inquiries, see to the contact options below.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.
"""


class CogDocs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.header = lambda x, y: y * len(x) + '\n' + x + '\n' + y * len(x)
        self.tag_transform = lambda x: x.replace(' ','-')
        self.issubcommand = lambda x: ' ' in x
        self.issue_template = "https://github.com/Kreusada/Kreusada-Cogs/issues/{}"

    def format_issues_and_prs(self, content):
        for x in content.split():
            num = x.strip('#')
            if x.startswith('#') and num.isdigit():
                content = content.replace(x, f"(`{x} <{self.issue_template.format(num)}>`_)")
        return content

    @commands.command()
    async def changelog(self, ctx, date: str):
        """
        Create items for a changelog entry.
        
        Type `stop` to stop generating changelogs.
        """
        if date.lower() == "today":
            date = datetime.datetime.now().strftime("%d/%m/%Y")
        def check(x):
            return x.author == ctx.author and x.channel == ctx.channel

        data = []
        await ctx.send("Start adding changes for this changelog entry. Type `stop` to end the process.")
        while True:
            try:
                content = await self.bot.wait_for("message", timeout=30, check=check)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long to respond.")
            if content.content.lower() == "stop":
                break
            else:
                await content.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                data.append(content.content)
        composed = f"{self.header(date, '-')}\n\n"
        for cl in data:
            composed += f"* {self.format_issues_and_prs(cl)}\n"
        await ctx.send(box(composed, lang="asciidoc"))


    @commands.command()
    async def cogdoc(self, ctx, cog: str):
        if cog not in self.bot.cogs:
            return await ctx.send(f"`{cog}`` cog not found.")
        obj = self.bot.get_cog(cog)
        compose = f""".. _{obj.qualified_name.lower()}:

{self.header(obj.qualified_name, '=')}

This is the cog guide for the {obj.qualified_name.lower()} cog.
Throughout this guide, ``[p]`` will be considered as your prefix.

{self.header("Installation", "-")}

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add Kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada {obj.qualified_name.lower()}`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada {obj.qualified_name.lower()}`
"""
        if obj.__cog_description__:
            compose += f"""
{self.header("Usage", "-")}

{obj.__cog_description__}

"""
        else:
            compose += '\n'
        if not obj.walk_commands():
            compose += '\n' + footer
        else:
            compose += f""".. _{obj.qualified_name.lower()}-commands:

{self.header("Commands", "-")}

Here is a list of all commands available for this cog. 
There are {len([x for x in obj.walk_commands()])} in total.
"""
            for command in sorted([str(x) for x in obj.walk_commands()], key=len):
                command_obj = self.bot.get_command(command)

                aliases = []
                for x in command_obj.aliases:
                    if self.issubcommand(command):
                        aliases.append(f"* ``{command} {x}``")
                    else:
                        aliases.append(f"* ``{x}``")
                if aliases:
                    command_aliases = "\n\n**Aliases**\n\n" + "\n".join(aliases)
                else:
                    command_aliases = ''

                command_usage = command_obj.usage or command_obj.signature
                if not command_usage:
                    command_usage = ''
                compose += f"""
.. _{obj.qualified_name.lower()}-command-{self.tag_transform(command)}:

{self.header(command, '^')}

**Syntax**

.. code-block:: python

    [p]{command} {command_usage}

**Description**

{command_obj.format_shortdoc_for_context(ctx)}{command_aliases}
"""
        kwargs = {
            "content": f"Here is your cog guide for {cog}",
            "file": discord.File(io.BytesIO(compose.encode()), filename=f"{obj.qualified_name.lower()}.rst")
        }
        await ctx.send(**kwargs)

def setup(bot):
    bot.add_cog(CogDocs(bot))