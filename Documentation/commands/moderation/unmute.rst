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
::

	-Unmute _-*™#7519
	-Unmute _-*™#7519 False Mute

1. Unmutes `_-*™#7519` Using the default reason
2. Unmutes `_-*™#7519` Using the reason `False Mute`