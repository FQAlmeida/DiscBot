import requests
import json
import discord
import datetime
import random
from typing import Union

from ..apitoken.api_token import Token


class Gw2Build:
    def __init__(self):
        self.token_obj = Token()
        self.chars_url = "https://api.guildwars2.com/v2/characters/<character>?access_token=<API key>"
        self.skills_url = "https://api.guildwars2.com/v2/skills?ids="
        self.equips_url = "https://api.guildwars2.com/v2/items?ids="
        self.specs_url = "https://api.guildwars2.com/v2/specializations?ids="
        self.traits_url = "https://api.guildwars2.com/v2/traits?ids="
        self.item_stat_url = "https://api.guildwars2.com/v2/itemstats?ids="

    def mount_build(self, owner, character):
        check, token = self.check_api(owner)
        if check:
            skills_ids, equips_ids, specs_ids = self.get_data_from_server(
                character, token)
            skills_data = self.get_skills_data(skills_ids)
            equips_data, stat_data = self.get_equips_data(equips_ids)
            specs_data, traits_data = self.get_build_specs_data(specs_ids)
            msgs = list()
            msgs.append(self.build_skills_layout(skills_data, character))
            msgs.extend(self.build_traits_layout(
                traits_data, specs_data, character))
            msgs.extend(self.build_equips_layout(
                equips_ids, equips_data, stat_data, character))
            return msgs

    def check_api(self, owner) -> (bool, Union[str, None]):
        token = self.token_obj.get_token(owner)
        if not token:
            return False, None
        check = self.token_obj.check_token(token)
        if not check[0]:
            return False, None
        if "characters" not in check[1].get("permissions"):
            return False, None
        return True, token

    def get_skills_data(self, skills):
        ids = [skills.get("wvw").get(
            "heal"), *skills.get("wvw").get("utilities"), skills.get("wvw").get("elite"), ]
        ids = [item for item in map(str, ids)]
        data = requests.get(f"{self.skills_url}{','.join(ids)}").json()
        return data

    def get_equips_data(self, equips):
        ids = [item.get("id") for item in equips]
        ids = [item for item in map(str, ids)]
        stats_ids = [item.get("stats").get("id")
                     for item in equips if item and item.get("stats")]
        stats_ids = [item for item in map(str, stats_ids)]
        data = requests.get(f"{self.equips_url}{','.join(ids)}").json()
        stats_data = requests.get(
            f"{self.item_stat_url}{','.join(stats_ids)}").json()
        return data, stats_data

    def get_build_specs_data(self, specs):
        ids_specs = [spec.get("id") for spec in specs.get("wvw")]
        ids_specs = [ids for ids in map(str, ids_specs)]

        specs_url = f"{self.specs_url}{','.join(ids_specs)}"
        specs_data = requests.get(specs_url).json()

        ids_traits = list()
        for spec in specs_data:
            ids_traits += [*spec.get("minor_traits")]
        for spec in specs.get("wvw"):
            traits = spec.get("traits")
            ids_traits += traits
        ids_traits = [ids for ids in map(str, ids_traits)]
        traits_url = f"{self.traits_url}{','.join(ids_traits)}"
        traits_data = requests.get(traits_url).json()
        return specs_data, traits_data

    def get_data_from_server(self, character, token):
        url = self.chars_url.replace(
            "<character>", character).replace("<API key>", token)
        data = requests.get(url).json()
        skills = data.get("skills")
        equips = data.get("equipment")
        specs = data.get("specializations")
        return skills, equips, specs

    def build_skills_layout(self, data, character) -> discord.Embed:
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = "Skills"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(url=data[random.randint(0, len(data)-1)].get("icon"))
        for skill in data:
            msg.add_field(name=skill.get("slot"),
                          value=skill.get("name"), inline=False)
        return msg

    def build_traits_layout(self, traits_data, specs_data, character) -> list:
        msgs = list()
        for spec in specs_data:
            traits = list()
            minors = spec.get("minor_traits")
            majors = spec.get("major_traits")
            for trait in traits_data:
                trait_id = trait.get("id")
                if trait_id in [*majors, *minors]:
                    traits.append(trait)
            msgs.append(self._build_traits_layout(traits, spec, character))
        return msgs

    def _build_traits_layout(self, traits_data, specs_data, character) -> discord.Embed:
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = f"Traits - {specs_data.get('name')}"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(url=specs_data.get("icon"))
        for trait in traits_data:
            msg.add_field(name=trait.get("name"),
                          value=trait.get("description"), inline=False)
        return msg

    def _build_armor(self, equips, equips_data, stats, character):
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = f"Armors - {character}"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(
            url=equips_data[random.randint(0, len(equips_data)-1)].get("icon"))
        for armor in equips_data:
            stat = False
            for armor_aux in equips:
                if armor.get("id") == armor_aux.get("id"):
                    armor_data = armor_aux
                    break
            if armor_data:
                for stat_aux in stats:
                    stat_id_aux = stat_aux.get("id")
                    armor_stat = armor_data.get("stats")
                    if armor_stat:
                        stat_id = armor_stat.get("id")
                        if stat_id_aux == stat_id:
                            stat = stat_aux
                            break
            if not stat:
                stat_id_aux = armor.get("infix_upgrade")
                for stat_aux in stats:
                    stat_id = stat_aux.get("id")
                    if stat_id_aux == stat_id:
                        stat = stat_aux
                        break
            if stat:
                name = f"{stat.get('name')} {armor.get('details').get('type')}"
            else:
                name = f"{armor.get('details').get('type')} {armor.get('name')}"
            value = f"{armor.get('name')} {armor.get('chat_link')} level: {armor.get('level')}"
            msg.add_field(name=name, value=value, inline=False)
        return msg

    def _build_trinket(self, equips, equips_data, stats, character):
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = f"Trinkets - {character}"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(
            url=equips_data[random.randint(0, len(equips_data)-1)].get("icon"))
        for trinket in equips_data:
            stat = False
            for trinket_aux in equips:
                if trinket.get("id") == trinket_aux.get("id"):
                    trinket_data = trinket_aux
                    break
            if trinket_data:
                for stat_aux in stats:
                    stat_id_aux = stat_aux.get("id")
                    armor_stat = trinket_data.get("stats")
                    if armor_stat:
                        stat_id = armor_stat.get("id")
                        if stat_id_aux == stat_id:
                            stat = stat_aux
                            break
            if not stat:
                stat_id_aux = trinket.get("infix_upgrade")
                for stat_aux in stats:
                    stat_id = stat_aux.get("id")                    
                    if stat_id_aux == stat_id:
                        stat = stat_aux
                        break
            if stat:
                name = f"{stat.get('name')} {trinket.get('details').get('type')}"
            else:
                name = f"{trinket.get('details').get('type')} {trinket.get('name')}"
            value = f"{trinket.get('name')} {trinket.get('chat_link')} level: {trinket.get('level')}"
            msg.add_field(name=name, value=value, inline=False)
        return msg

    def _build_weapon(self, equips, equips_data, stats, character):
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = f"Weapons - {character}"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(
            url=equips_data[random.randint(0, len(equips_data)-1)].get("icon"))
        for weapon in equips_data:
            stat = False
            for weapon_aux in equips:
                if weapon.get("id") == weapon_aux.get("id"):
                    weapon_data = weapon_aux
                    break
            if weapon_data:
                for stat_aux in stats:
                    stat_id_aux = stat_aux.get("id")
                    armor_stat = weapon_data.get("stats")
                    if armor_stat:
                        stat_id = armor_stat.get("id")
                        if stat_id_aux == stat_id:
                            stat = stat_aux
                            break
            if not stat:
                stat_id_aux = weapon.get("infix_upgrade")
                for stat_aux in stats:
                    stat_id = stat_aux.get("id")
                    if stat_id_aux == stat_id:
                        stat = stat_aux
                        break
            if stat:
                name = f"{stat.get('name')} {weapon.get('details').get('type')}"
            else:
                name = f"{weapon.get('details').get('type')} {weapon.get('name')}"
            value = f"{weapon.get('name')} {weapon.get('chat_link')} level: {weapon.get('level')}"
            msg.add_field(name=name, value=value, inline=False)
        return msg

    def _build_back(self, equips, equips_data, stats, character):
        colour = discord.Colour.dark_purple()
        date = datetime.datetime.now()
        title = f"Backpack - {character}"
        description = f"{character} {title} - {date.date()}\n"

        msg = discord.Embed(title=title, timestamp=date,
                            description=description, colour=colour)
        msg.set_thumbnail(
            url=equips_data[random.randint(0, len(equips_data)-1)].get("icon"))
        for back in equips_data:
            stat = False
            for back_aux in equips:
                if back.get("id") == back_aux.get("id"):
                    back_data = back_aux
                    break
            if back_data:
                for stat_aux in stats:
                    stat_id_aux = stat_aux.get("id")
                    armor_stat = back_data.get("stats")
                    if armor_stat:
                        stat_id = armor_stat.get("id")
                        if stat_id_aux == stat_id:
                            stat = stat_aux
                            break
            if not stat:
                stat_id_aux = back.get("infix_upgrade")
                for stat_aux in stats:
                    stat_id = stat_aux.get("id")
                    if stat_id_aux == stat_id:
                        stat = stat_aux
                        break
            if stat:
                name = f"{stat.get('name')} {back.get('details').get('type')}"
            else:
                name = f"{back.get('details').get('type')} {back.get('name')}"
            value = f"{back.get('name')} {back.get('chat_link')} level: {back.get('level')}"
            msg.add_field(name=name, value=value, inline=False)
        return msg

    def build_equips_layout(self, equips, equips_data, stats_data, character):
        msgs = list()
        back = list()
        armor = list()
        weapon = list()
        trinket = list()
        for equip in equips_data:
            equip_type = equip.get("type").lower()
            if equip_type == "armor":
                armor.append(equip)
            elif equip_type == "weapon":
                weapon.append(equip)
            elif equip_type == "trinket":
                trinket.append(equip)
            elif equip_type == "back":
                back.append(equip)
        msgs.append(self._build_armor(equips, armor, stats_data, character))
        msgs.append(self._build_weapon(equips, weapon, stats_data, character))
        msgs.append(self._build_trinket(equips, trinket, stats_data, character))
        msgs.append(self._build_back(equips, back, stats_data, character))
        return msgs
