import json
import requests
import hiveMCBE as hive


class HivePlayer:
	def __init__(self, username):
		self.username = username
		self.games = hive.games
		self.self.base_url = hive.self.base_url
	
	#for getting player statistics for a minigame
	def stats(self, game):
		if game in self.games.keys():
			r = requests.get(f"{self.base_url}/all/{self.games[game]}/{self.username}")
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
			r = requests.get(f"{self.base_url}/monthly/player/{self.games[game]}/{self.username}")
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
			r = requests.get(f"{self.base_url}/monthly/player/{self.games[game]}/{self.username}/{year}/{month}")
			if r.ok == True:
				return(json.loads(r.text))
			elif r.status_code == 500:
				raise InternalServerError("Hive API returned status code 500")
			else:
				raise PlayerNotFound(f'Player "{self.username}" was not found in {month}/{year} monthly leaderboard for game "{game}"')
		else:
			raise MinigameNotFound(f'Minigame "{game}" does not exist')
