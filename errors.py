class HiveError(Exception):
	"This is base HiveMCBE exception class."

class PlayerNotFound(HiveError):
	"This will be raised when player is not found in the Hive database."

class MinigameNotFound(HiveError):
	"This will be raised when user asks for a minigame that does not exist."

class InternalServerError(HiveError):
	"This will be raised when API returns status code 500"

class LimitExceeded(HiveError):
	"This will be raised when user asks for more data than API can give"