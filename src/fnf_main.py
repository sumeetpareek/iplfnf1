# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
 
# OpenSocial Gifts imports
import test_data
import dummy
import all
 
# Map URLs to request handler classes
application = webapp.WSGIApplication([('/admin', test_data.AdminServer),
                                      ('/data/.*',dummy.DummyServer),
                                      ('/all/.*',all.AllServer)
                                      ],
                                     debug=True)
 
# Fire it up!
wsgiref.handlers.CGIHandler().run(application) 