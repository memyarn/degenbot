import os
import discord
from discord.ext import tasks
import datetime
import asyncio
import re
import pandas as pd #xd hehe
import numpy as np  #xd hehe
import logging
import sys

#because systemd is a bastard and won't display python print() in journalctl:
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)

np.random.seed()
intents = discord.Intents(messages=True)
intents.members = True
client = discord.Client(intents=discord.Intents.all()) #fuck the intents system tbh idc

#so that degenbot will always look in its own directory for its files, no matter where cwd is
bot_path = os.path.abspath(__file__)
dir_name = os.path.dirname(bot_path)
os.chdir(dir_name)
log.info('current directory: ' + dir_name)

jav_titles = np.asarray(pd.read_csv('some_jav_titles.csv')).flatten()
#there was no reason to do this in pandas and numpy, it was just for the meme.
log.info(str(jav_titles) + ', size: ' + str(jav_titles.size))
log.info('initization complete, ready to post!')

#903796962615242812 is #degeneral
#539959039967232002 is #degenerates
#613920172666912780 is #degenerarts
#734856994548088862 is #lewd-anime-images
#729138801104125952 is #anime-images
#the bot's userid is 729125116130230313

#.send(sender + " posted this: || " + content + " ||")

#jav_time = datetime.time(hour=17, minute=00, second=00) #this only works for discord.bot lol
@tasks.loop(hours=24)
async def post_jav(): #thomas if you're modifying this you only need to change this and the lunchtime function
	channel = client.get_channel(903796962615242812)
	jav_msg = str(np.random.choice(jav_titles)) #actually its kinda nice i can use randomchoice
	await channel.send(jav_msg)

@tasks.loop(hours=24)
async def post_lunchtime_jav():
	channel = client.get_channel(903796962615242812)
	jav_msg = str(np.random.choice(jav_titles))
	await channel.send(jav_msg)

@post_jav.before_loop
async def wait_for_work_to_be_over():
	it_is_time = False
	while not it_is_time:
		if datetime.datetime.now().hour == 17:  # 24 hour format
			log.info('The hour is upon us.')
			it_is_time = True
			return
		else:
			log.info('It is not yet time to strike.')
		
		await asyncio.sleep(420.69)

@post_lunchtime_jav.before_loop
async def wait_for_lunch():
	lunch_time = False
	while not lunch_time:
		if datetime.datetime.now().hour == 12:  # 24 hour format
			log.info('I am munching on snacks in the break room. I feel liberated.')
			lunch_time = True
			return
		else:
			log.info('Lunch hour has not yet arrived.')
		
		await asyncio.sleep(420.69)

@client.event
async def on_ready():
	if not post_jav.is_running(): #just in case i accidentally run more than one
		post_jav.start()
		log.info('post-work jav shitposting service enabled')
	if not post_lunchtime_jav.is_running():
		post_lunchtime_jav.start()
		log.info('lunchtime jav shitposting service enabled')

with open('discord_secret.txt', 'r') as secret_file:
    secret = secret_file.read().rstrip()

client.run(secret)