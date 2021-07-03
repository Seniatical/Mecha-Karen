.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Mute Command [Moderation].
    :theme-color: #f54646

Mute
====

Restrict a users permissions to speak

.. Attention:: Inorder for this command to work you must have set a :ref:`muterole`

Parameters
----------
**Member [Required]**

The `member/bot` to mute - Bots may be abit weird when it comes to muting due to discords intergrations system

**Time [Optional]**

The set duration for the mute - Defaults to **10 Seconds**

*Formatting the time*
::
	Scales:
		- S = Seconds
		- M = Minutes
		- H = Hours
		- D = Days

	Building a Time:
		10s, 30m, etc...

.. Tip:: To remove the duration limit set the time as "`*`"!

**Reason [Optional]**

The reason for the mute - Shows up in the *Audit Logs* for updating the members role

**Layout:**
::
	-Mute <Member> [Time=10s] [Reason="Wasn't Provided"]

Permissions
-----------
**Bot**
::
	Manage Channels
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

.. figure:: /images/mute1.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Mute Command

DMs
^^^
Tries to send a DM to the user if the users DMs are open or if the bot is not blocked by them.

.. figure:: /images/mute2.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Mute Command

Glossary
--------

. glossary::
	Mute
		Moderation command