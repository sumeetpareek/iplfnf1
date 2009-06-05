window.curr_user = 'user16'; //TODO remove this
window.curr_fact_club = '';
window.curr_fact_player = '';
// To know if fact-submit-button has focus
window.fact_add_focus = false;
window.curr_fact_page = 1;

function showLoading(obj,msg){
  obj.append("<div class=\"loading\">"+ msg +"</div>");
}

function hideLoading(obj) {
  obj.remove();
}

function startGettingData(){
  var params = {};
  params[gadgets.io.RequestParameters.CONTENT_TYPE] = gadgets.io.ContentType.JSON;
  var url = 'http://iplfnf1.appspot.com/all/country';
  gadgets.io.makeRequest(url, onLoadAllCountry, params);
}

function onLoadAllCountry(r) {
  all_country_full = r.data;
  all_country_coll = [];
  $.each(r.data, function(i,val){all_country_coll[i]=val.country_name;});
  //next we get the clubs
  var params = {};
  params[gadgets.io.RequestParameters.CONTENT_TYPE] = gadgets.io.ContentType.JSON;
  var url = 'http://iplfnf1.appspot.com/all/club';
  gadgets.io.makeRequest(url, onLoadAllClub, params);
}

function onLoadAllClub(r) {
  window.all_club_full = r.data;
  window.all_club_coll = [];
  $.each(r.data, function(i,val){all_club_coll[i]=val.name;});
	//next we get the players
  var params = {};
  params[gadgets.io.RequestParameters.CONTENT_TYPE] = gadgets.io.ContentType.JSON;
  var url = 'http://iplfnf1.appspot.com/all/players';
  gadgets.io.makeRequest(url, onLoadAllPlayer, params);
}

function onLoadAllPlayer(r) {
  window.all_player_full = r.data;
  window.all_player_coll = [];
  $.each(r.data, function(i,val){all_player_coll[i]=val.name;});
  // we get all the latest facts
    var params = {
      'methodType':'post',
      'contentType':'json',
      'postData':'user_id='+curr_user+'&fact_query=latest&fact_page=1'
    };
    var url = 'http://iplfnf1.appspot.com/fact/get';
    gadgets.io.makeRequest(url, onFactGet, params);
}

function onFactGet(r){
		 hideLoading($('.loading'));
		// show the fact container
		$("#fact-container").show();
		// iterate over each data > form markup > get user info from container > app info from the collections > append and slide
		$.each(r.data, function(i,val){
			var mk = '';
            var tags = '';
			var vw = 'vote-widget-active';
			var vu = 'vote-up-off';
			var vd = 'vote-down-off';
			if (val.curr_user_vote != 0){
				vw = 'vote-widget-inactive';
				if (val.curr_user_vote == 1){
					vu = 'vote-up-on';
				}
				else {
					vd = 'vote-down-on';
				}
			}
      // foreach tag that is returned we show them in a-tag by fetching the name
      for (var i=0;i<val.tags.length;i++) {
        var tag_detail = getTagDetail(val.tags[i]);
        if (tag_detail[0] == 'club'){
          tags += '<a href="#" title="Club" name="'+ all_club_full[tag_detail[1]].key +'" class="'+ all_club_full[tag_detail[1]].short_name +'">'+all_club_full[tag_detail[1]].name+'</a>';
        }
        if (tag_detail[0] == 'player'){
          tags += '<a href="#" title="Player" name="'+ all_player_full[tag_detail[1]].key +'" class="'+ all_player_full[tag_detail[1]].type +'">'+all_player_full[tag_detail[1]].name+'</a>';
        }
      }
			mk += '\
						<div id="'+ val.key +'" class="fact-wp" style="display:none;">\
							<div class="uimg"></div>\
							<div class="fact-meta">\
								<a class="uname" href="#">'+ val.creator +'</a>\
								<span class="fact-time">at '+ val.timestamp +'</span>\
							</div>\
							<div class="vote-widget '+ vw +'">\
								<span class="vote-btn vote-up '+ vu +'">I like this!</span><span class="vote-up-count">+'+ val.voteups +'</span>\
								<span class="vote-btn vote-down '+ vd +'">I hate this!</span><span class="vote-down-count">-'+ val.votedowns +'</span>\
                <span class="voting" style="display:none;">Registering your vote...</span>\
							</div>\
							<div class="fact-content">'+ val.content +'</div>\
							<div class="cb"></div>\
              <div class="fact-relatedto">'+ tags +'</div>\
						</div>\
			';
			$('#fact-list-wp').append(mk);
			$('.fact-wp:hidden').slideDown(1000);
		});
		// set to false
		first_fact_load = false;
}

