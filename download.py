#Look this up
from bs4 import BeautifulSoup
#Look up
import re
import os
import sys
import time
#Look this up - seems to be related to web scraping
import requests
import concurrent.futures as futures

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_FOLDER = os.path.join(CURRENT_DIR, 'j-archive archive')
NUM_THREADS = 2

#Multiprocessing to speed things up (each season can be done concurrently)
try:
	import multiprocessing
	NUM_THREADS = multiprocessing.cpu_count() * 2
	print('Using {} threads'.format(NUM_THREADS))
except (ImportError, NotImplementedError):
	pass

#Execute the multithreading
def main():
	create_save_folder()
	#CHANGE: Only want last season to try to build data first
	seasons = list(range(36,37))
	print(len(seasons))
	with futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
		for season in seasons:
			#First parameter is the method, second parameter is the parameter for that method
			f = executor.submit(download_season, season)

#Create folder to save results
def create_save_folder():
	if not os.path.isdir(SITE_FOLDER):
		sys_print("Creating {} folder".format(SITE_FOLDER))
		os.mkdir(SITE_FOLDER)

#Downloads data from each season
def download_season(season):
	sys_print('Downloading Season {}'.format(season))
	#Create subfolder for season #?
	season_folder = os.path.join(SITE_FOLDER, "season {}".format(season))
	if not os.path.isdir(season_folder):
		sys_print("Creating season {} folder".format(season))
		os.mkdir(season_folder)
	#Get page of the specified season
	seasonPage = requests.get('http://j-archive.com/showseason.php?season={}'.format(season))
	#LOOK UP
	seasonSoup = BeautifulSoup(seasonPage.text, 'lxml')
	#"re" from re import class
	epIdRe = re.compile(r'game_id=(\d+)')
	epNumRe = re.compile(r'\#(\d{1,4})')
	episodeRe = re.compile(r'http:\/\/www\.j-archive\.com\/showgame\.php\?game_id=[0-9]+')
	#Parse this list comprehension, specifically the "link.get('href')" thing
	episodeLinks = [link for link in seasonSoup.find_all('a') if episodeRe.match(link.get('href'))][::-1]
	#Traverse all episodes in this season
	for link in episodeLinks:
		#Get episode number
		episodeNumber = epNumRe.search(link.text.strip()).group(1)
		#Not sure what this is, maybe it's getting the link of the specific episode num? Don't think so
		gameFile = os.path.join(season_folder,'{}.html'.format(episodeNumber))
		#If they can't find the gameFile in the directory (so seems like it might be some sort of file)
		if not os.path.isfile(gameFile):
			episodeId = epIdRe.search(link['href']).group(1)
			gamePage = requests.get('http://j-archive.com/showgame.php?game_id={}'.format(episodeId))
			#Opening the file to write to it
			open(gameFile, 'wb').write(gamePage.content)
			time.sleep(5)
	sys_print('Season {} finished'.format(season))

#Just a print function
def sys_print(string):
	sys.stdout.write("{}\n".format(string))
	sys.stdout.flush()

if __name__=="__main__":
	main()