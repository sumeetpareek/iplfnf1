from db_general import *
from db_fact import *
from db_fantasy import *
from BeautifulSoup import BeautifulSoup

from google.appengine.ext import webapp
from google.appengine.ext.db import Key
import logging
import json

class FactServer(webapp.RequestHandler):
   
  def post(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/fact/get'):
      self._fact_get()
    if self.request.path.__eq__('/fact/set'):
      self._fact_set()
    if self.request.path.__eq__('/fact/vote'):
      self._fact_vote()
      
  def sanitize_html(self, value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name not in ['strong', 'em', 'p', 'ul', 'li', 'br', 'b']:
            tag.hidden = True
    return soup.renderContents()

  def _fact_get(self):
    fact2return = []
    # we get the user id and user key
    user_id = self.request.get("user_id")
    user_q = db.Query(User).filter('id =', user_id)
    curr_user = user_q.get()
    curr_user_key = curr_user.key()
    friend_ids = self.request.get("friend_ids", allow_multiple=True)
    fact_query = self.request.get("fact_query")
    fact_page = self.request.get("fact_page")
    # as there could be multiple comma separated values for fact_clubs and fact_players we create a list for them
    fact_clubs = self.request.get("fact_clubs", allow_multiple=True)
    fact_players = self.request.get("fact_players", allow_multiple=True)
    
    # create a query over the fact table and filter by the player and club tags in the request (thanks to expando class)
    q = db.Query(Fact)
    for fact_club in fact_clubs:
      q.filter(fact_club+ ' =', True)
    for fact_player in fact_players:
      q.filter(fact_player+ ' =', True)
    
    # filter the query further depending upon what is the criteria chosen by the app user, which is present in the request as 'fact_query' 
    if fact_query == 'latest':
      q.order('-timestamp')
    
    elif fact_query == 'most-liked':
      q.order('-total_vote_up')
    
    elif fact_query == 'most-disliked':
      q.order('-total_vote_down')
    
    elif fact_query == 'user-added':
      q.filter('creator =',curr_user_key).order('-timestamp')
    
    elif fact_query == 'friend-added':
      # fetch keys of all the friends by an "IN" query and create a list of such keys retrived
      friend_q = db.Query(User).filter('id IN', friend_ids)
      friend_r = friend_q.fetch()
      friend_key_list = []
      for friend in friend:
        friend_key_list.append(friend.key())
      q.filter('creator IN',friend_key_list).order('-timestamp')

    elif fact_query == 'user-liked':
      # we first retrive fact keys from Fact_Vote tables for those entities which the user voted +1
      vote_q = db.Query(Fact_Vote).filter('voter =', curr_user_key).filter('vote =', 1).order('-timestamp')
      vote_r = vote_q.fetch(10,(int(fact_page)-1)*10)
      # we create a list of the fact keys
      liked_list = []
      for vote_entity in vote_r:
        liked_list.append(vote_entity.fact.key())
      result = db.get(liked_list)

    elif fact_query == 'user-disliked':
      # we first retrive fact keys from Fact_Vote tables for those entities which the user voted -1
      vote_q = db.Query(Fact_Vote).filter('voter =', curr_user_key).filter('vote =', -1).order('-timestamp')
      vote_r = vote_q.fetch(10,(int(fact_page)-1)*10)
      # we create a list of the fact keys
      disliked_list = []
      for vote_entity in vote_r:
        disliked_list.append(vote_entity.fact.key())
      result = db.get(disliked_list)      
      
    # now we have the query ready so we fetch the results and return them in a "JSONed" list
    # since for user 'liked' and 'disliked phases result if already fetched, we do not do that again
    if fact_query != 'user-liked' and fact_query != 'user-disliked':
      result = q.fetch(10,(int(fact_page)-1)*10)
    for curr_fact in result:
      curr_user_vote = 0
      if db.Query(Fact_Vote).filter('voter =', curr_user_key).filter('fact =', curr_fact).get():
        curr_user_vote = db.Query(Fact_Vote).filter('voter =', curr_user_key).filter('fact =', curr_fact).get().vote 
      item = {'key' : str(curr_fact.key()),
              'content' : str(curr_fact.content),
              'timestamp' : curr_fact.timestamp.strftime('%I:%M%p ').lower() + curr_fact.timestamp.strftime('%b %d'),
              'creator' : str(curr_fact.creator.id),
              'tags' : curr_fact.dynamic_properties(),
              'curr_user_vote' : curr_user_vote,
              'voteups' : curr_fact.total_vote_up == None and '0' or curr_fact.total_vote_up,
              'votedowns' : curr_fact.total_vote_down == None and '0' or curr_fact.total_vote_down}
      fact2return.append(item)
    self.response.out.write(json.write(fact2return))
    
  def _fact_set(self):
    fact2return = []
    # we get the creator id
    fact_creator = self.request.get("fact_creator")
    fact_content = self.sanitize_html(self.request.get("fact_content"))
    # as there could be multiple comma separated values for fact_clubs and fact_players we create a list for them
    fact_clubs = self.request.get("fact_clubs").split(",")
    fact_players = self.request.get("fact_players").split(",")
    fact_creator_entity = db.Query(User).filter('id =', fact_creator).get()
    
    # we create a new fact instance, add the attributes and put() it
    new_fact = Fact()
    new_fact.creator = fact_creator_entity
    new_fact.content = fact_content
    for fact_club in fact_clubs:
      if fact_club:
        setattr(new_fact, fact_club, True)
    for fact_player in fact_players:
      if fact_player:
        setattr(new_fact, fact_player, True)
    new_fact.put()
    if new_fact.is_saved():
      item = {'status' : 'OK',
        'key' : str(new_fact.key()),
        'content' : str(new_fact.content),
        'timestamp' : new_fact.timestamp.strftime('%I:%M%p ').lower() + new_fact.timestamp.strftime('%b %d'),
        'creator' : str(new_fact.creator.id),
        'tags' : new_fact.dynamic_properties(),
        'new_user_vote' : 0,
        'voteups' : 0,
        'votedowns' : 0}
      fact2return.append(item)
      self.response.out.write(json.write(fact2return))
    else:
      item = {'status' : 'FAIL'}
      fact2return.append(item)
      self.response.out.write(json.write(fact2return))
      
  def _fact_vote(self):
    # we first catch the post values present in the request
    fact_key = self.request.get("fact_key")
    user_id = self.request.get("user_id")
    vote = self.request.get("vote")
    # we need to return what fact was voted successfully, to update count on client side and all
    returnval = []
    if vote == 'up':
      vote_val = 1
    elif vote == 'down':
      vote_val = -1
    # we get the user key
    user_q = db.Query(User).filter('id =', user_id)
    curr_user = user_q.get()
    curr_user_key = curr_user.key()
    fact = db.get(Key(fact_key))
    up_count = getattr(fact, 'total_vote_up') if getattr(fact, 'total_vote_up') else 0 
    down_count = getattr(fact, 'total_vote_down') if getattr(fact, 'total_vote_down') else 0
    has_voted = True if db.Query(Fact_Vote).filter('voter =', curr_user_key).filter('fact =', fact.key()).get() else False
    if (has_voted):
      item = {'status' : 'FAIL',
        'key' : fact_key,
        'vote' : vote}
      returnval.append(item)
    else:
      fact_vote = Fact_Vote()
      fact_vote.fact = fact
      fact_vote.voter = curr_user
      fact_vote.vote = vote_val
      if vote_val == 1:
        fact.total_vote_up = up_count+1
        returncount = up_count+1
      elif vote_val == -1:
        fact.total_vote_down = down_count+1
        returncount = down_count+1
      fact_vote.put()
      fact.put()
      item = {'status' : 'OK',
        'key' : fact_key,
        'vote' : vote,
        'count' : returncount}
      returnval.append(item)
    self.response.out.write(json.write(returnval))
        