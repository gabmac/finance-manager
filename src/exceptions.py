class NotFound(Exception):
	def __init__(self, reason: str):
		super().__init__(reason)