function registerFunctions() {
  // when a fact tag is clicked we need to fetch facts to that tag and the current query type
  $('.fact-relatedto a').livequery('click',function(){
    //reset curr club and player
    curr_fact_player = '';
    curr_fact_club = '';
    //set club or player tag to the clicked value
    if ($(this).attr('title')=='Club'){curr_fact_club = $(this).attr('name');}
    if ($(this).attr('title')=='Player'){curr_fact_player = $(this).attr('name');}
    //get what the current query_id is and send ajax request to get facts
    var query_id = $('#fact-tabs .active').attr('id');
    var params = {
      'methodType':'post',
      'contentType':'json',
      'postData':'data1=value1&data2=value2'
    };
    var url = 'http://iplfnf1.appspot.com/fact/get';
    gadgets.io.makeRequest(url, onLoadAllCountry, params);
    $.ajax({
      type: "POST",
      url: "http://localhost:8080/fact/get", //TODO remove local
      dataType: "json",
      data: ({user_id : curr_user, fact_query : query_id, fact_page:curr_fact_page, fact_clubs:curr_fact_club, fact_players:curr_fact_player}), //TODO remove hardcoded
      success: onFactGet
    });
  });
  
  $('.vote-widget .vote-up').livequery('mouseover', function(){
    $(this).addClass('vote-up-color');
  });
  $('.vote-widget .vote-up').livequery('mouseout', function(){
    $(this).removeClass('vote-up-color');
  });
  $('.vote-widget .vote-down').livequery('mouseover', function(){
    $(this).addClass('vote-down-color');
  });
  $('.vote-widget .vote-down').livequery('mouseout', function(){
    $(this).removeClass('vote-down-color');
  });
  $('.vote-widget-active .vote-up').livequery('click', function(){
    // we get the fact id
    var vote_fact_id = $(this).parent().parent().attr('id');
    // show a message to ease the wait
    var temp = $(this).siblings('.voting').html('Registering your vote... ').show();
    // send ajax request to cast the vote
    $.ajax({
      type: "POST",
      url: "http://localhost:8080/fact/vote", //TODO remove local
      dataType: "json",
      data: ({fact_key: vote_fact_id, user_id : curr_user, vote:'up'}), //TODO remove hardcoded
      success: onFactVote
    });
  });
  $('.vote-widget-active .vote-down').livequery('click', function(){
    // we get the fact id
    var vote_fact_id = $(this).parent().parent().attr('id');
    // show a message to ease the wait
    var temp = $(this).siblings('.voting').html('Registering your vote... ').show();
    // send ajax request to cast the vote
    $.ajax({
      type: "POST",
      url: "http://localhost:8080/fact/vote", //TODO remove local
      dataType: "json",
      data: ({fact_key: vote_fact_id, user_id : curr_user, vote:'down'}), //TODO remove hardcoded
      success: onFactVote
    });
  });
  $('#fact-reset').click(function(){
		$('#fact-add-form .msg-y').html('').hide();
		$('#fact-add-form .msg-r').html('').hide();
  });
   
   $('#fact-submit').focus(function(){
      fact_add_focus = true;
   });
   $('#fact-submit').blur(function(){
      fact_add_focus = false;
   });
   
	// getting previous and next pages of a fact
	$('#fact-prev').click(function(){
		if (curr_fact_page == 1) {
			// do nothing
		}
		else {
      showLoading($('#fact-list-wp'),"Aabra Ka Daabra..!! ");
			curr_fact_page -= 1;
			query_id = $('#fact-tabs .active').attr('id');
			// split animate all the current facts out
			$(".fact-wp:even").animate({left:500},1500,'linear',function(){$(this).remove();});
			$(".fact-wp:odd").animate({right:500},1500,'linear',function(){$(this).remove();});
		  $.ajax({
		    type: "POST",
		    url: "http://localhost:8080/fact/get", //TODO remove local
		    dataType: "json",
		    data: ({user_id : curr_user, fact_query : query_id, fact_page:curr_fact_page, fact_clubs:curr_fact_club, fact_players:curr_fact_player}), //TODO remove hardcoded
		    success: onFactGet
		  });
		}
	});
	
	$('#bold-add').click(function(){
		$(this).hide();
		$('#fact-add-wp').show();
		$('#fact-add-wp textarea').focus();
	});
	
	$('#fact-cancel').click(function(e){
		// get the textarea and pass to the restore function
		$('#fact-add-content').val('');
		restore_fact_add($('#fact-add-content'));
		e.preventDefault();
	});
	
	$('form#fact-add-form').submit(function(){
		// get the validation return value
		var fact_valid = fact_submit_validation(); //TODO make function
		// check validity, perform action and prevent default
		// if valid send ajax request
		if (fact_valid == 'ok'){
			// first we show the sending message
			$('div.fact-submit-msg-wp').show();
			$('div.fact-submit-msg-wp .msg-y').html('Submitting your fact to the cricket gods now...').show();
			$('div.fact-submit-msg-wp .msg-r').hide();
      // we get key values from the tags entered
			var clubs_str = $("#wickClub").val();
			var clubs_arr = new Array();
			$.each(all_club_full,function(i,val){
			  if (clubs_str.indexOf(val.name) >=0){
				clubs_arr.push(val.key);
			  }
			});
			var players_str = $("#wickPlayer").val();
			var players_arr = new Array();
			$.each(all_player_full,function(i,val){
			  if (players_str.indexOf(val.name) >=0){
				players_arr.push(val.key);
			  }
			});
            // we send a post request to set the fact
    var params = {}
    var postdata = {
      fact_creator : curr_user,
      fact_content : $('#fact-add-content').val(),
      fact_clubs : clubs_arr.join(","),
      fact_players : players_arr.join(",")
    };
    params[gadgets.io.RequestParameters.CONTENT_TYPE] = gadgets.io.ContentType.JSON;
    params[gadgets.io.RequestParameters.METHOD] = gadgets.io.MethodType.POST;
    params[gadgets.io.RequestParameters.POST_DATA] = gadgets.io.encodeValues(postdata); 
    var url = 'http://iplfnf1.appspot.com/fact/set';
    gadgets.io.makeRequest(url, onFactSet, params);
		}
		// if content is missing
		else if (fact_valid == 'content-missing') {
			$('#fact-add-form .fact-submit-msg-wp').show();
			$('#fact-add-form .msg-y').hide();
			$('#fact-add-form .msg-r').html('You are trying to submit the fact without writing any content. <br/>Sorry, that is like trying to score without a bat !?!!').show();
		}
		// if tag missing
		else if (fact_valid == 'tag-missing') {
			$('#fact-add-form .fact-submit-msg-wp').show();
			$('#fact-add-form .msg-y').hide();
			$('#fact-add-form .msg-r').html('You have not associated the fact with atleast one Player or Club. <br/>That is like bowling without declaring any style to the umpire !?!?!').show();
		}
		// if tag invalid
		else if (fact_valid == 'tag-invalid') {
			$('#fact-add-form .fact-submit-msg-wp').show();
			$('#fact-add-form .msg-y').hide();
			$('#fact-add-form .msg-r').html('You have associated incorrect tags with the fact. <br/>Its not possible to play cricket with a rugby ball !?!!').show();
		}
		return false;
	});
	
	$('#fact-next').click(function(){
    showLoading($('#fact-list-wp'),"Aabra Ka Daabra..!! ");
		curr_fact_page += 1;
		query_id = $('#fact-tabs .active').attr('id');
		// split animate all the current facts out
		$(".fact-wp:even").animate({left:500},1500,'linear',function(){$(this).remove();});
		$(".fact-wp:odd").animate({right:500},1500,'linear',function(){$(this).remove();});
	  $.ajax({
	    type: "POST",
	    url: "http://localhost:8080/fact/get", //TODO remove local
	    dataType: "json",
	    data: ({user_id : curr_user, fact_query : query_id, fact_page:curr_fact_page, fact_clubs:curr_fact_club, fact_players:curr_fact_player}), //TODO remove hardcoded
	    success: onFactGet
	  });
	});


	// querying for a different type of fact listing
	$('#fact-tabs a').click(function(){
		if($(this).is('.active')){
			// do nothing
		}
		else {
      // you obviously gotta start from the first page
      curr_fact_page = 1;
			// remove the active class from other option
			$('#fact-tabs .active').removeClass('active');
			// add active class to the present option
			$(this).addClass('active');
			// split animate all the current facts out
			$(".fact-wp:even").animate({left:500},1500,'linear',function(){$(this).remove();});
			$(".fact-wp:odd").animate({right:500},1500,'linear',function(){$(this).remove();});
			// get facts as per new query and show them
			var query_id = $(this).attr('id');
			showLoading($('#fact-list-wp'),"Aabra Ka Daabra..!! ");
		  $.ajax({
		    type: "POST",
		    url: "http://localhost:8080/fact/get", //TODO remove local
		    dataType: "json",
		    data: ({user_id : curr_user, fact_query : query_id, fact_page:1, fact_clubs:curr_fact_club, fact_players:curr_fact_player}), //TODO remove hardcoded
		    success: onFactGet
		  });
		}
	});
	
	// to restore the fact add area when it loses focus
	$('#fact-add-wp textarea').blur(function(){
      setTimeout("if (fact_add_focus == false){restore_fact_add()};",300);
	});

}

