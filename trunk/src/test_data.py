from db_model import Player
from db_model import Club
from db_model import Country
from google.appengine.ext import webapp
from google.appengine.ext import db

class AdminServer(webapp.RequestHandler):
  """Handles requests to /admin URLs and delegates to the Admin class."""
 
  def get(self):
    """Handle GET requests."""
    self.response.out.write('Welcome to the admin webapp')
    admin = Admin()
    admin.initPlayer()
    self.response.out.write('db refreshed')

class Admin:
    """init the db"""
    
    def initPlayer(self):
        for player in Player.all():
          result =  db.GqlQuery("SELECT * FROM Club WHERE name = :cname",cname=player.club_name)
          pclub = result.fetch(1, 0)
          player.club = pclub.key()
          player.put()