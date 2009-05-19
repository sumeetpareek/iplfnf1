from google.appengine.ext import db
import db_general
import datetime

### Uncomment loader classes to load data to local/remote datastore and then update all missing data
#
#
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