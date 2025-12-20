function temMaiuscula(str) {
    return /[A-Z]/.test(str);
}

function temMinuscula(str) {
    return /[a-z]/.test(str);
}

function temNumero(str) {
    return /\d/.test(str);
}

function temCaractereEspecial(str) {
    return /[!@#$%^&*(),.?":{}|<>]/.test(str);
}

function emailValido(str) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str);
}
document.addEventListener("DOMContentLoaded", ()=>{
    var texto = document.getElementById("textoerro");
    var btnCadastrar = document.getElementById("btnCadastrar");
    btnCadastrar.addEventListener("click", async () => {
        var nickname = document.getElementById("getNick").value;
        var email = document.getElementById("getEmail").value;
        var password = document.getElementById("getPass").value;
        var confirmPass = document.getElementById("getConfirmPass").value;
        var language = document.getElementById("getLang").value;

        if (!nickname || !email || !password || !confirmPass || !language){
            texto.textContent = "Por favor, preencha todos os dados corretamente";
            return;
        }

        if(!emailValido(email)){
            texto.textContent = "Por favor insira um endereço de email válido (email@exemplo.com)";
            return
        }

        if(password.length < 6 || password.length > 24 || !temMaiuscula(password) || !temMinuscula(password) || !temNumero(password) || !temCaractereEspecial(password)) {
            texto.innerHTML = "Um dos seguintes requisitos não foi cumprido: <br>- A senha tem que ser maior que 8 dígitos e menor que 24 dígitos;<br>- A senha deve conter pelo menos uma letra maiúscula;<br>- A senha deve conter pelo menos uma letra minúscula;<br>- A senha deve conter pelo menos um número;<br>- A senha deve conter pelo menos um caractere especial.";
            return;
        }
        
        if(confirmPass != password){
            texto.textContent = "As senhas não condizem!";
            return;
        }

        try {
            const response = await fetch("/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ nickname, email, password, language })
            });

            if (response.ok) {
                window.location.href = "/login"; // Redireciona após cadastro
            }
        } catch (error) {
            texto.textContent = "Erro ao cadastrar:", error;
        }

    })
});

document.addEventListener("DOMContentLoaded", ()=>{
    var texto = document.getElementById("textoerro");
    var btnLogin = document.getElementById("btnLogin");
    btnLogin.addEventListener("click", async () => {
        var email = document.getElementById("getEmail").value;
        var password = document.getElementById("getPass").value;

        
        if (!email || !password){
            texto.textContent = "Por favor, preencha todos os dados corretamente";
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                window.location.href = "/"; // Redireciona após cadastro
            } else {
                texto.textContent = "Não foi possível encontrar o usuário, tente novamente";
                email.focus();
            }
        } catch (error) {
                texto.textContent = "Falha na conexão. Tente novamente mais tarde";
        }
    })
});