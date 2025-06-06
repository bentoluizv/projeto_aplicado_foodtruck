// public/atendente/menu.js
// Lógica para carregar e exibir itens do menu.

document.addEventListener('DOMContentLoaded', async () => {
    const menuItemsList = document.getElementById('menuItems');
    const logoutBtn = document.getElementById('logoutBtn');
    menuItemsList.innerHTML = '<li>Carregando itens do menu...</li>';

    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
        alert('Você precisa estar logado para acessar esta página.');
        window.location.href = '../../index.html'; // Redirecionar para a página de login
        return;
    }

    // Lógica de logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (event) => {
            event.preventDefault();
            localStorage.removeItem('accessToken'); // Limpa o token
            window.location.href = '../../index.html'; // Redireciona para o login
        });
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/menu`, { // Assumindo /api/menu para obter o menu
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401 || response.status === 403) {
            alert('Sessão expirada ou acesso negado. Faça login novamente.');
            localStorage.removeItem('accessToken');
            window.location.href = '../../index.html';
            return;
        }

        const data = await response.json();

        if (response.ok) {
            menuItemsList.innerHTML = ''; // Limpa o "Carregando..."
            if (data.length === 0) {
                menuItemsList.innerHTML = '<li>Nenhum item no menu disponível.</li>';
            } else {
                data.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        <h3>${item.name}</h3>
                        <p>${item.description}</p>
                        <p>Preço: R$ ${item.price.toFixed(2)}</p>
                        <button class="add-to-order-btn" data-item-id="${item.id}" data-item-name="${item.name}" data-item-price="${item.price}">Adicionar ao Pedido</button>
                    `;
                    menuItemsList.appendChild(listItem);
                });
            }
        } else {
            menuItemsList.innerHTML = '<li>Erro ao carregar o menu.</li>';
            console.error('Erro ao carregar menu:', data.message || response.statusText);
        }
    } catch (error) {
        console.error('Erro na requisição do menu:', error);
        menuItemsList.innerHTML = '<li>Não foi possível conectar ao servidor para carregar o menu.</li>';
    }
});