###The bot grabs breaking news headlines and sends them to a specified IRC channel##
##The bot will randomly send them to IRC as they show up on the inerwebz##
##Register for a free api at https://newsapi.org ##
## add api key where it says news_api = ##
##visit us irc.twistednet.org
#Made with endoplasmic materials##
##KEEP IT SALTY##
#-G


import irc.client
import requests
import json
import threading
import time
import ssl

# IRC server configuration
server = "irc.twistednet.org"
port = 6697  # Default IRC SSL port
channel = "#dev"
botnick = "newsBot"

# News API configuration
news_api = "https://newsapi.org/v2/top-headlines?country=us&apiKey=PUT-YOUR-API-KEY-HERE"

# Function to periodically fetch and send news headlines
def send_news(connection):
    last_headline = None

    while True:
        response = requests.get(news_api)
        data = response.json()

        if data["status"] == "ok" and data["articles"]:
            headline = data["articles"][0]["title"]

            if headline != last_headline:
                connection.privmsg(channel, f"Breaking News: {headline}")
                last_headline = headline

        time.sleep(60)  # Check for new headlines every minute

# Function to handle the 'welcome' event
def on_welcome(connection, event):
    if irc.client.is_channel(channel):
        connection.join(channel)
        threading.Thread(target=send_news, args=(connection,)).start()

# Function to handle the 'disconnect' event
def on_disconnect(connection, event):
    while True:
        try:
            connection.reconnect()
        except irc.client.ServerConnectionError:
            time.sleep(60)  # Wait a minute before trying again
        else:
            break

# Create an IRC client
client = irc.client.Reactor()

try:
    ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
    connection = client.server().connect(server, port, botnick, connect_factory=ssl_factory)
except irc.client.ServerConnectionError as x:
    print(x)
    raise SystemExit(1)

connection.add_global_handler("welcome", on_welcome)
connection.add_global_handler("disconnect", on_disconnect)

# Start the IRC client
client.process_forever()
