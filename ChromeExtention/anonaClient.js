// Anona is a chrome extension for chat privacy and security.
// Using a sophisticated AI mechanism Anona can learn one's patterns of behavior
// and Alert when a stranger is using the chat application.

function sendKey(keyCode, timeStamp) {
	chrome.runtime.sendMessage({key: keyCode, time: timeStamp});
}

function onKeyDown(event) {
	// Take only keys that are not characters
	var keyCode = event.keyCode, date = new Date();
	if (keyCode > 7 && keyCode < 47) {
		console.log("keyDown: " + keyCode);
		sendKey(keyCode, generateDate(date));
	}
}

function generateDate(date) {
	return date.getHours() + " " + date.getMinutes() + " " + date.getSeconds() + " " + date.getMilliseconds() + " " + date.getDate() + " " + (date.getMonth()+1) + " " + date.getFullYear();
}

function onKeyPress(event) {
	// Take only keys that are characters
	var keyCode = event.keyCode;
	var date = new Date();
	if (keyCode > 33 && keyCode < 126){
		console.log("keyPress: " + keyCode);
		sendKey(keyCode, generateDate(date));
	}
	else if (keyCode > 1487 && keyCode < 1510){
		console.log("keyPress(Hebrew): " + keyCode);
		sendKey(keyCode, generateDate(date));
	}
}

function run() {
	var target = document.getElementById("app");
	
	var observer = new MutationObserver(
		function() {
			if (document.getElementById("main")){
				document.getElementById("main").addEventListener("keypress", onKeyPress);
				document.getElementById("main").addEventListener("keydown", onKeyDown);
			}
		}
	);

	var config = {childList: true, subtree: true, charecterData: true};
	
	observer.observe(target, config);
}

window.onload = run;