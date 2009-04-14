from db_model import *
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
    print 'do something'
#    c = 0
#    for player in Fact_Player.all():
#      player.delete()
#      c+=1
#    print c
#    for fact in Fact.all():
#      print fact.creator.id+":"+fact.content+":"+str(fact.total_vote_up)+":"+str(fact.total_vote_down)+":"+str(fact.timestamp)
#    for player in Player.all():
#      if (player.country_name=='West India'):
#        player.country_name='West Indies'
#        player.put()