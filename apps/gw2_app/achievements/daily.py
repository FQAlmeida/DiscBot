import requests

from apps.gw2_app.achievements.achievements import Achievements


class Daily:

    """
    Guild Wars 2 - Daily Achievements
    --- PvE ---
    1)
    2)
    ..
    n)

    --- PvP ---
    1)
    2)
    ..
    n)

    --- WvW ---
    1)
    2)
    ..
    n)

    --- Fractals ---
    1)
    2)
    ..
    n)

    --- Especial --- if exists
    1)
    2)
    ..
    n)
    """

    def __init__(self):
        self.url = "https://api.guildwars2.com/v2/achievements/daily"
        self.achiev_url = "https://api.guildwars2.com/v2/achievements?ids="

    def _get_dailies(self):
        return requests.get(self.url).json()

    def get_dailies(self):
        dailies = self._get_dailies()
        pve = dailies.get("pve")
        pvp = dailies.get("pvp")
        wvw = dailies.get("wvw")
        fractals = dailies.get("fractals")
        special = dailies.get("special")

        return {"pve": pve, "pvp": pvp, "wvw": wvw, "fractals": fractals, "special": special}

    def _build_achievements(self, dailies: dict):
        pass

    def _get_ids(self, dailies: dict):
        ids = []

        def _build_pve(pve, ids: list):
            for achiev in pve:
                ids.append(achiev.get("id"))
            return ids

        def _build_pvp(pvp, ids: list):
            for achiev in pvp:
                ids.append(achiev.get("id"))
            return ids

        def _build_wvw(wvw, ids: list):
            for achiev in wvw:
                ids.append(achiev.get("id"))
            return ids

        def _build_fractals(fractals, ids: list):
            for achiev in fractals:
                ids.append(achiev.get("id"))
            return ids

        def _build_special(special, ids: list):
            for achiev in special:
                ids.append(achiev.get("id"))
            return ids

        return _build_pve(dailies["pve"], ids)


if __name__ == "__main__":
    daily = Daily()
    dailies = daily.get_dailies()

    ids = daily._get_ids(dailies)
    ids = ",".join(map(str, ids))

    resp = requests.get(daily.achiev_url + ids).json()

    for achiev in resp:
        a = Achievements()
        a.id = achiev.get("id")
        a.name = achiev.get("name")
        a.description = achiev.get("description")
        a.requirements = achiev.get("requirement")
        print(a)
