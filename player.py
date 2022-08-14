import json
import requests
import HiveMCBE as hive


class HivePlayer:
	def __init__(self, username):
		self.username = username
		self.games = hive.games
		self.base_url = hive.base_url
	
	#for getting player statistics for a minigame
	async def fetch_stats(self, game):
		if game in self.games.keys():
			r = requests.get(f"{self.base_url}/all/{self.games[game]['identifier']}/{self.username}")
			if r.ok == True:
				data = hive.calculate_extra_stats(json.loads(r.text))
				#check if data is a list, if it is then its empty so raise PlayerNotFound
				if data == list():
					raise hive.PlayerNotFound(f'Player "{self.username}" was not found in Hive database')
				else:
					level = hive.calculate_level(game, data["xp"])
					data["level"] = level[0]
				
					data["xp_for_next_level"] = level[1]
				return data
			elif r.status_code == 500:
				raise hive.InternalServerError("Hive API returned status code 500")
			else:
				raise hive.PlayerNotFound(f'Player "{self.username}" was not found in Hive database')
		else:
			raise hive.MinigameNotFound(f'Minigame "{game}" does not exist')
	
	#for getting player entry in current monthly leaderboard
	async def fetch_in_monthly_lb(self,game):
		if game in self.games.keys():
			r = requests.get(f"{self.base_url}/monthly/player/{self.games[game]['identifier']}/{self.username}")
			if r.ok == True:
				return(json.loads(r.text))
			elif r.status_code == 500:
				raise hive.InternalServerError("Hive API returned status code 500")
			else:
				raise hive.PlayerNotFound(f'Player "{self.username}" was not found in monthly leaderboard for game "{game}"')
		else:
			raise hive.MinigameNotFound(f'Minigame "{game}" does not exist')
	
	#for getting player entry in leaderboard of a specific month
	async def fetch_in_specific_lb(self,game, year, month):
		if game in self.games.keys():
			r = requests.get(f"{self.base_url}/monthly/player/{self.games[game]['identifier']}/{self.username}/{year}/{month}")
			if r.ok == True:
				return(json.loads(r.text))
			elif r.status_code == 500:
				raise hive.InternalServerError("Hive API returned status code 500")
			else:
				raise hive.PlayerNotFound(f'Player "{self.username}" was not found in {month}/{year} monthly leaderboard for game "{game}"')
		else:
			raise hive.MinigameNotFound(f'Minigame "{game}" does not exist')
