# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
 
# OpenSocial Gifts imports
import test_data
import dummy
import all
import fact
 
# Map URLs to request handler classes
application = webapp.WSGIApplication([('/admin', test_data.AdminServer),
                                      ('/data/.*',dummy.DummyServer),
                                      ('/all/.*',all.AllServer),
                                      ('/fact/.*',fact.FactServer),
                                      ],
                                     debug=True)
 
# Fire it up!
wsgiref.handlers.CGIHandler().run(application) 