from google.appengine.ext import db
from google.appengine.ext import webapp
from db_fact import *
from db_fantasy import *
from db_general import *
import json
import datetime


class AllServer(webapp.RequestHandler):
  """Handles request for all constant application data entities"""
  
  def get(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/all/country'):
      self._get_all_country()
    if self.request.path.__eq__('/all/club'):
      self._get_all_club()
    if self.request.path.__eq__('/all/player'):
      self._get_all_player()
    if self.request.path.__eq__('/all/user'):
      self._get_all_user()
      
  def _get_all_country(self):
#    print 'check'
    country2return = []
    for country in Country.all():
      item = {'key' : str(country.key()),
              'country_name' : country.name}
      country2return.append(item)
    self.response.out.write(json.write(country2return))
    
  def _get_all_club(self):
    club2return = []
    for club in Club.all():
      item = {'key' : str(club.key()),
              'name' : club.name,
              'owner' : club.owner,
              'captain_name' : club.captain_name,
              'city' : club.city,
              'matches_total' : club.matches_total,
              'matches_won' : club.matches_won,
              'matches_lost' : club.matches_lost,
              'matches_tie' : club.matches_tie,
              'matches_cancelled' : club.matches_cancelled,
              'highest_score' : club.highest_score,
              'avg_score' : club.avg_score,
              'avg_opp_score' : club.avg_opp_score,
              'short_name' : club.short_name}
      club2return.append(item)
    self.response.out.write(json.write(club2return))
    
  def _get_all_player(self):
    player2return = []
    for player in Player.all():
      item = {'key' : str(player.key()),
              'name' : player.name,
              'type' : player.type,
              'country_key' : str(player.country.key()),
              'club_key' : str(player.club.key()),
              'dob' : player.dob.strftime("%d %B, %Y"),
              'age' : player.age,
              'battype' : player.battype,
              'bowltype' : player.bowltype,
              'status' : player.status,
              'price' : player.price,
              'country_name' : player.country_name,
              'club_name' : player.club_name,}
      player2return.append(item)
    self.response.out.write(json.write(player2return))
    
  def _get_all_user(self):
    user2return = []
    for user in User.all():
      item = {'key' : str(user.key()),
              'userid' : user.id}
      user2return.append(item)
    self.response.out.write(json.write(user2return))
