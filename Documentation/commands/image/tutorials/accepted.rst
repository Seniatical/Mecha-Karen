.. _Accepted:

.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Accepted images for image related commands [Tutorial] [Image].
    :theme-color: #f54646

Accepted Images
===============
Here we will discuss what Karen accepts as a valid image.

Accepted Image Types for URLS and Attachments
---------------------------------------------
Currently we only support the following content types:

* image/gif
* image/png
* image/jpg
* image/jpeg

.. Note:: Same principles apply with files.

Pre-built Variables
-------------------
These are the prebuilt functions and variables which you can use as a shortcut to edit an image.

.. glossary::

    Sample
        The GIF which the dev team use to test new features.
        We are confident you will like it!

    Icon
        The icon for the server you are currently into

    Karen
        The amazing avatar of Mecha Karen!

Attachments
-----------
To use an attachment as your image all you need to do is run the command which requires an image with the attachment linked.
The argument which will require the image will automatically be filled for you.
Other arguments will shift down by 1

For file types just refer to `Accepted Image Types for URLS and Attachments`_.

Example
^^^^^^^

.. Caution:: You do not need to include the `"This is my attachment"` when using the command.
             Only do so if it raises a missing parameter error!

.. figure:: /images/attachment.png
   :width: 400px
   :align: center
   :alt: Example usage for Attachments

Members
-------
Converts the given argument to a Member in your server. It will use the avatar of the provided member as your image.

Accepted formats
^^^^^^^^^^^^^^^^

* UserName#Discriminator
* Server Display Name
* User ID
* Mentioning the Member

Emojis
------
Uses an emoji to represent your images, They may become abit stretched in the process.

.. Note:: Only accepts custom emojis as of now

Cache
-----
If your looking to use one of the images from your cache as your image.
Check out :ref:`temp`.

What if it cant find my image?
------------------------------
If it is the case that I cannot locate your image when you have used a command I will then use your avatar as your image.

However, If it is the case you provide me with an invalid Image, I will use your avatar as the image.
