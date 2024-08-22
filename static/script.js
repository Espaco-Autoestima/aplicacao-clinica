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

// Pesquisa
// document.getElementById('pesquisa').addEventListener('input', function() {
//     var termo = this.value.trim();
//     if (termo.length > 2) { // Ignora pesquisas muito curtas
//         fetch(`/pesquisar?termo=${encodeURIComponent(termo)}`)
//             .then(response => response.json())
//             .then(data => {
//                 var resultadosDiv = document.getElementById('resultados');
//                 resultadosDiv.innerHTML = ''; // Limpa os resultados antigos
                
//                 data.resultados.forEach(resultado => {
//                     var div = document.createElement('div');
//                     div.textContent = `${resultado.nome} - ${resultado.cpf}`;
//                     resultadosDiv.appendChild(div);
//                 });
//             })
//             .catch(error => console.error('Erro ao buscar dados:', error));
//         }
// });