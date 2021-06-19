![Discord.py-Version](https://img.shields.io/badge/discord.py-1.7.1-blue?style=flat-square)
![Python-Version](https://img.shields.io/badge/python-3.9.1-green?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-pink?style=flat-square)
![Django-Version](https://img.shields.io/badge/Django-3.1.3-blue?style=flat-square)
![Flask-Version](https://img.shields.io/badge/Flask-1.1.2-blue?style=flat-square)

# Mecha Karen
Mecha Karen is an open sourced Discord bot - Built with discord.py

# Features
```
Moderation - Simple but powerful!
Image Manipulation - Mecha Karen has unique commands, Some apply effects and flip you over!
Logging - Mecha Karen can log everything that happens in your server.
Fast and Reliable - Mecha Karen heavily caches data to prevent constantly fetching from the DB, so you enjoy fast responses. 
                    It can also report any unknown errors automatically for you!
                    Need some help with the bot? Join the welcoming and friendly support server!
Customisable - You can customise everything from the prefix, to restricting commands to a certain channel!
Expanding - Mecha Karen doesn't stop growing! Got a feature request? - DM one of our devs and it may be added.
```

# 🔗 Links
[Dashboard](https://mechakaren.xyz/login)\
[API](https://api.mechakaren.xyz/docs)\
[Bot Documentation - W.I.P](https://docs.mechakaren.xyz/)\
[Support Server](https://discord.gg/Q5mFhUM)\
[Bot Invite](https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=0&scope=bot)

# Running Karen
Running KAREN is not easy - Mainly due to missing modules and parts.\
I will not make it easy for anybody - If you wish to run it, modify the bot.py file and do your thing!

## Simple Running

### Env Data
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

LAVALINK_SERVER_IP = "Lavalink server ip"
LAVALINK_SERVER_PORT = Lavalink-server-port
LAVALINK_SERVER_PASSWORD = "Your password for the env"
LAVALINK_REGION = "your server region"
LAVALINK_NODETYPE = "default-node"
```

### Linux
```sh
$ git clone https://github.com/Seniatical/Mecha-Karen/
$ cd Mecha-Karen

$ python3 -m venv ./venv --system-site-packages
$ source ./venv/bin/activate
$ pip3 install -r requirements.txt
$ deactivate

$ touch .env
$ nano .env
... Env data goes here

$ python3 main.py
```
To exit out of the NANO GUI press `Ctrl+X` then press `Y` and then press `ENTER`

### Windows
```
C:\> git clone https://github.com/Seniatical/Mecha-Karen/
C:\> cd Mecha-Karen

C:\> python3 -m venv ./venv --system-site-packages
C:\> path/to/venv/Scripts/activate.bat
C:\> pip install -r requirements.txt
C:\> deactivate

C:\> type nul > .env
... Next part cannot be in terminal for windows
... Go to your .env file and fill out the env data
... close the file and go to cmd again
C:\> python main.py
```

# Copyright
Mecha Karen is licensed and distributed under the APACHE 2.0 License - The copyright protects:
```
BOT
API
DOCUMENTATION
DASHBOARD
```

Any violations to the license will result in moderate action.
