import discord
from datetime import datetime
from table2ascii import table2ascii as t2a, PresetStyle
import utils
import constants

class Leaderboard:
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title")        
        self.color = kwargs.pop("color")        
        self.authorImg = kwargs.pop("authorImg")
        self.thumbnail = kwargs.pop("thumbnail")
        self.users = kwargs.pop("users")
        self.endTs = kwargs.pop("endTs")

    def getLeaderboard(self):
        self.endTs = self.endTs.astimezone()
        
        embed=discord.Embed(title=self.title, 
            description="** {0} (Last 24 hours)**".format(self.endTs.strftime(constants.PRETTY_TIME_FORMAT)), 
            color=self.color)
                
        embed.set_author(
            name="Leetcode", 
            url="https://leetcode.com", 
            icon_url=self.authorImg
        )

        embed.set_thumbnail(url=self.thumbnail)
       
        # [[1, 'avantika', 5, 5, 2, 12, 34], [2, 'monkbaby', 1, 1, 1, 3, 11], [3, 'what?', 1, 1, 0, 2, 4]]
        body = []
        for user in self.users:
            userData = []
            userData.append(user['username'])
            userData.append(int(user['easy']))
            userData.append(int(user['med']))
            userData.append(int(user['hard']))
            userData.append(int(user['total']))
            userData.append(int(user['score']))
            body.append(userData)

        sortedBody = sorted(body, key=lambda x: x[5], reverse=True)
        for i in range(0, len(sortedBody)):
            elem = sortedBody[i]
            elem.insert(0, i+1)

        output = t2a(
            header=["No.", "Name", "E", "M", "H", "T", "Score"],
            body=sortedBody,
            style=PresetStyle.double_compact
        )

        embed.add_field(name="", value=f"```\n{output}\n```", inline=False) 
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


