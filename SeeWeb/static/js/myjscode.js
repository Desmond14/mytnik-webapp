$( document ).ready(function() {
    console.log( "ready!" );
    console.log("Here we go!");
    $("table").tablesorter();
    $("#Bill_table").hide()
    $("#Container_table").hide();

    $("#nav_cont").click( function() {

        $("#Bill_table").hide();
        $("#Container_table").show();

    });

    $("#nav_bill").click( function() {
        
        $("#Container_table").hide();
        $("#Bill_table").show();

    });

    var currentdisplay = "xxxxxxxxxxxxxxxxxxxxxxxx";
    $("tr.success > td:first-child").click( function () {
    		//alert($(this).text())


    		var str1 ="#id_";
			var str2 = $(this).text();
			str1+=str2;
            var news=str1.replace(" ", "");

            if( currentdisplay != news )
            {               
                $(currentdisplay).hide();
                $(news).show();
                currentdisplay = news;
            }

    });

});