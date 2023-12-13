$(".video-checkbox").on("click", function () {
    console.log("clicked");
    let link = $(this).parent().find(".video-url").val();
    let requestData = {links: link}; // Data formatted to match your endpoint
    
    let selectedCount = $("#count-selected");
    if ($(this).is(":checked")) {
        selectedCount.text(parseInt(selectedCount.text()) + 1);
    } else {
        selectedCount.text(parseInt(selectedCount.text()) - 1);
    }

    sendRequest("/check", requestData, "POST")
});


$("#videoCheckbox").on("click", function () {
    console.log("clicked");
    let button = $(this);
    let checked = button.is(":checked");
    let requestData = {value: checked, setting: "onlyAudio"};
    console.log(requestData)

    sendRequest("/settings", requestData, "POST")
});


$("#download").on("click", function () {

    let btn = $(this);
    let input = btn.parent().find(".url-input");
    let urlInput = input.val();
    input.val("");
    let requestData = {links: urlInput};

    sendRequest("/download", requestData, "POST")
});

$("#add").on("click", function () {
    let btn = $(this);
    let input = btn.parent().find(".url-input");
    let urlInput = input.val();
    input.val("");

    let requestData = {links: urlInput};

    sendRequest("/add", requestData, "POST")
    window.location.reload();
});


function sendRequest(url, data, method) {
    $.ajax({
        url: url,
        type: method,
        data: data,
        success: function (data) {
            console.log(data);
            return data;
        },
        error: function (error) {
            console.error("Error:", error);
            return error;
        }
    });
}


function updateProgress() {
    $.ajax({
        url: '/progress',
        method: 'post',
        success: function (data) {
            console.log(data);
            if (data["progress"] !== data["total"]) {
                // $("#in-progress-blocker").show();
                // $("#in-progress-title").text("Precessed " + data["progress"] + " of " + data["total"] + " videos");
                // $("#in-progress-bar").width(data["progress"] / data["total"] * 100 + "%");
                window.location.reload();
            } else if ($("#in-progress-blocker").is(":visible")) {
                window.location.reload();
            }
        }
    });
}


setInterval(function () {
    updateProgress();
}, 1000);

