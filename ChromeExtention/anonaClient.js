// Anona is a chrome extension for chat privacy and security.
// Using a sefisticated AI mechanism Anona can learn one's patterns of behavior
// and Alert when a stranger is using the chat application

const WHATSAPP_WEB_URL = "https://web.whatssapp.com"

function isWhatsappOn(){
	return window.location.href.equals(WHATSAPP_WEB_URL)
}

function sendKeyboadData(event){
	var key = event.keyCode ? event.keyCode : event.which;
	return key
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
				window.onkeyup = sendKeyboadData();

			whatsappWebStatus = isWhatsappOn()
		}
	}
}
