import praw
import pdb
import time
import re
import os
import csv

# DISABLED function to call the value in one specific cell in the CSV file. Row and column numbering starts at 0,0
#def read_cell(x, y):
#    with open('perks.csv', 'r') as f:
#        reader = csv.reader(f)
#        y_count = 0
#        for n in reader:
#            if y_count == y:
#                cell = n[x]
#                return cell
#            y_count += 1

#API credentials:
bot = praw.Reddit(user_agent='Perkybot 1.0',
                  client_id='###',
                  client_secret='###',
                  username='Perkybot',
                  password='###S')

subreddit = bot.subreddit('deadbydaylight')

comments = subreddit.stream.comments()

#checks if the comments-replied-to document exists, and creates it if it does not
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

else:
    with open("comments_replied_to.txt", "r") as f:
       comments_replied_to = f.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))



#creates a list with all perknames from the Name column of the csv file
perkList = []
perkBracketList = []
with open('perks.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        perkList.append(row[0])
        perkBracketList.append(row[0])
perkList.remove('Name') # removes the name entry
perkBracketList.remove('Name') # removes the name entry



perkCounter = len(perkList) # var to hold the number of list objects
x = 1 
y = 0 # represents position of list object in list

# adds double brackets to beginning and end of perk name
while x <= perkCounter:
    perkBracketList[y] = "((" + perkList[y] + "))"
    y = y + 1
    x = x + 1

#creates a list with all descriptions in the description column of the csv file

descriptionList = []
with open('perks.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        descriptionList.append(row[1])
descriptionList.remove('Description') # removes the description entry

#creates a list with all characters in the character column of the csv file

characterList = []
with open('perks.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        characterList.append(row[2])
characterList.remove('Character') # removes the character entry

#creates a list with all characters in the character column of the csv file

levelList = []
with open('perks.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        levelList.append(row[3])
levelList.remove('Level') # removes the level entry


#aceintheholeVar = "**" + read_cell(0,1) + ":** " + read_cell(1,1) + " \n \n" + "[" + read_cell(2,1) + "]"

# scans the comments for the keywords
for comment in comments:
    text = comment.body # Fetch body
    author = comment.author # Fetch author
    if comment.id not in comments_replied_to:
        for perk in perkBracketList:
            if perk.lower() in comment.body.lower():
                print("String with " + perk + " found in comment " + comment.id)
                perkBracketIndex = perkBracketList.index(perk)
                descriptionIndex = perkBracketIndex
                message =  "**" + perkList[perkBracketIndex] + ":** " + " \n \n" + "* " + descriptionList[perkBracketIndex] + " \n \n" + "* Unlocked on " + characterList[perkBracketIndex] + " at level " + levelList[perkBracketIndex].format(author)
                comment.reply(message) # Send message
                print("Bot replying to: ", comment.id)
                comments_replied_to.append(comment.id)
                with open("comments_replied_to.txt", "w") as f:
                    for comment_id in comments_replied_to:
                        f.write(comment_id + "\n")
                time.sleep(10)
        if "((perkybot))" in comment.body.lower():
                print("String with perkybot found in comment " + comment.id)
                message =  "Hey there. I'm PerkyBot and I live on the DBD subreddit to provide information on killer and survivor perks. Use me by typing *((name of perk))* in any comment on this subreddit. If you want more information, visit my introduction post [here](https://nm.reddit.com/r/deadbydaylight/comments/aeitrp/introducing_perkybot_a_perk_bot_for_the_dbd/) or tag my system owner /u/Noxski".format(author)
                comment.reply(message) # Send message
                print("Bot replying to: ", comment.id)
                comments_replied_to.append(comment.id)
                with open("comments_replied_to.txt", "w") as f:
                    for comment_id in comments_replied_to:
                        f.write(comment_id + "\n")
                time.sleep(10)
