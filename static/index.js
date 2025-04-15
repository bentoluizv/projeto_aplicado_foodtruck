const toggle = () => {
    const toggleBtn = document.getElementById('toggleBtn');
    const menu = document.getElementById('menu');
    const isHidden = menu.classList.toggle('hidden');
    if (isHidden) {
        toggleBtn.innerHTML = '☰';
    } else {
        toggleBtn.innerHTML = '✖';
    }
}