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
function login(user,password,page) {
	
	$('span#trips.message').html('');
	error = false;

	if (_id == 'trips') {
		de = $('input.trips[name="destination"]').val();
		a = $('input.trips[name="activities"]').val();
		amt = $('input.trips[name="amount"]').val();
		c = $('input.trips[name="currency"]').val();
		e = $('input.trips[name="exchange"]').val();
		p = $('select.trips[name="payment"]').val();
		da = $('input.trips[name="date"]').val();
		u = '/journal_trips/';
		
		$("input.trips").each(function() {
			$(this).removeAttr('style');
			$(this).html("");
		});
		
		$("input.trips").each(function() {
			if ($(this).val()=='') {
				$(this).css('border-color','crimson');
				$('span#trips.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>red colour cannot be empty</span>");
				error = true;
			}
		});
		
		var d ={id:_id,destination:de,activities:a,amount:amt,currency:c,exchange:e,payment:p,date:da};
	} else if (_id == 'columns') {
		var name = 'all_table_columns'
	} else if (_id == 'functions') {
		var name = 'all_table_functions'
	}
	
	if (!error) {
		
	//console.log(d)
	$('span#trips.message').html(" <span style='font-family: monospace;font-size: small;color: black;'>saving <i class='fa fa-spinner fa-spin fa-3x fa-fw' aria-hidden='true'></i></span>"); // add the error to the dom

	$.ajax({
		url : location.protocol + '//' + location.host + u, // the endpoint
		type : "POST", // http method
		data : d, // data sent with the post request $('#post-text').val()
		// handle a successful response
		
		success : function(json) {
			if (json == 'success') {
				$('span#trips.message').html(" <span style='font-family: monospace;font-size: small;color: forestgreen;'>saved <i class='fa fa-check' aria-hidden='true'></i></span>"); // add the error to the dom
			} else {
				$('span#trips.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>saving failed due to "+json+" <i class='fa fa-exclamation' aria-hidden='true'></i></span>"); // add the error to the dom
				console.log(json);
			}
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('span#trips.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>ajax connection error due to "+err+" <i class='fa fa-exclamation' aria-hidden='true'></i></span>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
	}
};

function random()
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
};

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();