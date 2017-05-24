function onSignOut(e) {
    chrome.runtime.sendMessage({action: "SIGNOUT"});
    window.location.href = "popUpMain.html";
}


document.querySelector('#sign-out').addEventListener('click', onSignOut);