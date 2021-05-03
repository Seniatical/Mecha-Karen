Archive
=======

Reads every single message in a specified channel and places them into a `.md` file.

.. Attention:: Only adds messages which are applicable - Has some sort of content

Parameters
----------
**Channel [Optional]**

The channel to archive - Defaults to the current channel

**Layout:**
::
	-Archive [Channel=ctx.channel]

Permissions
-----------
**Bot**
::
	Attach Files
	Read Message History

**Author**
::
	Manage Channels

Cooldown
--------
60 Seconds - Per Server

Aliases
-------
There are no aliases for this command

Example Usage
-------------
::

	-Archive
	-Archive General

1. Archives the current channel
2. Archives `General` instead of the current channel