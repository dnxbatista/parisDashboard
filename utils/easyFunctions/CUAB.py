"""
Compare User And Bot
! Made To Paris Bot Dashboard !
! Right's To Paris Bot !
"""

from utils.oauth import OAuth
import requests
import json

class Discord_User:
    """
    Discord User Infos... [ NEED A TOKEN TO WORK ]
    """
    acessToken = None    

    @staticmethod
    def get_avatar():
        """
        Return's the avatar URL from the user
        """
        user = OAuth.get_user_json(Discord_User.acessToken)
        avatar = user.get("avatar")
        user_id = user.get("id")
        user_avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
        return user_avatar_url
    
    @staticmethod
    def get_username():
        """
        Return's the username
        """
        user = OAuth.get_user_json(Discord_User.acessToken)
        user_name = user.get("username")
        return user_name
    
    @staticmethod
    def get_email():
        """
        Return's the email from the user
        """
        user = OAuth.get_user_json(Discord_User.acessToken)
        user_email = user.get("email")
        return user_email
    
    @staticmethod
    def hasNitro():
        """
        Return's TRUE if the user has nitro, and FALSE if doesn't
        """
        user = OAuth.get_user_json(Discord_User.acessToken)
        user_nitro_status = user.get("premium_type")

        if user_nitro_status == 0:
            return False
        
        return True
    
    @staticmethod
    def get_id():
        """
        Return's the user id
        """
        user = OAuth.get_user_json(Discord_User.acessToken)
        user_id = user.get("id")
        return user_id
    
    @staticmethod
    def get_user_guilds():
        """
        Return's all guilds the user is in
        """
        user_guilds_res = requests.get(
        'https://discord.com/api/v8/users/@me/guilds',
        headers={'Authorization': f'Bearer {Discord_User.acessToken}'}
        )
        user_guilds = user_guilds_res.text
        json_data = json.loads(user_guilds)
        return json_data

class Discord_Bot:
    """
    Get Bot Informations...
    ! Bot Needs To Be Online !
    """
    @staticmethod
    def get_bot_guilds():
        """
        Return's all guilds the bot is in
        """
        bot_guilds = requests.post('http://localhost:3000/api/bot/get-guilds')
        json_data = json.loads(bot_guilds.text)
        return json_data
    
class BotAndUser:
    @staticmethod
    def get_guilds_id():
        """
        Return's the guilds ids that the user and the bot are in
        """
        #Get Bot Guilds
        bot_guilds = Discord_Bot.get_bot_guilds()
        bot_guilds_ids = [guild['id'] for guild in bot_guilds['bot_guilds']]

        #Get User Guilds
        user_guilds = Discord_User.get_user_guilds()
        user_guilds_ids = [guild['id'] for guild in user_guilds]

        #Converte Para Um Conjunto
        bot_guilds_ids_c = set(bot_guilds_ids)
        user_guilds_ids_c = set(user_guilds_ids)

        #Get The Intesection
        intersection = user_guilds_ids_c.intersection(bot_guilds_ids_c)

        #Return comuns ids
        comuns_id = list(intersection)
        return comuns_id
    
    @staticmethod
    def get_items_by_id():
        ids = BotAndUser.get_guilds_id()
        json_file = Discord_Bot.get_bot_guilds()
        bot_guilds = json_file['bot_guilds']
        data = [item for item in bot_guilds if item['id'] in ids]
        return json.dumps(data)

    @staticmethod 
    def get_guilds():
        """
        Return's the guilds that the user and the bot are in
        """   
        return BotAndUser.get_items_by_id()
    
class Discord_Guild:
    """
    Get Guild Informations... [ Need A Guild ID ]
    """
    guild_id = None

    @staticmethod
    def get_roles():
        """
        Get All Roles Of A Guild
        """

        url = "http://localhost:3000/api/guild/get-roles"
        data = {
            'guild_id': Discord_Guild.guild_id
        }
        res = requests.post(url, data)
        guild_roles = json.loads(res.text)
        if res.status_code == 200:
            return guild_roles['guild_roles']
        else:
            return 0
        
    def get_channels():
        """
        Get All Channels Of A Guild
        """

        url = "http://localhost:3000/api/guild/get-channels"
        data = {
            'guild_id': Discord_Guild.guild_id
        }
        res = requests.post(url, data)
        guild_channels = json.loads(res.text)
        if res.status_code == 200:
            return guild_channels['guild_channels']
        else:
            return 0
        
    def get_text_channels():
        guild_channels = Discord_Guild.get_channels()
        raw_text_channels = [channel for channel in guild_channels if channel.get('type') == 0]
        text_channels = json.dumps(raw_text_channels)
        data = json.loads(text_channels)
        return data
        
        
    