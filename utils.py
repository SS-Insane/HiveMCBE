import HiveMCBE as hive

def calculate_level(game, xp):
	game = hive.games[game]
	increment = game["xp increment"]
	rxp = -increment
	txp = 0
	i = 1
	while i <= game["max level"]:
		if i <= game["cap"]:
			rxp += increment
		txp += rxp
		if txp > xp:
			return [i - 1, txp - xp]
			i = game["max level"]
		i += 1
	return [game["max level"], 0]


def calculate_extra_stats(data):
	if "victories" in data:
		data["losses"] = data["played"] - data["victories"]
		if data["played"] != 0:
			data["win_rate"] = f"{round(data['victories']/data['played']*100)}%"
		else:
			data["win_rate"] = "0%"
	if "kills" in data:
		kills = data["kills"]
	elif "murders" in data:
		kills = data["murders"]
	elif "hider_kills" in data:
		kills = data["hider_kills"]
	else:
		pass
	if "deaths" in data:
		if ("kills" or "hider_kills" or "murders") in data:
			if data["deaths"] == 0:
				data["kdr"] = kills
			else:
				data["kdr"] = round(kills/data["deaths"])
	
	return data
