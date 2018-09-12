#! /usr/bin/python3

import praw
import time
import re

#Globals
VERSION = 1.1
POST_DELAY = 10 #seconds
REACTION_TICKER = 10 #minutes
REACTION_TIMEOUT = 3 #days
VOTE_THRESHOLD = 3 #score

#Setup
BLACKLIST_LOCATION = "/home/liam/application_data/atom/reddit/BestiaryBot/blacklist.txt"
LOGIN_LOCATION = "/home/liam/application_data/atom/reddit/BestiaryBot/login.txt"

login_file = open(LOGIN_LOCATION, "r")

CLIENT_ID = login_file.readline().strip()
CLIENT_SECRET = login_file.readline().strip()
USERNAME = login_file.readline().strip()
PASSWORD = login_file.readline().strip()
USER_AGENT = login_file.readline().strip()

#This variable holds the instance of PRAW that will talk to the reddit API
reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,username=USERNAME,password=PASSWORD,user_agent=USER_AGENT)

#Setup some subreddits
bossfightbestiary = reddit.subreddit("bossfightbestiary")
bossfight = reddit.subreddit("bossfight")

#This function determines whether a comment should be left on a post
def blacklisted(post):
    f = open(BLACKLIST_LOCATION,"r")
    for line in f:
        if post.id in line:
            f.close()
            return True
    f.close()
    return False

#Blacklist a comment to stop further comments being made on it
def blacklist(post):
    f = open(BLACKLIST_LOCATION,"a")
    f.write(post.id + " " + post.title)
    f.write("\n")
    f.close()

#The main looping part of the program
def main():
    print("Bestiary bot" + str(VERSION) + "has loaded!")
    while True:
        try:
            for post in bossfightbestiary.stream.submissions():
                title = post.title
                title = re.sub('\[.*?\]','',title)
                title = re.sub('\(.*?\)','',title)
                #print(title)
                original_url = ""
                if(not blacklisted(post)):
                    for submission in bossfight.search(title):
                        original_url = submission.shortlink
                        break
                        print("")
                    print("Handling: " + title)
                    blacklist(post)

                    if(original_url):
                        reply = "I did my best to find the [original](" + original_url + ")"
                    else:
                        reply = "Hi! I was unable to locate the original based on your title. Please link the original yourself. In the future, please use the title of the original r/bossfight post when posting here!"
                    comment = post.reply(reply)
                    comment.mod.distinguish(how='yes', sticky=True)

                    time.sleep(POST_DELAY)
        except Exception as e: print(e)
#Begin!
main()
