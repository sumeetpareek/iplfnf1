from google.appengine.ext import db
from db_fantasy import *
from db_general import *
import datetime

class Fact(db.Expando):
    creator = db.ReferenceProperty(User)
    content = db.TextProperty()
    total_vote_up = db.IntegerProperty()
    total_vote_down = db.IntegerProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)
        
class Fact_Vote(db.Model):
    fact = db.ReferenceProperty(Fact)
    voter = db.ReferenceProperty(User)
    vote = db.IntegerProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)