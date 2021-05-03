Kick
=====

Kicks a `Member/Bot` from the server

Parameters
----------
**Member [Required]**

The `member/bot` to kick

**Reason [Optional]**

The reason for the kick - Same reason which is used in the *Audit Logs*
The member being kicked will also recieve the same reason in the Direct Messages (DMs)

**Layout:**
::
	-Kick <Member> [Reason="Wasn't Provided."]

Permissions
-----------
**Bot**
::
	Kick Members
	Embed Links
	External Emojis - Optional

**Author:**
::
	Kick Members

Cooldown
--------
5 Seconds - Per User

Aliases
-------
There are no aliases for this command yet!

Example Usage
-------------
::

	-Kick _-*™#7519
	-Kick _-*™#7519 Being a Naughty Boy!

1. Kicks the member using default reason
2. Kicks the member using the reason `Being a Naughty Boy!`

*Both examples will attempt to send a DM to the user*