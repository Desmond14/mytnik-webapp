$(document).ready(function () {
	
	/*$('#containersWithStatus tfoot th').each( function () {
        var title = $('#containersWithStatus thead th').eq( $(this).index() ).text();
        $(this).html( '<input width="200px" type="text" placeholder="Search '+title+'" />' );
    } );*/
	
    var table = $('#containersWithStatus').DataTable({
        "ajax": "http://127.0.0.1:8000/webint/containers_with_status_datatables",
        "deferRender": true,
        "fnCreatedRow": function (row, aData, iDataIndex) {
            $(row).dblclick(function () {
                    var container_id = $(this).children().eq(1).text();
                    console.log(container_id);
                    var myURL = 'http://127.0.0.1:8000/webint/bills_per_cont/'.concat(container_id);
                    window.open(myURL);
            });
            appendCellsWithButtons($(row));
        }
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

    // Filtering statuses
	$("input[name='None']").change(function() {
		if(this.checked) {
			if($("input[name='InProgress']").prop('checked') == true && $("input[name='Done']").prop('checked') == true) {
				table.column(4).search(' ').draw();
			} else if($("input[name='InProgress']").prop('checked') == true) {
				table.column(4).search('NA|IP', true).draw();
			} else if($("input[name='Done']").prop('checked') == true) {
				table.column(4).search('NA|DO', true).draw();
			} else {
				table.column(4).search('NA').draw();
			}
		} else {
			if($("input[name='InProgress']").prop('checked') == true && $("input[name='Done']").prop('checked') == true) {
				table.column(4).search('IP|DO', true).draw();
			} else if($("input[name='InProgress']").prop('checked') == true) {
				table.column(4).search( 'IP' ).draw();
			} else if($("input[name='Done']").prop('checked') == true){
				table.column(4).search( 'DO' ).draw();
			} else {
				table.column(4).search('$^', true).draw();
			}
			
		}
	});
	
	$("input[name='InProgress']").change(function() {
		if(this.checked) {
			if($("input[name='None']").prop('checked') == true && $("input[name='Done']").prop('checked') == true) {
				table.column(4).search(' ').draw();
			} else if($("input[name='None']").prop('checked') == true) {
				table.column(4).search('IP|NA', true).draw();
			} else if($("input[name='Done']").prop('checked') == true) {
				table.column(4).search('IP|DO', true).draw();
			} else {
				table.column(4).search('IP').draw();
			}
		} else {
			if($("input[name='None']").prop('checked') == true && $("input[name='Done']").prop('checked') == true) {
				table.column(4).search('NA|DO', true).draw();
			} else if($("input[name='None']").prop('checked') == true) {
				table.column(4).search( 'NA' ).draw();
			} else if($("input[name='Done']").prop('checked') == true){
				table.column(4).search( 'DO' ).draw();
			} else {
				table.column(4).search('$^',true).draw();
			}
			
		}
	});
	
	$("input[name='Done']").change(function() {
		if(this.checked) {
			if($("input[name='None']").prop('checked') == true && $("input[name='InProgress']").prop('checked') == true) {
				table.column(4).search(' ').draw();
			} else if($("input[name='None']").prop('checked') == true) {
				table.column(4).search('DO|NA', true).draw();
			} else if($("input[name='InProgress']").prop('checked') == true) {
				table.column(4).search('DO|IP', true).draw();
			} else {
				table.column(4).search('DO').draw();
			}
		} else {
			if($("input[name='None']").prop('checked') == true && $("input[name='InProgress']").prop('checked') == true) {
				table.column(4).search('NA|IP', true).draw();
			} else if($("input[name='None']").prop('checked') == true) {
				table.column(4).search( 'NA' ).draw();
			} else if($("input[name='InProgress']").prop('checked') == true){
				table.column(4).search( 'IP' ).draw();
			} else {
				table.column(4).search('$^', true).draw();
			}
			
		}
	});
	
});

function appendCellsWithButtons($row) {
    $row.append(createEditCell($row));
    $row.append(createSaveCell($row));
    $row.append(createCancelCell($row));
}

function createEditCell($row) {
    return createCellWithButton("Edit", "edit-btn", function () {
        turnOnEditMode($row);
    });
}

function createSaveCell($row) {
    return createCellWithButton("Save", "save-btn", function () {
        saveChanges($row);
        turnOffEditMode($row);
    }).addClass("hidden");
}

function createCancelCell($row) {
    return createCellWithButton("Cancel", "cancel-btn", function () {
        cancelChanges($row);
        turnOffEditMode($row);
    }).addClass("hidden");
}

function createCellWithButton(buttonText, buttonUniqueClass, onClickFunction) {
    var $td = $("<td>");
    var $button = createButton(buttonText, buttonUniqueClass, onClickFunction);
    $td.append($button);
    return $td;
}

function createButton(buttonText, buttonUniqueClass, onClickFunction) {
    var $button = $("<button>");
    $button.addClass("btn btn-primary btn-xs");
    $button.addClass(buttonUniqueClass);
    $button.text(buttonText);
    $button.on("click", onClickFunction);
    return $button;
}

function turnOnEditMode($row) {
    $($row).find(".edit-btn").parent().addClass("hidden");
    $($row).find(".save-btn").parent().removeClass("hidden");
    $($row).find(".cancel-btn").parent().removeClass("hidden");

    var $statusCell = $row.children("td").eq(4);
    $statusCell.html(createContainerStatusSelect($statusCell.text()));

    var $assigneeCell = $row.children("td").eq(5);
    $assigneeCell.html(createAssigneeSelect($assigneeCell.text()));
}

function createContainerStatusSelect(currentStatus) {
    var select = $("<select></select>");
    var status_values = ["", "In progress", "Done"];
    for (var i = 0; i < status_values.length; i++) {
        var val = status_values[i];
        $("<option />", {value: val, text: val}).appendTo(select);
    }
    if (currentStatus == "NA") {
        $(select).val("");
    } else if (currentStatus == "IP") {
        $(select).val("In progress");
    } else {
        $(select).val("Done");
    }
    $(select).attr('data-old', currentStatus);
    return select;
}

function createAssigneeSelect(currentAssignee) {
    var $select = $("<select></select>");
    $("<option />", {value: "None", text: ""}).appendTo($select);
    var usernames = retrieveUsernamesFromDOM();
    for (var i = 0; i < usernames.length; i++) {
        var val = usernames[i];
        var option = $("<option />", {value: val, text: val});
        option.appendTo($select);
    }
    $($select).attr('data-old', currentAssignee);
    $($select).val(currentAssignee);
    return $select;
}

function retrieveUsernamesFromDOM() {
    var divWithUsernames = document.getElementById("usernames");

    var usernames = (divWithUsernames.getAttribute("data-usernames").replace(/&(l|g|quo)t;/g, function (a, b) {
        return {
            l: '<',
            g: '>',
            quo: '"'
        }[b];
    }));

    usernames = usernames.replace(/u'/g, '\'')
    usernames = usernames.replace(/'/g, '\"')
    return JSON.parse(usernames);
}

function turnOffEditMode($row) {
    $($row).find(".edit-btn").parent().removeClass("hidden");
    $($row).find(".save-btn").parent().addClass("hidden");
    $($row).find(".cancel-btn").parent().addClass("hidden");
}

function saveChanges($row) {
    saveContainerStatus($row);
    saveAssignee($row);
}

function saveContainerStatus($row) {
    // Consider retrieving this values from DOM data attribute instead
    var shortcutsToValues = {IP: "In progress", DO: "Done", NA: ""};
    var valuesToShortcuts = {"In progress": "IP", "Done": "DO", "": "NA"};

    var $statusCell = $row.children("td").eq(4);
    var $statusSelect = $statusCell.find(">:first-child");
    var oldStatusValue = shortcutsToValues[$statusSelect.attr("data-old")];

    var currentlySelectedStatus = $statusSelect.find("option:selected").text();
    if (oldStatusValue != currentlySelectedStatus) {
        console.log('Sending request');
        var containerId = $row.children('td').eq(1).text();
        console.log(containerId);
        sendContainerStatusUpdateRequest(valuesToShortcuts[currentlySelectedStatus], containerId)
    } else {
        console.log("Nothing changed");
    }
    $statusCell.html(valuesToShortcuts[currentlySelectedStatus]);
}

function saveAssignee($row) {
    var $assigneeCell = $row.children("td").eq(5);
    var $assigneeSelect = $assigneeCell.find(">:first-child");

    var oldValue = $assigneeSelect.attr("data-old");
    var selected = $assigneeSelect.find("option:selected").text();

    if (oldValue != selected) {
        console.log('sending request');
        var containerId = $row.children('td').eq(1).text();
        console.log(containerId);
        sendAssigneeUpdateRequest(selected, containerId);
    } else {
        console.log("Nothing changed");
    }
    if (selected == "") {
        $assigneeCell.html("None");
    } else {
        $assigneeCell.html(selected);
    }
}

function cancelChanges($row) {
    var $statusCell = $row.children("td").eq(4);
    var $statusSelect = $statusCell.find(">:first-child");
    $statusCell.html($statusSelect.attr("data-old"));

    var $assigneeCell = $row.children("td").eq(5);
    var $assigneeSelect = $assigneeCell.find(">:first-child");
    $assigneeCell.html($assigneeSelect.attr("data-old"));
}

function sendContainerStatusUpdateRequest(selectedStatus, containerId) {
    var theURL = "http://127.0.0.1:8000/webint/containers/status/";

    $.ajax({
        url: theURL,
        data: {
            container: containerId,
            new_status: selectedStatus,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        dataType: "json",
        type: "POST",
        success: function () {
            console.log("success");
        }
    });
}

function sendAssigneeUpdateRequest(selectedAssignee, containerId) {
    var theURL = "http://127.0.0.1:8000/webint/page/0/";
    $.ajax({
        url: theURL,
        data: {
            container: containerId,
            new_assignee: selectedAssignee,
            csrfmiddlewaretoken: $.cookie('csrftoken')
        },
        dataType: "json",
        type: "POST",
        success: function () {
            console.log("success");
        }
    });
}