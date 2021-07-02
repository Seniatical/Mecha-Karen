Unmute
======

Allows a muted user to speak again - User needs to be muted to start with

Parameters
----------

**Member [Required]**

The member to unmute - Must have your server :ref:`muterole` setup

**Reason [Optional]**

Reason for the unmute - Defaults to `{Author} Has unmuted this user`

**Layout:**
::
	-Unmute <Member> [Reason="{Author} Has unmuted this user"]

Permissions
-----------
**Bot**
::
	Manage Roles
	Embed Links
	External Emojis - Optional

**Author**
::
	Manage Messages

Cooldown
--------
10 Seconds - Per User

Aliases
-------
There are no aliases for this command yet!

Example Usage
-------------
.. figure:: /images/unmute1.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Unmute Command

DMs
^^^
Tries to send a DM to the user if the users DMs are open or if the bot is not blocked by them.

.. figure:: /images/unmute2.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Unmute Command