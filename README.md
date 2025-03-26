# Hub Digital de Links - Estevam Souza

![Estevam Souza](https://media.licdn.com/dms/image/v2/D4D03AQG1LthzngDNMQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1729293996215?e=1740614400&v=beta&t=fWNRhpyHopeBTOQF3H-KWLVvEh4TZeQRTY-_42RtzB4)

## 📋 Sobre o Projeto

Este projeto é um hub digital que centraliza todos os links relevantes para o desenvolvedor Estevam Souza. Ele foi desenvolvido com HTML, CSS e JavaScript para criar uma interface moderna, responsiva e fácil de usar, com efeitos visuais e recursos de busca.

### 🌟 Características Principais

- **Design Cyberpunk**: Interface com estilo futurista e efeitos visuais modernos
- **Pesquisa em Tempo Real**: Filtragem dinâmica de links por nome ou URL
- **Categorização**: Links organizados em seções temáticas para fácil navegação
- **Responsividade**: Adaptado para dispositivos móveis e desktop
- **Efeitos Visuais**: Hover effects e animações para melhorar a experiência do usuário
- **Botão Voltar ao Topo**: Navegação facilitada para listas extensas

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica do documento
- **CSS3**: Estilização e efeitos visuais
- **JavaScript**: Funcionalidades interativas como pesquisa e animações
- **Font Awesome**: Ícones para cada link
- **Integração com Dify**: ChatBot integrado para suporte

## 🔍 Estrutura do Projeto

```
hub-digital/
│
├── index.html        # Arquivo HTML principal
├── styles.css        # Folha de estilos CSS
├── README.md         # Este arquivo de documentação
└── images/           # Pasta de imagens (opcional)
```

## 📚 Organização de Links

O hub digital organiza os links nas seguintes categorias:

1. **Serviços** (17 links)
2. **Portfólio** (10 links)
3. **Templates & Serviços** (7 links)
4. **Currículo & Vagas** (8 links)
5. **Domínios & Hosting** (18 links)
6. **Desenvolvimento** (11 links)
7. **IoT & Desenvolvimento** (3 links)
8. **Cyber Segurança** (9 links)
9. **Inteligência Artificial** (15 links)
10. **Cloud & DevOps** (6 links)
11. **Segurança & Senhas** (4 links)
12. **Monetização** (4 links)
13. **Treino de Código** (3 links)
14. **Treino de Digitação** (1 link)
15. **Carteira de Cripto** (4 links)
16. **Armazenamento em Nuvem** (1 link)
17. **VPN** (2 links)
18. **Educação** (10 links)
19. **Documentação de Código** (7 links)
20. **Serviços de Pagamento** (1 link)

## 💻 Funcionalidades de Código

### Sistema de Pesquisa

```javascript
const searchInput = document.getElementById('searchInput');
const sections = document.querySelectorAll('.section');
const links = document.querySelectorAll('.link');
let searchTimeout;

function normalizeText(text) {
    return text.toLowerCase()
              .normalize('NFD')
              .replace(/[\u0300-\u036f]/g, '')
              .trim();
}

// Função de pesquisa em tempo real com debounce
searchInput.addEventListener('input', function(e) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const searchTerm = normalizeText(e.target.value);
        
        links.forEach(link => {
            const linkText = normalizeText(link.querySelector('.link-text').textContent);
            const href = normalizeText(link.getAttribute('href'));
            const shouldShow = linkText.includes(searchTerm) || 
                            href.includes(searchTerm);
            
            link.style.display = shouldShow ? 'flex' : 'none';
            link.classList.toggle('visible', shouldShow);
        });

        // Atualiza a visibilidade das seções e a contagem de links
        sections.forEach(section => {
            const visibleLinks = section.querySelectorAll('.link.visible').length;
            const counter = section.querySelector('.category-count');
            
            section.style.display = visibleLinks > 0 ? 'block' : 'none';
            if (counter) {
                counter.textContent = `${visibleLinks} link${visibleLinks !== 1 ? 's' : ''}`;
            }
        });
    }, 300);
});
```

### Botão Voltar ao Topo

```javascript
const scrollToTop = document.getElementById('scrollToTop');
let isScrolling;

// Exibe o botão quando o usuário rola para baixo
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTop.classList.add('visible');
        if (!isScrolling) {
            scrollToTop.classList.add('scrolling');
            clearTimeout(isScrolling);
        }
        
        isScrolling = setTimeout(() => {
            scrollToTop.classList.remove('scrolling');
            isScrolling = null;
        }, 150);
    } else {
        scrollToTop.classList.remove('visible', 'scrolling');
    }
});

// Rola a página para o topo quando o botão é clicado
scrollToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
```

## 🔧 Como Implementar Alterações

Para adicionar novos links ou categorias ao hub:

1. **Adicionar uma Nova Categoria**:

```html
<div class="section">
    <div class="section-header">
        <h2>Nome da Nova Categoria</h2>
        <span class="category-count">X links</span>
    </div>
    <div class="links">
        <!-- Links irão aqui -->
    </div>
</div>
```

2. **Adicionar um Novo Link**:

```html
<a href="https://url-do-link.com" class="link">
    <i class="fas fa-icone-apropriado"></i>
    <span class="link-text">Nome do Link</span>
    <div class="link-hover-effect"></div>
</a>
```

3. **Atualizar a Contagem de Links**:
   - Atualize o número na `<span class="category-count">` de cada seção.

## 🚀 Como Usar

1. Clone este repositório
2. Abra o arquivo `index.html` em seu navegador
3. Use a barra de pesquisa para filtrar links rapidamente
4. Clique nos links para acessar os recursos desejados
5. Use o botão de voltar ao topo para navegar facilmente pela página

## 📱 Compatibilidade

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+
- Opera 47+
- Navegadores móveis modernos

## 📄 Licença

Este projeto é para uso pessoal de Estevam Souza. Todos os direitos reservados.

## 👨‍💻 Contato

**Estevam Souza**  
Desenvolvedor Full Stack & Especialista em IA

- [LinkedIn](https://www.linkedin.com/in/estevam-souza)
- [GitHub](https://github.com/estevam5s)
- [Website](https://www.estevamsouza.com.br)