// public/atendente/menu.js
// Lógica para carregar e exibir itens do menu e gerenciar um pedido/carrinho.

// Variável para armazenar o pedido atual.
// Para persistência, poderíamos carregar do localStorage ao iniciar:
let currentOrder = JSON.parse(localStorage.getItem('currentOrder')) || [];

document.addEventListener('DOMContentLoaded', async () => {
    const menuItemsList = document.getElementById('menuItems');
    const logoutBtn = document.getElementById('logoutBtn');
    
    // Novas referências para os elementos do pedido
    const currentOrderList = document.getElementById('currentOrderList');
    const orderTotalSpan = document.getElementById('orderTotal');
    const finalizeOrderBtn = document.getElementById('finalizeOrderBtn');
    const clearOrderBtn = document.getElementById('clearOrderBtn');
    const tableNumberInput = document.getElementById('tableNumber');
    const orderNotesInput = document.getElementById('orderNotes');

    menuItemsList.innerHTML = '<li>Carregando itens do menu...</li>';

    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
        alert('Você precisa estar logado para acessar esta página.');
        window.location.href = '../index.html';
        return;
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (event) => {
            event.preventDefault();
            localStorage.removeItem('accessToken');
            localStorage.removeItem('currentOrder'); // Limpa o pedido ao deslogar
            window.location.href = '../index.html';
        });
    }

    // --- Função auxiliar para lidar com respostas da API (401/403 - Autenticação/Autorização) ---
    function handleAuthError(response) {
        if (response.status === 401 || response.status === 403) {
            alert('Sessão expirada ou acesso negado. Faça login novamente.');
            localStorage.removeItem('accessToken');
            localStorage.removeItem('currentOrder'); // Limpa o pedido ao deslogar
            window.location.href = '../index.html';
            return true; 
        }
        return false; 
    }

    // --- FUNÇÃO PARA ATUALIZAR A EXIBIÇÃO DO PEDIDO NA TELA ---
    function updateOrderDisplay() {
        if (currentOrder.length === 0) {
            currentOrderList.innerHTML = '<li>Nenhum item no pedido.</li>';
            orderTotalSpan.innerText = '0.00';
            return;
        }

        currentOrderList.innerHTML = ''; // Limpa a lista atual
        let total = 0;

        currentOrder.forEach(item => {
            const itemSubtotal = item.price * item.quantity;
            total += itemSubtotal;

            const listItem = document.createElement('li');
            listItem.innerHTML = `
                ${item.name} (x${item.quantity}) - R$ ${itemSubtotal.toFixed(2)}
                <button class="remove-item-btn" data-item-id="${item.id}">Remover</button>
            `;
            currentOrderList.appendChild(listItem);
        });

        orderTotalSpan.innerText = total.toFixed(2);
        localStorage.setItem('currentOrder', JSON.stringify(currentOrder)); // Salva no localStorage
    }

    // --- FUNÇÃO PARA ADICIONAR ITEM AO PEDIDO (CARRINHO) ---
    function addToOrder(itemId, itemName, itemPrice) {
        const existingItemIndex = currentOrder.findIndex(item => item.id === itemId);

        if (existingItemIndex > -1) {
            currentOrder[existingItemIndex].quantity += 1;
            console.log(`Quantidade de "${itemName}" no pedido aumentada para ${currentOrder[existingItemIndex].quantity}.`);
        } else {
            currentOrder.push({
                id: itemId,
                name: itemName,
                price: itemPrice, // Mantém o preço aqui para uso no frontend e no envio
                quantity: 1
            });
            console.log(`"${itemName}" adicionado ao pedido.`);
        }
        updateOrderDisplay(); // Atualiza a exibição do pedido
        alert(`"${itemName}" ${existingItemIndex > -1 ? 'quantidade atualizada' : 'adicionado'} ao pedido!`);
    }

    // --- FUNÇÃO PARA REMOVER ITEM DO PEDIDO ---
    currentOrderList.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-item-btn')) {
            const itemIdToRemove = event.target.dataset.itemId;
            currentOrder = currentOrder.filter(item => item.id !== itemIdToRemove);
            console.log(`Item ID ${itemIdToRemove} removido do pedido.`);
            updateOrderDisplay(); // Atualiza a exibição
        }
    });

    // --- EVENT LISTENER PARA LIMPAR O PEDIDO ---
    clearOrderBtn.addEventListener('click', () => {
        if (confirm('Tem certeza que deseja limpar o pedido atual?')) {
            currentOrder = [];
            updateOrderDisplay();
            localStorage.removeItem('currentOrder');
            alert('Pedido limpo!');
        }
    });

    // --- FUNÇÃO PARA FINALIZAR O PEDIDO (Enviar para o Backend) ---
    finalizeOrderBtn.addEventListener('click', async () => {
        if (currentOrder.length === 0) {
            alert('O pedido está vazio. Adicione itens antes de finalizar.');
            return;
        }

        const tableNumber = tableNumberInput.value.trim();
        const orderNotes = orderNotesInput.value.trim();

        if (!tableNumber) {
            alert('Por favor, insira o número da mesa.');
            return;
        }
        if (isNaN(parseInt(tableNumber)) || parseInt(tableNumber) <= 0) {
            alert('Número da mesa inválido. Deve ser um número inteiro positivo.');
            return;
        }

        // Prepara os dados do pedido para enviar ao backend
        const orderData = {
            table_number: parseInt(tableNumber),
            notes: orderNotes,
            items: currentOrder.map(item => ({
                product_id: item.id,
                quantity: item.quantity,
                // CORREÇÃO: Enviando o campo 'price' como solicitado pelo backend
                price: item.price 
            }))
        };

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/orders/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(orderData)
            });

            if (handleAuthError(response)) return;

            const result = await response.json();

            if (response.ok) {
                alert(`Pedido #${result.id} finalizado com sucesso! Total: R$ ${result.total_amount ? result.total_amount.toFixed(2) : 'N/A'}`);
                currentOrder = []; // Limpa o carrinho após o sucesso
                updateOrderDisplay(); // Atualiza a UI
                localStorage.removeItem('currentOrder'); // Limpa do localStorage
                tableNumberInput.value = ''; // Limpa os campos
                orderNotesInput.value = '';
                // Opcional: Redirecionar para uma página de confirmação ou para o menu principal
            } else {
                alert(`Erro ao finalizar pedido: ${result.detail || result.message || response.statusText}`);
                console.error('Erro ao finalizar pedido:', result);
            }
        } catch (error) {
            console.error('Erro na requisição para finalizar pedido:', error);
            alert('Não foi possível conectar ao servidor para finalizar o pedido.');
        }
    });


    // --- Chamadas Iniciais ---
    fetchProducts(); // Carrega os produtos do menu ao iniciar
    updateOrderDisplay(); // Carrega o pedido do localStorage ao iniciar (se existir)

    // --- GET /api/v1/products/ (Função para carregar produtos do menu) ---
    async function fetchProducts() {
        const offset = 0; 
        const limit = 100; 
        const queryParams = new URLSearchParams({ offset, limit });

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/products/?${queryParams.toString()}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'accept': 'application/json'
                }
            });

            if (handleAuthError(response)) return;

            const data = await response.json();

            if (response.ok) {
                menuItemsList.innerHTML = '';
                const items = data.products; 

                if (!items || items.length === 0) {
                    menuItemsList.innerHTML = '<li>Nenhum item no menu disponível.</li>';
                } else {
                    items.forEach(item => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `
                            <h3>${item.name}</h3>
                            <p>${item.description}</p>
                            <p>Preço: R$ ${item.price ? item.price.toFixed(2) : 'N/A'}</p>
                            <p>Disponível: ${item.is_available ? 'Sim' : 'Não'}</p>
                            <button class="add-to-order-btn" 
                                    data-item-id="${item.id}" 
                                    data-item-name="${item.name}" 
                                    data-item-price="${item.price}">
                                Adicionar ao Pedido
                            </button>
                        `;
                        menuItemsList.appendChild(listItem); 

                        const addButton = listItem.querySelector('.add-to-order-btn');
                        if (addButton) {
                            addButton.addEventListener('click', () => {
                                addToOrder(item.id, item.name, item.price);
                            });
                        }
                    });
                }
            } else {
                menuItemsList.innerHTML = '<li>Erro ao carregar o menu.</li>';
                console.error('Erro ao carregar menu:', data.detail || data.message || response.statusText);
            }
        } catch (error) {
            console.error('Erro na requisição do menu:', error);
            menuItemsList.innerHTML = '<li>Não foi possível conectar ao servidor para carregar o menu.</li>';
        }
    }
});