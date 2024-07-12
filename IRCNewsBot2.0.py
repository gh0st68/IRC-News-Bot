import irc.client
import requests
import json
import threading
import time
import ssl
from jaraco.stream import buffer
import traceback

irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer

server_address = "127.0.0.1"
port = 6697
channel = "#Twisted"
botnick = "n"

news_api = "https://newsapi.org/v2/top-headlines?country=us&apiKey=put_API_key_here"

def send_news(connection):
    recent_headlines = []
    print("News fetching thread started.")
    while True:
        try:
            print("Fetching news from API...")
            response = requests.get(news_api, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data["status"] == "ok" and data["articles"]:
                headline = data["articles"][0]["title"]
                print(f"Received headline: {headline}")
                if headline not in recent_headlines:
                    connection.privmsg(channel, f"Breaking News: {headline}")
                    recent_headlines.append(headline)
                    print("Headline sent to IRC channel.")
                    if len(recent_headlines) > 100:
                        recent_headlines.pop(0)
                        print("Old headlines removed from the list.")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            traceback.print_exc()
            print("Sleeping for 60 seconds before retrying...")
            time.sleep(14400)
        except Exception as e:
            print(f"General error: {str(e)}")
            traceback.print_exc()
            print("Sleeping for 60 seconds before retrying...")
            time.sleep(60)
        else:
            print("Operation successful. Waiting for next update cycle.")
            time.sleep(60)

def on_welcome(connection, event):
    print("Connected to IRC server. Joining channel...")
    if irc.client.is_channel(channel):
        connection.join(channel)
        print(f"Joined channel: {channel}")
        threading.Thread(target=send_news, args=(connection,)).start()

def on_disconnect(connection, event):
    print("Disconnected from IRC server. Attempting to reconnect...")
    while True:
        try:
            connection.reconnect()
        except irc.client.ServerConnectionError as e:
            print(f"Reconnection failed: {str(e)}")
            print("Sleeping for 60 seconds before retrying...")
            time.sleep(60)
        else:
            print("Reconnected successfully.")
            break

client = irc.client.Reactor()

try:
    ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
    server = client.server()
    server.buffer_class = buffer.LenientDecodingLineBuffer
    connection = server.connect(server_address, port, botnick, connect_factory=ssl_factory)
    print(f"Connected to IRC server at {server_address}:{port} as {botnick}.")
except irc.client.ServerConnectionError as x:
    print(f"Failed to connect to IRC server: {x}")
    raise SystemExit(1)

connection.add_global_handler("welcome", on_welcome)
connection.add_global_handler("disconnect", on_disconnect)

print("Starting the IRC client processing loop.")
client.process_forever()
