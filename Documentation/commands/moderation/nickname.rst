.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Nickname Command [Moderation].
    :theme-color: #f54646

Nickname
========

Change the nickname of a member in a server

Parameters
----------
**Member [Required]**

The `member/bot` whose nickname is going to be changed

**New_Nickname [Required]**

The new nickname to replace the previous nickname

.. WARNING:: Discord poses a 32 character limit so all nicknames will be trimmed down to 32 chars to prevent errors!

**Layout:**
::
	-Nickname <Member> <New-Nickname>

Permissions
-----------
**Bot**
::
	Manage Nicknames
	Embed Links
	External Emojis - Optional

**Member**
::
	Manage Nicknames

Cooldown
--------
10 Seconds - Per User

Aliases
-------
Nick

Example Usage
-------------

.. figure:: /images/nickname.png
   :width: 400px
   :align: center
   :alt: Example Usage of the Nickname Command

Glossary
--------
   
. glossary::
	Nickname
		Moderation command

	Nick
		Moderation command [Aliase of *Nickname*]