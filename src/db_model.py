from google.appengine.ext import db

class Player(db.Model):
    name = db.StringProperty()
    type = db.StringProperty()
    country = db.ReferenceProperty(Country) #TODO
    club = db.ReferenceProperty(Club) #TODO
    dob = db.DateProperty()
    age = db.IntegerProperty()
    battype = db.StringProperty()
    bowltype = db.StringProperty()
    status = db.IntegerProperty()
    price = db.IntegerProperty()

class Club(db.Model):
    name = db.StringProperty()
    owner = db.StringProperty()
    city = db.StringProperty()
    total_matches = db.IntegerProperty()
    wins = db.IntegerProperty()
    losses = db.IntegerProperty()
    ties = db.IntegerProperty()
    canceled = db.IntegerProperty()
    short_code = db.StringProperty()
    
class Country(db.Model):
    name = db.StringProperty()

class User(db.Model):
    id = db.StringProperty()
    orkut = db.BooleanProperty()
    facebook = db.BooleanProperty()
    total_facts_points = db.IntegerProperty()
    total_fantasy_points = db.IntegerProperty()

class Fact(db.Model):
    creator = db.ReferenceProperty(User)
    content = db.TextProperty()
    total_vote_up = db.IntegerProperty()
    total_vote_down = db.IntegerProperty()
    timestamp = db.TimeProperty()

class Fact_Player(db.Model):
    fact = db.ReferenceProperty(Fact)
    player = db.ReferenceProperty(Player)
    
class Fact_Club(db.Model):
    fact = db.ReferenceProperty(Fact)
    club = db.ReferenceProperty(Club)
        
class Fact_Vote(db.Model):
    fact = db.ReferenceProperty(Fact)
    voter = db.ReferenceProperty(User)
    vote = db.IntegerProperty()
    timestamp = db.TimeProperty()
