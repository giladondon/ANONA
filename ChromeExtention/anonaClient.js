// Anona is a chrome extension for chat privacy and security.
// Using a sophisticated AI mechanism Anona can learn one's patterns of behavior
// and Alert when a stranger is using the chat application

alert("Anona AI can now know when you are chatting on whatsapp web")

var context_id = -1;

chrome.input.ime.onFocus.addListener(function(context) {
    context_id = context.contextID;
});

chrome.input.ime.onKeyEvent.addListener(
    function(engineID, keyData) {
        if (keyData.type == "keydown" && keyData.key.match(/^[a-z]$/)) {
            chrome.input.ime.commitText({"contextID": context_id,
                                         "text": keyData.key.toUpperCase()});
            return true;
        } else {
            return false;
        }
});