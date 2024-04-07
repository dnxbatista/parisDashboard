from flask import Flask, render_template, request, session, redirect, url_for
from utils.oauth import OAuth
from utils.easyFunctions.CUAB import Discord_User, BotAndUser, Discord_Guild
from dotenv import load_dotenv
import json
import requests
import os

#Dotenv
load_dotenv()
SECRET_KEY = os.getenv('FLASK_SECRETKEY')
DEVS_IDS = os.getenv('DEVS_IDS')

#Flask Config
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

#Home Page
@app.route('/')
def homepage():
    return render_template('index.html', discord_url=OAuth.discord_login_url)

#Login Method (Return To Servers Room Page)
@app.route('/servers', methods= ["GET", "POST"])
def login():
    #Get Code And Token From OAuth
    code = request.args.get("code")
    acessToken = OAuth.get_access_token(code)

    #CUAB Config
    Discord_User.acessToken = acessToken

    #User Vars
    user_avatar_url = Discord_User.get_avatar()
    username = Discord_User.get_username()

    #Get user ID and store in cookies
    user_id = Discord_User.get_id()

    #Find User API Token
    url = "http://localhost:3000/api/auth/login"
    user_data = {
        'user_id': user_id
    }
    res = requests.post(url, user_data)
    if res.status_code != 200: return redirect(url_for('homepage'))
    user_token = json.loads(res.text)

    #Saves Data In Cookies
    session["token"] = acessToken  #Discord Token
    session['user_token'] = user_token['token'] #API Token
    session["user_id"] = user_id # Discord UserID

    #Guilds
    guilds = BotAndUser.get_guilds()
    data = json.loads(guilds)

    return render_template('serversRoom.html', guilds=data, user_avatar_url=user_avatar_url, username=username)

#Servers Configuration Page
@app.route('/servers/painel/<server_id>')
def serverConfig(server_id):
    #Validate User
    if not session.get("token") or not session.get("user_token"):
        return redirect(url_for('homepage'))
    
    #Save Server ID In Cookies
    session["server_id"] = server_id 
    
    #Set Discord Guild ID
    Discord_Guild.guild_id = server_id

    #User
    user_avatar_url = Discord_User.get_avatar()
    username = Discord_User.get_username()

    return render_template('serverConfig.html', user_avatar_url=user_avatar_url, username=username, guild_roles=Discord_Guild.get_roles(), guild_channels=Discord_Guild.get_text_channels())

#Admin Page
@app.route('/developer')
def adminRoom():
    if not session.get("token") or not session.get("user_id") == DEVS_IDS:
        return redirect("/")
    
    #User
    user_avatar_url = Discord_User.get_avatar()
    username = Discord_User.get_username()

    return render_template('adminRoom.html', user_avatar_url=user_avatar_url, username=username)

#API Methods
@app.route('/api/commands/add-server', methods=["POST"])
def addServer():
    if not session.get("token") or not session.get("user_id") == DEVS_IDS:
        return redirect("/")
    
    #Get Vars From Form
    guild_name = request.form['guild_name']
    guild_id = request.form['guild_id']
    buyer_user_id = request.form['buyer_user_id']
    rent_expire_date = request.form['rent_expire_date']

    #API Data
    url = "http://localhost:3000/api/commands/add-server"
    data = {
        'user_id': session.get('user_id'),
        'user_token': session.get('user_token'),
        'guild_name':  guild_name,
        'guild_id': guild_id,
        'buyer_user_id': buyer_user_id,
        'rent_expire_date': rent_expire_date
    }
    res = requests.post(url, data)
    if res.status_code != 200:
        return redirect(url_for('homepage'))

    return redirect(url_for('adminRoom'))

@app.route('/api/commands/set', methods=["POST"])
def set_command():
    if not session.get("token") or not session.get("user_token"):
        return redirect(url_for('homepage'))
    
    #Get Vars From Form
    button_name = request.form['button_name']
    role_id = request.form['role_id']
    channel_id = request.form['channel_id']
    prefix_name = request.form['prefix_name']

    #Check
    if role_id == 0 or channel_id == 0:
        return redirect('/')
    
    #API Data
    url = "http://localhost:3000/api/commands/set"
    data = {
        'user_id': session.get('user_id'),
        'user_token': session.get('user_token'),
        'button_name': button_name,
        'role_id': role_id,
        'channel_id': channel_id,
        'prefix_name': prefix_name,
    }
    res = requests.post(url, data)
    if res.status_code == 200:
        return redirect(url_for('serverConfig', server_id=session['server_id']))
    else:
        return redirect('/')
    

if __name__ == "__main__":
    app.run(debug=True)