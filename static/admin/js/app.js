// Selecionar o botão de alternância de modo
const toggleDarkModeButton = document.getElementById('toggle-dark-mode');
const darkModeClass = 'dark-mode';

// Atualizar ícone e classe do botão com base no estado do modo
const updateButton = () => {
    if (document.body.classList.contains(darkModeClass)) {
        toggleDarkModeButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-brightness-high-fill" viewBox="0 0 16 16">
                <path d="M12 8a4 4 0 1 1-8 0 4 4 0 0 1 8 0M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/>
            </svg>`;
        toggleDarkModeButton.classList.replace('btn-dark', 'btn-light');
    } else {
        toggleDarkModeButton.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="yellow" class="bi bi-moon-stars-fill" viewBox="0 0 16 16">
                <path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/>
                <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.73 1.73 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.73 1.73 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.73 1.73 0 0 0 1.097-1.097zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.16 1.16 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.16 1.16 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732z"/>
            </svg>`;
        toggleDarkModeButton.classList.replace('btn-light', 'btn-dark');
    }
};

// Verificar no localStorage se o modo escuro está ativado
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add(darkModeClass);
}

// Atualizar o botão ao carregar a página
updateButton();

// Alternar entre os modos e salvar no localStorage
toggleDarkModeButton.addEventListener('click', () => {
    document.body.classList.toggle(darkModeClass);
    localStorage.setItem('darkMode', document.body.classList.contains(darkModeClass) ? 'enabled' : 'disabled');
    updateButton();
});

// Garante que a mensagem de erro seja exibida pelo modal.
document.addEventListener('DOMContentLoaded', function() {
    const errorData = document.getElementById('error-data');
    
    if (errorData) {
        const errorMessage = errorData.getAttribute('data-error');
        
        if (errorMessage) {
            // Exibe o modal com a mensagem de erro
            const modal = new bootstrap.Modal(document.getElementById('errorModal'));
            document.getElementById('errorMessage').innerText = errorMessage;
            modal.show();
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");

    form.addEventListener("submit", (event) => {
        let isValid = true;
        
        // Validação do Nome de Usuário
        const username = document.getElementById("id_username");
        const usernameRegex = /^[a-zA-Z0-9]+$/; // Apenas letras e números
        if (!usernameRegex.test(username.value)) {
            username.classList.add("is-invalid");
            isValid = false;
        } else {
            username.classList.remove("is-invalid");
        }

        // Validação da Senha
        const password1 = document.getElementById("id_password1");
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$/;
        if (!passwordRegex.test(password1.value)) {
            password1.classList.add("is-invalid");
            isValid = false;
        } else {
            password1.classList.remove("is-invalid");
        }

        // Confirmação da Senha
        const password2 = document.getElementById("id_password2");
        if (password1.value !== password2.value) {
            password2.classList.add("is-invalid");
            isValid = false;
        } else {
            password2.classList.remove("is-invalid");
        }

        // Impedir o envio se houver erros
        if (!isValid) {
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const passwordField = document.getElementById("id_password1");
    const passwordRequirements = document.getElementById("passwordRequirements");
    const minLength = document.getElementById("minLength");
    const uppercase = document.getElementById("uppercase");
    const number = document.getElementById("number");
    const specialChar = document.getElementById("specialChar");

    const togglePassword1 = document.getElementById("togglePassword1");
    const passwordIcon1 = document.getElementById("passwordIcon1");

    // Função para verificar se a senha atende aos requisitos
    function validatePassword() {
        const password = passwordField.value;

        // Requisito: ao menos 8 caracteres
        if (password.length >= 8) {
            minLength.classList.remove("text-danger");
            minLength.classList.add("text-success");
        } else {
            minLength.classList.remove("text-success");
            minLength.classList.add("text-danger");
        }

        // Requisito: pelo menos uma letra maiúscula
        if (/[A-Z]/.test(password)) {
            uppercase.classList.remove("text-danger");
            uppercase.classList.add("text-success");
        } else {
            uppercase.classList.remove("text-success");
            uppercase.classList.add("text-danger");
        }

        // Requisito: pelo menos um número
        if (/\d/.test(password)) {
            number.classList.remove("text-danger");
            number.classList.add("text-success");
        } else {
            number.classList.remove("text-success");
            number.classList.add("text-danger");
        }

        // Requisito: pelo menos um caractere especial
        if (/[@#$%^&+=]/.test(password)) {
            specialChar.classList.remove("text-danger");
            specialChar.classList.add("text-success");
        } else {
            specialChar.classList.remove("text-success");
            specialChar.classList.add("text-danger");
        }
    }

    // Chamando a função de validação enquanto o usuário digita a senha
    passwordField.addEventListener("input", validatePassword);

    // Alternando a visibilidade da senha
    togglePassword1.addEventListener("click", function() {
        // Alterna o tipo do campo de senha
        const type = passwordField.type === "password" ? "text" : "password";
        passwordField.type = type;

        // Alterando o texto do botão (modificar conforme seu CSV)
        if (passwordField.type === "password") {
            togglePassword1.innerHTML =  `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-eye" viewBox="0 0 16 16">
                                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
                                </svg>`;
        } else {
            togglePassword1.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-eye-slash" viewBox="0 0 16 16">
                                <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z"/>
                                <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
                                <path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12z"/>
                              </svg>`; // Texto quando a senha está visível
        }
    });
});

