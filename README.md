# IRC News Bot

This is an IRC bot that fetches and sends breaking news headlines from a news API to a specified IRC channel.

VISIT US @ IRC.TWISTEDNET.ORG CHANNEL #DEV

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Libraries](#libraries)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
  - [Using Screen](#using-screen)
- [License](#license)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.6+
- `pip3` (Python package installer)
- `screen` (Terminal multiplexer for Unix)

### Libraries

Install the necessary Python libraries using `pip3`. Run the following command:

```bash
pip3 install irc requests jaraco.stream
```

## Configuration

Edit the bot's configuration directly in the script to set the IRC server, port, channel, bot nickname, and news API URL. Replace `put_API_key_here` with your actual API key.

```python
server_address = "irc.twistednet.org"
port = 6697
channel = "#dev"
botnick = "n"

news_api = "https://newsapi.org/v2/top-headlines?country=us&apiKey=put_API_key_here"
```

## Running the Bot

To run the bot, execute the script using Python:

```bash
python3 ircnewsbot2.0.py
```

### Using Screen

To run the bot in the background and keep it running after closing your terminal, use `screen`. Follow these steps:

1. Start a new screen session:

    ```bash
    screen -S irc-news-bot
    ```

2. Run the bot within the screen session:

    ```bash
    python ircnewsbot2.0.py
    ```

3. Detach from the screen session to leave the bot running:

    Press `Ctrl + A`, then `D`.

4. To reattach to the screen session later, use:

    ```bash
    screen -r irc-news-bot
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
