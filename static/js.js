function worker() {
    var str_input = $("#strinput").val();
    $.get('/progress/' + str_input, function(data) {
        if (data["status_message"] != 'Done!') {
            window.alert(data["status"]);
            $("#bar").attr("aria-valuenow", data["status"]);
            $("#bar").css("width", data["status"] + "%");
            setTimeout(worker, 1000)
        }
    })
}

function loading() {
    $("#loading").show();
    $("#form").hide();
    setTimeout(worker, 1000);
    // setTimeout(function () {
    //     $.get('/progress/' + str_input, function (data) {
    //         window.alert(data);
    //         // if (progress < 100) {
    //         //     progress_bar.set_progress(progress)
    //         //     setTimeout(worker, 1000)
    //         // }
    //     })
    // }, 2000)
}