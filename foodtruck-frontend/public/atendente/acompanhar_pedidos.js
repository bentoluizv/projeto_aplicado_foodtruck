// public/atendente/acompanhar_pedidos.js
// Lógica para carregar e atualizar o status dos pedidos.

document.addEventListener('DOMContentLoaded', async () => {
    const activeOrdersList = document.getElementById('activeOrdersList');
    const logoutBtn = document.getElementById('logoutBtn');
    activeOrdersList.innerHTML = '<li>Carregando pedidos...</li>';

    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
        alert('Você precisa estar logado para acessar esta página.');
        window.location.href = '../../index.html';
        return;
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (event) => {
            event.preventDefault();
            localStorage.removeItem('accessToken');
            window.location.href = '../../index.html';
        });
    }

    async function loadOrders() {
        activeOrdersList.innerHTML = '<li>Carregando pedidos...</li>';
        try {
            const response = await fetch(`${API_BASE_URL}/api/pedidos`, { // Assumindo /api/pedidos para listar pedidos
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

            const orders = await response.json();

            if (response.ok) {
                activeOrdersList.innerHTML = ''; // Limpa o "Carregando..."
                if (orders.length === 0) {
                    activeOrdersList.innerHTML = '<li>Nenhum pedido ativo no momento.</li>';
                } else {
                    orders.forEach(order => {
                        const listItem = document.createElement('li');
                        // Ajuste para exibir os itens do pedido. Assumindo que 'items' é um array de objetos com 'name' e 'quantity'
                        const itemsHtml = order.items.map(item => `${item.name} (x${item.quantity})`).join(', ');

                        listItem.innerHTML = `
                            <h3>Pedido #${order.id}</h3>
                            <p>Status: <span class="order-status">${order.status}</span></p>
                            <p>Itens: ${itemsHtml}</p>
                            ${order.status !== 'pronto para retirada' && order.status !== 'entregue' ? `
                                <button class="update-status-btn" data-order-id="${order.id}" data-new-status="pronto para retirada">Marcar como Pronto para Retirada</button>
                            ` : ''}
                            ${order.status === 'pronto para retirada' ? `
                                <button class="update-status-btn" data-order-id="${order.id}" data-new-status="entregue">Marcar como Entregue</button>
                            ` : ''}
                        `;
                        activeOrdersList.appendChild(listItem);
                    });
                }
            } else {
                activeOrdersList.innerHTML = '<li>Erro ao carregar pedidos.</li>';
                console.error('Erro ao carregar pedidos:', orders.message || response.statusText);
            }
        } catch (error) {
            console.error('Erro na requisição de pedidos:', error);
            activeOrdersList.innerHTML = '<li>Não foi possível conectar ao servidor para carregar pedidos.</li>';
        }
    }

    // Carrega os pedidos ao carregar a página
    loadOrders();

    // Lógica para atualizar status de pedidos
    activeOrdersList.addEventListener('click', async (event) => {
        if (event.target.classList.contains('update-status-btn')) {
            const orderId = event.target.dataset.orderId;
            const newStatus = event.target.dataset.newStatus;

            try {
                const response = await fetch(`${API_BASE_URL}/api/pedidos/${orderId}/status`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: newStatus }),
                });

                if (response.status === 401 || response.status === 403) {
                    alert('Sessão expirada ou acesso negado. Faça login novamente.');
                    localStorage.removeItem('accessToken');
                    window.location.href = '../../index.html';
                    return;
                }

                const data = await response.json();

                if (response.ok) {
                    alert(`Status do Pedido #${orderId} atualizado para "${newStatus}".`);
                    loadOrders(); // Recarrega a lista para mostrar o status atualizado
                } else {
                    alert(data.message || 'Erro ao atualizar status do pedido.');
                    console.error('Erro ao atualizar status:', data);
                }
            } catch (error) {
                console.error('Erro na requisição de atualização de status:', error);
                alert('Não foi possível conectar ao servidor para atualizar o status.');
            }
        }
    });
});