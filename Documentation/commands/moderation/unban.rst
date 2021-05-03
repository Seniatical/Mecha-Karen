Unban
=====

Unbans a previously banned `Member/Bot` from the server

Parameters
----------
**Member [Required]**

The `member/bot` to unban

**Reason [Optional]**

The reason for the unban - Same reason which is used in the *Audit Logs*

**Layout:**
::
	-Unban <Member> [Reason="Wasn't Provided."]

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

	-Unban 475357293949485076
	-Unban _-*™#7519 He's Now a Good Boy

.. Note:: Using `-Unban _-*™` Will not work due to discriminator problems

1. Unbans the member using there `ID`
2. Unbans the member using there name and modifying the reason

*The member will only recieve a DM if the bot can still DM them*
