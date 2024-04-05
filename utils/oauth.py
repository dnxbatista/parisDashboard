import requests

class OAuth:
    client_id = "1170221058314473543"
    client_secret = "Y-1vMj5tLtGPgIWnJBg6vARe7pthkKhC"
    redirect_uri = "http://127.0.0.1:5000/servers"
    scope = "identify%20guilds%20email%"
    discord_login_url = "https://discord.com/oauth2/authorize?client_id=1170221058314473543&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fservers&scope=identify+email+guilds"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"

    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id": OAuth.client_id,
            "client_secret": OAuth.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": OAuth.redirect_uri,
            "scope": OAuth.scope
        }

        access_token = requests.post(url=OAuth.discord_token_url, data=payload).json()
        return access_token.get("access_token")

    @staticmethod
    def get_user_json(access_token):
        url = f"{OAuth.discord_api_url}/users/@me"
        headers = {"Authorization": f"Bearer {access_token}"}

        user_object = requests.get(url=url, headers=headers).json()
        return user_object




