from ..apitoken.api_token import Token

class Gw2Build:
    def __init__(self, owner):
        self.token_obj = Token()
        self.token = token_obj.get_token(self.owner)
        self.owner = owner
    
    def check_api(self):
        check = self.token_obj.check_token(self.token)
        if not self.token or not check[0]:
            return False
        
        return True