from google.appengine.ext import db
from db_fact import *
from db_fantasy import *
import datetime

class Club(db.Model):
    name = db.StringProperty()
    owner = db.StringProperty()
    captain_name = db.StringProperty()    
    city = db.StringProperty()
    matches_total = db.IntegerProperty()
    matches_won = db.IntegerProperty()
    matches_lost = db.IntegerProperty()
    matches_tie = db.IntegerProperty()
    matches_cancelled = db.IntegerProperty()
    highest_score = db.IntegerProperty()
    avg_score = db.FloatProperty()
    avg_opp_score = db.FloatProperty()
    short_name = db.StringProperty()
    
class Country(db.Model):
    name = db.StringProperty()
    misc = db.StringProperty()

class Player(db.Model):
    name = db.StringProperty()
    type = db.StringProperty()
    country = db.ReferenceProperty(Country) 
    club = db.ReferenceProperty(Club)
    dob = db.DateProperty()
    age = db.IntegerProperty()
    battype = db.StringProperty()
    bowltype = db.StringProperty()
    status = db.IntegerProperty()
    price = db.FloatProperty()
    country_name = db.StringProperty()
    club_name = db.StringProperty()

class User(db.Model):
    id = db.StringProperty()
    orkut = db.BooleanProperty()
    facebook = db.BooleanProperty()
    total_facts_points = db.IntegerProperty()
    total_fantasy_points = db.IntegerProperty()
