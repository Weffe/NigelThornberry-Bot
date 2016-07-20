#!/usr/bin/env python3
__author__ = 'Rogelio Negrete - Weffe'

#Built on PRAW 3.5: http://praw.readthedocs.io/en/v3.5.0/
#Inspiration taken from ButtsBot: https://github.com/jadunawa/ButtsBot

import praw
import re
import time
from datetime import datetime
try:
    from .PickleList import PickleList
except Exception: #ImportError
    from PickleList import PickleList

def start_bot():

    #pre-load our nigel pics list
    nigelObj = PickleList('nigelpicslinks.p')
    permalinkObj = PickleList('permalinks.p')

    r = praw.Reddit('NigelThornberry by Weffe')
    r.login('NigelThornberry-Bot', 'nigelthornberry', disable_warning='True')

    #subreddit = r.get_subreddit('NigelThornberryBot')
    #subreddit = r.get_random_subreddit()

    subs = ('NigelThornberryBot+' + str(r.get_random_subreddit()))
    subreddit = r.get_subreddit(subs)

    print("\n-----------------------\nWorking in", str(subreddit))

    #get 15 hot submissions
    for submission in subreddit.get_hot(limit=15):

        submission_date = datetime.fromtimestamp(submission.created_utc)  # get submission date
        day_ago = datetime.fromtimestamp(time.time() - (24 * 60 * 60))  # find date for 24 hours ago

        # ignore posts over 24 hours old
        if (int((day_ago - submission_date).days) + 1 < 2):

            submission.replace_more_comments(limit=None, threshold=0) #get all comments
            all_comments = submission.comments #make array of comments
            flat_comments = praw.helpers.flatten_tree(all_comments) #flatten comments, order is not taken into concern

            regex_pattern = re.compile(r"(?:\S+\s)?\S*" + 'smash' + r"\S*(?:\s\S+)?", re.IGNORECASE) #our regex pattern to work with

            counter = 1 # for log purposes

            for comment in flat_comments:
                search_result = re.search(regex_pattern, str(comment)) #result looks like this: [word] [keyword] [word]
                comment_permalink = comment.permalink

                #we found our keyword in the comment!
                #we dont reply to ourselves
                #we dont reply to the same user twice via permalink
                if search_result and str(comment.author) != "NigelThornberry-Bot" and permalinkObj.is_link_in_list(comment_permalink) == False:

                    current_date = datetime.now()

                    #add permalink into our picke list to ignore in the future
                    #save as a tuple to our pickle_list
                    permalinkObj.add_to_pickle_list((comment_permalink, current_date))

                    text_reply = "> "

                    #we need to modify [keyword] so that its bold in the reply
                    comment_qoute = list(search_result.group(0).split()) #split search_result into a list
                    for x in range(0, len(comment_qoute)):
                        if re.match(r"smash\S*", comment_qoute[x], re.IGNORECASE) != None:
                            comment_qoute[x] = ' **' + comment_qoute[x] + '** ' #replacing our keyword with bold characters on reddit
                    comment_qoute = ''.join(comment_qoute) #concatenate our list
                    text_reply += comment_qoute + "\n\n[Did someone say smashing?!](" + nigelObj.choose_random_nigel_pic() + ")"

                    #send reply and upvote
                    comment.reply(text_reply)
                    comment.upvote()

                    #print permalink to the comment we responded to
                    print("\n[" + str(counter) +"] Comment Made: " + comment_permalink)
                    counter = counter + 1

    #save our updated pickle_list for the next runtime
    permalinkObj.clean_up_permalink_list()
    permalinkObj.save_pickle_list()

def main():
    start_bot()

if __name__ == '__main__':
    main()
