import yaml
import logging
from bot.irc_client import OsuArenaBot

def load_config():
  try:
    with open('config/config.yaml', 'r') as f:
      config = yaml.safe_load(f)
      if not config or 'irc' not in config or 'api' not in config:
        raise ValueError("Invalid configuration file format.")
      return config
  except FileNotFoundError:
    logging.error("Configuration file not found. Please ensure 'config/config.yaml' exists.")
    raise
  
def main():
  logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
      logging.FileHandler('data/logs/bot.log'),
      logging.StreamHandler(),
    ],
  )
  
  try:
    config = load_config()
    api_config = config['api']
    irc_config = config['irc']
  except Exception as e:
    logging.error(f"Failed to load configuration: {str(e)}")
    return
  
  bot = OsuArenaBot(
    username = irc_config['irc_config'],
    password = irc_config['irc_password'],
    api_config = api_config,
  )

  bot.start()
  
if __name__ == '__main__':
  main()
