from db_model import Player
from db_model import Club
from db_model import Country
from google.appengine.ext import webapp
from google.appengine.ext import db
import json

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
    print 'fuck '
    for player in Player.all():
      print player.name+":"+player.type+":"+player.club.name+":"+player.country.name+":"+str(player.age)+":"+str(player.status)+":"+str(player.price)
#    for player in Player.all():
#      if (player.country_name=='West India'):
#        player.country_name='West Indies'
#        player.put()