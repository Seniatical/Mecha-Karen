  ![Discord.py-Version](https://img.shields.io/badge/discord.py-1.7.1-blue?style=flat-square)
  ![Python-Version](https://img.shields.io/badge/python-3.9.1-green?style=flat-square)
  ![MongoDB](https://img.shields.io/badge/MongoDB-pink?style=flat-square)
  ![Django-Version](https://img.shields.io/badge/Django-3.1.3-blue?style=flat-square)
  ![Flask-Version](https://img.shields.io/badge/Flask-1.1.2-blue?style=flat-square)

<h1 align="center">
  <img src="https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.png?size=512" height='100px' width='100px'>
</h1>
<h1 align="center">Mecha Karen</h1>
<h4 align="center">Fun, Powerful and Unique</h4>

<h1 align="center">Features</h1>
<p allign="center">
    - Moderation - Simple but powerful!
    - Image Manipulation - Mecha Karen has unique commands, Some apply effects and flip you over!
    - Logging - Mecha Karen can log everything that happens in your server.
    - Fast and Reliable - Mecha Karen heavily caches data to prevent constantly fetching from the DB, so you enjoy fast responses. 
                          It can also report any unknown errors automatically for you!
                          Need some help with the bot? Join the welcoming and friendly support server!
    - Customisable - You can customise everything from the prefix, to restricting commands to a certain channel!
    - Expanding - Mecha Karen doesn't stop growing! Got a feature request? - DM one of our devs and it may be added.
</p>

<h1 allign="center">🔗 Links</h1>
<p allign="center">
    <a href="https://mechakaren.xyz/login">Dashboard</a>
    <a href="https://api.mechakaren.xyz/docs">Bot Documentation - W.I.P</a>
    <a href="https://docs.mechakaren.xyz/">Bot Documentation - W.I.P</a>
    <a href="https://discord.gg/Q5mFhUM">Support Server</a>
    <a href="https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=0&scope=bot">Bot Invite</a>
</p>

<h1 allign="center">Running Karen</a>
<p allign="center">
    Running KAREN is not easy - Mainly due to missing modules and parts.\
    I will not make it easy for anybody - If you wish to run it, modify the bot.py file and do your thing!
</p>

<h2 allign="center">Basic Use of Running Karen</h2>
<p allign="center">
    This area will show you the major steps of running Mecha-Karen on your machine. If you run into any errors which are related to the steps below, contact me on discord so i can issue a fix for the issue. 
    If it due to the code - A majority of the causes are stated in the repo in them sections, so give them a read before asking for help.
    
    I am not going to help you self host karen due to many reasons.
    
    If your self hosting karen - please make sure to follow the license. 
    This project has taken a very long to make and crediting would be nice.
    If you wish to learn more about the licence <a href='#license'>click here</a>!
</p>

<h2 allign="center">Env file data</h2>
```
MONGO_DB_URI = "Your mongo DB URI"
DISCORD_BOT_TOKEN = "Your discord bot token"
RECONNECT = True
SERVER_IP = "the IP to run your websocket on"
SERVER_PORT = 8000
START_SERVER = True
IS_MAIN = True
ALT_TOKEN = "Optional feature to run an alt instead of your main acc - change IS_MAIN to false"
API_TOKEN = "API Token for the mecha karen API - https://api.mechakaren.xyz"
OPEN_WEATHER_API_KEY = "Your api key for open-weather"

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
```

<h2 allign="center">Linux</h2>
```sh
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
```
To exit out of the NANO GUI press `Ctrl+X` then press `Y` and then press `ENTER`

<h2 allign="center">Windows</h2>
```
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
```

<h1 allign="center" name="license"></h1>
<p allign="center">
    Mecha Karen is licensed and distributed under the APACHE 2.0 License - The copyright protects:
    <code>
        BOT
        API
        DOCUMENTATION
        DASHBOARD
    </code>

    Any violations to the license will result in moderate action.
</p>    
    
