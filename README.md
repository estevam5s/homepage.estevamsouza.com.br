# Hub de Serviços

<div align="center">

![Hub de Serviços](https://via.placeholder.com/1200x300/4361ee/ffffff?text=Hub+de+Servi%C3%A7os)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

*Um dashboard profissional para gerenciar, analisar e acessar seus links favoritos*

</div>

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características](#-características)
- [Demonstração](#-demonstração)
- [Instalação](#-instalação)
- [Utilização](#-utilização)
- [Personalização](#-personalização)
- [Arquitetura](#-arquitetura)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Contato](#-contato)

## 🔍 Visão Geral

O **Hub de Serviços** é uma aplicação web desenvolvida com Python e Streamlit que transforma a maneira como você organiza e acessa seus links profissionais. Este dashboard interativo oferece visualizações analíticas avançadas, categorização intuitiva e um sistema de busca eficiente para gerenciar centenas de links em um único local.

## ✨ Características

### Principais Funcionalidades

- **Dashboard Analítico**
  - Métricas em tempo real
  - Visualizações de distribuição de links
  - Destaques por categoria

- **Gerenciamento de Links**
  - Organização por categorias
  - Cartões interativos com descrições
  - Sistema de busca avançado

- **Insights e Análises**
  - Tendências de uso
  - Padrões de acesso por dia da semana
  - Classificação por popularidade

- **Gerenciamento de Categorias**
  - Adição de novas categorias
  - Visualização da distribuição de links
  - Análise de categorias mais populares

- **Interface Responsiva**
  - Design limpo e profissional
  - Adaptação a diferentes dispositivos
  - Navegação intuitiva

## 🖼️ Demonstração

<div align="center">

| Dashboard | Links | Análises |
|:-------------------------:|:-------------------------:|:-------------------------:|
| ![Dashboard](https://via.placeholder.com/400x225/4361ee/ffffff?text=Dashboard) | ![Links](https://via.placeholder.com/400x225/4895ef/ffffff?text=Links) | ![Análises](https://via.placeholder.com/400x225/3a0ca3/ffffff?text=An%C3%A1lises) |

</div>

## 🛠️ Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. Clone o repositório:
```bash
git clone https://github.com/estevam5s/hub-servicos.git
cd hub-servicos
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
streamlit run app.py
```

5. Acesse o dashboard em seu navegador:
```
http://localhost:8501
```

## 🚀 Utilização

### Dashboard

O **Dashboard Principal** oferece uma visão geral de todas as suas estatísticas e análises:

- **Métricas Gerais**: Total de links, número de categorias, links por categoria
- **Distribuição de Links**: Visualização da distribuição de links por categoria
- **Links em Destaque**: Acesso rápido aos links mais importantes ou frequentemente utilizados

### Gerenciamento de Links

A página de **Links** permite:

- **Visualizar** todos os links organizados por categoria
- **Pesquisar** links por título, categoria ou descrição
- **Filtrar** por categorias específicas
- **Acessar** diretamente qualquer link com um único clique

### Análises

A página de **Análise** fornece insights detalhados:

- **Estatísticas de Uso**: Visualização de padrões de acesso ao longo do tempo
- **Mapa de Calor**: Identificação de padrões de uso por dia da semana
- **Tendências**: Análise de tendências de uso por categoria

### Gerenciamento de Categorias

A página de **Categorias** permite:

- **Adicionar** novas categorias
- **Visualizar** a distribuição de links por categoria
- **Remover** categorias existentes (com confirmação)

## 🎨 Personalização

### Adicionar Novos Links

Para adicionar novos links, modifique a função `load_links_data()` no arquivo `app.py`:

```python
# Adicionar um novo link
new_titles = ['Meu Novo Site']
new_urls = ['https://meunovo.site']
new_icons = ['fas fa-globe']
new_descriptions = ['Descrição do meu novo site']

data['title'].extend(new_titles)
data['url'].extend(new_urls)
data['icon'].extend(new_icons)
data['category'].extend(['Minha Categoria'] * len(new_titles))
data['description'].extend(new_descriptions)
```

### Personalizar Estilos

Para modificar a aparência do dashboard, ajuste as definições CSS na função `local_css()`:

```python
# Alteração de cores
css = css.replace('--primary-color: #4361ee;', '--primary-color: #YOUR_COLOR;')
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular organizada da seguinte forma:

```
hub-servicos/
├── app.py             # Aplicação principal Streamlit
├── requirements.txt   # Dependências do projeto
├── README.md          # Documentação
└── .streamlit/        # Configurações do Streamlit
    └── config.toml    # Configurações da interface
```

### Componentes Principais

- **Carregamento de Dados**: Estrutura de dados para organização de links
- **Interface do Usuário**: Componentes Streamlit para visualização e interação
- **Visualizações**: Gráficos e análises com Plotly
- **Estilização**: CSS personalizado para uma interface profissional

## 👥 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Envie para o GitHub (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

Por favor, certifique-se de atualizar os testes conforme apropriado e seguir o código de conduta do projeto.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

**Estevam Souza**

- Website: [estevamsouza.com.br](https://www.estevamsouza.com.br)
- LinkedIn: [linkedin.com/in/estevam-souza](https://www.linkedin.com/in/estevam-souza)
- Email: contato@estevamsouza.com.br

---

<div align="center">

Desenvolvido com ❤️ por [Estevam Souza](https://github.com/estevam5s)

</div>