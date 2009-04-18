from google.appengine.ext import db
from db_fact import *
from db_general import *
import datetime

class Match(db.Model):
    stadium = db.StringProperty()
    city = db.StringProperty()
    start_time = db.DateTimeProperty()
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
    user = db.ReferenceProperty(User)
    mid = db.ReferenceProperty(Match)
    name = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
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


