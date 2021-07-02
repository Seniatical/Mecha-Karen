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
.. figure:: /images/Purge/classic.png
   :width: 400px
   :align: center
   :alt: Example Usage of clear command

.. figure:: /images/Purge/member.png
   :width: 400px
   :align: center
   :alt: Example Usage of clear command

.. figure:: /images/Purge/role.png
   :width: 400px
   :align: center
   :alt: Example Usage of clear command

.. figure:: /images/Purge/regex.png
   :width: 400px
   :align: center
   :alt: Example Usage of clear command