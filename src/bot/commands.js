const logger = require('../utils/logger');
const { getUserStats } = require('./api');

async function handleCommand(message, username) {
  const [command, ...args] = message.slice(1).split(' ');

  switch (command.toLowerCase()) {
    case 'stats':
      try {
        const stats = await getUserStats(args[0] || username);
        return `Stats for ${stats.username}: PP: ${stats.pp}, Rank: #${stats.global_rank}`;
      } catch (error) {
        logger.error(`Error fetching stats for ${args[0] || username}: ${error.message}`);
        return 'Failed to fetch stats. Please try again later.';
      }
    case 'help':
      return 'Available commands: $stats [username], $help';
    default:
      return 'Unknown command. Type $help for available commands.';
  }
}

module.exports = { handleCommand };
