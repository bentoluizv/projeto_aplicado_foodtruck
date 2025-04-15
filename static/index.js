const toggleMenuDropdown = () => {
    const toggleBtn = document.getElementById('toggleBtn');
    const menu = document.getElementById('menu');
    const isHidden = menu.classList.toggle('hidden');
    if (isHidden) {
        toggleBtn.innerHTML = '☰';
    } else {
        toggleBtn.innerHTML = '✖';
    }
};

const toggleCategoriesModal = () => {
    const dialog = document.getElementById('dialog');
    const addButton = document.getElementById('modalBtn');
    const cancelButton = document.getElementById('cancelButton');

    addButton.addEventListener('click', () => {
        dialog.classList.remove('hidden');
    });

    cancelButton.addEventListener('click', () => {
        dialog.classList.add('hidden');
    });
};