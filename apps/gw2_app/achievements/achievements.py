import requests


class Achievements:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.requirements = ""
        self.locked_text = ""
        self.achievement_url = "https://api.guildwars2.com/v2/achievements?ids="

    def _get_achievement_json(self, ids: list):
        ids_str = ",".join(map(str, ids))
        resp = requests.get(f"{self.achievement_url}{ids_str}").json() if ids_str != "" else []
        return resp

    def get_achievements(self, ids: list):
        resp = self._get_achievement_json(ids)
        final_list = []
        for achievement in resp:
            if isinstance(achievement, str):
                continue
            aux = Achievements()
            aux.id = achievement.get("id")
            aux.name = achievement.get("name")
            aux.description = achievement.get("description")
            aux.requirements = achievement.get("requirement")
            aux.locked_text = achievement.get("locked_text")
            final_list.append(aux)
        return final_list

    def __str__(self):
        return f"id: {self.id}\n" \
               f"name: {self.name}\n" \
               f"desc: {self.description}\n" if self.description != "" and self.description is not None else "" \
               f"req: {self.requirements}\n" if self.requirements != "" and self.requirements is not None else "" \
               f"lock: {self.locked_text}" if self.locked_text != "" and self.locked_text is not None else ""
