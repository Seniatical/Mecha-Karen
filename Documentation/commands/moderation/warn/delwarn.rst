Delwarn
=======

Remove a specific warning from a user

Parameters
----------
**Member [Required]**

The member to delete the warn from

**Warn [Required]**

The warn number to be removed

**Reason [Optional]**

The reason for removing the warn - Defaults to `Wasn't Provided`

**Layout:**
::
	-Delwarn <Member> <Warn> [Reason="Wasn't Provided"]

Permissions
-----------
**Bot**
::
	Embed Links

**Author**
::
	Manage Messages

Cooldown
--------
5 Seconds - Per User

Aliases
-------
There are no aliases for this command yet!

Example Usage
-------------
::

	-Delwarn _-*™#7519 1
	-Delwarn _-*™#7519 1 False Warn

1. Deletes warn number `1` for `_-*™#7519` using the reason `Wasn't Provided`
2. Deleted warn number `1` for `_-*™#7519` using the reason `False Warn`