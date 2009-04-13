from db_model import *
from google.appengine.ext import webapp
import logging
import json
from db_model import Fact_Player
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
                    'creator' : str(curr_fact.creator),
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
                    'creator' : str(curr_fact.creator),
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
                  'creator' : str(curr_fact.creator),
                  'voteup' : curr_fact.total_vote_up,
                  'votedown' : curr_fact.total_vote_down}
          fact2return.append(item)
      self.response.out.write(json.write(fact2return))        