def createTableUsers():
    return """CREATE TABLE IF NOT EXISTS users (id serial primary key, created_at timestamp NOT NULL 
    DEFAULT (current_timestamp AT TIME ZONE 'UTC'), username VARCHAR(80) not null);
   """

def createTableDailyStats():
    return """CREATE TABLE IF NOT EXISTS daily_stats (id serial primary key, ts timestamp NOT NULL, stats JSONB, created_at timestamp NOT NULL 
    DEFAULT (current_timestamp AT TIME ZONE 'UTC'));
    """

def addUsernameQuery(username):
    return "INSERT INTO users(username) VALUES('{0}')".format(username)

def removeUsernameQuery(username):
    return "DELETE FROM users WHERE username='{0}'".format(username)

def getUsernameQuery():
    return "SELECT username FROM users"


def addStatstoDailyLBQuery(users, timestamp):
    return "INSERT INTO daily_stats(stats, ts) VALUES('{0}', '{1}')".format(users, timestamp)

def getStatsWeeklyQuery():
    return "SELECT * FROM daily_stats order by ts desc limit 7"

async def getUsernames(db):
    response = await db.fetch(getUsernameQuery())
    users = []
    for row in response:        
        users.append(row['username'])
    return users
