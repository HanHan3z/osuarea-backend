const { BanchoClient } = require('bancho.js');
const logger = require('../utils/logger');
const { handleCommand } = require('./commands');
const { ircUsername, ircPassword } = require('../utils/config');

class OsuBot {
  constructor() {
    this.client = new BanchoClient({ username: ircUsername, password: ircPassword });
  }

  async start() {
    try {
      await this.client.connect();
      logger.info('Connected to osu! IRC server');
      
      this.client.on('PM', async (message) => {
        logger.info(`Received PM from ${message.user.ircUsername}: ${message.message}`);
        
        if (message.message.startsWith('$')) {
          const response = await handleCommand(message.message, message.user.ircUsername);
          if (response) {
            await message.user.sendMessage(response);
            logger.info(`Sent response to ${message.user.ircUsername}: ${response}`);
          }
        }
      });
    } catch (error) {
      logger.error(`Failed to connect to IRC: ${error.message}`);
    }
  }
}

module.exports = OsuBot;
