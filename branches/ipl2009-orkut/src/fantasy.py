from db_general import *
from db_fact import *
from db_fantasy import *
from google.appengine.ext.db import Key

from google.appengine.ext import webapp
import logging
import json

class FantasyServer(webapp.RequestHandler):
   
  def get(self):
    if self.request.path.__eq__('/fantasy/put'):
      self._match_put()
      
  def post(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/fantasy/get'):
      self._fan_get()
    if self.request.path.__eq__('/fantasy/set'):
      self._fan_set()
    if self.request.path.__eq__('/fantasy/put'):
      self._match_put()
          
  def _fan_set(self):
    user_id = self.request.get("userid")
    user_q = db.Query(User).filter('id =', user_id)
    curr_user = user_q.get()
    curr_user_key = curr_user.key()
    userid = self.request.get("userid")
    req_players = self.request.get("team_players", allow_multiple=True)
    mid = self._get_match(datetime.datetime.today())
    print str(mid)+"is the mid"
    new_team = User_Team()
    new_team.user = curr_user_key
    i = 1
    for player in req_players:
     setattr(new_team, "player_"+str(i), Key(player))
     i = i+1  
    new_team.name = "VenkyX1"
    new_team.mid = mid
    new_team.put()
    
    if new_team.is_saved():
      print 'OK'
    else:
      print 'FAIL'
      
  def _fan_get(self):

    team2return = []
    # we get the user id and user key
    user_id = self.request.get("user_id")
    user_q = db.Query(User).filter('id =', user_id)
    curr_user = user_q.get()
    curr_user_key = curr_user.key()
       
    q = db.Query(User_Team)
    q.filter('user =',curr_user_key).order('-created_at')
    result = q.get()
    print result.name
    item = {'user' : str(curr_user_key),
              'mid' : str(result.mid.key()),
              'created_at' : str(result.created_at),
              'player_1' : result.player_1.name,
              'player_2' : result.player_2.name,
              'player_3' : result.player_3.name,
              'player_4' : result.player_4.name,
              'player_5' : result.player_5.name,
              'player_6' : result.player_6.name,
              'player_7' : result.player_7.name,
              'player_8' : result.player_8.name,
              'player_9' : result.player_9.name,
              'player_10' : result.player_10.name,
              'player_11' : result.player_11.name }
    team2return.append(item)
    self.response.out.write(json.write(team2return))
    
  def _get_match(self, time):
    query = db.Query(Match)
    query.filter('start_time <=',time).order('-start_time')
    result = query.get()
    return result.key()

  def _put_match_performance(self):
      
    match_perform = Match_Performance()
    
    mid = self.request.get("mid")
    match_perform.mid = Key(mid)
    pid = self.request.get("pid")
    match_perform.pidf = Key(pid)
    
    match_perform.one = self.request.get("one")
    match_perform.two = self.request.get("two")
    match_perform.three = self.request.get("three")
    match_perform.four = self.request.get("four")
    match_perform.five = self.request.get("five")
    match_perform.six = self.request.get("six")
    match_perform.balls_faced = self.request.get("balls_faced")
    
    total_runs = self._match_total_runs()
    match_perform.batting_points = self._match_total_batting_points()
        
    match_perform.balls_bowled = self.request.get("balls_bowled")
    match_perform.runs_conceived = self.request.get("runs_conceived")
    match_perform.wickets = self.request.get("wickets")
    match_perform.maidens = self.request.get("maidens")
    
    match_perform.bowling_points = self._match_total_bowling_points()
    
    match_perform.catches = self.request.get("catches")
    match_perform.runouts = self.request.get("runouts")
    match_perform.stumps = self.request.get("stumps")
        
    match_perform.feilding_points = self._match_total_fielding_points()
    
    match_perform.put()
  
    if match_perform.is_saved():
      print 'OK'
    else:
      print 'FAIL'

  def _match_total_runs(self):
    one = self.request.get("one")  
    two = self.request.get("two")
    three = self.request.get("three")
    four = self.request.get("four")
    five = self.request.get("five")
    six = self.request.get("six")
    
    total_runs = one + two + three + four + five + six
    return total_runs
  
  def _match_total_batting_points(self):
    one = self.request.get("one")  
    two = self.request.get("two")
    three = self.request.get("three")
    four = self.request.get("four")
    five = self.request.get("five")
    six = self.request.get("six")
    balls_faced = self.request.get("balls_faced")
    
    total_batting_poitns = (one * 2) + (two * 3) + (three * 4) + (four * 5) + (five * 6) + (six * 7) - (balls_faced * 2)
    return total_batting_poitns
  
  
  def _match_total_bowling_points(self):
    balls_bowled = self.request.get("balls_bowled")
    runs_conceived = self.request.get("runs_conceived")
    wickets = self.request.get("wickets")
    maidens = self.request.get("maidens")
    
    total_bowling_poitns = (balls_bowled * 2) + (runs_conceived * 3) + (wickets * 4) + (maidens * 5)
    return total_bowling_poitns
  
  
  def _match_total_fielding_points(self):
    catches = self.request.get("catches")
    runouts = self.request.get("runouts")
    stumps = self.request.get("stumps")
    
    total_fielding_poitns = (catches * 2) + (runouts * 3) + (stumps * 4)
    return total_fielding_poitns
  
  def _match_put(self):
    for match in Match.all():
      if match.start_time is None:
        match.delete()
#      print "hi venky:"
#      print match.matchno
#      print match.stadium
#      print str(match.key)
#    match = Match()
#    match.matchno = 3
#    match.stadium = "great hyderabad"
#    match.city = "hyderabad"
#    match.start_time = datetime.datetime.today()
#    match.put()
#    if match.is_saved():
#      print 'OK'
#    else:
#      print 'FAIL'

#  def _team_cost(self, teamref):
    