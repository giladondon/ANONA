// Anona is a chrome extension for chat privacy and security.
// Using a sophisticated AI mechanism Anona can learn one's patterns of behavior
// and Alert when a stranger is using the chat application

const WHATSAPP_WEB_URL = "https://web.whatssapp.com"

function isWhatsappOn(){
    chrome.tabs.getSelected(null, function(tab) {
            tab = tab.id;
            tabUrl = tab.url;

            return tab.url.equals(WHATSAPP_WEB_URL)
    });
}

function sendKeyboardData(event){
	var key = event.keyCode ? event.keyCode : event.which;
	alert(key)
	return key
}

function getTabUrl(tab){
    console.log(tab.url)
    return tab.url
}


function main() {
	whatsappWebStatus = isWhatsappOn()

	while (true){
		if (whatsappWebStatus != isWhatsappOn()) {
			if (whatsappWebStatus){
				window.onkeyup = function(e){
					e.preventDefault();
				}
			}
			else
				window.onkeyup = sendKeyboardData;

			whatsappWebStatus = isWhatsappOn()
		}
	}
}

console.log("START DEBUGGING")
chrome.tabs.getSelected(null, function(tab) {
        tab = tab.id;
        tabUrl = tab.url;

        console.log(tab.url);
    });
main()
