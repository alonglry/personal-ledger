var company = ''
var ticker = ''
var type = ''
var exchange = ''
var initial_price = ''
var type2 = ''
var currency = ''

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
		t = ticker //$('tr.sats_article [name="ticker"]').text()//.val();		
		c = $('tr.sats_article [name="company"]').val();
		ty = type //$('tr.sats_article [name="type"]').text()//.val();
		//de = $('tr.sats_article [name="descr"]').val();
		u = $('tr.sats_article [name="url"]').val();
		//sc = $('tr.sats_article [name="screenshot"]').val();
		//v = $('tr.sats_article [name="validation"]').val();
		//l = $('tr.sats_article [name="lower_price"]').val();
		//up = $('tr.sats_article [name="upper_price"]').val();
		cu = currency //$('tr.sats_article [name="currency"]').val();
		st = $('tr.sats_article [name="start_date"]').html();
		//en = $('tr.sats_article [name="end_date"]').val();
		i = initial_price;
		
		var d ={name:'article',company:c,ticker:t,src:s,type:ty,url:u,currency:cu,start_date:st,initial_price:i};
	} else if (_table=='sats_source_add') {
		s = $('input.source#id_src').val();
		de = $('input.source#id_descr').val();
		u = $('input.source#id_url').val();
		
		var d = {name:'source',src:s,descr:de,url:u}
	
	} else {
		var d = {table:_table,id:_id,column:_column,value:_value}; // data sent with the post request $('#post-text').val()
	}
	console.log(d);
	
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

