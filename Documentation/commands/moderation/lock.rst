Lock
====

Stop a certain role from from talking in a specified channel

.. Important::

	.. deprecated:: 1.5.2
   		Unlock command no longer exists, Read below

	To unlock a channel run the command again

	**Using the same configurations as before!**

	*Example*
	::
		-Lock General Supporters

		Now to unlock it

		-Lock General Supporters

		And your done!


Parameters
----------
**Channel [Optional]**

The channel to restrict access to - Defaults to current channel

**Role [Optional]**

The role to restrict access from - Defaults to `@everyone`

**Layout:**
::
	-Lock [channel=ctx.channel] [role=ctx.guild.default_role]

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

Cooldown
--------
10 Seconds - Per User

Aliases
-------
There are no aliases for this command yet!

Example Usage
-------------
::

	-Lock
	-Lock General
	-Lock General Supporters

1. Locks the current channel for the default role (`@everyone`)
2. Locks the channel called `General` for the role default role
3. Locks the channel called `General` for the `Supporters` role