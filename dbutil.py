import queries
import json
import logging

log = logging.getLogger(__name__)

async def createTables(bot):
    await bot.db.execute(queries.createTableUsers())
    await bot.db.execute(queries.createTableDailyStats())

async def saveDailyLBStats(bot, users, timestamp):
        
    users_json = json.dumps(users)    
    await bot.db.execute(queries.addStatstoDailyLBQuery(users_json, timestamp.strftime("%Y-%m-%d %H:%M:%S")))