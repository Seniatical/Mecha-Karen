Ban
====

Bans a `Member/Bot` from the server

Parameters
----------
**Member [Required]**

The `member/bot` to ban

**Reason [Optional]**

The reason for the ban - Same reason which is used in the *Audit Logs*
The member being banned will also recieve the same reason in the Direct Messages (DMs)

**Layout:**
::
	-Ban <Member> [Reason="Wasn't Provided."]

Permissions
-----------
**Bot**
::
	Ban Members
	Embed Links
	External Emojis - Optional

**Author:**
::
	Ban Members

Cooldown
--------
5 Seconds - Per User

Aliases
-------
There are no aliases for this command yet!

Example Usage
-------------
::

	-Ban _-*™#7519
	-Ban _-*™#7519 Being a Naughty Boy!

1. Bans the member using default reason
2. Bans the member using the reason `Being a Naughty Boy!`

*Both examples will attempt to send a DM to the user*