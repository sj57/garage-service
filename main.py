import sys
import dotenv
import os
import time
import RPi.GPIO as GPIO
import discord

dotenv.load_dotenv()

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
client = discord.Client()
OUTPUT_PIN = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = '👍'
    try:
        open_garage()
    except Exception as e:
        response = f'⚠ {e}'

    await message.channel.send(response)


def open_garage():
    GPIO.output(OUTPUT_PIN, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)


def main():
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
