from google.appengine.ext import db
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
    
class Match(db.Model):
    stadium = db.StringProperty()
    city = db.StringProperty()
    start_time = db.DateTimeProperty()
    team_one = db.ReferenceProperty(Club,collection_name="match_club_one")
    team_two = db.ReferenceProperty(Club,collection_name="match_club_two")
    team_one_name = db.StringProperty()
    team_two_name = db.StringProperty()
    
## Uncomment loader classes to load data to local/remote datastore and then update all missing data


#class PlayerLoader(Loader):
#    def __init__(self):
#      Loader.__init__(self, 'Player',
#                    [('name', str),
#                     ('dob', lambda x: datetime.datetime.strptime(x, '%m/%d/%y').date()),
#                     ('country_name', str),
#                     ('battype', str),
#                     ('bowltype', str),
#                     ('type', str),
#                     ('club_name', str),
#                     ('status', int),
#                     ('price', float),
#                     ])
#      
#class CountryLoader(Loader):
#  def __init__(self):
#    Loader.__init__(self, 'Country',
#                    [('name', str),
#                     ('misc', str)
#                     ])
#
#class ClubLoader(Loader):
#  def __init__(self):
#    Loader.__init__(self, 'Club',
#                    [('name', str),
#                     ('city', str),
#                     ('short_name', str),
#                     ('captain_name', str),
#                     ('owner', str),
#                     ('matches_total', int),
#                     ('matches_won', int),
#                     ('matches_lost', int),
#                     ('matches_tie', int),
#                     ('matches_cancelled', int),
#                     ('highest_score', int),
#                     ('avg_score', float),
#                     ('avg_opp_score', float),
#                     ])
#    
#class MatchLoader(Loader):
#    def __init__(self):
#      Loader.__init__(self, 'Match',
#                    [('start_time', lambda x: datetime.datetime.strptime(x, '%d-%B-%Y:%I %p')),
#                     ('city', str),
#                     ('team_one_name', str),
#                     ('team_two_name', str),
#                     ])