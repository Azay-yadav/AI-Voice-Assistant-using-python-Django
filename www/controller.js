$(document).ready(function () {
    // Handle send button click
    $("#SendBtn").click(function () {
        var message = $("#chatbox").val().trim();
        if (message !== "") {
            eel.processQuery(message);  // Send query to Python
            $("#chatbox").val("");    // Clear input field
        }
    });

    // Handle enter key press in input field
    $("#chatbox").keypress(function (e) {
        if (e.which == 13) {  // Enter key
            $("#SendBtn").click();
        }
    });

    // Ensure chat canvas is visible when chat button is clicked
    $("#ChatBtn").click(function () {
        $("#offcanvasScrolling").offcanvas('show');
    });

    // Display Speak Message
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message").text(message);
        $('.siri-message').textillate('start');
    }

    // Display hood
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
                <div class="width-size">
                    <div class="sender_message">${message}</div>
                </div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(receiverText)
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
                <div class="width-size">
                    <div class="receiver_message">${message}</div>
                </div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(hideLoader)
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }

    eel.expose(hideFaceAuth)
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }

    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }

    eel.expose(hideStart)
    function hideStart() {
        $("#Start").attr("hidden", true);
        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");
        }, 1000);
        setTimeout(function () {
            $("#Oval").attr("hidden", false);
        }, 1000);
    }
});