import discord

class Post:
    def __init__(self, **kwargs):
        self.title = kwargs.pop("title")
        self.titleUrl = kwargs.pop("titleUrl")
        self.description = kwargs.pop("description")
        self.color = kwargs.pop("color")
        self.submitTime = kwargs.pop("submitTime")
        self.authorName = kwargs.pop("authorName")
        self.authorImg = kwargs.pop("authorImg")
        self.authorUrl = kwargs.pop("authorUrl")
        self.thumbnail = kwargs.pop("thumbnail")
        self.footer = kwargs.pop("footer")
        self.difficulty = kwargs.pop("difficulty")
        self.status = kwargs.pop("status")        
        self.acRate = kwargs.pop("acRate")  
        self.lang = kwargs.pop("lang")
        

    def getPost(self):

        embed=discord.Embed(title=self.title, 
            url=self.titleUrl, 
            description=self.description, 
            timestamp=self.submitTime,
            color=self.color)
                
        embed.set_author(name=self.authorName, 
            url=self.authorUrl, 
            icon_url=self.authorImg)

        embed.set_thumbnail(url=self.thumbnail)

        embed.add_field(name="Difficulty", value=self.difficulty, inline=False)
        embed.add_field(name="Status", value=self.status, inline=True)
        embed.add_field(name="Lang", value=self.lang, inline=True)   
        # embed.add_field(name="Topics", value=self.topics, inline=True)        
        
        embed.set_footer(text=self.footer)
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
