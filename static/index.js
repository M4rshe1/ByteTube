$(".video-checkbox").on("click", function () {
    console.log("clicked");
    let link = $(this).parent().find(".video-url").val();
    let requestData = {links: link}; // Data formatted to match your endpoint

    $.ajax({
        url: "/check",
        type: "POST",
        data: requestData, // Sending data in the format expected by the endpoint
        success: function (data) {
            console.log(data);
            // Handle the response as needed
        },
        error: function (error) {
            console.error("Error:", error);
            // Handle errors, if any
        }
    });
});


$("#videoCheckbox").on("click", function () {
    console.log("clicked");
    let button = $(this);
    let checked = button.is(":checked");
    let requestData = {value: checked, setting: "onlyAudio"};
    console.log(requestData)

    $.ajax({
        url: "/settings",
        type: "POST",
        data: requestData,
        success: function (data) {
            console.log(data);
            // Handle the response as needed
        },
        error: function (error) {
            console.error("Error:", error);
            // Handle errors, if any
        }
    });
});
let submitted = false;
$("#add-form").on("submit", function (event) {
    if (submitted) {
        
    event.preventDefault(); // Prevent the default form submission behavior

    let form = $(this);
    let urlInput = form.find(".url-input").val();
    let btn = $(event.target)
    console.log(btn)
    
    
    if (btn.hasClass("add-btn")) {
        form.action = "/add"
    } else if (btn.hasClass("download-directly-btn")) {
        form.action = "/download"
    }

    if (urlInput !== "") {
        
        form.submit()
        submitted = true;
    }
    }
});

