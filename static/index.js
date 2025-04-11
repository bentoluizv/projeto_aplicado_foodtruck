const tooggle = () => {
        const aside = document.querySelector('aside');
        const menuButton = document.querySelector('button[hx-on\\:click="tooggle()"]');
        menuButton.textContent = aside.classList.contains('hidden') ? '✕' : '☰';
        aside.classList.toggle('hidden');
    }