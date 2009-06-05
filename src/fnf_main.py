# Standard libraries
import wsgiref.handlers
 
# AppEngine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
 
from db_fact import *
from db_fantasy import *
from db_general import *
import test_data
import dummy
import all
import fact
import fantasy

def main():
  application = webapp.WSGIApplication([
    ('/admin', test_data.AdminServer),
    ('/data/.*',dummy.DummyServer),
    ('/all/.*',all.AllServer),
    ('/fact/.*',fact.FactServer),
    ('/fantasy/.*',fantasy.FantasyServer)], debug=True)
  run_wsgi_app(application)
 
# Fire it up!
if __name__ == '__main__':
  main()