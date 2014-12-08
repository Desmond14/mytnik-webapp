$(document).ready(function() {

	url1 = "/webint/manifests_datatables";
	url2 = "/webint/containers_datatables";
	url3 = "/webint/bills_datatables";
	url4 = "/webint/bills_per_cont_datatables/" + window.location.pathname.split("/").slice(-2)[0];
	
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
});