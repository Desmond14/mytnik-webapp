$( document ).ready(function() {

		$("table").tablesorter();

		$(".contlinkbutton").click( function() {

		var theURL = "http://127.0.0.1:8000/webint/ajax/cont/".concat($('#storeID').text()).concat('/page/').concat($(this).text());
		console.log(theURL);

		
		$.ajax({
	    // the URL for the request
		    //url: "webint/page/1/",
		    url: theURL,

		    // whether this is a POST or GET request
		    type: "GET",
		 	 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: function( data ) {

		    	console.log(data.length);
		    	console.log(data[0].length);
		        for(var i=0 ; i < data.length ; i++)
		        {
		        	var str1 ="#cont_tr_";
		        	var str2 =i;
		        	var str3 =str1.concat(str2);
		        	//var id = "#tr_"+toString(i)+"_td_";
		        	var id = str3.concat("_td_");
		        	for(var j=0 ; j < 13 ; j++)
		        	{
		        		var current = id.concat(j);
		        		$(current).text(data[i][j]);
		        	}
		        }

		        /////////// Clearing if we didnt get 20 rows
		        if(data.length != 20)
		        {

		        	for(var i=data.length ; i < 20 ; i++)
			        {
			        	var str1 ="#cont_tr_";
			        	var str2 =i;
			        	var str3 =str1.concat(str2);
			        	//var id = "#tr_"+toString(i)+"_td_";
			        	var id = str3.concat("_td_");
			        	for(var j=0 ; j < 13 ; j++)
			        	{
			        		var current = id.concat(j);
			        		$(current).text("");
			        	}
			        }
		        }

		        $("table").trigger("update"); 
		    },
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		}); 
	});


		$(".linkbutton").click( function() {

		var theURL = "http://127.0.0.1:8000/webint/ajax/id/".concat($('#storeID').text()).concat('/page/').concat($(this).text());
		console.log(theURL);

		
		$.ajax({
	    // the URL for the request
		    //url: "webint/page/1/",
		    url: theURL,

		    // whether this is a POST or GET request
		    type: "GET",
		 	 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: function( data ) {

		    	console.log(data.length);
		    	console.log(data[0].length);
		        for(var i=0 ; i < data.length ; i++)
		        {
		        	var str1 ="#bill_tr_";
		        	var str2 =i;
		        	var str3 =str1.concat(str2);
		        	//var id = "#tr_"+toString(i)+"_td_";
		        	var id = str3.concat("_td_");
		        	for(var j=0 ; j < 12 ; j++)
		        	{
		        		var current = id.concat(j);
		        		$(current).text(data[i][j]);
		        	}
		        }

		        /////////// Clearing if we didnt get 20 rows
		        if(data.length != 20)
		        {

		        	for(var i=data.length ; i < 20 ; i++)
			        {
			        	var str1 ="#bill_tr_";
			        	var str2 =i;
			        	var str3 =str1.concat(str2);
			        	//var id = "#tr_"+toString(i)+"_td_";
			        	var id = str3.concat("_td_");
			        	for(var j=0 ; j < 12 ; j++)
			        	{
			        		var current = id.concat(j);
			        		$(current).text("");
			        	}
			        }
		        }

		        $("table").trigger("update"); 
		    },
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		}); 
	});


});