from db_general import *
from db_fact import *
from db_fantasy import *

from google.appengine.ext import webapp
import logging
import json

class FactServer(webapp.RequestHandler):
   
  def post(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/fact/get'):
      self._fact_get()

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
      q.filter(curr_user_key+ ' =',1).order('-timestamp')

    elif fact_query == 'user-liked':
      q.filter(curr_user_key+ ' =',-1).order('-timestamp')      
      
    # now we have the query ready so we fetch the results and return them in a "JSONed" list
    result = q.fetch(10,int(fact_page)-1)
    for curr_fact in result:
      curr_user_vote = getattr(curr_fact, str(curr_user_key), 0)
      creator = User.get_by_key_name(str(curr_fact.creator))
      item = {'key' : str(curr_fact.key()),
              'content' : str(curr_fact.content),
              'timestamp' : str(curr_fact.timestamp),
              'creator' : str(creator.id),
              'tags' : curr_fact.dynamic_properties(),
              'curr_user_vote' : curr_user_vote,
              'voteups' : curr_fact.total_vote_up,
              'votedowns' : curr_fact.total_vote_down}
      fact2return.append(item)
    self.response.out.write(json.write(fact2return))
#      
#      
#    # if the querytype for getting facts is 'user-liked'
#    elif fact_query == 'user-liked' or fact_query == 'user-disliked':
#      # find who the user is
#      user_q = db.Query(User).filter('id =', user_id)
#      curr_user = user_q.get()
#      # get the fact keys for which the user has voted up/down depending on fact_query type
#      if fact_query == 'user-liked':
#        vote_q = db.Query(Fact_Vote).filter('voter =',curr_user.key()).filter('vote =',1).order('-timestamp')
#      elif fact_query == 'user-disliked':
#        vote_q = db.Query(Fact_Vote).filter('voter =',curr_user.key()).filter('vote =',-1).order('-timestamp')
#      vote_result = vote_q.fetch(10,int(fact_page)-1)
#      for curr_vote in vote_result:
#        item = {'key' : str(curr_fact.key()),
#                'content' : str(curr_fact.content),
#                'timestamp' : str(curr_fact.timestamp),
#                'creator' : curr_fact.creator.id,
#                'tags' : curr_fact.dynamic_properties(),
#                'voteups' : curr_fact.total_vote_up,
#                'votedowns' : curr_fact.total_vote_down}
#        fact2return.append(item)
#      self.response.out.write(json.write(fact2return))
#      
#      
#      
#            result = q.fetch(10,int(fact_page)-1)
#      for curr_fact in result:
#        item = {'key' : str(curr_fact.key()),
#                'content' : str(curr_fact.content),
#                'timestamp' : str(curr_fact.timestamp),
#                'creator' : str(curr_fact.creator.key()),
#                'voteup' : curr_fact.total_vote_up,
#                'votedown' : curr_fact.total_vote_down}
#        fact2return.append(item)
#      self.response.out.write(json.write(fact2return))
#      
