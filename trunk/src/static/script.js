$(document).ready(function(){
	window.curr_user = 'user15'; //TODO remove this
  // to know if fact-submit-button has focus
   window.fact_add_focus = false;
	window.curr_fact_page = 1;
	showLoading($("#fnf-container"),"Aabra Ka Daabra..!! ");
	registerFunctions();
	startGettingData();
	//$(".fact-wp:odd").animate({left: 500}, 1500);
	//$(".fact-wp:even").animate({right: 500}, 1500);
});

function showLoading(obj,msg){
	obj.append("<div class=\"loading\">"+ msg +"</div>");
}

function hideLoading(obj) {
obj.remove();
}

function startGettingData(){
  window.first_fact_load = true;
  $.ajax({
    type: "GET",
    url: "http://localhost:8080/all/country", //TODO remove local
    dataType: "json",
    success: onLoadAllCountry
  });
}

function onLoadAllCountry(data, textStatus) {
  window.all_country_full = data;
  window.all_country_coll = [];
  $.each(data, function(i,val){all_country_coll[i]=val.country_name;});
  //next we get the clubs
  $.ajax({
    type: "GET",
    url: "http://localhost:8080/all/club", //TODO remove local
    dataType: "json",
    success: onLoadAllClub
  });
}

function onLoadAllClub(data, textStatus) {
  window.all_club_full = data;
  window.all_club_coll = [];
  $.each(data, function(i,val){all_club_coll[i]=val.name;});
	//next we get the players
  $.ajax({
    type: "GET",
    url: "http://localhost:8080/all/player", //TODO remove local
    dataType: "json",
    success: onLoadAllPlayer
  });
}

function onLoadAllPlayer(data, textStatus) {
  window.all_player_full = data;
  window.all_player_coll = [];
  $.each(data, function(i,val){all_player_coll[i]=val.name;});
  // we get all the matches
  $.ajax({
    type: "GET",
    url: "http://localhost:8080/all/match", //TODO remove local
    dataType: "json",
    success: onLoadAllMatch
  });
}

function onLoadAllMatch(data, textStatus) {
  window.all_match_full = data;
  // we finally get all the latest facts
  $.ajax({
    type: "POST",
    url: "http://localhost:8080/fact/get", //TODO remove local
    dataType: "json",
    data: ({user_id : curr_user, fact_query : "latest", fact_page:curr_fact_page}), //TODO remove hardcoded
    success: onFactGet
  });
}

function onFactGet(data,textStatus){
		 hideLoading($('.loading'));
		// show the fact container
		$("#fact-container").show();
		// iterate over each data > form markup > get user info from container > app info from the collections > append and slide
		$.each(data, function(i,val){
			var mk = '';
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
							</div>\
							<div class="fact-content">'+ val.content +'</div>\
							<div class="cb"></div>\
						</div>\
			';
			$('#fact-list-wp').append(mk);
			$('.fact-wp:hidden').slideDown(1000);
		});
		// set to false
		first_fact_load = false;
}

function registerFunctions() {
   
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
			curr_fact_page -= 1;
			query_id = $('#fact-tabs .active').attr('id');
			// split animate all the current facts out
			$(".fact-wp:even").animate({left:500},1500,'linear',function(){$(this).remove();});
			$(".fact-wp:odd").animate({right:500},1500,'linear',function(){$(this).remove();});
		  $.ajax({
		    type: "POST",
		    url: "http://localhost:8080/fact/get", //TODO remove local
		    dataType: "json",
		    data: ({user_id : curr_user, fact_query : query_id, fact_page:curr_fact_page}), //TODO remove hardcoded
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
            $.ajax({
              type: "POST",
              url: "http://localhost:8080/fact/set", //TODO remove local
              dataType: "text",
              data: ({fact_creator : curr_user, fact_content : $('#fact-add-content').val()}), //TODO remove hardcoded
              success: onFactSet
            });
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
		curr_fact_page += 1;
		query_id = $('#fact-tabs .active').attr('id');
		// split animate all the current facts out
		$(".fact-wp:even").animate({left:500},1500,'linear',function(){$(this).remove();});
		$(".fact-wp:odd").animate({right:500},1500,'linear',function(){$(this).remove();});
	  $.ajax({
	    type: "POST",
	    url: "http://localhost:8080/fact/get", //TODO remove local
	    dataType: "json",
	    data: ({user_id : curr_user, fact_query : query_id, fact_page:curr_fact_page}), //TODO remove hardcoded
	    success: onFactGet
	  });
	});


	// querying for a different type of fact listing
	$('#fact-tabs a').click(function(){
		if($(this).is('.active')){
			// do nothing
		}
		else {
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
		    data: ({user_id : curr_user, fact_query : query_id, fact_page:1}), //TODO remove hardcoded
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
	else if ($('#wickPlayer').val() == '' && $('#wickPlayer').val() == '') {
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
	// get user entered tags
	var clubs = $.makeArray($("#wickClub").val());
	var players = $.makeArray($("#wickPlayer").val());
	// if any tag is not in the collection return false
	$.each(clubs,function(i,val){
		if (all_club_coll.indexOf(val) < 0) {return false;}
	});
	$.each(players,function(i,val){
		if (all_player_coll.indexOf(val) < 0) {return false;}
	});
	return true;
}

function onFactSet(data,textStatus){
  if (data == 'OK'){
    alert('done man');
  }
  else {alert ('asshole');}
}