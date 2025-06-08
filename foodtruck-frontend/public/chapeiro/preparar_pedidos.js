// public/chapeiro/preparar_pedidos.js
// Lógica para carregar pedidos por status em colunas e permitir a mudança de status.

document.addEventListener('DOMContentLoaded', async () => {
    // Referências para os contêineres de cada coluna
    const pendingOrdersList = document.getElementById('pendingOrdersList');
    const processingOrdersList = document.getElementById('processingOrdersList');
    const completedOrdersList = document.getElementById('completedOrdersList');
    const cancelledOrdersList = document.getElementById('cancelledOrdersList');

    // Referências para os contadores de cada coluna
    const countPending = document.getElementById('count-pending');
    const countProcessing = document.getElementById('count-processing');
    const countCompleted = document.getElementById('count-completed');
    const countCancelled = document.getElementById('count-cancelled');

    const loadingMessage = document.getElementById('loadingMessage');
    const noOrdersMessage = document.getElementById('noOrdersMessage');
    const logoutBtn = document.getElementById('logoutBtn');

    const accessToken = localStorage.getItem('accessToken');

    // --- Validação de Autenticação ---
    if (!accessToken) {
        alert('Você precisa estar logado para acessar esta página.');
        window.location.href = '../index.html';
        return;
    }

    // --- Configuração da API_BASE_URL ---
    if (typeof API_BASE_URL === 'undefined') {
        console.error("API_BASE_URL não está definida. Verifique common.js ou seu escopo.");
        alert("Erro de configuração: API_BASE_URL não encontrada.");
        return;
    }

    // --- Logout ---
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (event) => {
            event.preventDefault();
            localStorage.removeItem('accessToken');
            localStorage.removeItem('currentOrder');
            window.location.href = '../index.html';
        });
    }

    // --- Tratamento de Erros de Autenticação/Autorização da API ---
    function handleAuthError(response) {
        if (response.status === 401 || response.status === 403) {
            alert('Sessão expirada ou acesso negado. Faça login novamente.');
            localStorage.removeItem('accessToken');
            localStorage.removeItem('currentOrder');
            window.location.href = '../index.html';
            return true;
        }
        return false;
    }

    // --- Função para Carregar Pedidos (Requisição GET) ---
    async function loadAllOrders() {
        loadingMessage.style.display = 'block';
        noOrdersMessage.style.display = 'none';

        // Limpa todas as colunas
        pendingOrdersList.innerHTML = '';
        processingOrdersList.innerHTML = '';
        completedOrdersList.innerHTML = '';
        cancelledOrdersList.innerHTML = '';

        // Reseta contadores
        let counts = { PENDING: 0, PROCESSING: 0, COMPLETED: 0, CANCELLED: 0 };

        try {
            const queryParams = new URLSearchParams();
            // Solicita pedidos de TODOS os status que você quer exibir nas colunas
            queryParams.append('status', 'PENDING');
            queryParams.append('status', 'PROCESSING');
            queryParams.append('status', 'COMPLETED');
            queryParams.append('status', 'CANCELLED');

            const response = await fetch(`${API_BASE_URL}/api/v1/orders/?${queryParams.toString()}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'accept': 'application/json'
                }
            });

            if (handleAuthError(response)) {
                loadingMessage.style.display = 'none';
                return;
            }

            const result = await response.json();

            if (response.ok) {
                const orders = result.orders;
                loadingMessage.style.display = 'none';

                if (!orders || orders.length === 0) {
                    noOrdersMessage.style.display = 'block';
                } else {
                    // Distribui os pedidos nas colunas corretas
                    orders.forEach(order => {
                        const orderCard = document.createElement('div');
                        const displayStatus = order.status.toUpperCase();
                        orderCard.classList.add('order-card', displayStatus.toLowerCase());
                        
                        const itemsHtml = order.items && order.items.length > 0
                            ? order.items.map(item => `
                                <li>
                                    ${item.product_name || `(ID: ${item.product_id})`} 
                                    <span class="item-quantity">x${item.quantity}</span> 
                                    <span class="item-price">R$ ${item.price ? item.price.toFixed(2) : '0.00'}</span>
                                </li>`
                            ).join('')
                            : '<li>Nenhum item detalhado disponível.</li>';

                        // --- Geração do Dropdown de Status ---
                        let statusOptionsHtml = '';
                        const allStatuses = ['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED'];

                        let allowedNextStatuses = [];
                        if (displayStatus === 'PENDING') {
                            allowedNextStatuses = ['PROCESSING', 'CANCELLED'];
                        } else if (displayStatus === 'PROCESSING') {
                            allowedNextStatuses = ['COMPLETED', 'CANCELLED'];
                        } else if (displayStatus === 'COMPLETED') {
                            allowedNextStatuses = ['PROCESSING', 'CANCELLED']; // Exemplo: permite reativar ou cancelar um completo
                        } else if (displayStatus === 'CANCELLED') {
                            allowedNextStatuses = ['PENDING']; // Exemplo: permite reabrir um cancelado
                        }
                        
                        // Inclui o status atual como selecionado e desabilitado
                        // e adiciona os status permitidos como opções selecionáveis.
                        statusOptionsHtml = `
                            <select class="status-select" data-order-id="${order.id}">
                                <option value="${displayStatus}" selected disabled>${displayStatus}</option>
                                ${allowedNextStatuses.map(status => {
                                    if (status !== displayStatus) { // Evita duplicar o status atual como opção selecionável
                                        return `<option value="${status}">${status}</option>`;
                                    }
                                    return '';
                                }).join('')}
                            </select>
                            <button class="update-status-btn btn-primary" data-order-id="${order.id}" disabled>Atualizar</button>
                        `;

                        orderCard.innerHTML = `
                            <div class="order-header">
                                <h3>Pedido #${order.id.substring(0, 12)}</h3>
                                <span class="order-locator">Mesa: ${order.locator || 'N/A'}</span>
                            </div>
                            <p class="order-status-display">Status: <span class="status-badge ${displayStatus.toLowerCase()}">${displayStatus}</span></p>
                            <div class="order-details">
                                <h4>Itens:</h4>
                                <ul class="order-items-list">${itemsHtml}</ul>
                                <p class="order-notes">Obs: ${order.notes || 'N/A'}</p>
                                <p class="order-total">Total: <strong>R$ ${order.total ? order.total.toFixed(2) : '0.00'}</strong></p>
                            </div>
                            <div class="order-actions">
                                ${statusOptionsHtml}
                            </div>
                        `;

                        // Adiciona o card à coluna correta
                        switch (displayStatus) {
                            case 'PENDING':
                                pendingOrdersList.appendChild(orderCard);
                                counts.PENDING++;
                                break;
                            case 'PROCESSING':
                                processingOrdersList.appendChild(orderCard);
                                counts.PROCESSING++;
                                break;
                            case 'COMPLETED':
                                completedOrdersList.appendChild(orderCard);
                                counts.COMPLETED++;
                                break;
                            case 'CANCELLED':
                                cancelledOrdersList.appendChild(orderCard);
                                counts.CANCELLED++;
                                break;
                            default:
                                console.warn('Status desconhecido:', order.status);
                        }
                    });

                    // Atualiza os contadores
                    countPending.textContent = ` (${counts.PENDING})`;
                    countProcessing.textContent = ` (${counts.PROCESSING})`;
                    countCompleted.textContent = ` (${counts.COMPLETED})`;
                    countCancelled.textContent = ` (${counts.CANCELLED})`;
                }
            } else {
                loadingMessage.style.display = 'none';
                noOrdersMessage.textContent = `Erro ao carregar pedidos: ${result.detail || result.message || response.statusText}`;
                noOrdersMessage.style.display = 'block';
                console.error('Erro ao carregar pedidos:', result.detail || result.message || response.statusText);
            }
        } catch (error) {
            console.error('Erro na requisição de pedidos:', error);
            loadingMessage.style.display = 'none';
            noOrdersMessage.textContent = 'Não foi possível conectar ao servidor.';
            noOrdersMessage.style.display = 'block';
        }
    }

    // --- Event Listener para mudança no dropdown e clique no botão 'Atualizar' ---
    // Os listeners são anexados ao elemento pai 'orders-board' para delegar eventos
    // Isso é mais eficiente do que anexar a cada 'pendingOrdersList', 'processingOrdersList', etc.
    const ordersBoard = document.querySelector('.orders-board'); // Obtenha o contêiner principal

    ordersBoard.addEventListener('change', (event) => {
        if (event.target.classList.contains('status-select')) {
            const selectElement = event.target;
            const updateButton = selectElement.nextElementSibling; // O botão "Atualizar" é o próximo irmão

            // O valor da opção selecionada (que pode ser o status atual disabled)
            const selectedValue = selectElement.value;
            // O status atual real do card (armazenado na primeira opção desabilitada)
            const currentActualStatus = selectElement.querySelector('option[selected][disabled]').value;

            if (selectedValue !== currentActualStatus) {
                updateButton.disabled = false; // Habilita o botão se a seleção mudou
            } else {
                updateButton.disabled = true; // Desabilita se voltar ao status original
            }
        }
    });

    ordersBoard.addEventListener('click', async (event) => {
        if (event.target.classList.contains('update-status-btn')) {
            const button = event.target;
            const orderId = button.dataset.orderId;
            const selectElement = button.previousElementSibling;
            const newStatus = selectElement.value; // Pega o novo status do dropdown

            const confirmUpdate = confirm(`Deseja realmente mudar o status do pedido #${orderId.substring(0, 8)} para "${newStatus}"?`);
            if (!confirmUpdate) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/orders/${orderId}`, {
                    method: 'PATCH',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                        'Content-Type': 'application/json',
                        'accept': 'application/json'
                    },
                    body: JSON.stringify({ status: newStatus }),
                });

                if (handleAuthError(response)) return;

                const result = await response.json();

                if (response.ok) {
                    alert(`Status do Pedido #${orderId.substring(0, 8)} atualizado para "${newStatus}".`);
                    loadAllOrders(); // Recarrega TODOS os pedidos para que sejam redistribuídos corretamente
                } else {
                    alert(result.detail || result.message || 'Erro ao atualizar status do pedido. Verifique as transições permitidas no backend.');
                    console.error('Erro ao atualizar status:', result);
                }
            } catch (error) {
                console.error('Erro na requisição de atualização de status:', error);
                alert('Não foi possível conectar ao servidor para atualizar o status.');
            }
        }
    });

    // --- Carrega pedidos ao iniciar a página ---
    loadAllOrders();
});