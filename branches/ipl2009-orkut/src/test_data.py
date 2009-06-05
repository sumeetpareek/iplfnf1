from db_fact import *
from db_fantasy import *
from db_general import *
from google.appengine.ext import webapp
from google.appengine.ext import db
import json
import datetime

class AdminServer(webapp.RequestHandler):
  """Handles requests to /admin URLs and delegates to the Admin class."""
 
  def get(self):
    """Handle GET requests."""
    self.response.out.write('This is test page')
    admin = Admin()
    admin.init()
    self.response.out.write('db refreshed')

class Admin:
  """init the db"""

  def init(self):
    print 'hi'
    count = 1
    for fact in Fact.all():
      print str(count) + '=='
      print fact.content + '=='
      print str(fact.total_vote_up) + '--'
      print str(fact.total_vote_down)+ '--'
      print '<br>'
      count += 1

#    for club in Club.all():
#      print club.name
#    for country in Country.all():
#      print country.name
#    count = 1
#    for player in Player.all():
#      print str(count) + '--'
#      print player.name + '--'
#      print str(player.age) + '--'
#      print player.club.name + '--'
#      print player.country.name + '--<br>'
#      count += 1
    
#
#    for user in User.all():
#      if user.id == 'sumeet':
#        user.delete()
#      print user.id
#
#    for match in Match.all():
#      if match.team_one is not None and match.team_two is not None:
#          print match.team_one.name
#          print match.team_two.name
#          print '<><><><>'
#      else:
#          print match.team_one_name
#          print match.team_two_name
#          print '---'
#          
#    count = 0
#    for match in Match.all():
#      count +=1
#      print match.team_one_name
#      print match.team_two_name
#      print match.city
#      print match.start_time
#      print '---'
#    print 'total match=='+str(count)
#    for fact in Fact.all():
#      print fact.content
#      print fact.creator.id
#      print '--'