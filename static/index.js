$(".video-checkbox").on("click", function () {
    // console.log("clicked");
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
    // console.log("clicked");
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


$(".download-this-btn").on("click", function () {
    let btn = $(this);
    let url = btn.parent().find(".video-url").val();
    let requestData = {links: url};

    sendRequest("/download", requestData, "POST")
});

$("#import-btn").on("click", function () {
    let btn = $(this);
    let checkbox = btn.parent().find(".file-input-checkbox");
    let form = btn.parent()
    let fileInput = btn.parent().find(".file-input");
//     open file dialog WITH ONLY txt, json and csv files
    fileInput.attr("accept", ".txt,.json,.csv");
    fileInput.click();
    fileInput.on("change", function () {
        let delete_before_import = confirm("Do you want to delete all videos before import?")
        if (delete_before_import) {
            checkbox.prop("checked", true);
        } else {
            checkbox.prop("checked", false);
        }
        form.submit();
    })

});

$(".export-button").on("click", async function () {
        let btn = $(this);
        let file_type = btn.attr("file");
        let res = await sendRequest("/export", {convert: file_type}, "POST")
        console.log(res)
        
        if (res.status === 200) {
            createMessage(res.message, "Success");
        } else if (res.status === 500) {
            createMessage(res.message, "Error");
        }
    }
);


async function sendRequest(url, data, method) {
    let res;
    await $.ajax({
        url: url,
        type: method,
        data: data,
        success: function (respond) {
            res = respond;
        },
        error: function (error) {
            res = error;
        }
    });
    return res;
}


function updateProgress() {
    $.ajax({
        url: '/progress',
        method: 'post',
        success: function (data) {
            // console.log(data);
            if (data["progress"] !== data["total"]) {
                // $("#in-progress-blocker").show();
                // $("#in-progress-title").text("Precessed " + data["progress"] + " of " + data["total"] + " videos");
                // $("#in-progress-bar").width(data["progress"] / data["total"] * 100 + "%");
                window.location.reload();
            } else if ($("#in-progress-blocker").is(":visible")) {
                window.location.reload();
            }
        },
        error: function (error) {
            createMessage("You have lost connection to the server.", "Warning");
        }
    });
}


function createMessage(msg, type) {
    let messageBox = $("#messages");
    let message = $("<div></div>").addClass("message-box").addClass("message-" + type);
    let messageHeader = $("<div></div>").addClass("message-header");
    let messageTitle = $("<div></div>").addClass("message-box-title").text(type);
    let messageIcons = $("<div></div>").addClass("message-icons");
    let messageText = $("<div></div>").addClass("message-box-text").text(msg);
    let messageInfoIcon = $("<i></i>").addClass("fa-solid").addClass("fa-circle-info").addClass("message-Info-icon").addClass("message-icon");
    let messageErrorIcon = $("<i></i>").addClass("fa-solid").addClass("fa-circle-exclamation").addClass("message-Error-icon").addClass("message-icon");
    let messageWarningIcon = $("<i></i>").addClass("fa-solid").addClass("fa-triangle-exclamation").addClass("message-Warning-icon").addClass("message-icon");
    let messageSuccessIcon = $("<i></i>").addClass("fa-solid").addClass("fa-circle-check").addClass("message-Success-icon").addClass("message-icon");
    
    messageHeader.append(messageTitle);
    messageHeader.append(messageIcons);
    messageIcons.append(messageInfoIcon);
    messageIcons.append(messageErrorIcon);
    messageIcons.append(messageWarningIcon);
    messageIcons.append(messageSuccessIcon);
    message.append(messageHeader);
    message.append(messageText);
    messageBox.append(message);
    setTimeout(function () {
        message.fadeOut(1000);
        setTimeout(function () {
            message.remove();
        }, 1000);
    }, 5000);
}


setInterval(function () {
    updateProgress();
}, 1000);



