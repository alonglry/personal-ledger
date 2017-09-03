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
function update_post(_table,_id,_column,_value) {
	if (_table == 'tables') {
		var name = 'all_tables';
	} else if (_table == 'columns') {
		var name = 'all_table_columns'
	} else if (_table == 'functions') {
		var name = 'all_table_functions'
	}
	
	$.ajax({
		url : location.protocol + '//' + location.host + '/tables/', // the endpoint
		type : "POST", // http method
		data : {table:_table,id:_id,column:_column,value:_value}, // data sent with the post request $('#post-text').val()
		// handle a successful response
		
		success : function(json) {
			//console.log(_id + ' ' + name + ' field ' + _column + ' value is ' + _value);
			console.log(json);
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
};

function delete_post(_table,_id) {
	if (_table == 'tables') {
		var name = 'all_tables';
	} else if (_table == 'columns') {
		var name = 'all_table_columns'
	}
	
	$.ajax({
		url : location.protocol + '//' + location.host + '/tables/', // the endpoint
		type : "POST", // http method
		data : {table:_table,id:_id,value:'delete'}, // data sent with the post request $('#post-text').val()
		// handle a successful response
		
		success : function(json) {
			//console.log(_id + ' in ' + name + ' deleted');
			console.log(json);
			remove(_id,_table);
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
};

//create new table or column
function create_post(_table) {
	if (_table == 'tables') {
		p = $('input.new[name="project"]').val();
		f = $('input.new[name="model_file_name"]').val();
		t = $('input.new[name="table_name"]').val();
		v = $('input.new[name="verbose_name"]').val();
		vp = $('input.new[name="verbose_name_plural"]').val();
		o = $('input.new[name="ordering"]').val();
		d = $('input.new[name="definition"]').val();
		m = $('input.new[name="model_form"]').val();
		u = $('input.new[name="unicode"]').val();
		b = $('input.new[name="backup"]').val();
		r = $('input.new[name="retention_d"]').val();
		
		var d ={table:'tables',id:'new',project:p,model_file_name:f,table_name:t,verbose_name:v,verbose_name_plural:vp,ordering:o,definition:d,model_form:m,unicode:u,backup:b,retention_d:r};
	} else if (_table == 'columns') {		
		pj = $('td[name="project"]').not('.new').text();
		mfn = $('td[name="model_file_name"]').not('.new').text();
		tn = $('td[name="table_name"]').not('.new').text();
		
		s= $('td.new[name="sn"]').text();
		c = $('td.new[name="column_name"]').text();
		v = $('td.new[name="verbose_name"]').text();
		vp = $('td.new[name="verbose_name_plural"]').text();
		d = $('td.new[name="definition"]').text();
		dv = $('td.new[name="default_value"]').text();
		co = $('td.new[name="choice_options"]').text();
		dt = $('td.new[name="data_type"]').text();
		mil = $('td.new[name="min_length"]').text();
		mal = $('td.new[name="max_length"]').text();
		dp = $('td.new[name="decimal_place"]').text();
		p = $('td.new[name="path"]').text();
		n = $('td.new[name="nullable"]').text();
		b = $('td.new[name="blank"]').text();
		uk = $('td.new[name="unique_key"]').text();
		mf = $('td.new[name="model_form"]').text();
		fkt = $('td.new[name="foreign_key_table"]').text();
		fkc = $('td.new[name="foreign_key_column"]').text();
		fkod = $('td.new[name="foreign_key_on_delete"]').text();
		asfk = $('td.new[name="auto_save_foreign_key"]').text();
		
		var d ={table:'columns',id:'new',project:pj,model_file_name:mfn,table_name:tn,sn:s,column_name:c,verbose_name:v,verbose_name_plural:vp,definition:d,default_value:dv,choice_options:co,data_type:dt,min_length:mil,max_length:mal,decimal_place:dp,path:p,nullable:n,blank:b,unique_key:uk,model_form:mf,foreign_key_table:fkt,foreign_key_column:fkc,foreign_key_on_delete:fkod,auto_save_foreign_key:asfk,model_form:mf};
	} else if (_table == 'functions') {
		pj = $('td[name="project"]').not('.new').text();
		mfn = $('td[name="model_file_name"]').not('.new').text();
		tn = $('td[name="table_name"]').not('.new').text();
		v = $('textarea#new').val();
		
		var d = {table:'functions',id:'new',project:pj,model_file_name:mfn,table_name:tn,value:v};
	} else if (_table == 'files') {
		pj = $('td[name="project"]').not('.new').text();
		mfn = $('td[name="model_file_name"]').not('.new').text();
		tn = $('td[name="table_name"]').not('.new').text();
		
		var d = {table:'files',id:'new',project:pj,model_file_name:mfn,table_name:tn};
		
		$('#message').html('<p>model file saving <i class="fa fa-spinner fa-spin fa-fw" aria-hidden="true"></i></p>');
	}
	
	$.ajax({
		url : location.protocol + '//' + location.host + '/tables/', // the endpoint
		type : "POST", // http method
		data : d, // data sent with the post request
		
		// handle a successful response
		success : function(json) {
			if (_table == 'tables') {
				console.log(p + '/' + f + '/' + t + ' table created');
				console.log(json);
				add(json,_table);
			} else if (_table == 'files') {
				console.log(pj + '/' + mfn + '/' + tn + ' file created');
				console.log(json);
				if (String(json) == "success\n") {
					$('#message').html('<p>model file updated <i class="fa fa-check" aria-hidden="true"></i></p>');
				} else {
					$('#message').html("<p>"+String(json)+"</p>");
				}
			} else {
				console.log(_table + ' created');
				console.log(json);
				add(json,_table);	
			}
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			console.log(xhr);
			
			$('#message').html("<p>"+err+"</p>");
			//$('#message').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
			//	" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			//console.log(xhr.status + ": " + xhr.responseText + " " + errmsg); // provide a bit more info about the error to the console
		}
	});
};

function remove(id,attr) {
	if (attr=='block') {
		$("div.block#".concat(id).concat(".block")).fadeOut()
	} else if (attr=='columns') {
		$("tr#".concat(id)).fadeOut()
	}
}

function add(json,attr) {
	if (attr=='tables') {
		var o = JSON.parse(json);
		html = '<fieldset>\
		        <legend>'+o.project+' - <b>'+o.model_file_name+'</b></legend>\
				<div class="block" id="'+o.id+'">\
				<table><tr>\
				<th nowrap style="background-color: burlywood;">project</th>\
				<th nowrap>model file name</th>\
				<th nowrap>table name</th>\
				<th nowrap>verbose name</th>\
				<th nowrap>plural</th>\
				<th nowrap>ordering</th>\
				<th nowrap>definition</th>\
				<th nowrap>form</th>\
				<th nowrap>unicode</th>\
				<th nowrap>backup</th>\
				<th nowrap>keep days</th><td></td></tr>\
				<tr class="hovercolor">\
				<td nowrap contenteditable id="'+o.id+'" name="project" tab="tables">'+o.project+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="model_file_name" tab="tables">'+o.model_file_name+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="table_name" tab="tables" style="background-color: gainsboro;">'+o.table_name+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="verbose_name" tab="tables">'+o.verbose_name+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="verbose_name_plural" tab="tables">'+o.verbose_name_plural+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="ordering" tab="tables">'+o.ordering+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="definition" tab="tables">'+o.definition+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="model_form" tab="tables">'+o.model_form+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="unicode" tab="tables">'+o.unicode+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="backup" tab="tables">'+o.backup+'</td>\
				<td nowrap contenteditable id="'+o.id+'" name="retention_d" tab="tables">'+o.retention_d+'</td>\
				<td nowrap>\
				<i class="fa fa-expand" aria-hidden="true" data-toggle="collapse" data-target="#{{ t.id }}.collapse" id="'+o.id+'"></i>\
				<a href="/tables/{{ t.table_name }}" target="_blank" style="color: inherit;"><i class="fa fa-external-link" aria-hidden="true"></i></a>\
				</td>\
				</tr></table></fieldset>'
		
		$('fieldset:last').before(html);
		
		$('input.new').val('');

	} else if (attr=='columns') {
		var o = JSON.parse(json);
		
		html = '<tr class="hovercolor" id="'+o.id+'">\
				<td nowrap contenteditable id="'+o.id+'" name="sn" tab="columns">'+o.sn+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="column_name" tab="columns">'+o.column_name+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="verbose_name" tab="columns">'+o.verbose_name+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="verbose_name_plural" tab="columns">'+o.verbose_name_plural+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="definition" tab="columns">'+o.definition+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="default_value" tab="columns">'+o.default_value+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="choice_options" tab="columns">'+o.choice_options+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="data_type" tab="columns">'+o.data_type+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="min_length" tab="columns">'+o.min_length+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="max_length" tab="columns">'+o.max_length+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="decimal_place" tab="columns">'+o.decimal_place+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="path" tab="columns">'+o.path+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="nullable" tab="columns">'+o.nullable+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="blank" tab="columns">'+o.blank+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="unique_key" tab="columns">'+o.unique_key+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="model_form" tab="columns">'+o.model_form+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="foreign_key_table" tab="columns">'+o.foreign_key_table+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="foreign_key_column" tab="columns">'+o.foreign_key_column+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="foreign_key_on_delete" tab="columns">'+o.foreign_key_on_delete+'</td>\
			    <td nowrap contenteditable id="'+o.id+'" name="auto_save_foreign_key" tab="columns">'+o.auto_save_foreign_key+'</td>\
			    <td nowrap><i id="'+o.id+'" class="fa fa-trash-o delete" aria-hidden="true" tab="columns"></i></td>\
			    </tr>'
		$('table#columns tr:last').before(html);
		
		$('td.new').text('');
	} else if (attr == 'functions') {
		var o = JSON.parse(json);
		$('textarea#new').attr("id",o.id);
	}
}

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();