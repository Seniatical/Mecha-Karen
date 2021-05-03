Clear
=====

Delete up 100 messages in bulk using a variety of different searching techniques

Parameters
----------
**Amount [Required]**

A number denoting the total amount of messages to delete

**Filter [Optional]**

Allows you to select which messages to delete.

**Current Options:**
	- Member
	- Role
	- REGEX expression (Matches to message content)

**Layout:**
::
	-Purge <Amount> [Filter]

Permissions
-----------
**Bot**
::
	Manage Messages
	Embed Links
	External Emojis - Optional

**Author**
::
	Manage Messages

Cooldown
--------
5 Seconds - Per User

Aliases
-------
Purge

Example Usage
-------------
::

	1. -Purge 10
	2. -Purge 10 _-*™#7519
	3. -Purge 10 Supporters
	4. -Purge 10 ^Hello World!

1. Deletes any 10 messages above the authors message
2. Deletes 10 messages which were ONLY sent by `_-*™#7519`
3. Deletes 10 messages which were ONLY sent by users with the `Supporters` Role
4. Deleted 10 messages which matched the regex expression 