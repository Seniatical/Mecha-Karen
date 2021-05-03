Slowmode
========

Sets a slowmode on a specified channel or the current one

Parameters
----------

**Time [Optional]**

The length of the slowmode (*In Seconds*), Defaults to 0

.. WARNING:: The max figure for time is `21600` which is basically 6 Hours

**Channel [Optional]**

Target channel - Defaults the channel the command is executed in

**Layout:**
::
	-Slowmode [Time=0] [Channel=ctx.channel]

Permissions
-----------
**Bot**
::
	Manage Channels
	Embed Links
	External Emojis - Optional

**Author**
::
	Manage Channels

Aliases
-------
There are no aliases for this command!

Example Usage
-------------
::

	-Slowmode 10
	-Slowmode 10 General

1. Sets a slowmode of 10 seconds in the current channel
2. Sets a slowmode of 10 seconds in the channel named `General`