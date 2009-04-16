# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
 
from db_fact import *
from db_fantasy import *
from db_general import *
import test_data
import dummy
import all
import fact
import fantasy
 
# Map URLs to request handler classes
application = webapp.WSGIApplication([('/admin', test_data.AdminServer),
                                      ('/data/.*',dummy.DummyServer),
                                      ('/all/.*',all.AllServer),
                                      ('/fact/.*',fact.FactServer),
                                      ('/fantasy/.*',fantasy.FantasyServer),
                                      ],
                                     debug=True)
 
# Fire it up!
wsgiref.handlers.CGIHandler().run(application) 