function restore_fact_add(){
	if ($('#fact-add-content').val() == '') {
		// reset the form, hide add part, show bold part
		$('#wickPlayer').val('');
		$('#wickClub').val('');
		$('#fact-add-wp').hide();
		$('#bold-add').show();
		$('#fact-add-form .msg-y').html('').hide();
		$('#fact-add-form .msg-r').html('').hide();
	}
	else {
		// do nothing
	}
}

function fact_submit_validation(){
	if ($('#fact-add-content').val() == '') {
		return 'content-missing';
	}
	else if ($('#wickPlayer').val() == '' && $('#wickClub').val() == '') {
		return 'tag-missing';
	}
	else if (!tags_valid()){
		return 'tag-invalid';
	}
	else {
		return 'ok';
	}
}

function tags_valid(){
  // make complete collection a string and input tags as array
  var club_str = all_club_coll.join(",");
  var player_str = all_player_coll.join(",");
  //var input_club = new Array();
  //var input_player = new Array();
  var input_club = $("#wickClub").val().split(", ");
  var input_player = $("#wickPlayer").val().split(", ");
  // iterate over input tags and if they are not in collection return false
  for (var i=0;i<input_club.length;i++) {
    if (input_club[i] != '' && club_str.indexOf(input_club[i]) < 0){
      return false;
    }
  }
  for (var i=0;i<input_player.length;i++) {
    if (input_player[i] != '' && player_str.indexOf(input_player[i]) < 0){
      return false;
    }
  }
  // if all is fine return true :)
  return true;
}

