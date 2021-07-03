.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Using your cache in Image Manipulation [Tutorial] [Images].
    :theme-color: #f54646

.. _temp:

Temporarily Saving Your Image
=============================

Ever wanted to save that image for a little longer?

Well now you can!

.. Caution:: These images last only whilst the bot is online!

How is it Done?
---------------
Mecha Karen has an internal cache for all users - This means you can save little pieces of information within me!

.. Tip:: Make sure to check out :ref:`CacheCommands`!

Adding an Image to your cache
-----------------------------
So to add your image to my cache you will need to do::
	-Cache Set <Image> [category="image"]

Image can be one of -
	* Link
	* Attachment
	* Discord Member *Uses their avatar*
	* Discord Emoji *Custom Only*

Example Using the command
^^^^^^^^^^^^^^^^^^^^^^^^^

.. image:: /images/saving.png
   :width: 400px
   :align: center

Using Your Cache For Image Commands
-----------------------------------
To run a command using an image from your cache you will need to do::
	-Command From Cache

If you have you more then 1 image in your cache and you want to use another image - Use::
	-Command From Cache 1/2/etc...

Example Using the command
^^^^^^^^^^^^^^^^^^^^^^^^^
Command Used in this example: *Invert*

.. image:: /images/from_cache.png
   :width: 400px
   :align: center

**Using a different cache slot**

Cache slots start from 0 - So doing `-Invert From Cache 1` will use your second image.

.. image:: /images/from_cache_difslot.png
   :width: 400px
   :align: center