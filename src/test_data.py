from db_model import Player
from google.appengine.ext import webapp

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
            player.delete()
        player = Player()
        player.name = 'sumeet'
        player.type = 'bat'
        player.put()  