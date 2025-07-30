const OsuBot = require('./bot/irc');
const logger = require('./utils/logger');

async function main() {
  logger.info('Starting osu! IRC bot...');
  const bot = new OsuBot();
  await bot.start();
}

main().catch((error) => {
  logger.error(`Bot crashed: ${error.message}`);
  process.exit(1);
});
