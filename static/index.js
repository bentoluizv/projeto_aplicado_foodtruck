// htmx.logAll();

const onCategorySelect = (ctx) => {
    ctx.classList.add('border-orange-600', 'border-2');
    for (const elt of ctx.parentElement.children) {
        if (elt !== ctx) {
            elt.classList.remove('border-orange-600', 'border-2');
        }
    }
};

const toggleMenuDropdown = (forceClose = false) => {
    const toggleBtn = document.getElementById('toggleBtn');
    const menu = document.getElementById('menu');

    if (forceClose) {
        menu.classList.add('hidden');
        toggleBtn.innerHTML = '☰';
        return;
    }

    const isHidden = menu.classList.toggle('hidden');
    toggleBtn.innerHTML = isHidden ? '☰' : '✖';
};

const onIconClick = (id) => {
    const iconInput = document.getElementById('icon_url');
    const iconElement = document.getElementById(`icon-${id}`);
    const iconImgElement = iconElement.children[0];
    const srcUrl = iconImgElement.getAttribute('src');
    iconInput.value = srcUrl;
    iconElement.classList.add("border-2", "border-orange-600");
    console.log(iconInput)
    console.log(iconInput.value)
    removeIconSelection(iconElement);
};

const removeIconSelection = (keepElt) => {
    const iconInput = document.getElementById('icon_url');
    const iconElements = document.querySelectorAll('.border-orange-600');

    if (keepElt) {
        iconElements.forEach((icon) => {
            if (icon.id !== keepElt.id) {
                icon.classList.remove('border-orange-600');
                icon.classList.add('border-2', 'border-zinc-800');
            }
        });
        return;
    }

    iconElements.forEach((icon) => {
        icon.classList.remove('border-orange-600');
        icon.classList.add('border-2', 'border-zinc-800');
    });
    iconInput.value = '';
};

const toggleNewCategoriesModal = () => {
    const dialog = htmx.find("#new-category-dialog");

    if (!dialog.isHidden) {
        removeIconSelection()
    }

    dialog.classList.toggle('hidden');
};

const toggleHidden = (id) => {
    const dialog = htmx.find(id);
    dialog.classList.toggle('hidden');
};

const selectImage = (ctx) => {
    console.log(ctx);
}


document.addEventListener('htmx:afterRequest', (event) => {
    isMenuLink = event.detail.elt.classList.contains('menu-link')

    if (isMenuLink) {
        toggleMenuDropdown(true);
    }
});

