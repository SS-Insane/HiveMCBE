import requests
import json
from hiveMCBE.errors import *

class HivePlayer:
	def __init__(self, username):
		self.username = username
		self.games = ["wars", "dr", "hide", "sg", "murder", "sky", "ctf", "drop", "ground", "build"]
	
	#for getting player statistics for a minigame
	def stats(self, game):
		if game in self.games:
			r = requests.get(f"https://api.playhive.com/v0/game/all/{game}/{self.username}")
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
		if game in self.games:
			r = requests.get(f"https://api.playhive.com/v0/game/monthly/player/{game}/{self.username}")
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
		if game in self.games:
			r = requests.get(f"https://api.playhive.com/v0/game/monthly/player/{game}/{self.username}/{year}/{month}")
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
	games = ["wars", "dr", "hide", "sg", "murder", "sky", "ctf", "drop", "ground", "build"]
	if all_time == True:
		type = "all"
	else:
		type = "monthly"
	if count > 50:
		raise LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in games:
		r = requests.get(f"https://api.playhive.com/v0/game/{type}/{game}")
		if r.ok == True:
			lb = json.loads(r.text)
			return(lb[0:count]) #slicing the dict acc. to user specified length
		elif r.status_code == 500:
			raise InternalServerError("Hive API returned status code 500")
	else:
		raise MinigameNotFound(f'Minigame "{game}" does not exist')

#for getting leaderboard for a specific month
def specific_leaderboard(game, year, month, count = 50):
	games = ["wars", "dr", "hide", "sg", "murder", "sky", "ctf", "drop", "ground", "build"]
	if count > 50:
		raise LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in games:
		r = requests.get(f"https://api.playhive.com/v0/game/monthly/{game}/{year}/{month}/{count}/0")
		if r.ok == True:
			return(json.loads(r.text))
		elif r.status_code == 500:
			raise InternalServerError("Hive API returned status code 500")
	else:
		raise MinigameNotFound(f'Minigame "{game}" does not exist')