function onLogin(e) {
	var mail = document.querySelector('#email').value,
	pass = document.querySelector('#password').value;
	chrome.runtime.sendMessage({email: mail, password: pass, action: "SIGNIN"});
}


document.querySelector('#sign-in').addEventListener('click', onLogin);