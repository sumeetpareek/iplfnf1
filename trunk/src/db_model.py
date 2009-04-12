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

class Fact(db.Model):
    creator = db.ReferenceProperty(User)
    content = db.TextProperty()
    total_vote_up = db.IntegerProperty()
    total_vote_down = db.IntegerProperty()
    timestamp = db.TimeProperty(auto_now_add=True)

class Fact_Player(db.Model):
    fact = db.ReferenceProperty(Fact)
    player = db.ReferenceProperty(Player)
    timestamp = db.TimeProperty(auto_now_add=True)
    
class Fact_Club(db.Model):
    fact = db.ReferenceProperty(Fact)
    club = db.ReferenceProperty(Club)
    timestamp = db.TimeProperty(auto_now_add=True)
        
class Fact_Vote(db.Model):
    fact = db.ReferenceProperty(Fact)
    voter = db.ReferenceProperty(User)
    vote = db.IntegerProperty()
    timestamp = db.TimeProperty(auto_now_add=True)
    
class Match(db.Model):
    stadium = db.StringProperty()
    city = db.StringProperty()
    start_time = db.TimeProperty()
    team_one = db.ReferenceProperty(Club,collection_name="match_club_one")
    team_two = db.ReferenceProperty(Club,collection_name="match_club_two")
    
class Match_Performance(db.Model):
    mid = db.ReferenceProperty(Match)
    pid = db.ReferenceProperty(Player)
    one = db.IntegerProperty()
    two = db.IntegerProperty()
    three = db.IntegerProperty()
    four = db.IntegerProperty()
    five = db.IntegerProperty()
    six = db.IntegerProperty()
    total_runs = db.IntegerProperty()
    balls_faced = db.IntegerProperty()
    balls_bowled = db.IntegerProperty()
    runs_conceived = db.IntegerProperty()
    wickets = db.IntegerProperty()
    maidens = db.IntegerProperty()
    catches = db.IntegerProperty()
    runouts = db.IntegerProperty()
    stumps = db.IntegerProperty()
    batting_points = db.IntegerProperty()
    bowling_points = db.IntegerProperty()
    feilding_points = db.IntegerProperty()

class User_Team(db.Model):
    user = db.ReferenceProperty()
    mid = db.ReferenceProperty(Match)
    name = db.StringProperty()
    created_at = db.TimeProperty()
    cost = db.IntegerProperty()
    total_points = db.IntegerProperty()
    player_1 = db.ReferenceProperty(Player,collection_name="user_team_player_1")
    player_2 = db.ReferenceProperty(Player,collection_name="user_team_player_2")
    player_3 = db.ReferenceProperty(Player,collection_name="user_team_player_3")
    player_4 = db.ReferenceProperty(Player,collection_name="user_team_player_4")
    player_5 = db.ReferenceProperty(Player,collection_name="user_team_player_5")
    player_6 = db.ReferenceProperty(Player,collection_name="user_team_player_6")
    player_7 = db.ReferenceProperty(Player,collection_name="user_team_player_7")
    player_8 = db.ReferenceProperty(Player,collection_name="user_team_player_8")
    player_9 = db.ReferenceProperty(Player,collection_name="user_team_player_9")
    player_10 = db.ReferenceProperty(Player,collection_name="user_team_player_10")
    player_11 = db.ReferenceProperty(Player,collection_name="user_team_player_11")


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