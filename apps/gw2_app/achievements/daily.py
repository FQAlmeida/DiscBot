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
        self.url_tomorrow = "https://api.guildwars2.com/v2/achievements/daily/tomorrow"
        self.achievements_obj = Achievements()

    def __get_dailies(self, tomorrow=False):
        return requests.get(self.url if not tomorrow else self.url_tomorrow).json()

    def _get_dailies(self, tomorrow=False):
        dailies = self.__get_dailies(tomorrow)
        pve = dailies.get("pve")
        pvp = dailies.get("pvp")
        wvw = dailies.get("wvw")
        fractals = dailies.get("fractals")
        special = dailies.get("special")

        return {"pve": pve, "pvp": pvp, "wvw": wvw, "fractals": fractals, "special": special}

    def get_dailies(self, tomorrow=False):
        dailies = self._get_dailies(tomorrow)
        ids_list = self._get_ids(dailies)
        return self._build_achievements(ids_list)

    def _build_achievements(self, ids: dict):
        final_dailies = {"pve": [], "pvp": [], "wvw": [], "fractals": [], "special": []}
        for key, ids_list in ids.items():
            final_dailies[key] = self.achievements_obj.get_achievements(ids_list)
        return final_dailies

    def _get_ids(self, dailies: dict):
        ids = {"pve": [], "pvp": [], "wvw": [], "fractals": [], "special": []}

        def _build_pve(pve):
            for achievement in pve:
                ids["pve"].append(achievement.get("id"))
            return ids

        def _build_pvp(pvp):
            for achievement in pvp:
                ids["pvp"].append(achievement.get("id"))
            return ids

        def _build_wvw(wvw):
            for achievement in wvw:
                ids["wvw"].append(achievement.get("id"))
            return ids

        def _build_fractals(fractals):
            for achievement in fractals:
                ids["fractals"].append(achievement.get("id"))
            return ids

        def _build_special(special):
            for achievement in special:
                ids["special"].append(achievement.get("id"))
            return ids

        _build_pve(dailies["pve"])
        _build_pvp(dailies["pvp"])
        _build_wvw(dailies["wvw"])
        _build_fractals(dailies["fractals"])
        _build_special(dailies["special"])

        return ids


if __name__ == "__main__":
    daily = Daily()
    dailies = daily._get_dailies()

    ids = daily._get_ids(dailies)

    # final_disct = dict(str, list(Achievements))
    final_dict = daily._build_achievements(ids)

    for key, value in final_dict.items():
        print(f"{key:*^50}")
        for v in value:
            print(v)
