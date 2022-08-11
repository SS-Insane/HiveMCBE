import json
import requests 
import HiveMCBE as hive

#for getting monthly leaderboard or all time leaderboard if all_time == True
def leaderboard(game, count = 50, all_time = False):
	if all_time == True:
		type = "all"
	else:
		type = "monthly"
	if count > 50:
		raise LimitExceeded("cannot fetch more than 50 entries in leaderboard")
	if game in hive.games.keys():
		r = requests.get(f"{hive.base_url}/{type}/{hive.games[game]}")
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
	if game in hive.games.keys():
		r = requests.get(f"{hive.base_url}/monthly/{hive.games[game]}/{year}/{month}/{count}/0")
		if r.ok == True:
			return(json.loads(r.text))
		elif r.status_code == 500:
			raise InternalServerError("Hive API returned status code 500")
	else:
		raise MinigameNotFound(f'Minigame "{game}" does not exist')