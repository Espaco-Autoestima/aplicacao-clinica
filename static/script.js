document.addEventListener('DOMContentLoaded', function() {
    // Seleciona apenas as categorias com a classe 'toggle'
    const toggleCategories = document.querySelectorAll('.category.toggle');
    
    toggleCategories.forEach(category => {
        category.addEventListener('click', function(e) {
            e.preventDefault(); // Impede o comportamento padrão do link
            
            // Deixa ativo texto
            category.classList.toggle('active');
            
            //Deixa a subcategoria associada a categoria
            const submenu = category.nextElementSibling;
            
            // Abre o submenu
            if (submenu.style.display === 'block') {
                submenu.style.display = 'none';
            } else {
                submenu.style.display = 'block';
            }
        });
    });
});

// Pesquisa de clientes por telefone
document.getElementById('botao-buscar').addEventListener('click', function(event) {
    event.preventDefault(); // Impede o envio do formulário padrão

    const telefone = document.getElementById('pesquisa').value;

    fetch('/pesquisar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'pesquisa': telefone
        })
    })
    .then(response => response.text())
    .then(data => {
        document.body.innerHTML = data; // Atualiza o conteúdo da página com a resposta
    })
    .catch(error => console.error('Erro:', error));
});