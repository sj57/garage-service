# garage-service
A simple hack, to remotely open a garage. 

This code is a Discord bot that allows you to control a garage door using a Raspberry Pi. When the bot receives a message, it will attempt to open the garage door by triggering a low signal on the specified output pin for 1 second and then returning it to a high signal.

![PXL_20221226_122529600](https://user-images.githubusercontent.com/1287098/209539552-e18e0a60-ea62-4740-9198-f9a69701886a.jpg)


## Setup

1. Get a Raspberry pi and install a simple OS. I'm using Ubuntu
1. Connect the output pin specified in the `OUTPUT_PIN` variable to your garage door opener circuit

1. Create a Discord bot ([see this on how to create a bot](https://www.writebots.com/discord-bot-token/))

1. Clone the project somewhere 

1. Create a `.env` file in the root directory of the project and set the `DISCORD_TOKEN` environment variable to your Discord bot's token.
    ```env
    DISCORD_TOKEN=<discord bot token>
    ```

1. Run the script with `python3 main.py` and test by sending any message to the bot

1. Install as systemd service
    ```
    sudo nano /etc/systemd/system/garage.service
    ```
    add the content of the `garage.service` file to the file and save it
    ```
    sudo systemctl daemon-reload
    sudo systemctl enable garage
    sudo systemctl start garage
    ```

