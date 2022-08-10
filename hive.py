import json
import requests
from hiveMCBE.errors import *

base_url = "https://api.playhive.com/v0/game"
games = {
					"TREASURE_WARS": "wars", 
					"DEATH_RUN": "dr", 
					"HIDE_AND_SEEK": "hide", 
					"SURVIVAL_GAMES": "sg", 
					"MURDER_MYSTERY": "murder", 
					"SKY_WARS": "sky", 
					"CAPTURE_THE_FLAG": "ctf", 
					"BLOCK_DROP": "drop", 
					"GROUND_WARS": "ground", 
					"JUST_BUILD": "build"
				}


class HivePlayer:
	def __init__(self, username):
		self.username = username
		self.games = games
	
	#for getting player statistics for a minigame
	def stats(self, game):
		if game in self.games.keys():
			r = requests.get(f"{base_url}/all/{self.games[game]}/{self.username}")
			if r.ok == True:
				return(json.loads(r.text)) #converting json text to dict
			elif r.status_code == 500:
				raise InternalServerError("Hive API returned status code 500")
			else:
				raise PlayerNotFound(f'Player "{self.username}" was found in Hive database')
		else:
			raise MinigameNotFound(f'Minigame "{game}" does not exist')
	
	#for getting player entry in current monthly leaderboard
	def monthly_leader(self,game):
		if game in self.games.keys():
			r = requests.get(f"{base_url}/monthly/player/{self.games[game]}/{self.username}")
			if r.ok == True:
				return(json.loads(r.text))
			elif r.status_code == 500:
				raise InternalServerError("Hive API returned status code 500")
			else:
				raise PlayerNotFound(f'Player "{self.username}" was not found in monthly leaderboard for game "{game}"')
		else:
			raise MinigameNotFound(f'Minigame "{game}" does not exist')
	
	#for getting player entry in leaderboard of a specific month
	def specific_monthly_leader(self,game, year, month):
		if game in self.games.keys():
			r = requests.get(f"{base_url}/monthly/player/{self.games[game]}/{self.username}/{year}/{month}")
			if r.ok == True:
				return(json.loads(r.text))
			elif r.status_code == 500:
				raise InternalServerError("Hive API returned status code 500")
			else:
				raise PlayerNotFound(f'Player "{self.username}" was not found in {month}/{year} monthly leaderboard for game "{game}"')
		else:
			raise MinigameNotFound(f'Minigame "{game}" does not exist')


#for getting monthly leaderboard or all time leaderboard if all_time == True
def leaderboard(game, count = 50, all_time = False):
	if all_time == True:
		type = "all"
	else:
		type = "monthly"
	if count > 50:
		raise LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in games.keys():
		r = requests.get(f"{base_url}/{type}/{games[game]}")
		if r.ok == True:
			lb = json.loads(r.text)
			return(lb[0:count]) #slicing the dict acc. to user specified length
		elif r.status_code == 500:
			raise InternalServerError("Hive API returned status code 500")
	else:
		raise MinigameNotFound(f'Minigame "{game}" does not exist')

#for getting leaderboard for a specific month
def specific_leaderboard(game, year, month, count = 50):
	if count > 50:
		raise LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in games.keys():
		r = requests.get(f"{base_url}/monthly/{games[game]}/{year}/{month}/{count}/0")
		if r.ok == True:
			return(json.loads(r.text))
		elif r.status_code == 500:
			raise InternalServerError("Hive API returned status code 500")
	else:
		raise MinigameNotFound(f'Minigame "{game}" does not exist')