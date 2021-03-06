#!/usr/bin/env python

import praw
from credentials import *
import requests
import urllib
from prawcore import NotFound
import sys

# connect to reddit
reddit = praw.Reddit(client_id=ID,
                     client_secret=SECRET,
                     password=PASSWORD,
                     user_agent=AGENT,
                     username=USERNAME)

# obtain reddit to download images from, and number of images to download
subreddit_exists = True
subreddit = str(raw_input('Please enter subredit: '))

# check that subreddit exists
try:
    reddit.subreddits.search_by_name(subreddit, exact=True)
except NotFound:
    print 'Subreddit %s does not exist.' % subreddit
    sys.exit(0)

# get number of pics requested
num_pics = int(raw_input('Please enter number of pics: '))
count = 0

# find images/gifs in subreddit
for submission in reddit.subreddit(subreddit).hot():
    if count < num_pics:
        if 'https://i.imgur.com/' or 'https://i.redd.it/' in submission.url:
            img_url = submission.url
            extension = img_url.rsplit('.', 1)
            extension = extension[1]
            if extension in ['jpg', 'gif', 'jpeg', 'png']:
                print 'Downloading...'
                img = urllib.urlretrieve(
                    img_url, 'images/%s_%s.%s' % (subreddit, str(submission.id[:4]), extension))
                count += 1
            if extension == 'gifv':
                print 'Downloading...'
                img_url = img_url.rsplit('.', 1)
                img_url[1] = '.gif'
                img_url = img_url[0] + img_url[1]
                img = urllib.urlretrieve(
                    img_url, 'images/%s_%s.%s' % (subreddit, str(submission.id[:4]), 'gif'))
                count += 1
print '\nCompleted!\n'
