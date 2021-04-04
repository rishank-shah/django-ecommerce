const togglePassword1 = document.querySelector('#togglePassword1');
	const password = document.querySelector('#password');
	togglePassword1.addEventListener('click', function (e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
});
	