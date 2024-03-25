from flask import Flask, render_template, request, session, redirect, jsonify
from oauth import OAuth
from utils.easyFunctions.CUAB import Discord_User, Discord_Bot, BotAndUser
import json
import requests

#Flask Config
app = Flask(__name__)
app.config["SECRET_KEY"] = "Jn2n43JSnu43NJsad87928NJh23uih3Çç@fesç"


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
    session["token"] = acessToken  

    #CUAB Config
    Discord_User.acessToken = acessToken

    #User Vars
    user_avatar_url = Discord_User.get_avatar()
    username = Discord_User.get_username()

    guilds = BotAndUser.get_guilds()
    data = json.loads(guilds)

    return render_template('serversRoom.html', guilds=data, user_avatar_url=user_avatar_url, username=username)

#Servers Configuration Page
@app.route('/serverconfig')
def serverConfig():

    #check if user has a token in the cookies
    if not session.get("token"):
        return redirect("/")

    return render_template('serverConfig.html')

#Just A Test
@app.route('/sendMSG', methods= ["GET", "POST"])
def sendMSG():
    #check if user has a token in the cookies
    if not session.get("token"):
        return redirect("/")

    if request.method == 'GET':
        return "Return Method GET"
    
    text = request.form['text']

    url = "http://localhost:3000/send-message/"
    data = {
        'message': text,
        'channel' : '1174180918118854706',
        }

    res = requests.post(url, data)
    print(res.text)
    return render_template('serverConfig.html')


if __name__ == "__main__":
    app.run(debug=False)