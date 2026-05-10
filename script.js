document.addEventListener('DOMContentLoaded', () => {
    const copyButton = document.querySelector('button');
    if (copyButton) {
        copyButton.addEventListener('click', () => {
            const code = document.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(() => {
                const icon = copyButton.querySelector('i');
                icon.classList.replace('far', 'fas');
                icon.classList.replace('fa-copy', 'fa-check');
                setTimeout(() => {
                    icon.classList.replace('fas', 'far');
                    icon.classList.replace('fa-check', 'fa-copy');
                }, 2000);
            });
        });
    }
});
