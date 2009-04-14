from db_fact import *
from db_fantasy import *
from db_general import *
from google.appengine.ext import webapp
import logging
import json

class FactServer(webapp.RequestHandler):
   
  def post(self):
    """Handle GET requests."""
    if self.request.path.__eq__('/fact/get'):
      self._fact_get()

  def _fact_get(self):
    tag_type = None
    user_id = self.request.get("user_id")
    fact_tag = self.request.get("fact_tag")
    fact_query = self.request.get("fact_query")
    fact_page = self.request.get("fact_page")
    if fact_tag is not None and fact_tag != '':
      tag_type = db.Key(fact_tag).kind()
    # start the query
    q = None
    fact2return = []
    if fact_query == 'latest':
      # if we want latest facts with some tag or the other
      if tag_type is not None:
        if tag_type == 'Player':
          q = db.Query(Fact_Player).filter('player =',db.Key(fact_tag)).order('-timestamp')
          result = q.fetch(10,int(fact_page)-1)
          for val in result:
            curr_fact = db.get(val.fact.key())
            item = {'key' : str(curr_fact.key()),
                    'content' : str(curr_fact.content),
                    'timestamp' : str(curr_fact.timestamp),
                    'creator' : str(curr_fact.creator.key()),
                    'voteup' : curr_fact.total_vote_up,
                    'votedown' : curr_fact.total_vote_down}
            fact2return.append(item)
        elif tag_type == 'Club':
          q = db.Query(Fact_Club).filter('club =',db.Key(fact_tag)).order('-timestamp')
          result = q.fetch(10,int(fact_page)-1)
          for val in result:
            curr_fact = db.get(val.fact.key())
            item = {'key' : str(curr_fact.key()),
                    'content' : str(curr_fact.content),
                    'timestamp' : str(curr_fact.timestamp),
                    'creator' : str(curr_fact.creator.key()),
                    'voteup' : curr_fact.total_vote_up,
                    'votedown' : curr_fact.total_vote_down}
            fact2return.append(item)
      # if we want latest facts without any tags at all
      else:
        q = db.Query(Fact).order('-timestamp')
        result = q.fetch(10,int(fact_page)-1)
        for curr_fact in result:
          item = {'key' : str(curr_fact.key()),
                  'content' : str(curr_fact.content),
                  'timestamp' : str(curr_fact.timestamp),
                  'creator' : str(curr_fact.creator.key()),
                  'voteup' : curr_fact.total_vote_up,
                  'votedown' : curr_fact.total_vote_down}
          fact2return.append(item)
      self.response.out.write(json.write(fact2return))
      
    # if the querytype for getting facts is 'user-added'
    elif fact_query == 'user-added':
      user_q = db.Query(User).filter('id =', user_id)
      curr_user = user_q.get()
      q = db.Query(Fact).filter('creator =',curr_user.key()).order('-timestamp')
      result = q.fetch(10,int(fact_page)-1)
      for curr_fact in result:
        item = {'key' : str(curr_fact.key()),
                'content' : str(curr_fact.content),
                'timestamp' : str(curr_fact.timestamp),
                'creator' : str(curr_fact.creator.key()),
                'voteup' : curr_fact.total_vote_up,
                'votedown' : curr_fact.total_vote_down}
        fact2return.append(item)
      self.response.out.write(json.write(fact2return))
      
    # if the querytype for getting facts is 'user-liked'
    elif fact_query == 'user-liked' or fact_query == 'user-disliked':
      # find who the user is
      user_q = db.Query(User).filter('id =', user_id)
      curr_user = user_q.get()
      # get the fact keys for which the user has voted up/down depending on fact_query type
      if fact_query == 'user-liked':
        vote_q = db.Query(Fact_Vote).filter('voter =',curr_user.key()).filter('vote =',1).order('-timestamp')
      elif fact_query == 'user-disliked':
        vote_q = db.Query(Fact_Vote).filter('voter =',curr_user.key()).filter('vote =',-1).order('-timestamp')
      vote_result = vote_q.fetch(10,int(fact_page)-1)
      for curr_vote in vote_result:
        item = {'key' : str(curr_vote.fact.key()),
                'content' : str(curr_vote.fact.content),
                'timestamp' : str(curr_vote.fact.timestamp),
                'creator' : str(curr_vote.fact.creator.key()),
                'voteup' : curr_vote.fact.total_vote_up,
                'votedown' : curr_vote.fact.total_vote_down}
        fact2return.append(item)
      self.response.out.write(json.write(fact2return))