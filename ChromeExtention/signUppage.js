function onSignUp(e){
	var mail = document.querySelector('#email').value;
	var pass = document.querySelector('#password').value;
	var confirm = document.querySelector('#confirm-password').value;
	
	if(confirm == pass){
		chrome.runtime.sendMessage({email: mail, password: pass, action: "SIGNUP"});
	}
}


document.querySelector('#sign-up').addEventListener('click', onSignUp)