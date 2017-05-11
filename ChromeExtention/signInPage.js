function onLogin(e) {
	var mail = document.querySelector('#email').value,
	pass = document.querySelector('#password').value;
	chrome.runtime.sendMessage({email: mail, password: pass, action: "SIGNIN"}).then(function (){
            window.location.href = "signOutPage.html";
        });
}


document.querySelector('#sign-in').addEventListener('click', onLogin);