function onFactSet(r){
  if (r.data[0].status == 'OK'){
	// we show the message that fact is submitted
	$('div.fact-submit-msg-wp .msg-y').html('Cricket gods accepted your fact :)');
	// restore the entire fact-add region
	$('#fact-add-content').val('');
	setTimeout("restore_fact_add()",1200);
  // slide the new fact down
  var mk = '';
  var tags = '';
  // foreach tag that is returned we show them in a-tag by fetching the name
  for (var i=0;i<r.data[0].tags.length;i++) {
    var tag_detail = getTagDetail(r.data[0].tags[i]);
    if (tag_detail[0] == 'club'){
      tags += '<a href="#" title="Club" name="'+ all_club_full[tag_detail[1]].key +'" class="'+ all_club_full[tag_detail[1]].short_name +'">'+all_club_full[tag_detail[1]].name+'</a>';
    }
    if (tag_detail[0] == 'player'){
      tags += '<a href="#" title="Player" name="'+ all_player_full[tag_detail[1]].key +'" class="'+ all_player_full[tag_detail[1]].type +'">'+all_player_full[tag_detail[1]].name+'</a>';
    }
  }
  mk += '\
        <div id="'+ r.data[0].key +'" class="fact-wp" style="display:none;background:#FFEE96 !important">\
          <div class="uimg"></div>\
          <div class="fact-meta">\
            <a class="uname" href="#">'+ r.data[0].creator +'</a>\
            <span class="fact-time">at '+ r.data[0].timestamp +'</span>\
          </div>\
          <div class="vote-widget vote-widget-active">\
            <span class="vote-btn vote-up vote-up-off">I like this!</span><span class="vote-up-count">+'+ r.data[0].voteups +'</span>\
            <span class="vote-btn vote-down vote-down-off">I hate this!</span><span class="vote-down-count">-'+ r.data[0].votedowns +'</span>\
            <span class="voting" style="display:none;">Registering your vote...</span>\
          </div>\
          <div class="fact-content">'+ r.data[0].content +'</div>\
          <div class="cb"></div>\
              <div class="fact-relatedto">'+ tags +'</div>\
        </div>\
  ';
  $('#fact-list-wp').prepend(mk);
  setTimeout("$('.fact-wp:hidden').slideDown(1000)",1500);;
  }
  else {alert ('IPL fact you tried to add could not get submitted.');}
}

