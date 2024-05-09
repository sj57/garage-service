import os
import sys
import dotenv
import time
import RPi.GPIO as GPIO
import discord
from logging.handlers import RotatingFileHandler
import logging

dotenv.load_dotenv()

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
client = discord.Client()
OUTPUT_PIN = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))


def init_logging(log_file_path=None, max_file_size_bytes=5000000, backups=10, file_level=logging.DEBUG, stdout_level=logging.INFO, disable_noisy_loggers=True):
    handlers = []
    handler = logging.StreamHandler()
    handler.setLevel(stdout_level)
    handlers.append(handler)

    if log_file_path:
        handler = RotatingFileHandler(log_file_path, maxBytes=max_file_size_bytes, backupCount=backups, encoding='utf-8')
        handler.setLevel(file_level)
        handlers.append(handler)

    if disable_noisy_loggers:
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("backoff").setLevel(logging.WARNING)
        logging.getLogger("chardet").setLevel(logging.WARNING)
        logging.getLogger("chardet.charsetprober").setLevel(logging.WARNING)
        logging.getLogger("chardet.universaldetector").setLevel(logging.WARNING)

    logging.basicConfig(handlers=handlers,
                        level=min(file_level, stdout_level),
                        format='%(asctime)s %(levelname)s - %(message)s')


# @client.event
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
    time.sleep(0.8)
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)


def main():
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    client.run(DISCORD_TOKEN)


if __name__ == '__main__':
    try:
        log_dir_path = os.path.join(SCRIPT_DIR, 'logs')
        os.makedirs(log_dir_path, exist_ok=True)
        log_file_name = 'service.log'
        log_file_path = os.path.join(log_dir_path, log_file_name)
        init_logging(log_file_path=log_file_path)
        logging.info('Starting garage door opener...')
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception(f'Error: {e}')
    finally:
        GPIO.cleanup()
        logging.info('Garage door opener stopped.')
