// public/chapeiro/preparar_pedidos.js
// Lógica para carregar pedidos pendentes e atualizar seu status.

document.addEventListener('DOMContentLoaded', async () => {
    const pendingOrdersList = document.getElementById('pendingOrdersList');
    const logoutBtn = document.getElementById('logoutBtn');
    pendingOrdersList.innerHTML = '<li>Carregando pedidos pendentes...</li>';

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

    async function loadPendingOrders() {
        pendingOrdersList.innerHTML = '<li>Carregando pedidos pendentes...</li>';
        try {
            // Requisição para obter pedidos pendentes (apenas para chapeiro)
            const response = await fetch(`${API_BASE_URL}/api/chapeiro/pedidos_pendentes`, { // Endpoint específico para chapeiro
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
                pendingOrdersList.innerHTML = ''; // Limpa o "Carregando..."
                if (orders.length === 0) {
                    pendingOrdersList.innerHTML = '<li>Nenhum pedido pendente no momento.</li>';
                } else {
                    orders.forEach(order => {
                        const listItem = document.createElement('li');
                        const itemsHtml = order.items.map(item => `<li>${item.name} (x${item.quantity})</li>`).join('');

                        listItem.innerHTML = `
                            <h3>Pedido #${order.id}</h3>
                            <p>Status: <span class="order-status">${order.status}</span></p>
                            <h4>Itens:</h4>
                            <ul>${itemsHtml}</ul>
                            ${order.status === 'novo' || order.status === 'Novo Pedido' ? `
                                <button class="update-status-btn" data-order-id="${order.id}" data-new-status="em preparo">Marcar como Em Preparo</button>
                            ` : ''}
                            ${order.status === 'em preparo' || order.status === 'Em Preparo' ? `
                                <button class="update-status-btn" data-order-id="${order.id}" data-new-status="pronto">Marcar como Pronto</button>
                            ` : ''}
                        `;
                        pendingOrdersList.appendChild(listItem);
                    });
                }
            } else {
                pendingOrdersList.innerHTML = '<li>Erro ao carregar pedidos pendentes.</li>';
                console.error('Erro ao carregar pedidos pendentes:', orders.message || response.statusText);
            }
        } catch (error) {
            console.error('Erro na requisição de pedidos pendentes:', error);
            pendingOrdersList.innerHTML = '<li>Não foi possível conectar ao servidor para carregar pedidos pendentes.</li>';
        }
    }

    // Carrega os pedidos ao carregar a página
    loadPendingOrders();

    // Lógica para atualizar status de pedidos pelo chapeiro
    pendingOrdersList.addEventListener('click', async (event) => {
        if (event.target.classList.contains('update-status-btn')) {
            const orderId = event.target.dataset.orderId;
            const newStatus = event.target.dataset.newStatus;

            try {
                // Endpoint de atualização de status para o chapeiro
                const response = await fetch(`${API_BASE_URL}/api/chapeiro/pedidos/${orderId}/status`, {
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
                    loadPendingOrders(); // Recarrega a lista
                } else {
                    alert(data.message || 'Erro ao atualizar status do pedido.');
                    console.error('Erro ao atualizar status:', data);
                }
            } catch (error) {
                console.error('Erro na requisição de atualização de status do chapeiro:', error);
                alert('Não foi possível conectar ao servidor para atualizar o status.');
            }
        }
    });
});