$( document ).ready(function() {

	console.log("Zaczynamy Ajaxa");
	$("table").tablesorter();

	$( ".single_row" ).dblclick(function() {


		var row_with_data = $(this).text();
		// replacing multiple spaces
		var str_with_no_multiple_spaces = row_with_data.replace(/\s{2,}/g, ' ');
		if( str_with_no_multiple_spaces != " ")
		{
			var unbref = str_with_no_multiple_spaces.split(" ")[1];
			var myURL = 'http://127.0.0.1:8000/webint/unbreference/'.concat(unbref);
		    window.open(myURL,unbref);
		}

	});


    /* NIE UZYWANE
	$("#singmanf").keyup(function (e) {
	    if (e.keyCode == 13) {
	        // Do something
	        var myURL = 'http://127.0.0.1:8000/webint/manifestID/'.concat($(this).val());
	        window.open(myURL,'Singel Manifest');
	    }
	});

    */

	$(".linkbutton").click( function() {

		var theURL = "http://127.0.0.1:8000/webint/page/";
		theURL+=$(this).text();
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

		        for(var i=0 ; i < data.length ; i++)
		        {
		        	var str1 ="#tr_";
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
			        	var str1 ="#tr_";
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
