  ![Discord.py-Version](https://img.shields.io/badge/discord.py-2.0.0a-blue?style=flat-square)
  ![Python-Version](https://img.shields.io/badge/python-3.8.5-green?style=flat-square)
  ![MongoDB](https://img.shields.io/badge/MongoDB-pink?style=flat-square)
  ![Django-Version](https://img.shields.io/badge/Django-3.1.3-blue?style=flat-square)
  
<p align="center">
  <a href="https://github.com/rapptz/discord.py" target="_blank">
    <img src="https://img.shields.io/badge/discord.py-2.0.0a-blue?style=flat-square" />
  </a>

<h1 align="center">
  <img src="https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.png?size=512" height='100px' width='100px'>
</h1>
<h1 align="center">Mecha Karen</h1>
<h4 align="center">Fun, Powerful and Unique</h4>

<h1 align="center">Features</h1>
<p align="center">
  <ul align="">
    <li>Moderation - Simple but powerful!</li>
    <li>Image Manipulation - Mecha Karen has unique commands, some apply effects and flip you over!</li>
    <li>Logging - Mecha Karen can log everything that happens in your server.</li>
    <li>Fast and Reliable - Mecha Karen heavily caches data to prevent constantly fetching from the DB, so you enjoy fast response times.<br>
                          - It can also report any unknown errors automatically for you!<br>
                          - Need some help with the bot? Join the welcoming and friendly support server!</li>
    <li>Customisable - You can customise everything from the prefix, to restricting commands to a certain channel!</li>
    <li>Expanding - Mecha Karen doesn't stop growing! Got a feature request? - DM one of our devs and it may be added.</li>
  </ul>  
</p>

<h1 align="center" name='links'>🔗 Links</h1>
<p align="">
    <a href="https://mechakaren.xyz/login">Dashboard</a><br>
    <a href="https://api.mechakaren.xyz/docs">Bot Documentation - W.I.P</a><br>
    <a href="https://discord.gg/Q5mFhUM">Support Server</a><br>
    <a href="https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=0&scope=bot">Bot Invite</a><br>
</p>

<h1 align="center">Running Karen</h1>
<p align="">
  Running KAREN is not easy - Mainly due to missing modules and parts. Some modules have also been customised to suit karens running style - of which I do not include in this repo.<br>
  I will not make it easy for anybody - If you wish to run it, modify some areas of the bot and you should be good to go!<br>
  This repo is not meant to be directly copied as it contains pre-releases which are very unstable and are never used in production, The purpose of this repo is for testing and helping to improve the bot!
</p>

<h2 align="center">Basic Use of Running Karen</h2>
<p align="">
    This area will show you the major steps of running Mecha-Karen on your machine. If you run into any errors which are related to the steps below, contact me on Discord so I can issue a fix for the issue.<br><br>
    If it due to the code - A majority of the causes are stated in the repo in relevant sections, so give them a read before asking for help.<br>
    I will not help or provide support for self hosting Karen.<br>
    If you are self hosting Karen - please make sure to follow the license.<br>
    This project has had a lot of time and effort invested into it, so I would appreciate it if credit was given.<br>
    If you wish to learn more about the license <a href='#license'>click here</a>!
</p>

<h2 align="center">Env File</h2>
<p align="">
  
    MONGO_DB_URI = "Your Mongo DB URI"
    DISCORD_BOT_TOKEN = "Your Discord bot token"
    RECONNECT = True
    SERVER_IP = "the IP to run your websocket on"
    SERVER_PORT = 8000
    START_SERVER = True
    IS_MAIN = True
  
    ALT_TOKEN = "Optional feature to run an alt instead of your main acc - change IS_MAIN to false"
    API_TOKEN = "API Token for the mecha karen API - https://api.mechakaren.xyz"
    OPEN_WEATHER_API_KEY = "Your api key for open-weather"
    PEXEL_API_TOKEN = "your api token for the pexel api"
  
    LAVALINK_SERVER_IP = "Lavalink server ip"
    LAVALINK_SERVER_PORT = Lavalink-server-port
    LAVALINK_SERVER_PASSWORD = "Your password for the env"
    LAVALINK_REGION = "your server region"
    LAVALINK_NODETYPE = "default-node"
  
    IPC_SECRET_KEY = "The key which will be used to authenticate requests from dashboard to bot"
    IPC_HOST = "The host which the server will run off of"
  
    REDDIT_USERNAME = ""
    REDDIT_PASSWORD = ""
    REDDIT_CLIENT_ID = ""
    REDDIT_CLIENT_SECRET = ""
  
  All the stuff here goes into your <code>.env</code> file. This file should be in the same directory as <code>main.py</code>.
</p>

<h2 align="center">Linux</h2>
<p align="">
  
    $ git clone https://github.com/Seniatical/Mecha-Karen/
    $ cd Mecha-Karen/Bot
    $ touch .env
    $ nano .env
    ... Env data goes here
  
    $ python3 -m venv ./venv --system-site-packages
    $ source ./venv/bin/activate
  
    (venv) $ pip3 install -r requirements.txt
    (venv) $ python3 main.py
    (venv) $ deactivate

  To exit out of the NANO GUI press `Ctrl+X` then press `Y` and then press `ENTER`
</p>
  
<h2 align="center">Windows</h2>
<p align="">
  
    C:\> git clone https://github.com/Seniatical/Mecha-Karen/
    C:\> cd Mecha-Karen/Bot
    C:\> type nul > .env
    ... Next part cannot be in terminal for windows
    ... Go to your .env file and fill out the env data
    ... close the file and go to cmd again
  
    C:\> python3 -m venv ./venv --system-site-packages
    C:\> path/to/venv/Scripts/activate.bat
    (venv) C:\> pip install -r requirements.txt
    (venv) C:\> python main.py
    (venv) C:\> deactivate
  
  The <code>type nul > .env</code> is used to create an empty file for you.
</p>

<h2 align="center">Successful Launch Example</h2>
<p align="">
  <img src="https://i.gyazo.com/82089c03e8c74c08f947dbd87cd19d8e.png"></img>
</p>

<h1 align="center" name="license"></h1>
<p align="">
  Mecha Karen is licensed and distributed under the APACHE 2.0 License - The copyright protects:
  
    BOT
    API
    DOCUMENTATION
    DASHBOARD

  Any violations to the license will result in action being taken.
  
  <h2 allign="center">Self-Hosting Agreement</h2>
  <dl>
    <dt><b>You must not use Mecha Karen's name, license, or logo in your works.</b><dt>
    <dd>I have tried my best to not hard-code urls and names were I could, in newer regions.</dd>
    <dt><b>You must follow the license as stated <a href="https://github.com/Seniatical/Mecha-Karen/blob/main/LICENSE">here</a>.</b></dt>
    <dt><b>You cannot provide offical support for errors related to the bot, but help for features within the bot is allowed.</b></dt>
    <dt><b>You cannot publicly release your self-hosted bot if it contains more then 20% of Karens works and code.</b></dt>
    <dd>You can have your self hosted bot in smaller servers WHICH you own or manage.</dd>
    <dt><b>Provide full credits to both CONTRIBUTORS and the original creator</b></dt>
    <dd>Include links, which can be found <a href='#links'>here</dd>
  </dl>
</p>    
    
<h1 align="center">Modified Libs</h1>
<p>
  A list of modified libraries which are made to suit karen running style.
  <strong>Note: These are not all the libraries!</strong>
  
  TagScript: <a href="https://github.com/Seniatical/TagScript">Click Here</a>
</p>
