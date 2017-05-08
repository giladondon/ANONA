function onSignUp(e) {
	var mail = document.querySelector('#email').value,
    pass = document.querySelector('#password').value,
	confirm = document.querySelector('#confirm-password').value;
	
	if (confirm === pass) {
		chrome.runtime.sendMessage({email: mail, password: pass, action: "SIGNUP"});
	}
}


document.querySelector('#sign-up').addEventListener('click', onSignUp);