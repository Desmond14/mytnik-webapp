$(document).on('dblclick', '.single_row', function() {

    	var row_with_data = $(this).text();
		// replacing multiple spaces
		var str_with_no_multiple_spaces = row_with_data.replace(/\s{2,}/g, ' ');
		console.log(str_with_no_multiple_spaces);
		if( str_with_no_multiple_spaces != " ")
		{
			var contid = str_with_no_multiple_spaces.split(" ")[2];
			console.log(contid);
			var myURL = 'http://127.0.0.1:8000/webint/bills_per_cont/'.concat(contid);
		    //window.open(myURL,unbref);
		    window.open(myURL);
		}

});