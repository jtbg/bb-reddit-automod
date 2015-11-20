#!/usr/bin/env python2.7
import nflgame.live
import nflgame.game
import logging
import praw
from prawoauth2 import PrawOAuth2Mini

#Load bot settings
from settings import (app_key, app_secret, access_token, refresh_token, user_agent, scopes, subreddit, log_path, db_path)

#Configure logging
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y @ %H:%M :', level=logging.INFO)

#Callback function
def cb(active, completed, diffs):
    for g in active:
        if (g.home == 'BUF' or g.away == 'BUF'):
            time_remaining = str(g.time)
            gameInfo = '%s :: %s (%d) vs. %s (%d)' % (time_remaining, g.home, g.score_home, g.away, g.score_away)
            logging.info(gameInfo)

            if (time_remaining == 'Q4 02:00' or time_remaining.startswith('Q4 01')):
                logging.info("The two minute warning has been reached. Post the post-game thread and quit.")

                #Authenticate to Reddit
                logging.info("Authenticating to Reddit...")
                reddit_client = praw.Reddit(user_agent=user_agent)
                oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key, app_secret=app_secret, access_token=access_token, refresh_token=refresh_token, scopes=scopes)
                oauth_helper.refresh()

                #Post the thread
                postGameThreadTitle = "Post-Game Thread: " + g.away + "@" + g.home

                submission = reddit_client.submit(subreddit, postGameThreadTitle, 
                    text=("* Please be mindful of our sidebar rules.\n\n"
                    "* Please report any violations.\n\n"
                    "* Self-post threads are subject to deletion during and after the game."))

                #Sticky the thread
                logging.info("Stickying the thread")
                submission.sticky()
                logging.info("Update complete. Exiting game monitor.")

                exit()

logging.info("Intializing game monitor...")
nflgame.live.run(cb)