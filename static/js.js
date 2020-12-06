function worker() {
    var str_input = $("#strinput").val();
    $.get('/progress/' + str_input, function(data) {
        if (data["status_message"] != 'Done!') {
            $("#bar").attr("aria-valuenow", data["status"]);
            $("#bar").css("width", data["status"] + "%");
            $("#loading_text").text(data["message"]);
            setTimeout(worker, 1500)
        }
    })
}

function loading() {
    $("#loading").show();
    $("#loading_text").show();
    $("#form").hide();
    $("#my_column").removeClass('col-sm');
    $("#my_column").addClass('col-sm-6');
    setTimeout(worker, 1500);
}