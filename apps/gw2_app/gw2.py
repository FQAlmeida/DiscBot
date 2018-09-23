from apps.gw2_app.achievements import daily
from apps.gw2_app.apitoken import api_token


class GW2:
    def __init__(self):
        self.token = api_token.Token()
        self.daily = daily.Daily()
