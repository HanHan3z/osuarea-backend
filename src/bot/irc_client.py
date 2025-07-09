import irc.bot
import irc.strings
import logging
import threading
import time
from typing import Dict

# Commands
from comm.pop import PopCommand
from comm.play import PlayCommand

# API
from api.osu_api import OsuApi

class OsuArenaBot(irc.bot.SingleServerIRCBot):
  def __init__(self, username, password, api_config: Dict[str, str]):
    server = 'irc.ppy.sh'
    port = 6667
    
    super().__init__([(server, port)], username, username)
    self.password = password
    self.logger = logging.getLogger(__name__)
    
    if not isinstance(api_config, dict) or 'client_id' not in api_config or 'client_secret' not in api_config:
      raise ValueError("API configuration must be a dictionary with 'client_id' and 'client_secret'.")
    self.api = OsuApi(api_config['client_id'], api_config['client_secret'])
    
    self.comm = {
      '!pop': PopCommand(),
      '!p': PlayCommand(),
      '!play': PlayCommand(),
    }
    
    self.cooldowns = {}
    self.cooldown_duration = 5
    self.cooldown_lock = threading.Lock()
    
  def on_welcome(self, connection, event):
    connection.privmsg('NickServ', f'IDENTIFY {self.password}')
    self.logger.info(f'Connected to Bancho IRC server as {self.connection.get_nickname()}')
    
  def on_privmsg(self, connection, event):
    msg = event.arguments[0].strip()
    sender = event.source.nick
    self.logger.info(f'Received private message from {sender}: {msg}')
    
    comm_name = msg.lower().split()[0] if msg else ''
    if comm_name in self.comm:
      current_time = time.time()
      with self.cooldown_lock:
        last_used = self.cooldowns.get(f'{sender}:{comm_name}', 0)
        if current_time - last_used < self.cooldown_duration:
          remaining = int(self.cooldown_duration - (current_time - last_used))
          connection.privmsg(sender, f'Please wait {remaining} seconds before using this command again.')
          self.logger.info(f'Command {comm_name} is on cooldown for {sender}. Remaining time: {remaining} seconds.')
          return
        self.cooldowns[f'{sender}:{comm_name}'] = current_time      
      response = self.comm[comm_name].execute(sender, msg)
      if response:
        connection.privmsg(sender, response)
        self.logger.info(f'Sent response to {sender}: {response}')
