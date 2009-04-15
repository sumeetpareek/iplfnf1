from db_general import *
from db_fact import *
from db_fantasy import *
from google.appengine.ext.db import Key

from google.appengine.ext import webapp
import logging
import json

class FantasyServer(webapp.RequestHandler):
   
  def post(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/fantasy/get'):
      self._fan_get()
    if self.request.path.__eq__('/fantasy/set'):
      self._fan_set()
          
  def _fan_set(self):

    for team in User_Team.all():
      team.delete()
    team_creator = self.request.get("userid")
    req_players = self.request.get("team_players", allow_multiple=True)
    team_creator_entity = db.Query(User).filter('id =', team_creator).get()
    
    new_team = User_Team()
    new_team.creator = team_creator
    i = 1
    for player in req_players:
     setattr(new_team, "player_"+str(i), Key(player))
     i = i+1  
    new_team.name = "VenkyX1"
    new_team.put()
    
    if new_team.is_saved():
      print 'OK'
    else:
      print 'FAIL'
    
    for team in User_Team.all():
      print team.name
      print team.player_1
      print team.player_4