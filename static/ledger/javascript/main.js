$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

// AJAX for posting
function create_post(_table,_id,_column,_value) {
	console.log("create post is working!"); // sanity check
	
	if (_table=='sats_article_add') {
		s = $('tr.sats_article [name="src"]').val();
		t = $('tr.sats_article [name="ticker"]').val();
		c = $('tr.sats_article [name="company"]').val();
		ty = $('tr.sats_article [name="type"]').val();
		de = $('tr.sats_article [name="descr"]').val();
		u = $('tr.sats_article [name="url"]').val();
		sc = $('tr.sats_article [name="screenshot"]').val();
		v = $('tr.sats_article [name="validation"]').val();
		l = $('tr.sats_article [name="lower_price"]').val();
		up = $('tr.sats_article [name="upper_price"]').val();
		cu = $('tr.sats_article [name="currency"]').val();
		st = $('tr.sats_article [name="start_date"]').val();
		en = $('tr.sats_article [name="end_date"]').val();
		
		var d ={name:'article',company:c,ticker:t,src:s,type:ty,descr:de,url:u,screenshort:sc,validation:v,lower_price:l,upper_price:up,currency:cu,start_date:st,end_date:en};
	} else {
		var d = {table:_table,id:_id,column:_column,value:_value}; // data sent with the post request $('#post-text').val()
	}
	
	$.ajax({
		url : "", // the endpoint
		type : "POST", // http method
		data : d, // data sent with the post request $('#post-text').val()
		// handle a successful response
		success : function(json) {
			console.log(json);
			remove(_table,_id);
			add(json,_table);
			//$('#post-text').val(''); // remove the value from the input
			console.log("success"); // another sanity check
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
};
//http://d.yimg.com/aq/autoc?query=singtel&region=SG&lang=en-US
var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();

function remove(var1,id) {
	if (var1=='sats_article_delete') {
		$(".sats_article#".concat(id)).fadeOut();
	}
}

function add(id,var1) {
	if (var1=='sats_article_add') {
		//document.open("text/html", "replace");
		//document.write(json);
		//document.close();
		
		s = $('tr.sats_article [name="src"]').val();
		t = $('tr.sats_article [name="ticker"]').val();
		c = $('tr.sats_article [name="company"]').val();
		ty = $('tr.sats_article [name="type"]').val();
		de = $('tr.sats_article [name="descr"]').val();
		u = $('tr.sats_article [name="url"]').val();
		sc = $('tr.sats_article [name="screenshot"]').val();
		v = $('tr.sats_article [name="validation"]').val();
		l = $('tr.sats_article [name="lower_price"]').val();
		up = $('tr.sats_article [name="upper_price"]').val();
		cu = $('tr.sats_article [name="currency"]').val();
		st = $('tr.sats_article [name="start_date"]').val();
		en = $('tr.sats_article [name="end_date"]').val();
		
		if (u!='') {
			u = '<a href="'+u+'" target="_blank">link</a>';
		}
		
		var html = '<tr class="sats_article" id="'+id+'">\
					<td><a href="'+id+'" target="_blank">'+id+'</a></td>\
					<td>'+s+'</td>\
					<td nowrap>'+c+'</td>\
					<td>'+ty+'</td>\
					<td>'+t+'</td>\
					<td>'+de+'</td>\
					<td>'+u+'</td>\
					<td></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="validation" value="'+v+'"/></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="lower_price" value="'+l+'"/></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="upper_price" value="'+up+'"/></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="currency" value="'+cu+'"/></td>\
					<td></td>\
					<td nowrap>'+st+'</td>\
					<td nowrap>'+en+'</td>\
					<td></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="status" value=""/></td>\
					<td style="text-align:center;"><i class="fa fa-trash-o" aria-hidden="true" id="'+id+'" tab="sats_article_delete"></i></td>\
					</tr>\
					<tr class="sats_article" id="new" style="display:none"></tr>';
					
		$(".sats_article#new").replaceWith(html).fadeIn();
		
		s = $('tr.sats_article [name="src"]').val('');
		t = $('tr.sats_article [name="ticker"]').val('');
		c = $('tr.sats_article [name="company"]').val('');
		ty = $('tr.sats_article [name="type"]').val('');
		de = $('tr.sats_article [name="descr"]').val('');
		u = $('tr.sats_article [name="url"]').val('');
		sc = $('tr.sats_article [name="screenshot"]').val('');
		v = $('tr.sats_article [name="validation"]').val('');
		l = $('tr.sats_article [name="lower_price"]').val('');
		up = $('tr.sats_article [name="upper_price"]').val('');
		cu = $('tr.sats_article [name="currency"]').val('');
		st = $('tr.sats_article [name="start_date"]').val('');
		en = $('tr.sats_article [name="end_date"]').val('');
	}
}