function onFactVote(data,textStatus){
  // if ok
  if (data[0].status == 'OK'){
    $('#'+data[0].key+' .voting').html('Done :) ').css('background','#FFEE96').css('padding-left','4px');
    if (data[0].vote == 'up'){
      // update vote count
      $('#'+data[0].key+' .vote-up-count').html('+'+data[0].count);
      // update widget classes
      $('#'+data[0].key+' .vote-widget').removeClass('vote-widget-active').addClass('vote-widget-inactive');
      $('#'+data[0].key+' .vote-up').removeClass('vote-up-off').addClass('vote-up-on');
    }
    if (data[0].vote == 'down'){
      $('#'+data[0].key+' .vote-down-count').html('-'+data[0].count);
      // update widget classes
      $('#'+data[0].key+' .vote-widget').removeClass('vote-widget-active').addClass('vote-widget-inactive');
      $('#'+data[0].key+' .vote-down').removeClass('vote-down-off').addClass('vote-down-on');
    }
  }
  else {
    $('#'+data[0].key+' .voting').html('Failed :( ').css('background','#FFEE96').css('padding-left','4px');
  }
  
  // hide the voting message from the fact in question
  setTimeout("$('#"+data[0].key+" .voting').hide()",2000);
}

// gives the player or club name when the key is passed
function getTagDetail(key) {
  var toReturn = new Array();
  for (var i=0;i<all_club_full.length;i++) {
    if (all_club_full[i].key == key){
      toReturn[0] = 'club';
      toReturn[1] = i;
      return toReturn;
    }
  }
  for (var i=0;i<all_player_full.length;i++) {
    if (all_player_full[i].key == key){
      toReturn[0] = 'player';
      toReturn[1] = i;
      return toReturn;
    }
  }
  toReturn[0] = 'none';
  return toReturn;
}