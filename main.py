from quart import Quart, render_template, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
import requests

app = Quart(__name__)
app.config["SECRET_KEY"] = "test123"
app.config["DISCORD_CLIENT_ID"] = 1170221058314473543
app.config["DISCORD_CLIENT_SECRET"] = "Y-1vMj5tLtGPgIWnJBg6vARe7pthkKhC"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
	return await render_template("index.html")

@app.route("/login")
async def login():
	return await discord.create_session()

@app.route("/send-message")
async def sendMSG():
	url = 'http://localhost:3000/send-message'
	payload = {'message': 'Hello World!'}
	x = requests.post(url, json=payload)
	print(x.text)
	return "YOU KNOW IS NO THE SAME AT IS WAS"


@app.route("/callback")
async def callback():
	try:
		await discord.callback()
	except:
		return redirect(url_for("login"))

	user = await discord.fetch_user()
	return f"{user.name}"


if __name__ == "__main__":
	app.run(debug=True)