// AJAX for getting stock
function create_stock(_company) {
	console.log("getting stock for " + _company); 
		
	$.ajax({
		url : "", // the endpoint
		type : "POST", // http method
		data : {table:'sats_company_get',column:_company},
		
		// handle a successful response
		success : function(json) {
			//console.log(json);
			console.log('success');
			//var o = json.split("},{");
			var o = JSON.parse(json).ResultSet.Result;
			if (o.length > 0) {
				var j = [];
				for (var i = 0; i < o.length; i++) {
					var s = [o[i].name + '(' + o[i].symbol + ') - ' + o[i].exchDisp +'('+o[i].exch+')'+ ' - ' + o[i].typeDisp]+'('+o[i].type+')'
					var d = '{symbol:"'+o[i].symbol+'",name:"'+o[i].name+'",exchDisp:"'+o[i].exchDisp+'",typeDisp:"'+o[i].typeDisp+'"}'
					var h = "<li>"+s+'</li>'
					j = j.concat(s)
				}
				
				console.log(j)
				
				$( "#stockpick" ).autocomplete({
					source: j
				});
			}
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
};
//http://d.yimg.com/aq/autoc?query=singtel&region=SG&lang=en-US&callback=YAHOO.util.ScriptNodeDataSource.callbacks
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
		t = ticker //$('tr.sats_article [name="ticker"]').text();
		c = $('tr.sats_article [name="company"]').val();
		ty = type //$('tr.sats_article [name="type"]').text();
		//de = $('tr.sats_article [name="descr"]').val();
		u = $('tr.sats_article [name="url"]').val();
		//sc = $('tr.sats_article [name="screenshot"]').val();
		//v = $('tr.sats_article [name="validation"]').val();
		//l = $('tr.sats_article [name="lower_price"]').val();
		//up = $('tr.sats_article [name="upper_price"]').val();
		cu = $('tr.sats_article [name="currency"]').val();
		//st = $('tr.sats_article [name="start_date"]').val();
		//en = $('tr.sats_article [name="end_date"]').val();
		
		if (u!='') {
			u = '<a href="'+u+'" target="_blank"><i class="fa fa-link" aria-hidden="true"></i></a>';
		}
		
		//if (v='min') {
		//	va = '(> ' + l + ') ~';
		//}
		
		var html = '<tr class="sats_article" id="'+id+'">\
					<td><a href="'+id+'" target="_blank">'+id+'</a></td>\
					<td style="font-size: x-small;text-align: right;">'+s+'</td>\
					<td nowrap style="padding: 0px 10px;">'+c+'</td>\
					<td class="smallgrey">'+type2+'</td>\
					<td style="padding: 0px 10px;text-align:center;">'+t+'</td>\
					<td class="center">'+u+'</td>\
					<td>'+va+'</td>\
					<td nowrap>'+st+' - '+en+'</td>\
					<td></td>\
					<td><input class="update" id="'+id+'" tab="sats_article_update" col="status" value=""/></td>\
					<td style="text-align:center;"><i class="fa fa-trash-o" aria-hidden="true" id="'+id+'" tab="sats_article_delete"></i></td>\
					</tr>\
					<tr class="sats_article" id="new" style="display:none"></tr>';
					
		$(".sats_article#new").replaceWith(html).fadeIn();
		
		s = $('tr.sats_article [name="src"]').val('');
		t = $('tr.sats_article [name="ticker"]').text('');
		c = $('tr.sats_article [name="company"]').val('');
		ty = $('tr.sats_article [name="type"]').text('');
		//de = $('tr.sats_article [name="descr"]').val('');
		u = $('tr.sats_article [name="url"]').val('');
		//sc = $('tr.sats_article [name="screenshot"]').val('');
		//v = $('tr.sats_article [name="validation"]').val('');
		//l = $('tr.sats_article [name="lower_price"]').val('');
		//up = $('tr.sats_article [name="upper_price"]').val('');
		//cu = $('tr.sats_article [name="currency"]').val('');
		//st = $('tr.sats_article [name="start_date"]').val('');
		//en = $('tr.sats_article [name="end_date"]').val('');
	} else if (var1=='sats_source_add') {
	
		s = $('input.source#id_src').val();
		de = $('input.source#id_descr').val();
		u = $('input.source#id_url').val();
		
		if (u!='') {
			u = '<a href="'+u+'" target="_blank"><i class="fa fa-link" aria-hidden="true"></i></a>'
		}
		
		var html = '<div class="source" style="margin-right: 5px;"><table>\
				    <tr><td class="source">'+s+' '+u+'</td></tr>\
					<tr><td class="source"><textarea rows="3" cols="20" class="update source" id="'+id+'" tab="sats_source_update" col="descr">'+de+'</textarea></td></tr>\
					<tr><td class="source"><table class="source">\
					<tr><td>total</td><td>success</td><td>fail</td></tr><tr><td>0</td><td>0</td><td>0</td></tr>\
					</table></td></tr>\
					</table></div>'
		
		$(".source#new").before(html).fadeIn();
		
		$('input.source#id_src').val('');
		$('input.source#id_descr').val('');
		$('input.source#id_url').val('');
		
		$("select#id_src").append($('<option>', {
			value: s,
			text: s
		}));
	}
}

function get_stock(str) {
	var arr = str.split(" - ");
	company = arr[0].replace("$ ","").split("(")[0]; //company
	ticker = arr[0].split("(")[1].replace(")",""); //ticker
	type = arr[2].split("(")[0]; //type
	exchange = arr[1].split("(")[1].replace(")",""); //exchange
	
	currency = 'USD';
	
	if (exchange == 'SES') {
		currency = 'SGD';
	} else if (exchange == 'HKEX') {
		currency = 'HKD'
	}
	
	type2 = type + ' - ' + exchange + ' - ' + currency
	
	$('tr.sats_article [name="type"]').html(type2);
	$('tr.sats_article [name="ticker"]').html(ticker);
	$('tr.sats_article [name="start_date"]').html(formatDate(0));
	//$('tr.sats_article [name="end_date"]').val(formatDate(3));
	
	delay(function(){
		$('input#stockpick').val(company);
	}, 500 );
	
	$.ajax({
		url : "", // the endpoint
		type : "POST", // http method
		data : {table:'get_current_price',id:ticker}, // data sent with the post request
		
		// handle a successful response
		success : function(json) {
			initial_price = json
			$('tr.sats_article [name="initial_price"]').html(json)
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
}

function formatDate(delta) {
	var d = new Date(),
        month = '' + (d.getMonth() + 1 + delta),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

/*
YUI().use('autocomplete', 'datasource', function (Y) {
	var oDS, acNode = Y.one('#ysearchinput');

	oDS = new Y.DataSource.Get({
		source: "http://d.yimg.com/aq/autoc?query=",
		generateRequestCallback: function (id) {
			YAHOO = {}; 
			YAHOO.util = {}; 
			YAHOO.util.ScriptNodeDataSource = {};
			YAHOO.util.ScriptNodeDataSource.callbacks =	YUI.Env.DataSource.callbacks[id];
			return "&callback=YAHOO.util.ScriptNodeDataSource.callbacks";
			//return "&callback=False";
			//return "";
		}
	});
	
	oDS.plug(Y.Plugin.DataSourceJSONSchema, {
		schema: {
			resultListLocator: "ResultSet.Result",
			resultFields: ["symbol", "name", "exch", "type", "exchDisp", "typeDisp"]
		}
	});
	
	acNode.plug(Y.Plugin.AutoComplete, {
		maxResults: 10,
		activateFirstItem: true,
		resultTextLocator: 'symbol',
		resultFormatter: function (query, results) {
			return Y.Array.map(results, function (result) {
				var asset = result.raw;

				return asset.symbol +
					" " + asset.name +
					" (" + asset.type +
					" - " + asset.exchDisp + ")";
			});
		},
		requestTemplate:  "{query}&region=SG&lang=en-SG",
		source: oDS,
		width: 'auto'
	});
	
	acNode.ac.after('resultsChange', function (e) {
		var newWidth = this.get('boundingBox').get('offsetWidth');
		acNode.setStyle('width', Math.max(newWidth, 100));
	});
});
*/