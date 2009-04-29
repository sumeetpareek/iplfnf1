$(document).ready(function(){
	window.curr_user = 'user15'; //TODO remove this
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

function registerFunctions(){
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
		restore_fact_add($(this));
	});
}

function restore_fact_add(ele){
	if (ele.val() == '') {
		// reset the form, hide add part, show bold part
		$('#wickPlayer').val('');
		$('#wickClub').val('');
		$('#fact-add-wp').hide();
		$('#bold-add').show();
	}
	else {
		// do nothing
	}
}