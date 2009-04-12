from db_model import *
from google.appengine.ext import webapp
import logging
import json
from db_model import Fact_Player
class factServer(webapp.RequestHandler):
   
  def get(self):
    logging.info("favorite_foods1 parameter is not found.")
    logging.debug("favorite_foods1 parameter is not found.")
    logging.error("favorite_foods1 parameter is not found.")
    self.response.out.write('''
    <html>
      <body>
        <form method="post" action="/test?user=user6&pg=1">
          <p><b>Welcome to Facts<b></p>
          <p>Favorite foods:</p>
          <select name="like">
            <option value="MostLiked">MostLiked</option>
            <option value="MostDisliked">MostDisliked</option>
            <option value="YouLiked">YouLiked</option>
            <option value="YouDisliked">YouDisliked</option>
            <option value="YourFrndLiked">YourFrndLiked</option>
            <option value="YourFrndDisliked">YourFrndDisliked</option>
            <option value="Latest" selected="selected">Latest</option>
          </select>
          <b>TAG Choice</b>
          <select name="tag">''')
    for player in Player.all():
      self.response.out.write('''  <option value="'''+str(player.key())+'''">'''+player.name+'''</option>''')
    for club in Club.all():
      self.response.out.write('''  <option value="'''+str(club.key())+'''">'''+club.name+'''</option>''')
    self.response.out.write(''' </select>
            <b>Country Choice</b>
          <select name="country">''')
    for country in Country.all():
      self.response.out.write('''  <option value="'''+country.name+'''">'''+country.name+'''</option>''')
    self.response.out.write(''' </select>
          <input type="submit">
       </form>
      </body>
    </html>
    ''')
    logging.info("favorite_foods1 parameter is not found.")    

  def post(self):
#    try:
        like = self.request.get("like")
        user = self.request.get("user")
        club = self.request.get("club", allow_multiple=True)
        country = self.request.get("country")
        pg = self.request.get("pg")
      
        #initialinzation
        q1 = None
        #Switch case
        if like=='MostLiked':
          q1 = db.Query(Fact_Player)
          names = self.request.get("player", allow_multiple=True)
          player_keys = []
          for name in names:
            item = db.Key(name)
            player_keys.append(item)
#          print player_keys
          q1.filter('player IN', player_keys)
          results = q1.fetch(1000,0)
          fids = []
          print 'fuck'
          for result in results:
#            print result
            item = result.fact.key()
            fids.append(item)
          print fids
          q2 = db.Query(Fact)
          q2.filter('__key__ IN',fids)
          result2 = q2.fetch(10,0)
          for r2 in result2:
            print r2.content
        elif like=='MostDisliked':
          q1 = db.Query(Fact).order('-total_vote_down')
        elif like=='YouLiked':    
          q1 = db.Query(Fact).order('-total_vote_up').filter('creator = ', userRef)
        elif like=='YouDisliked':
          q1 = db.Query(Fact).order('-total_vote_down').filter('creator = ', userRef)
        elif like=='YourFrndLiked':
          q1 = db.Query(Fact).order('-total_vote_up').filter('user = ', userRef)
          print q1.get()
        elif like=='YourFrndDisliked':
          q1 = db.Query(Fact).order('-total_vote_down').filter('user = ', userRef)
        elif like=='Latest':
          tag = self.request.get("tag")
          tag_key = db.Key(tag)
          if (tag_key.kind() == 'Player'):
            myq = db.Query(Fact_Player)
            myq.filter('player =',tag_key)
          elif (tag_key.kind() == 'Club'):
            myq = db.Query(Fact_Club)
            myq.filter('club =',tag_key)
          myq.order('-timestamp')
          result = myq.fetch(10,(int(pg)-1)*10)
#          print "ven k"
#          for r in result:
#            print r.fact.content
        
        else:
          q1 = None
        #execution of resultant query
        
        facts2return = []
        for val in result


#    except:
#      self.response.out.write('all most like fact data')
