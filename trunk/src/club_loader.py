import datetime
from google.appengine.ext import db


class ClubLoader(Loader):
  def __init__(self):
    Loader.__init__(self, 'Club',
                    [('name', str),
                     ('type', str),                     
                     ('dob', lambda x: datetime.datetime.strptime(x, '%m/%d/%Y').date()),
                     ('age', int),
                     ('battype', str),
                     ('bowltype', str),
                     ('status', int),
                     ('price', float)
                     ])
    