1. git clone this repo
2. install postgres 12.18 on your local. You should be able to use other versions but they haven't been tested with lcbot.
3. create user `lcbot`
4. create database `lcbot` using user `lcbot`
5. Create a `.env` file in your `lcbot` cloned repo with following content.

```
GUILD_TOKEN = 121341231214124 #demo values
CHANNEL_TOKEN = 124135325345435 #demo values
AUTH_TOKEN = 'rk24h5k2jhrb2kfbh24k5gj45gkjtgk34j5g4k2jhr45' #demo values

DB_USER = "lcbot"
DB_PASS = "lcbot"
DB_HOST = "127.0.0.1"
DB_NAME = "lcbot"
```
You can modify the DB credentials based on what you have done.

6. Create a discord server and create atleast one text channel where you want to test things. You can use this [link](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server)
7. Right click on the text channel and click `Copy Link`. It should look something like :
`https://discord.com/channels/121341231214124/124135325345435`
8. The first key after `https://discord.com/channels/` is your `GUILD_TOKEN` and the key after it is your `CHANNEL_TOKEN`.
9. Follow this [link](https://www.writebots.com/discord-bot-token/) to get your bot AUTH_TOKEN and register it to your discord server.
10. Replace the appropriate token values in your `.env` file with the ones you just got.
11. Go to a terminal and run lcbot using `python3 main.py` from the root directory of the repo. You should be able to see your bot come online in your discord server.
