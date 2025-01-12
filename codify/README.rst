.. _codify:

======
Codify
======

This is the cog guide for the codify cog. You will
find detailed docs about usage and commands.

Throughout this documentation, ``[p]`` is considered as your prefix.

------------
Installation
------------

Let's firstly add my repository if you haven't already:

* :code:`[p]repo add kreusada https://github.com/Kreusada/Kreusada-Cogs`

Next, let's download the cog from the repo:

* :code:`[p]cog install kreusada codify`

Finally, you can see my end user data statements, cog requirements, and other cog information by using:

* :code:`[p]cog info kreusada codify`

-----
Usage
-----

Get a message and wrap it in a codeblock.

.. _codify-commands:

--------
Commands
--------

Here's a list of all commands available for this cog.

.. _codify-command-codify:

^^^^^^
codify
^^^^^^

**Syntax**

.. code-block:: ini

    [p]codify <message_id> [language=python] [escape_markdown=False]

**Description**

Get a message and wrap it in a codeblock.

**Arguments**

* ``<message_id>``: The message's ID to convert into a codeblock.
* ``[language]``: The language of the codeblock. If none is provided, it defaults to python.
* ``[escape_markdown]``: Determines whether to escape the ``<message_id>``. If none is provided, it defaults to False.

---------------
Receive Support
---------------

Feel free to ping me at the `Red Cog Support Server <https://discord.gg/GET4DVk>`_ in :code:`#support_kreusada-cogs`.