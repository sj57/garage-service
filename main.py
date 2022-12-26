import sys
import dotenv

sys.path.append('/home/ubuntu/.local/lib/python3.8/site-packages')

dotenv.load_dotenv()

import os
import time
import RPi.GPIO as GPIO
import discord

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
client = discord.Client()
OUTPUT_PIN = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)


@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = "פתחתי"
    try:
        open_garage()
    except Exception as e:
        response = str(e)

    await message.channel.send(response)


def open_garage():
    GPIO.output(OUTPUT_PIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)


def main():
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
