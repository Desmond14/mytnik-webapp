$(document).ready(function () {

    url1 = "http://127.0.0.1:8000/webint/manifests_datatables";
    url2 = "http://127.0.0.1:8000/webint/containers_datatables";
    url3 = "http://127.0.0.1:8000/webint/bills_datatables";
    url4 = "http://127.0.0.1:8000/webint/bills_per_cont_datatables/" + window.location.pathname.split("/").slice(-2)[0];
    url5 = "http://127.0.0.1:8000/webint/containers_with_status_datatables";

    $('#manifests').DataTable({
        "ajax": url1,
        "deferRender": true
    });

    $('#containers').DataTable({
        "ajax": url2,
        "deferRender": true
    });

    $('#bills').DataTable({
        "ajax": url3,
        "deferRender": true
    });

    $('#billsPerCont').DataTable({
        "ajax": url4,
        "deferRender": true
    });

    $('#containersWithStatus').DataTable({
        "ajax": url5,
        "deferRender": true,
        "fnCreatedRow": function (row, aData, iDataIndex) {
            //add double-click here
            appendCellsWithButtons($(row));
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
    } else {
        console.log("Nothing changed");
    }
    $statusCell.html(valuesToShortcuts[currentlySelectedStatus]);
}

function saveAssignee($row) {
    var $assigneeCell = $row.children("td").eq(5);
    var $assigneeSelect = $assigneeCell.find(">:first-child");

    var old_value = $assigneeSelect.attr("data-old");
    var selected = $assigneeSelect.find("option:selected").text();

    if (old_value != selected) {
        console.log('sending request');
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