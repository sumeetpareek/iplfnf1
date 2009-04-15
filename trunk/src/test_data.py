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
    admin.initPlayer()
    self.response.out.write('db refreshed')

class Admin:
  """init the db"""

  def initPlayer(self):
    print 'do something'
#    v='agdpcGxmbmYxcgwLEgZQbGF5ZXIYEww'
#    q=db.Query(Fact).filter(v+' =', True)
#    r=q.get()
#    print json.write(r.dynamic_properties())
    c = 0
    for player in User.all():
      print player.id
      c+=1
    print c
#    for fact in Fact.all():
#      print fact.creator.id+":"+fact.content+":"+str(fact.total_vote_up)+":"+str(fact.total_vote_down)+":"+str(fact.timestamp)
#    for player in Player.all():
#      if (player.country_name=='West India'):
#        player.country_name='West Indies'
#        player.put()