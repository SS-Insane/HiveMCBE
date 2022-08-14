import json
import requests 
import HiveMCBE as hive

#for fetching monthly leaderboard OR all time leaderboard if all_time == True
async def fetch_leaderboard(game, count = 50, all_time = False):
	if all_time == True:
		type = "all"
	else:
		type = "monthly"
	if count > 50:
		raise hive.LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in hive.games.keys():
		r = requests.get(f"{hive.base_url}/{type}/{hive.games[game]['identifier']}")
		if r.ok == True:
			lb = json.loads(r.text)
			return(lb[0:count]) #slicing the dict acc. to user specified length
		elif r.status_code == 500:
			raise hive.InternalServerError("Hive API returned status code 500")
	else:
		raise hive.MinigameNotFound(f'Minigame "{game}" does not exist')

#for fetching leaderboard for a specific month
async def fetch_specific_leaderboard(game, year, month, count = 50):
	if count > 50:
		raise hive.LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in hive.games.keys():
		r = requests.get(f"{hive.base_url}/monthly/{hive.games[game]['identifier']}/{year}/{month}/{count}/0")
		if r.ok == True:
			return(json.loads(r.text))
		elif r.status_code == 500:
			raise hive.InternalServerError("Hive API returned status code 500")
	else:
		raise hive.MinigameNotFound(f'Minigame "{game}" does not exist')