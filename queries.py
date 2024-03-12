

def addUsernameQuery(username):
    return "INSERT INTO users(username) VALUES('{0}')".format(username)

def removeUsernameQuery(username):
    return "DELETE FROM users WHERE username='{0}'".format(username)

def getUsernameQuery():
    return "SELECT username FROM users"

async def getUsernames(bot):
    response = await bot.db.fetch(getUsernameQuery())
    users = []
    for row in response:        
        users.append(row['username'])
    return users
