import datetime as dt
from datetime import datetime, timezone
import constants
import queries
import utils
import json
import logging
from discord.ext import commands, tasks
import leaderboard
import dbutil
import api

log = logging.getLogger(__name__)


@tasks.loop(time = constants.DAILY_LB_TIME)       
async def makeDailyLeaderboardPost(db, channel):
    
    try:
        questions = utils.getAllQuestionsMap()
        usernames = await queries.getUsernames(db)    
        # print(usernames)
        now = datetime.now(tz=timezone.utc)        
        endTs = utils.floor_dt(now, constants.INTERVAL_DELTA)
        startTs = endTs - constants.INTERVAL_DAILY_DELTA
        logging.info('Checking between {0} to {1} {2} for daily leaderboard'.format(endTs, startTs, 'UTC'))
        
        users = []
        for user in usernames:
            response = await api.getUserSubmissions(user)
            filtered_submissions = utils.filterSubmissions(response, startTs, endTs)    
            lbUser = utils.getDailyLeaderboardUser(user, filtered_submissions, questions)       
            users.append(lbUser)
            # print(user + " : "  + str(len(response)) + " : " + str(len(filtered_submissions)))
        
        # users = [{'username':'avantikababy', 'easy':4, 'med':2, 'hard':1, 'total':7, 'score':16},
        #         {'username':'monkbaby', 'easy':0, 'med':1, 'hard':2, 'total':3, 'score':15}
        # ]

        await dbutil.saveDailyLBStats(db, users, endTs)
        logging.info('Saved daily leaderboard stats for {0}'.format(endTs))

        lb = leaderboard.Leaderboard(title=constants.DAILY_LB_TITLE, desc=constants.DAILY_LB_DESC, 
                                     color=constants.EMBED_COLOR_DAILY_LB, thumbnail=constants.DAILY_LB_THUMBNAIL, 
                                     users=users, authorImg = constants.DAILY_LB_AUTHOR_URL, endTs = endTs, type = "DAILY")
                        
        await channel.send(embed=lb.getLeaderboard())
    except Exception as e:
        logging.exception(e)



@tasks.loop(time = constants.WEEKLY_LB_TIME)       
async def makeWeeklyLeaderboardPost(db, channel):
    day = dt.datetime.utcnow().weekday()
    if day != constants.WEEKLY_LB_DAY:return
    try:
        # usernames = await queries.getUsernames(bot)            
        
        now = datetime.utcnow()        
        startTs = now - constants.INTERVAL_WEEKLY_DELTA
        endDate = now.strftime(constants.DATE_FORMAT)
        startDate = startTs.strftime(constants.DATE_FORMAT)
        
        logging.info('Checking between {0} to {1} {2} for weekly leaderboard'.format(endDate, startDate, 'UTC'))
                
        response = await db.fetch(queries.getStatsWeeklyQuery())                

        userRecords = {}                
        endTs = datetime.min
        for record in response:            
            endTs = utils.maxTimestamp(record['ts'], endTs)
            stats = record['stats']
            json_stats = json.loads(stats)            
            # logging.info(json_stats)
            for stat in json_stats:                
                if stat['username'] not in userRecords.keys():
                    userRecords[stat['username']] = []                
                userRecords[stat['username']].append(stat)                            
                    
        # logging.info(userRecords)
        
        users = []
        for u in userRecords.keys():
            user = {}
            stats = userRecords[u]           
            for daily in stats:                
                if 'easy' in daily: user['easy'] = user.get('easy', 0) + daily['easy']
                if 'med' in daily: user['med'] = user.get('med', 0) + daily['med']
                if 'hard' in daily: user['hard'] = user.get('hard', 0) + daily['hard']
                if 'total' in daily: user['total'] = user.get('total', 0) + daily['total']
                if 'score' in daily: user['score'] = user.get('score', 0) + daily['score']
            user['username'] = u
            users.append(user)

        # logging.info(users)

        lb = leaderboard.Leaderboard(title=constants.WEEKLY_LB_TITLE, desc=constants.WEEKLY_LB_DESC, 
                                     color=constants.EMBED_COLOR_WEEKLY_LB, thumbnail=constants.WEEKLY_LB_THUMBNAIL, 
                                     users=users, authorImg = constants.DAILY_LB_AUTHOR_URL, endTs = endTs, type = "WEEKLY")
                                         
        await channel.send(embed=lb.getLeaderboard())
    except Exception as e:
        logging.exception(e)