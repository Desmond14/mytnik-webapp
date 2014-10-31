$(document).ready(function() {

	url1 = "http://127.0.0.1:8000/webint/manifests_datatables";
	url2 = "http://127.0.0.1:8000/webint/containers_datatables";
	url3 = "http://127.0.0.1:8000/webint/bills_datatables";
	url4 = "http://127.0.0.1:8000/webint/bills_per_cont_datatables/" + window.location.pathname.split("/").slice(-2)[0];
	url5 = "http://127.0.0.1:8000/webint/containers_with_status_datatables";
	
	$('#manifests').DataTable({
		"ajax" : url1,
		"deferRender": true
	});

	$('#containers').DataTable({
		"ajax" : url2,
		"deferRender": true
	});

	$('#bills').DataTable({
		"ajax" : url3,
		"deferRender": true
	});
	
	$('#billsPerCont').DataTable({
		"ajax" : url4,
		"deferRender": true
	});
	
	// Setup - add a text input to each footer cell
    $('#containersWithStatus tfoot th').each( function () {
        var title = $('#containersWithStatus thead th').eq( $(this).index() ).text();
        $(this).html( '<input width="200px" type="text" placeholder="Search '+title+'" />' );
    } );
	
	var table = $('#containersWithStatus').DataTable({
		"ajax" : url5,
		"deferRender": true
	});
	
	// Apply the search
    table.columns().eq( 0 ).each( function ( colIdx ) {
        $( 'input', table.column( colIdx ).footer() ).on( 'keyup change', function () {
            table
                .column( colIdx )
                .search( this.value )
                .draw();
        } );
    } );
    
    //TODO To jest jeszcze do zrobienia
	/*$(':checkbox').click(function() {
		table.column( 4 ).search( 'NA' ).draw();
	});*/
    

});