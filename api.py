import traceback
import requests
import asyncio
from datetime import datetime, timedelta, timezone
import constants
import utils
from constants import LC_API_URL
import sys
import json

import logging
log = logging.getLogger(__name__)

def requestGet(url, headers={}, payload={}):
    try:
        response = requests.get(url, headers=headers, params=payload)    
        if response.status_code != 200:
            log.error("Url is not working properly! - {0}".format(url))
            log.error(response.status_code)            
            raise
        response_json = response.json()
        return response_json       
        
    except Exception as e:
        log.error("Unexpected error:", e)
    return {}

    

def requestPost(url, headers={}, proxies={}, payload={}):
    response = requests.post(url, json=payload, headers=headers, proxies=proxies)    
    log.info(response.text)
    if response.status_code == 200:
        response_json = response.json()
    else:
        log.info(response.status_code)
        raise Exception
    return response_json


#There are 2 major bugs
#1. There can be duplicate or missed posts due to minor difference in when the last scheduled function ran
#2. There will be duplicate posts for the same question if the user submits multiple AC submissions as the timestamp
#    in the LC api keeps the last submission time for a question. So since that keeps changing I will keep posting it again
#3. Also I dont change the submission url from the AC submission list. Meaning even if the timestamp is of the first
#   time you solved, the url is still of the latest accepted submission   
async def getUserProfile(username):
    link = LC_API_URL + "/{0}".format(username)
    response = requestGet(link)
    return response

async def getUserSubmissions(username):
    response=[]
    try:
        suffix = "/acSubmission"
        link = LC_API_URL + "/{0}".format(username) + suffix
        response_json = requestGet(link)
        response = response_json['submission']
    except Exception as e:
        log.error("Unexpected error:", e)
    return response

async def getQuestion(titleSlug):
    suffix = "/select?titleSlug={0}".format(titleSlug)
    link = LC_API_URL + suffix
    response = requestGet(link)
    return response



async def getUserDataFromLC(username, questions, startTs = datetime.min, endTs = datetime.utcnow()):    
    user = {}
    try:
        response_json = await getUserProfile(username)      
        user['username'] = response_json['username']
        user['avatar'] = response_json['avatar']
        submissions = utils.getValidSubmissions(response_json['submission'], response_json['acSubmission'], startTs, endTs)
        user['postableSubmissions'] = submissions
        for i in user['postableSubmissions']:
            titleSlug = i['titleSlug']            
            if titleSlug not in questions: 
                logging.error("Could not find {0} during making a post".format(titleSlug))
                continue

            questionResponse = questions[titleSlug]
            i['question'] = questionResponse
    except Exception as e:
        logging.error(e)
    
    return user
    
async def main():
    now = datetime.now(tz=timezone.utc)
    endTs = utils.floor_dt(now, constants.INTERVAL_HOUR_DELTA)
    startTs = endTs - constants.INTERVAL_DAILY_DELTA
    response = await getUserSubmissions('avantika')
    filtered = utils.filterSubmissions(response, startTs, endTs)
    print(filtered)
    

# print (utils.getAllQuestionsMap())
# asyncio.run(main())
    



