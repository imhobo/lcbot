from datetime import datetime
import json
import constants

def floor_dt(dt, delta):
    return dt - (dt - datetime.min) % delta

def getDifficulty(difficulty):
    if difficulty == "Easy":
        return ":green_circle: {0}".format(difficulty)
    elif difficulty == "Medium":
        return ":yellow_circle: {0}".format(difficulty)
    return ":red_circle: {0}".format(difficulty)

def getTopics(topics):
    topicString = ""
    for t in topics:
        topicString += "`" + t['name'] + "` "
    return topicString

def getDifficultyString(difficultyLevel):        
    level = difficultyLevel['level']
    if level == 1:
        return "Easy"
    elif level == 2:
        return "Medium"
    else:
        return "Hard"
    

def getAllQuestionsMap():
    with open(constants.ALGORITHMS_API_FILE) as user_file:
        file_contents = user_file.read()

    parsed_json = json.loads(file_contents)
    stat_status_pairs = parsed_json['stat_status_pairs']
    link = constants.LC_URL + "/problems/"
    questions = {}
    for pair in stat_status_pairs:
        question = {}     
        stat = pair['stat']        
        difficulty = pair['difficulty']    
        acRate = str(round(float((int(stat['total_acs'])/int(stat['total_submitted']))) * 100, 2))
        for key in stat:
            question[key] = stat[key]

        question['link'] = link + stat['question__title_slug']
        question['difficulty'] = getDifficultyString(difficulty)
        question['acRate'] = acRate
        questions[stat['question__title_slug']] = question
    return questions

    # print(questions)

def filterSubmissions(submissions, startTs, endTs):
    validAcSubmissions = []
    for i in submissions:
        acSubmissionTs = datetime.fromtimestamp(int(i["timestamp"]))
        if(endTs > acSubmissionTs and startTs <= acSubmissionTs):
             validAcSubmissions.append(i)
    return validAcSubmissions


def getValidSubmissions(submission, acSubmission, startTs, endTs):
        
    validAcSubmissions = []
    titleToTs = {}

    for i in submission:
        if i['statusDisplay'] == 'Accepted':
            submissionTs = int(i["timestamp"])
            titleSlug = i["titleSlug"]            
            if titleSlug in titleToTs:                
                titleToTs[titleSlug] = min(submissionTs, titleToTs[titleSlug])
            else :
                titleToTs[titleSlug] = submissionTs

    for i in acSubmission:
        acSubmissionTs = datetime.fromtimestamp(int(i["timestamp"]))
        if(endTs > acSubmissionTs and startTs <= acSubmissionTs):            
            titleSlug = i["titleSlug"]            
            if(titleSlug in titleToTs):
                submissionTs = datetime.fromtimestamp(titleToTs[titleSlug])
                                
                if(submissionTs < startTs and submissionTs > (startTs - constants.INTERVAL_DAILY_DELTA)):
                    continue
            
                elif(submissionTs != acSubmissionTs and 
                    submissionTs >= startTs and submissionTs < endTs):
                    i["timestamp"] = str(round(submissionTs.timestamp()))
            
            validAcSubmissions.append(i)

    return validAcSubmissions


def getDailyLeaderboardUser(username, submissions, questions):

    user = {}
    total = len(submissions)
    easy = 0
    medium = 0
    hard = 0
    for s in submissions:
        titleSlug = s['titleSlug']
        question = questions[titleSlug]
        if(question['difficulty'] == "Easy"):
            easy += 1
        elif(question['difficulty'] == "Medium"):
            medium += 1            
        elif(question['difficulty'] == "Hard"):
            hard += 1    

    score = easy + medium * 3 + hard * 7

    user['username'] = username
    user['easy'] = easy
    user['med'] = medium
    user['hard'] = hard  
    user['total'] = total
    user['score'] = score

    # print(user)
    return user