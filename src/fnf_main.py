# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
 
# OpenSocial Gifts imports
import test_data 
 
# Map URLs to request handler classes
application = webapp.WSGIApplication([('/admin', test_data.AdminServer)],
                                     debug=True)
 
# Fire it up!
wsgiref.handlers.CGIHandler().run(application)