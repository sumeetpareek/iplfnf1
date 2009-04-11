# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
 
# OpenSocial Gifts imports
import test_data
import dummy
 
# Map URLs to request handler classes
application = webapp.WSGIApplication([('/admin', test_data.AdminServer),
                                      ('/data/dummy_user',dummy.dummyServer),
                                      ('/data/dummy_fact',dummy.dummyServer),
                                      ('/data/dummy_fact_player',dummy.dummyServer),
                                      ('/data/dummy_fact_club',dummy.dummyServer),
                                      ('/data/dummy_fact_vote',dummy.dummyServer),
                                      ('/data/player_update_age',dummy.dummyServer),
                                      ('/data/player_update_status',dummy.dummyServer),
                                      ('/data/player_update_clubref',dummy.dummyServer),
                                      ('/data/player_update_countryref',dummy.dummyServer)
                                      ],
                                     debug=True)
 
# Fire it up!
wsgiref.handlers.CGIHandler().run(application)