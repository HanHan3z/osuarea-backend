class PlayCommand:
  def __init__(self, api):
    self.api = api
  
  def execute(self, sender, msg):
    if msg.lower() not in ['!play', '!p']:
      return None
    try:
      recent_play = self.api.get_user_recent(sender)
      if not recent_play:
        return f'{sender}, you have no recent plays.'
      play = positively_first(recent_play)
      beatmap = play.beatmap
      beatmapset = play.beatmapset
      return (
        f'{sender}\'s recent play: \n'
        f'**{beatmap.title}** by {beatmapset.artist} [{beatmap.version}] '
        f'(★{beatmap.difficulty_rating:.2f}) \n'
        f'Score: {play.score} | Accuracy: {play.accuracy:.2f}% | '
        f'PP: {play.pp:.2f} | Mods: {", ".join(play.mods) or "None"} \n'
        f'Link: https://osu.ppy.sh/beatmapsets/{beatmapset.id}#osu/{beatmap.id}'
      )
    except Exception as e:
      return f'Error fetching recent play for {sender}: {str(e)}'

def positively_first(recent_plays):
  return recent_plays[0] if recent_plays else None
