import re
import requests as r
import sqlite3


class Token:
    def __init__(self):
        self.pattern = "(.{8}-)(.{4}-){3}(.{20}-)(.{4}-){3}(.{12})"
        self.regex = re.compile(self.pattern)
        self.url_token = "https://api.guildwars2.com/v2/tokeninfo?access_token="
        self.account_url = "https://api.guildwars2.com/v2/account?access_token="
        self.conn = sqlite3.connect("data/gw2_database.SQLITE")

    def check_token(self, token):
        result = self.regex.fullmatch(token)
        if result:
            url = f"{self.url_token}{token}"
            req = r.get(url)
            json_req = req.json()
            if "text" in json_req:
                return False
            permissions = json_req.get("permissions")
            id = json_req.get("id")
            return True, {"id": id, "permissions": permissions}

    def update_token(self, owner, token):
        check = self.check_token(token)
        if check:
            cursor = self.conn.cursor()
            data = self.get_token_owner(owner)
            for row in data:
                if owner in row[0]:
                    self._remove_permissions(owner)
                    cursor.execute(
                        "UPDATE tokens "
                        "SET token_value =:token "
                        "WHERE token_owner =:owner",
                        {"token": token, "owner": owner}
                    )
                    self._add_permissions(
                        token=token, owner=owner, permissions=check[1]["permissions"])
                    cursor.close()
                    self.conn.commit()
                    return True
            cursor.close()
        return False

    def get_token_owner(self, owner):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT token_owner "
            "FROM tokens "
            "where token_owner =:owner",
            {"owner": owner}
        )
        data = cursor.fetchall()
        return data
        

    def get_token(self, owner):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT token_value "
            "FROM tokens "
            "where token_owner =:owner",
            {"owner": owner}
        )
        data = cursor.fetchall()
        if len(data) == 1 and type(data[0][0]) == str:
            return data[0][0]
        else:
            return None

    def get_tokens(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tokens")
        data = cursor.fetchall()
        return data

    def add_token(self, token, owner):
        check = self.check_token(token)
        if check:
            data = self.get_tokens()
            for row in data:
                if token in row[1]:
                    return False
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO tokens (token_value, token_owner) "
                "values (?, ?)",
                (token, owner)
            )
            self._add_permissions(check[1]["permissions"], token, owner)
            cursor.close()
            self.conn.commit()
            return True
        return False

    def remove_token(self, owner):
        cursor = self.conn.cursor()
        data = self.get_token_owner(owner)
        for row in data:
            if owner in row[0]:
                cursor.execute(
                    "DELETE FROM tokens "
                    "WHERE token_owner =:owner",
                    {"owner": owner}
                )
                cursor.close()
                self.conn.commit()
                return True
        cursor.close()
        return False

    def _add_permissions(self, permissions: list, token: str, owner: str):
        cursor = self.conn.cursor()
        for permission in permissions:
            cursor.execute(
                "INSERT INTO tokens_permissions (token_value, permission_name, token_owner)"
                "VALUES (?, ?, ?)",
                (token, permission, owner)
            )
        cursor.close()
        self.conn.commit()

    def _remove_permissions(self, owner: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM tokens_permissions "
            "WHERE token_owner=:owner",
            {"owner": owner}
        )
        cursor.close()
        self.conn.commit()
