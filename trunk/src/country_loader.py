from google.appengine.ext import db

class CountryLoader(Loader):
  def __init__(self):
    Loader.__init__(self, 'Country',
                    [('name', str)
                     ])
    