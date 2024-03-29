import datetime as dt
import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
from datetime import datetime, timedelta, date, timezone
import random
import asyncio
import asyncpg
from api import getUserDataFromLC, getUserSubmissions
from post import Post
import queries
import utils
import constants
import leaderboard
from dotenv import load_dotenv
import os
import dbutil
import json
import lbutil

load_dotenv()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
GUILD_TOKEN = int(os.getenv('GUILD_TOKEN'))
CHANNEL_TOKEN = int(os.getenv('CHANNEL_TOKEN'))


credentials = {"user": DB_USER, "password": DB_PASS, "database": DB_NAME, "host": DB_HOST}

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix="!",
            intents = kwargs.pop("intents")
        )        
    
    async def on_ready(self):
        logging.info("Username: {0}\nID: {0.id}".format(self.user))
        await self.tree.sync(guild=discord.Object(id=GUILD_TOKEN))
        logging.info('We have logged in as {0.user}'.format(self))
        self.db = await asyncpg.create_pool(**credentials)
        await dbutil.createTables(self.db)
        channel = bot.get_channel(CHANNEL_TOKEN)   
        logging.info('DB pool created')        
        
        makePosts.start()
        lbutil.makeDailyLeaderboardPost.start(bot.db, channel)
        lbutil.makeWeeklyLeaderboardPost.start(bot.db, channel)
        logging.info('Started tracking LC submissions for everyone')
        
    async def on_message(self, message):        
        await self.process_commands(message)
        if message.content.startswith('ping'):                              
            await message.channel.send('pong')     

description = "A discord bot written in Python that lets you socialize with your leetcode friends."
intents = discord.Intents.all()
bot = Bot(description=description, intents=intents)                   

async def run():
        
    try:
        await bot.start(AUTH_TOKEN)
    except KeyboardInterrupt:
        await bot.db.close()
        await bot.logout()


@tasks.loop(time = utils.getPostTimes())       
async def makePosts():    
    # Choose the time interval window for checking submissions    
    now = datetime.now(tz=timezone.utc)
    endTs = utils.floor_dt(now, constants.INTERVAL_DELTA)
    startTs = endTs - constants.INTERVAL_POST_DELTA
    logging.info('Checking between {0} to {1} {2}'.format(endTs, startTs, now.astimezone().tzname()))

    questions = utils.getAllQuestionsMap()
    usernames = await queries.getUsernames(bot.db)          
    allPosts = []
    for user in usernames:
        userData = await getUserDataFromLC(user, questions, startTs, endTs)
        posts = getPostsFromUserData(userData)
        logging.info("user: {} , posts: {}".format(user, len(posts)))
        allPosts+=posts

    sortedPosts = sorted(allPosts, key=lambda x: x.submitTime)
    for post in sortedPosts:
        channel = bot.get_channel(CHANNEL_TOKEN)                    
        await channel.send(embed=post.getPost())





@bot.tree.command(name="add",description="Adds your leetcode username",guild=discord.Object(id=GUILD_TOKEN))
@app_commands.describe(username="Leetcode username to be added")
async def slash_command(interaction:discord.Interaction, username: str):
    await bot.db.execute(queries.addUsernameQuery(username))
    await interaction.response.send_message("Added " + username)

@bot.tree.command(name="remove",description="Removes your leetcode username",guild=discord.Object(id=GUILD_TOKEN))
@app_commands.describe(username="Leetcode username to be removed")
async def slash_command(interaction:discord.Interaction, username: str):
    await bot.db.execute(queries.removeUsernameQuery(username))
    await interaction.response.send_message("Removed " + username)   

# @bot.tree.command(name="dailylb",description="Shows the daily leaderboard",guild=discord.Object(id=GUILD_TOKEN))
# async def slash_command(interaction:discord.Interaction):
#     await makeDailyLeaderboardPost()
#     logging.info("Slash command completed for daily leaderboard")

# @bot.tree.command(name="weekly",description="Shows the weekly leaderboard",guild=discord.Object(id=GUILD_TOKEN))
# async def slash_command(interaction:discord.Interaction):
#     await interaction.response.send_message("Weekly dailyboard")


#prefix command example
# @bot.command(
#     name="test",
#     description="My first application Command",
#     guild=discord.Object(id=GUILD_TOKEN)
# )
# async def first_command(interaction):
#     await interaction.channel.send("Hello from prefix command")


def getPostsFromUserData(userData):

    posts = []
    try:
        color = 0x109319
        user = userData['username']
        title = "{0} just solved a Leetcode problem!".format(user)    
        host = constants.LC_URL
        thumbnail = "https://cdn.pixabay.com/photo/2016/03/31/17/55/achievement-1294004_1280.png"
        status = ":white_check_mark: Accepted"    
        footer = "This problem has an AC Rate of {0}"
        
        for p in userData['postableSubmissions']:
            ts = utils.getTimeFromEpoch(int(p['timestamp']))

            if 'question' not in p: continue
            q = p['question']
            acRate = q['acRate']
            description = "[** #LC {0} - {1}**]({2})".format(q['frontend_question_id'], q['question__title'], q['link'])
            post = Post(title=title, titleUrl=host + p['url'], description=description, color=color, 
                        submitTime=ts,authorName=user, 
                        authorImg=userData['avatar'], authorUrl= host +"/{0}".format(user) , thumbnail=thumbnail,
                        footer = footer.format(acRate), difficulty=utils.getDifficulty(q['difficulty']), status=status,                     
                        acRate=acRate, lang=p['lang']
                    )
            posts.append(post)
    
    except Exception as e:
        logging.info("Empty userData object. No post object created")
        
    return posts

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

    
