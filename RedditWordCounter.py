#This bot is written by a script kiddie and most likely is riddled with erros.
#You have been warned
#scriptHijo

import praw
import config
import time
import os
import requests
import re
import io
from collections import Counter

def clean_files():
    open('words.txt', 'w').close();
    open('commented.txt', 'w').close();

def bot_login(): 
	print ("Logging in")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "Comment counter")
	print ("Logged in")
	return r
			
def run_bot(r, comments_replied_to, sub_name):
	
	#Start of program
	print ("Obtaining comments in subreddit: " + sub_name + "\n")
	
	#Counter, increments when a comment is saved
	i = 0
	q = 0
	
	#Loop through subreddit submissions on the top 100 post of all time
	for submission in r.subreddit(sub_name).top('all', limit = 100):
		q = q + 1
		#Loops though each top level comment in the submission
		for top_level_comment in submission.comments:
		
			#Try catches an error if the comment has been deleted
			try:
				#Check that comment hasnt been saved already
				if top_level_comment.id not in comments_replied_to and top_level_comment.author != r.user.me():
					#Add comment to list of comments replied to
					comments_replied_to.append(top_level_comment.id)
					
					#Open file to write comments to
					with io.open("words.txt", "a", encoding = "utf-8") as f:
							#Same comment body to a list
							j = top_level_comment.body + " "
							#increment counter
							i = i + 1 

							#Clean up list of white spaces and special chars
							j = re.sub('\s+',' ', j)
							j = re.sub('[^A-Za-z ]+','',j)
							#Write list of comments to file
							f.write(j)
					#Write replied to comment ID's to a file for next run
					print ("Comment #" + str(i))	
					with open ("commented", "a") as f:
						f.write(top_level_comment.id + "\n")
			except AttributeError:
				pass

            
	
	#Sleeping
	print ("Comments saved: " + str(i) + "\n")
	print ("Posts scanned: " + str(q) + "\n")
	#time.sleep(10)
	
def get_saved_comments():
	if not os.path.isfile("commented.txt"):
		comments_replied_to = []
	else:
		with open("commented.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			#comments_replied_to = filter(none, comments_replied_to)
			
	return comments_replied_to

#This function opens a file with comments, and counts frequency of words, and sorts most to least
def count_words():

	#Start of function
	print("Formatting comments...." + "\n")
	
	#Open file with comments
	with io.open("words.txt","r", encoding = "utf-8") as f:
		#Read all words in, converting to lower case to count both uppercase and lowercase words as the same word
		words = f.read().lower()
		
		#Create a list of all the words in the comments file
		content = words.split()
		
	#Create a counter list from out list of commented words
	common = Counter(content)
	
	#Open file of words to exclude from out count
	with open("exclude.txt", "r") as f:
		#Save exclude words to a list to search through
		exclude = f.read()
	#Open file to write counted and sorted list to
	k = 1; #Counter for words
	with open (sub_name + ".txt", "w") as f:
		#Loop through each word in count
		for word, count in common.most_common():
			#Check if word is a word to exclude
			if word not in exclude:
				f.write("{0}, {1}\n".format(word, count))
				k = k + 1
	
#Log into reddit
r = bot_login()

#make sure files are fresh
clean_files();

#List of comment id's saved
comments_replied_to = get_saved_comments()

#print (comments_replied_to)

sub_name = "pcmasterrace"

#start bot
run_bot(r, comments_replied_to, sub_name)

#Count words from subreddit
count_words()

print("Comments counted and added to file\nGoodbybe..")