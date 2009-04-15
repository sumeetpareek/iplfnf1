from db_fact import *
from db_fantasy import *
from db_general import *
from google.appengine.ext import webapp


class DummyServer(webapp.RequestHandler):
  """Handles requests to /admin URLs and delegates to the Admin class."""
 
  def get(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/data/dummy_and_update'):
      self._gen_user()
      self._gen_fact()
      self._gen_fact_player()
      self._gen_fact_club()
      self._gen_fact_vote()
      self._update_age()
      self._update_clubref()
      self._update_countryref()

  def _gen_user(self):
    for user in User.all():
      user.delete()
    count_user =1
    while(count_user<21):
      user = User()
      user.id = "user"+str(count_user)
      user.orkut = True
      user.facebook = False
      user.total_facts_points = 10+count_user
      user.total_fantasy_points = 100+count_user
      count_user+=1
      user.put()
    self.response.out.write('deleted and recreated all user data')
    
  def _gen_fact(self):
    for fact in Fact.all():
      fact.delete()
    count_fact =1
    while(count_fact<21):
      fact = Fact()
      query = db.Query(User).filter('id =', 'user'+str(count_fact%11))
      user = query.get()
      fact.creator = user
      fact.content = "this is fact number -- "+str(count_fact)
      fact.total_vote_up = count_fact
      fact.total_vote_down = 20-count_fact
      count_fact+=1
      fact.put()
    self.response.out.write('deleted and recreated all fact data')
    
  def _gen_fact_player(self):
    count_fp =0
    query = db.Query(Fact)
    flist = query.fetch(20, 0)
    query = db.Query(Player)
    plist = query.fetch(20, 0)
    for fact in flist:
      player=plist[count_fp]
      pkey = player.key()
      setattr(fact, str(pkey), True)
      count_fp+=1
      fact.put()
    self.response.out.write('all facts are now tagged with players')
    
  def _gen_fact_club(self):
    count_fc =0
    query = db.Query(Fact)
    flist = query.fetch(20, 0)
    query = db.Query(Club)
    clist = query.fetch(20, 0)
    for fact in flist:
      club=clist[count_fc%8]
      ckey = club.key()
      setattr(fact, str(ckey), True)
      count_fc+=1
      fact.put()
    self.response.out.write('all facts are now tagged with clubs')
    
  def _gen_fact_vote(self):
    count_fvf =0
    count_fvu =0
    query = db.Query(Fact)
    flist = query.fetch(20, 0)
    query = db.Query(User)
    ulist = query.fetch(20, 0)
    for f in flist:
      count_fvu = 0
      total_up = f.total_vote_up
      total_down = f.total_vote_down
      while(count_fvu<20):
        u = ulist[count_fvu]
        if(count_fvu<=count_fvf):
          v = 1
          total_up+=1
        else:
          v=-1
          total_down+=1
        f.total_vote_up = total_up
        f.total_vote_down = total_down
        setattr(f, str(u.key()), v)
        count_fvu+=1
        f.put()
      count_fvf+=1
    self.response.out.write('all facts have now been voted upon')
    
  def _update_countryref(self):
    for player in Player.all():
      if (player.country == None):
        query = Country.all()
        query.filter('name =', player.country_name)
        cref = query.get()
        player.country = cref
        player.put()
    self.response.out.write('player country set')
    
  def _update_clubref(self):
    for player in Player.all():
      if (player.club == None):
        query = Club.all()
        query.filter('name =', player.club_name)
        cref = query.get()
        player.club = cref
        player.put()
    self.response.out.write('player club set')
    
  def _update_age(self):
    for player in Player.all():
      if(player.age == 0 or player.age == None):
        pda1 = player.dob.year
        pda = datetime.date.today()
        player.age = pda.year - pda1 
        player.put()
    self.response.out.write('player age set')