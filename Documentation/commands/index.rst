.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: All the commands for Mecha Karen!
    :theme-color: #f54646

Commands
========

Sub-Section of the documentation holding all the commands within Mecha Karen

.. DANGER:: Do not literally include **<>** and **[ ]** when using a command!

.. sidebar:: Key

	<...> = Required argument

	[...] = Optional argument
	
	[...=?] = Optional argument with a default value

Commands
--------

.. toctree::
	:titlesonly:
	:caption: Command Categories

    moderation/index
    image/index

Glossary
--------
Vocabulary which are on this page and will be included throughout this section.

.. glossary:: 
	Parameters
	   Arguments which you pass into the command when using it
 
	Layout
	   Text representing the command and its arguments
 
	Permissions
	   The permissions needed for a command to be ran by both bot and user
 
	Cooldown
	   The timeout duration after running a command
	   Can be one of:

	   - `User`: The member who has just run the command
	   - `Role`: Every member who has that specific role
	   - `Guild`: The entire server
 
	Aliases
	   A different name for the same command
 
	Example Usage
	   An image showing you an example of how to use a command.

	DM
	   A message sent directly to a user if the bot has permissions to.
	   E.g. Owner Concent/Acknowledgement, DMs are open.