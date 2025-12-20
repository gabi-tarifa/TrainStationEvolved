var btnSignup = document.getElementById("btnSignup");
var btnLogin = document.getElementById("btnLogin");

btnSignup.addEventListener("click", () => {
    window.location.href='/signup';
});

btnLogin.addEventListener("click", () => {
    window.location.href='/login';
});