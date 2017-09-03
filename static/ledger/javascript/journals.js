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
function save(_id) {
	
	//trips
	if (_id == 'trips') {
		$('span#trips.message').html('');
		error = false;
	
		de = $('input.trips[name="destination"]').val();
		a = $('input.trips[name="activities"]').val();
		amt = $('input.trips[name="amount"]').val();
		c = $('input.trips[name="currency"]').val();
		e = $('input.trips[name="exchange"]').val();
		p = $('select.trips[name="payment"]').val();
		y = $('input.trips[name="year"]').val();
		m = $('input.trips[name="month"]').val();
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
		
		var d = {id:_id,destination:de,activities:a,amount:amt,currency:c,exchange:e,payment:p,year:y,month:m};
	}
	
	//fundsupermart
	else if (_id == 'fundsupermart') {
		$('span#fundsupermart.message').html('');
		error = false;
	
		c = $('select.fundsupermart[name="choice"]').val();
		f = $('input.fundsupermart[name="fund"]').val();
		u = $('input.fundsupermart[name="unit"]').val();
		a = $('input.fundsupermart[name="amount"]').val();
		da = $('input.fundsupermart[name="date"]').val();
		u = '/journal_fundsupermart/';
		
		$("input.fundsupermart").each(function() {
			$(this).removeAttr('style');
			$(this).html("");
		});
		
		$("input.fundsupermart").each(function() {
			if ($(this).val()=='') {
				if (!(c == 'commission' && $(this).attr("name")=='unit')) {
					$(this).css('border-color','crimson');
					$('span#fundsupermart.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>red colour cannot be empty</span>");
					error = true;
				}
			}
		});
		
		var d = {id:_id,choice:c,fund:f,unit:u,amount:a,date:da};
	}
	
	//sos
	else if (_id == 'sos') {
		$('span#sos.message').html('');
		error = false;
	
		c = $('select.sos[name="choice"]').val();
		un = $('input.sos[name="unit"]').val();
		a = $('input.sos[name="amount"]').val();
		da = $('input.sos[name="date"]').val();
		u = '/journal_sos/';
		
		$("input.sos").each(function() {
			$(this).removeAttr('style');
			$(this).html("");
		});
		
		$("input.sos").each(function() {
			if ($(this).val()=='') {
				if (!(c == 'dividend' && $(this).attr("name")=='unit')) {
					$(this).css('border-color','crimson');
					$('span#sos.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>red colour cannot be empty</span>");
					error = true;
				}
			}
		});
		
		var d = {id:_id,choice:c,unit:un,amount:a,date:da};
	}
	
	//cpf
	else if (_id == 'cpf') {
		$('span#cpf.message').html('');
		error = false;
	
		o = $('input.cpf[name="ordinary"]').val();
		s = $('input.cpf[name="special"]').val();
		m = $('input.cpf[name="medisave"]').val();
		me = $('input.cpf[name="medishield"]').val();
		d = $('input.cpf[name="dps"]').val();
		da = $('input.cpf[name="date"]').val();
		u = '/journal_cpf/';
		
		$("input.cpf").each(function() {
			$(this).removeAttr('style');
			$(this).html("");
		});
		
		var d = {id:_id,ordinary:o,special:s,medisave:m,medishield:me,dps:d,date:da};
	}
	
	//basic
	else if (_id == 'basic') {
		$('span#basic.message').html('');
		error = false;
	
		c = $('select.basic[name="choice"]').val();
		a = $('input.basic[name="amount"]').val();
		y = $('input.basic[name="year"]').val();
		m = $('input.basic[name="month"]').val();		
		u = '/journal_basic_expense/';
		
		$("input.basic").each(function() {
			$(this).removeAttr('style');
			$(this).html("");
		});
		
		$("input.basic").each(function() {
			if ($(this).val()=='') {
				$(this).css('border-color','crimson');
				$('span#basic.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>red colour cannot be empty</span>");
				error = true;
			}
		});
		
		var d = {id:_id,choice:c,amount:a,year:y,month:m};
	}
	
	//setting
	else if (_id == 'id_test_mode' || _id == 'id_remove_test') {
		$('span#setting.message').html('');
		error = false;
	
		a = $('input[id="'+_id+'"]').is(':checked');
		u = '/journal_setting/';
		
		var d = {id:_id,action:a};
	}
	
	if (!error) {
		
	//console.log(d)
	$('span#'+_id+'.message').html(" <span style='font-family: monospace;font-size: small;color: black;'>saving <i class='fa fa-spinner fa-spin fa-fw' aria-hidden='true'></i></span>"); // add the error to the dom

	$.ajax({
		url : location.protocol + '//' + location.host + u, // the endpoint
		type : "POST", // http method
		data : d, // data sent with the post request $('#post-text').val()
		// handle a successful response
		
		success : function(json) {
			if (json == 'success') {
				$('span#'+_id+'.message').html(" <span style='font-family: monospace;font-size: small;color: forestgreen;'>saved <i class='fa fa-check' aria-hidden='true'></i></span>"); // add the error to the dom
				console.log(json);
			} else {
				$('span#'+_id+'.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>saving failed due to "+json+" <i class='fa fa-exclamation' aria-hidden='true'></i></span>"); // add the error to the dom
				console.log(json);
			}
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('span#'+_id+'.message').html(" <span style='font-family: monospace;font-size: small;color: crimson;'>ajax connection error due to "+err+" <i class='fa fa-exclamation' aria-hidden='true'></i></span>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
	}
};

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();