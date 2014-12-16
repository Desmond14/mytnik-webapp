$(document).ready(function() {
    $('#alert_table').DataTable({
		"deferRender": true
	});

    $(".single_row").dblclick(function () {

                    var container_id = $(this).children().eq(6).text();
                    container_id = container_id.replace(/\s+/g, '');
                    var myURL = 'http://127.0.0.1:8000/webint/bills_per_cont/'.concat(container_id);
                    window.open(myURL);
            });

});