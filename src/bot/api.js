const osu = require('node-osu');
const axios = require('axios');
const logger = require('../utils/logger');
const { apiClientId, apiClientSecret } = require('../utils/config');

const osuApi = new osu.Api(apiClientId, {
  clientSecret: apiClientSecret,
  baseUrl: 'https://osu.ppy.sh/api/v2',
});

async function getAccessToken() {
  try {
    const response = await axios.post('https://osu.ppy.sh/oauth/token', {
      grant_type: 'client_credentials',
      client_id: apiClientId,
      client_secret: apiClientSecret,
      scope: 'public',
    });
    return response.data.access_token;
  } catch (error) {
    logger.error(`Failed to get access token: ${error.message}`);
    throw error;
  }
}

async function getUserStats(username) {
  try {
    const token = await getAccessToken();
    const response = await axios.get(`https://osu.ppy.sh/api/v2/users/${username}/osu`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return {
      username: response.data.username,
      pp: response.data.statistics.pp,
      global_rank: response.data.statistics.global_rank,
    };
  } catch (error) {
    logger.error(`Failed to fetch user stats for ${username}: ${error.message}`);
    throw error;
  }
}

module.exports = { getUserStats };
