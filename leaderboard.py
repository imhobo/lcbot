import discord
from table2ascii import table2ascii as t2a, PresetStyle
import utils
import constants

class Leaderboard:
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title")
        self.desc = kwargs.pop("desc")        
        self.color = kwargs.pop("color")        
        self.authorImg = kwargs.pop("authorImg")
        self.thumbnail = kwargs.pop("thumbnail")
        self.users = kwargs.pop("users")
        self.endTs = kwargs.pop("endTs")
        self.type = kwargs.pop("type")

    def getLeaderboard(self):
        self.endTs = self.endTs.astimezone()
        
        embed=discord.Embed(title="** {0} **".format(self.title), 
            description="** {0} ({1})**".format(self.endTs.strftime(constants.PRETTY_TIME_FORMAT), self.desc), 
            color=self.color)
                
        embed.set_author(
            name="Leetcode", 
            url="https://leetcode.com", 
            icon_url=self.authorImg
        )

        embed.set_thumbnail(url=self.thumbnail)
               
        body = []
        for user in self.users:
            userDict = {}            
            userDict['username'] = user['username']
            userDict['score'] = int(user['score'])
            stats = []                        
            stats.append(int(user['easy']))
            stats.append(int(user['med']))
            stats.append(int(user['hard']))
            stats.append(int(user['total']))
            stats.append(int(user['score']))
            userDict['stats'] = stats            
            body.append(userDict)

        sortedBody = sorted(body, key=lambda x: x['score'], reverse=True)
    
        for i in range(0, len(sortedBody)):
            user = sortedBody[i]
            user['rank'] =  i+1

        # sortedBody = [{'rank': 1, 'username': 'avantikababy', 'stats': [15, 15, 12, 12, 34]}, 
        #               {'rank': 2, 'username': 'monkbaby', 'stats': [1, 1, 1, 3, 11]}
        #               ]
             
        for user in sortedBody:
            output = t2a(
                    header=["E", "M", "H", "T", "Pts"],
                    body=[user['stats']],
                    style=PresetStyle.plain
                    )
            if self.type == "WEEKLY":
                suffix = ""
                if user['rank'] == 1:suffix = ":first_place:"
                elif user['rank'] == 2:suffix = ":second_place:"
                elif user['rank'] == 3:suffix = ":third_place:"
                embed.add_field(name="{0}. {1} {2}".format(user['rank'], user['username'], suffix), value=f"```\n{output}\n```", inline=False) 
            elif self.type == "DAILY":                
                embed.add_field(name="{0}. {1}".format(user['rank'], user['username']), value=f"```\n{output}\n```", inline=False) 

        embed.set_footer(text="Easy = 1 Medium = 3 Hard = 7")
        return embed
    



# color = 0x109319
# user = "avantika"

# status = ":white_check_mark: Accepted"
# title = "{0} just solved a Leetcode problem!".format(user)
# thumbnail = "https://cdn.pixabay.com/photo/2016/03/31/17/55/achievement-1294004_1280.png"

# #profile
# authorName = user
# authorImg = "https://assets.leetcode.com/users/default_avatar.jpg"
# authorUrl = "https://leetcode.com/{0}".format(user)

# #recentAcSubmissionList
# questionTitleSlug = "roman-to-integer"
# questionTitle = "Roman to Integer"
# questionUrl = "https://leetcode.com/problems/{0}".format(questionTitleSlug)
# runtime = "6 ms"
# memory = "44.5 MB"
# submissionUrl = "https://leetcode.com/submissions/detail/1196837528/"
# submitTime = date.fromtimestamp(1709827844)
# lang = "java"

# #question
# questionId = 13
# description = "[** #LC {0} - {1}**]({2})".format(questionId, questionTitle, questionUrl)
# topics = "`Array` `Hash Table` `Math` `Geometry`"
# difficulty = ":green_circle: Easy"
# acRate = "60.79"
# footer = "This problem has an AC Rate of {0}".format(acRate)

# post = Post(title=title, titleUrl=submissionUrl, description=description, color=color, submitTime=submitTime,
#             authorName=authorName, authorImg=authorImg, authorUrl=authorUrl, thumbnail=thumbnail,
#             footer = footer, difficulty=difficulty, status=status, runtime=runtime, memory=memory,
#             acRate=acRate, questionUrl=questionUrl, lang=lang, topics=topics
#         )


