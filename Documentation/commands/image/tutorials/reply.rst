.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: How to use a reply as your image [Tutorial] [Images].
    :theme-color: #f54646

Using Images From Reply's
=========================

Did you know that you can use images by replying to the message?

.. caution::

	* The will need *READ MESSAGE HISTORY* permissions inorder for this feature to work.
	* The message must also be *RESOLVED*.

How to use it
-------------
So to use an image from an embed or just somebody elses attachment just simply reply to the message
whilst using using the command as normal!

Example
^^^^^^^
Command Used: *Invert*

.. figure:: /images/reply.png
   :width: 400px
   :align: center
   :alt: Example usage for Reply feature

Errors which may arise
----------------------
Problems which may occur if you either:

* Message replied to has no embed or attachment
* Embed has no image, thumbnail, author, footer
* Attachment in the message is either of the wrong type or cannot be resolved
* Filesize too large

The bot will try again to download the image but if it cannot it will either:

* Return an error message
* Use your avatar as the image

Glossary
--------

.. glossary::

    Read Message History
		A discord permission which must be granted to the bot,
		If not then some features may be restricted or not work as intented.

	Resolved
		Something that was recorded during the bots uptime.