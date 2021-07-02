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
.. figure:: /images/Lock/lock2.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Lock Command

.. figure:: /images/Lock/lock1.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Lock Command