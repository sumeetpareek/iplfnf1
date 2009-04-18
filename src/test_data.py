from db_fact import *
from db_fantasy import *
from db_general import *
from google.appengine.ext import webapp
from google.appengine.ext import db
import json

class AdminServer(webapp.RequestHandler):
  """Handles requests to /admin URLs and delegates to the Admin class."""
 
  def get(self):
    """Handle GET requests."""
    self.response.out.write('Welcome to the admin webapp')
    admin = Admin()
    admin.init()
    self.response.out.write('db refreshed')

class Admin:
  """init the db"""

  def init(self):
    for player in Player.all():
      print player.name
      if player.name == 'sumeet':
        player.delete()

    for user in User.all():
      if user.id == 'sumeet':
        user.delete()
      print user.id
      
#    for fact in Fact_Vote.all():
#      print fact.voter.id
#      print fact.fact.content
#      print fact.vote
#      print '--'