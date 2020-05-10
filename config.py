from pymongo import MongoClient
from datetime import datetime
import discord

client = MongoClient(MONGOSTRING)
mydb = client["utilities"]
guildscol = mydb["guilds"]
userscol = mydb["users"]
memberscol = mydb["members"]
mutescol = mydb["mutes"]

launch_time = datetime.utcnow()
