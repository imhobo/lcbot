import queries
import json
import logging

log = logging.getLogger(__name__)

async def createTables(db):
    await db.execute(queries.createTableUsers())
    await db.execute(queries.createTableDailyStats())

async def saveDailyLBStats(db, users, timestamp):
        
    users_json = json.dumps(users)    
    await db.execute(queries.addStatstoDailyLBQuery(users_json, timestamp.strftime("%Y-%m-%d %H:%M:%S")))