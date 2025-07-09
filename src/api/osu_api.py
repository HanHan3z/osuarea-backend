from ossapi import OssApi

class OsuApi:
  def __init__(self, client_id, client_secret):
    self.api = OssApi(client_id, client_secret)
    
  def get_user_recent(self, username):
    try:
      return self.api.user_scores(username, mode='osu', limit=1, type='recent')
    except Exception as e:
      raise Exception(f'Failed to fetch recent scores: {str(e)}')
