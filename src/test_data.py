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
    for club in Club.all():
      print club.short_name
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
#    for club in Club.all():
#      print club.name
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