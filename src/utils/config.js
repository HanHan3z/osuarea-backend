const dotenv = require('dotenv');

dotenv.config();

module.exports = {
  ircUsername: process.env.OSU_IRC_USERNAME,
  ircPassword: process.env.OSU_IRC_PASSWORD,
  apiClientId: process.env.OSU_API_CLIENT_ID,
  apiClientSecret: process.env.OSU_API_CLIENT_SECRET,
};
