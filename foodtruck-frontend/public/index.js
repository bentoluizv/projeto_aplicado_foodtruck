// public/index.js
// Lógica de manipulação do formulário de login e chamada à API de autenticação.

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;

            const errorMessage = document.getElementById('errorMessage');
            errorMessage.innerText = '';

            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);
            // formData.append('role', role); // Adicione se seu backend espera a função no token request

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/token`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData.toString(),
                });

                const data = await response.json();

                if (response.ok) {
                    // Armazene o token de acesso
                    localStorage.setItem('accessToken', data.access_token);
                    // localStorage.setItem('tokenType', data.token_type); // Se houver token_type

                    // Redireciona com base na função
                    if (role === 'atendente') {
                        window.location.href = './atendente/menu.html';
                    } else if (role === 'chapeiro') {
                        window.location.href = './chapeiro/preparar_pedidos.html';
                    }
                } else {
                    errorMessage.innerText = data.detail || data.message || 'Usuário ou senha inválidos.';
                    console.error('Erro de login:', data);
                }
            } catch (error) {
                console.error('Erro na requisição de login:', error);
                errorMessage.innerText = 'Ocorreu um erro ao tentar fazer login. Verifique sua conexão.';
            }
        });
    }
});