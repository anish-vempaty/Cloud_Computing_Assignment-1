var checkout = {};

// Set your API Gateway Invoke URL here
const API_INVOKE_URL = "https://somethingrandom.execute-api.us-east-1.amazonaws.com/prod/chatbot";

$(document).ready(function () {
    var $messages = $('.messages-content'),
        d, h, m,
        i = 0;

    $(window).on("load", function () {
        $messages.mCustomScrollbar();
        insertResponseMessage("Hi there, I'm your personal Concierge. How can I help?");
    });

    function updateScrollbar() {
        $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
            scrollInertia: 10,
            timeout: 0
        });
    }

    function setDate() {
        d = new Date();
        if (m != d.getMinutes()) {
            m = d.getMinutes();
            $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
        }
    }

    function callChatbotApi(message) {
        console.log("Sending message to API:", message);
        return fetch(API_INVOKE_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: [
                    {
                        type: "unstructured",
                        unstructured: {
                            text: message
                        }
                    }
                ]
            })
        })
        .then(response => response.json());
    }

    function insertMessage() {
        var msg = $('.message-input').val();
        if ($.trim(msg) === '') {
            return false;
        }
        $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        $('.message-input').val(null);
        updateScrollbar();

        callChatbotApi(msg)
            .then((data) => {
                console.log("Chatbot Response:", data);

                if (data.messages && data.messages.length > 0) {
                    console.log("Received " + data.messages.length + " messages");

                    for (var message of data.messages) {
                        if (message.type === "unstructured") {
                            insertResponseMessage(message.unstructured.text);
                        } else if (message.type === "structured" && message.structured.type === "product") {
                            var html = '';
                            insertResponseMessage(message.structured.text);
                            setTimeout(function () {
                                html = '<img src="' + message.structured.payload.imageUrl + '" width="200" height="240" class="thumbnail" /><b>' +
                                    message.structured.payload.name + '<br>$' +
                                    message.structured.payload.price +
                                    '</b><br><a href="#" onclick="' + message.structured.payload.clickAction + '()">' +
                                    message.structured.payload.buttonLabel + '</a>';
                                insertResponseMessage(html);
                            }, 1100);
                        } else {
                            console.log("Message type not implemented:", message);
                            insertResponseMessage("Oops! I didn't understand that.");
                        }
                    }
                } else {
                    insertResponseMessage("Oops, something went wrong. Please try again.");
                }
            })
            .catch((error) => {
                console.error("API Error:", error);
                insertResponseMessage("Sorry, there was an error. Please try again.");
            });
    }

    $('.message-submit').click(function () {
        insertMessage();
    });

    $(window).on('keydown', function (e) {
        if (e.which == 13) {
            insertMessage();
            return false;
        }
    });

    function insertResponseMessage(content) {
        $('<div class="message loading new"><figure class="avatar"><img src="https://media.tenor.com/images/4c347ea7198af12fd0a66790515f958f/tenor.gif" /></figure><span></span></div>').appendTo($('.mCSB_container'));
        updateScrollbar();

        setTimeout(function () {
            $('.message.loading').remove();
            $('<div class="message new"><figure class="avatar"><img src="https://media.tenor.com/images/4c347ea7198af12fd0a66790515f958f/tenor.gif" /></figure>' + content + '</div>').appendTo($('.mCSB_container')).addClass('new');
            setDate();
            updateScrollbar();
            i++;
        }, 500);
    }
});
