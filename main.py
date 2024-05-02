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
    return render_template('home/index.html', discord_url=OAuth.discord_login_url)

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
    if data is False:
        return redirect(url_for('homepage'))

    return render_template('servers/servers-ROOM.html', guilds=data, user_avatar_url=user_avatar_url, username=username)

#Server Painel Page's
@app.route('/servers/painel/<server_id>')
def painel_Home(server_id):
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

    return render_template('servers/painel-HOME.html',guild=BotAndUser.get_guild_by_id(server_id), user_avatar_url=user_avatar_url, username=username)

@app.route('/servers/painel/comandos/set')
def painel_set():
    if not session.get("token") or not session.get("user_token"):
        return redirect(url_for('homepage'))

    #User
    username = Discord_User.get_username()
    user_avatar_url = Discord_User.get_avatar()

    return render_template('servers/painel-SET.html', guild_channels=Discord_Guild.get_text_channels(), guild_roles=Discord_Guild.get_roles(), user_avatar_url=user_avatar_url, username=username)

#Admin Page
@app.route('/admin')
def adminRoom():
    if not session.get("token") or not session.get("user_id") == DEVS_IDS:
        return redirect("/")
    
    #User
    user_avatar_url = Discord_User.get_avatar()
    username = Discord_User.get_username()

    return render_template('admin/admin-HOME.html', user_avatar_url=user_avatar_url, username=username)

#API Methods
@app.route('/api/commands/add-server', methods=["POST"])
def addServer():
    if not session.get("token") or not session.get("user_id") in DEVS_IDS:
        print("User Doens't Have Permission\n")
        return redirect("/")
    
    #Get Vars From Form
    guild_name = request.form['guild_name']
    guild_id = request.form['guild_id']
    buyer_user_id = request.form['buyer_user_id']
    rent_expire_date = request.form['rent_expire_date']

    #API Data & Send
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

    #Get Command Params
    try:
        #First Button:
        b1_activated = True
        button_name_1 = request.form['button_name_1']
        role1_input_1 = request.form['role1_input_1']
        role2_input_1 = request.form['role2_input_1']
        prefix_name_1 = request.form['prefix_name_1']
        has_id_1 = request.form['id_1']
        

        #Second Button:
        try:
            b2_activated = True
            button_name_2 = request.form['button_name_2']
            role1_input_2 = request.form['role1_input_2']
            role2_input_2 = request.form['role2_input_2']
            prefix_name_2 = request.form['prefix_name_2']
            has_id_2 = request.form['id_2']
        except:
            b2_activated = False
            button_name_2 = 0
            role1_input_2 = 0
            role2_input_2 = 0
            prefix_name_2 = 0
            has_id_2 = 0

            #Third Button:
        try:
            b3_activated = True
            button_name_3 = request.form['button_name_3']
            role1_input_3 = request.form['role1_input_3']
            role2_input_3 = request.form['role2_input_3']
            prefix_name_3 = request.form['prefix_name_3']
            has_id_3 = request.form['id_3']
        except:
            b3_activated = False
            button_name_3 = 0
            role1_input_3 = 0
            role2_input_3 = 0
            prefix_name_3 = 0
            has_id_3 = 0

        # Check For Null Inputs
        if role1_input_1 == 0:
            if role2_input_1 == 0:
                return redirect(url_for('homepage'))
        
        if prefix_name_1 == '':
            prefix_name_1 = 0
        
        if prefix_name_2 == '':
            prefix_name_2 = 0
        
        if prefix_name_3 == '':
            prefix_name_3 = 0

        #Get Channel Id
        selected_Channel = request.form['channel_selector']

        buttonsInfo = [
            {
                "activated": b1_activated,
                "name": button_name_1,
                "role_1": role1_input_1,
                "role_2": role2_input_1,
                "prefix": prefix_name_1,
                "has_id": has_id_1
            },
            {
                "activated": b2_activated,
                "name": button_name_2,
                "role_1": role1_input_2,
                "role_2": role2_input_2,
                "prefix": prefix_name_2,
                "has_id": has_id_2
            },
            {
                "activated": b3_activated,
                "name": button_name_3,
                "role_1": role1_input_3,
                "role_2": role2_input_3,
                "prefix": prefix_name_3,
                "has_id": has_id_3
            },
        ] 

        buttonsDump = json.dumps(buttonsInfo)

        #API Data
        url = "http://localhost:3000/api/commands/set"
        data = {
            #API Auth
            'user_id': session.get('user_id'),
            'user_token': session.get('user_token'),
            #Command Data
            'buttons_data': buttonsDump,
            'selected_channel': selected_Channel
            }
        res = requests.post(url, data)
        if res.status_code != 200:
            return redirect(url_for('homepage'))
    except RuntimeError:
        print(RuntimeError)
        return redirect(url_for('homepage'))

    return redirect(url_for('painel_set')) 

if __name__ == "__main__":
    app.run(debug=True)