import datetime
from google.appengine.ext import db

class PlayerLoader(Loader):
  def __init__(self):
    Loader.__init__(self, 'Player',
                    [('name', str),
                     ('type', str),
                     ('country', str),
                     ('club', str),
                     ('dob', lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
                     ('age', int),
                     ('battype', str),
                     ('bowltype', str),
                     ('status', int),
                     ('price', float)
                     ])