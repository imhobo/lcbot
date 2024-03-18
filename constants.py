import datetime as dt
from datetime import datetime, timedelta

POST_INTERVAL_MINUTES = 60
INTERVAL_DELTA = timedelta(minutes=30)
INTERVAL_POST_DELTA = timedelta(minutes=POST_INTERVAL_MINUTES)
INTERVAL_CUSTOM_DELTA = timedelta(minutes=90)
INTERVAL_DAILY_DELTA = timedelta(hours=24)
INTERVAL_WEEKLY_DELTA = timedelta(days=7)
LC_API_URL = "http://localhost:3000"
ALGORITHMS_API_FILE = "resources/algorithms"
EMBED_COLOR_DAILY_LB = 0x109319
EMBED_COLOR_WEEKLY_LB = 0xFFD700
DAILY_LB_TITLE = "Daily Leaderboard"
DAILY_LB_DESC = "Last 24 hours"
DAILY_LB_AUTHOR_URL = "https://upload.wikimedia.org/wikipedia/commons/1/19/LeetCode_logo_black.png"
DAILY_LB_THUMBNAIL = "https://raw.githubusercontent.com/imhobo/lcbot/main/assets/medal.png"
DAILY_LB_TIME = dt.time(hour=0, minute=30) #utc time zone
WEEKLY_LB_TIME = dt.time(hour=1, minute=30) #utc time zone
WEEKLY_LB_DAY = 1 #0 = mon, 6 = sun
WEEKLY_LB_TITLE = "Weekly Leaderboard"
WEEKLY_LB_DESC = "Last 7 days"
WEEKLY_LB_THUMBNAIL = "https://raw.githubusercontent.com/imhobo/lcbot/main/assets/weekly_lb.png"
POST_THUMBNAIL = "https://cdn.pixabay.com/photo/2016/03/31/17/55/achievement-1294004_1280.png"
PRETTY_TIME_FORMAT = "%-d %b, %Y %-I:%M %p %Z "
LC_URL = 'https://leetcode.com'
DATE_FORMAT = "%Y-%m-%d"