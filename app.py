import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests
import base64
from streamlit_option_menu import option_menu
import plotly.express as px
import streamlit.components.v1 as components
import numpy as np
import datetime

# Configuração da página
st.set_page_config(
    page_title="Estevam Souza - Hub de Serviços",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS personalizado
def local_css():
    css = """
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary-color: #4361ee;
        --primary-light: #4895ef;
        --primary-dark: #3a0ca3;
        --secondary-color: #3f37c9;
        --accent-color: #4cc9f0;
        --text-color: #111827;
        --text-secondary: #4b5563;
        --bg-color: #f9fafb;
        --card-bg: #ffffff;
        --border-color: #e5e7eb;
    }

    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-color);
    }

    .stApp {
        background-color: var(--bg-color);
    }

    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        color: var(--text-color);
    }

    .link-card {
        display: block;
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        text-decoration: none;
        color: var(--text-color);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .link-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: var(--primary-light);
    }

    .link-card-content {
        display: flex;
        align-items: center;
    }

    .link-card-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        background-color: #f3f4f6;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        color: var(--primary-color);
        font-size: 20px;
    }

    .link-card-text {
        flex: 1;
    }

    .link-card-text h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        color: var(--text-color);
    }

    .link-description {
        margin: 4px 0 0;
        font-size: 14px;
        color: var(--text-secondary);
    }

    .link-card-arrow {
        color: var(--text-secondary);
        font-size: 14px;
    }

    .link-card:hover .link-card-arrow {
        color: var(--primary-color);
    }

    .category-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--primary-light);
        color: var(--primary-dark);
    }

    .profile-section {
        text-align: center;
        margin-bottom: 32px;
    }

    .profile-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .profile-name {
        margin-top: 16px;
        font-size: 24px;
        font-weight: 700;
    }

    .profile-title {
        color: var(--text-secondary);
        font-size: 16px;
        margin-top: 4px;
    }

    .category-count {
        display: inline-block;
        background-color: #f3f4f6;
        border-radius: 16px;
        padding: 2px 10px;
        margin-left: 8px;
        font-size: 14px;
        color: var(--text-secondary);
    }

    .search-container {
        margin-bottom: 24px;
    }

    .stat-card {
        background-color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid var(--border-color);
    }

    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 4px;
    }

    .stat-label {
        color: var(--text-secondary);
        font-size: 14px;
    }

    .stat-icon {
        font-size: 24px;
        color: var(--primary-light);
        margin-bottom: 8px;
    }

    .dashboard-title {
        margin-bottom: 24px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 8px;
    }

    /* Ocultar spinner do Streamlit */
    .stSpinner {
        display: none !important;
    }

    .st-emotion-cache-ch5dnh {
        margin-top: -75px;
    }

    /* Estilo para o menu de navegação */
    .nav-link {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        text-decoration: none;
        color: var(--text-color);
        transition: all 0.2s ease;
    }

    .nav-link:hover {
        background-color: #f3f4f6;
    }

    .nav-link.active {
        background-color: var(--primary-color);
        color: white;
    }

    .nav-icon {
        margin-right: 10px;
        width: 20px;
        text-align: center;
    }

    /* Ajustes responsivos */
    @media screen and (max-width: 992px) {
        .profile-section {
            text-align: left;
            display: flex;
            align-items: center;
        }
        
        .profile-image {
            width: 80px;
            height: 80px;
            margin-right: 20px;
        }
        
        .profile-info {
            flex: 1;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Função para carregar uma imagem da web
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# Função para criar cartões de links
def create_link_card(icon, title, url, description=""):
    card_html = f"""
    <a href="{url}" target="_blank" class="link-card">
        <div class="link-card-content">
            <div class="link-card-icon"><i class="{icon}"></i></div>
            <div class="link-card-text">
                <h3>{title}</h3>
                <p class="link-description">{description}</p>
            </div>
            <div class="link-card-arrow">
                <i class="fas fa-external-link-alt"></i>
            </div>
        </div>
    </a>
    """
    return card_html

# Função para contar links por categoria
def count_links_by_category(links_data):
    counts = links_data.groupby('category').size().reset_index(name='count')
    return counts

# Carregar dados de links
@st.cache_data
def load_links_data():
    # Dados estruturados de todos os links
    data = {
        'title': [],
        'url': [],
        'icon': [],
        'category': [],
        'description': []
    }
    
    # Serviços
    services_titles = ['Dify', 'Chatwoot', 'Hasura', 'Evolution', 'Typebot', 'n8n', 'Portainer', 
                      'Code Server (VSCode)', 'VPS Hostinger', 'EmailJS', 'NestJS DevTools', 
                      'Cloudflare', 'Hostzone', 'Pi-hole', 'DocHub', 'Supabase', 'Leadster']
    
    services_urls = [
        'https://llm.estevamsouza.com.br/signin',
        'https://chatwoot.estevamsouza.com.br/app/accounts/1/conversations/1',
        'http://145.223.27.163:8585/console/login?redirect_url=%2F',
        'https://evolutionapi.estevamsouza.com.br/manager/instance/f7cfff4b-47b7-4944-b5ca-e48e6f758f4a/dashboard',
        'https://app.typebot.io/signin?redirectPath=/typebots?',
        'https://automation.estevamsouza.com.br/home/workflows',
        'https://portainer.estevamsouza.com.br/#!/auth',
        'http://145.223.27.163:8443/login?folder=/home/coder&to=',
        'https://hpanel.hostinger.com/vps/678324/overview',
        'https://dashboard.emailjs.com/sign-in',
        'https://devtools.nestjs.com/login',
        'https://www.cloudflare.com/pt-br/',
        'https://hostzone.com.br/',
        'http://192.168.1.140/admin/groups/clients',
        'https://www.dochub.com/',
        'https://supabase.com/dashboard/projects',
        'https://app.leadster.com.br/'
    ]
    
    services_icons = ['fas fa-server', 'fas fa-comments', 'fas fa-database', 'fas fa-code-branch', 
                     'fas fa-robot', 'fas fa-network-wired', 'fas fa-ship', 'fas fa-code', 
                     'fas fa-server', 'fas fa-envelope', 'fas fa-tools', 'fas fa-cloud', 
                     'fas fa-server', 'fas fa-filter', 'fas fa-file-alt', 'fas fa-database', 
                     'fas fa-funnel-dollar']
    
    services_descriptions = [
        'Plataforma de IA e LLM',
        'Sistema de gestão de conversas',
        'Ferramenta GraphQL',
        'API WhatsApp',
        'Criador de chatbots',
        'Automação de fluxos de trabalho',
        'Gestão de containers',
        'Editor de código remoto',
        'Servidor VPS',
        'Serviço de envio de emails',
        'Ferramentas para NestJS',
        'Serviços de DNS e CDN',
        'Serviço de hospedagem',
        'Bloqueador de anúncios para rede',
        'Edição de documentos',
        'Banco de dados e backend',
        'Geração de leads'
    ]
    
    data['title'].extend(services_titles)
    data['url'].extend(services_urls)
    data['icon'].extend(services_icons)
    data['category'].extend(['Serviços'] * len(services_titles))
    data['description'].extend(services_descriptions)

    # Portfólio
    portfolio_titles = ['Landing Page', 'LinkedIn', 'Blog', 'Website', 'Newsletter', 
                        'Artigos', 'Setup', 'VSCode', 'Git Connected', 'Star History']
    
    portfolio_urls = [
        'https://landingpage.estevamsouza.com.br',
        'https://www.linkedin.com/in/estevam-souza',
        'https://blog.estevamsouza.com.br',
        'https://www.estevamsouza.com.br',
        'https://newsletter.estevamsouza.com.br',
        'https://artigos.estevamsouza.com.br',
        'https://setup.estevamsouza.com.br',
        'https://vscode.estevamsouza.com.br',
        'https://gitconnected.com/estevam5s?configure_resume=true',
        'https://www.star-history.com/#estevam5/estevam5s&Date'
    ]
    
    portfolio_icons = ['fas fa-globe', 'fab fa-linkedin', 'fas fa-blog', 'fas fa-user', 
                       'fas fa-envelope', 'fas fa-file-alt', 'fas fa-desktop', 'fas fa-code', 
                       'fab fa-git', 'fas fa-chart-line']
    
    portfolio_descriptions = [
        'Página de destino',
        'Perfil profissional',
        'Blog pessoal',
        'Website pessoal',
        'Newsletter tecnológica',
        'Artigos técnicos',
        'Meu setup de desenvolvimento',
        'Configuração de VSCode',
        'Perfil em Git Connected',
        'Histórico de estrelas no GitHub'
    ]
    
    data['title'].extend(portfolio_titles)
    data['url'].extend(portfolio_urls)
    data['icon'].extend(portfolio_icons)
    data['category'].extend(['Portfólio'] * len(portfolio_titles))
    data['description'].extend(portfolio_descriptions)

    # Templates e Serviços
    templates_titles = ['Render', 'Railway', 'MailChimp', 'Envato Elements Templates', 
                        'Template Monster', 'ThemeForest', 'Zoho Mail']
    
    templates_urls = [
        'https://render.com',
        'https://railway.com',
        'https://mailchimp.com/pt-br',
        'https://elements.envato.com/pt-br/web-templates',
        'https://www.templatemonster.com',
        'https://themeforest.net/category/all',
        'https://www.zoho.com/pt-br/mail'
    ]
    
    templates_icons = ['fas fa-server', 'fas fa-train', 'fab fa-mailchimp', 'fas fa-palette', 
                       'fas fa-brush', 'fas fa-store', 'fas fa-envelope']
    
    templates_descriptions = [
        'Plataforma cloud',
        'Plataforma de hospedagem',
        'Marketing por email',
        'Templates para web',
        'Marketplace de templates',
        'Marketplace de temas',
        'Serviço de email'
    ]
    
    data['title'].extend(templates_titles)
    data['url'].extend(templates_urls)
    data['icon'].extend(templates_icons)
    data['category'].extend(['Templates & Serviços'] * len(templates_titles))
    data['description'].extend(templates_descriptions)

    # Currículo e Vagas
    jobs_titles = ['Currículo LinkedIn', 'Indeed Profile', 'Remote OK', 'Startup Jobs', 
                  'Glassdoor', 'Freelancer', 'Canva', 'Arc.dev', 'Crossover', 
                  'RemoteHub', 'Notion Jobs', 'Jora', 'IEL Estágios']
    
    jobs_urls = [
        'https://www.linkedin.com/in/estevam-souza/overlay/1730776596333/single-media-viewer/?type=DOCUMENT&profileId=ACoAACm6b_QBezL5lfr48f3yqBlHmvETB2WMPt4',
        'https://profile.indeed.com/p/estevams-2704c7s',
        'https://remoteok.com',
        'https://startup.jobs/',
        'https://www.glassdoor.com.br/Vaga/index.htm',
        'https://www.freelancer.com/login',
        'https://www.canva.com/',
        'https://arc.dev/remote-jobs',
        'https://www.crossover.com/auth/login?returnUrl=%2Fmy-profile',
        'https://www.remotehub.com/',
        'https://job-boards.greenhouse.io/notion',
        'https://my.jora.com/Notion-International-jobs',
        'https://carreiras.iel.org.br/'
    ]
    
    jobs_icons = ['fas fa-file-pdf', 'fas fa-briefcase', 'fas fa-laptop-house', 'fas fa-rocket', 
                 'fas fa-building', 'fas fa-laptop-code', 'fas fa-paint-brush', 'fas fa-globe', 
                 'fas fa-network-wired', 'fas fa-home', 'fas fa-briefcase', 'fas fa-search', 
                 'fas fa-graduation-cap']
    
    jobs_descriptions = [
        'Meu currículo no LinkedIn',
        'Perfil profissional no Indeed',
        'Portal de vagas remotas',
        'Vagas em startups',
        'Portal de vagas e avaliações',
        'Plataforma para trabalho freelance',
        'Design gráfico para currículo',
        'Vagas remotas para desenvolvedores',
        'Plataforma de trabalho remoto',
        'Diretório de empresas remotas',
        'Vagas na Notion',
        'Agregador de vagas',
        'Portal de estágios'
    ]
    
    data['title'].extend(jobs_titles)
    data['url'].extend(jobs_urls)
    data['icon'].extend(jobs_icons)
    data['category'].extend(['Currículo & Vagas'] * len(jobs_titles))
    data['description'].extend(jobs_descriptions)

    # Domínios & Hosting
    domains_titles = ['Vercel Domains', 'Registro.br', 'Netlify', 'Hostinger', 'Heroku', 
                     'Streamlit', 'GoDaddy', 'HostGator', 'Locaweb', 'Wix Domínios', 
                     'Shopify Domínios', 'Canva Domínios', 'Domínio Web', 'Umbler', 
                     'Squarespace', 'Hostnet', 'King Host', 'Super Domínios', 'Gatsby']
    
    domains_urls = [
        'https://vercel.com/domains',
        'https://registro.br',
        'https://www.netlify.com',
        'https://hpanel.hostinger.com/websites',
        'https://id.heroku.com/login',
        'https://streamlit.io/',
        'https://www.godaddy.com/pt-br/dominios',
        'https://www.hostgator.com.br/registro-de-dominio/',
        'https://www.locaweb.com.br/registro-de-dominio-web/',
        'https://pt.wix.com/dominio/gratis',
        'https://www.shopify.com/br/dominios',
        'https://www.canva.com/pt_br/dominios/',
        'https://www.dominioweb.com.br/',
        'https://www.umbler.com/br/registro-de-dominio',
        'https://domains.squarespace.com/pt',
        'https://www.hostnet.com.br/registro-de-dominio/',
        'https://king.host/registro-de-dominio',
        'https://superdominios.org/',
        'https://www.gatsbyjs.com/'
    ]
    
    domains_icons = ['fas fa-globe', 'fas fa-server', 'fas fa-cloud', 'fas fa-server', 
                    'fas fa-cloud-upload-alt', 'fas fa-stream', 'fas fa-globe', 'fas fa-server', 
                    'fas fa-globe', 'fas fa-globe', 'fab fa-shopify', 'fas fa-globe', 
                    'fas fa-globe', 'fas fa-globe', 'fas fa-square', 'fas fa-server', 
                    'fas fa-crown', 'fas fa-globe', 'fas fa-rocket']
    
    domains_descriptions = [
        'Registro de domínios na Vercel',
        'Registro de domínios .br',
        'Hospedagem de sites e CI/CD',
        'Hospedagem de sites',
        'Plataforma cloud',
        'Framework para dashboards',
        'Registro internacional de domínios',
        'Hospedagem de sites',
        'Hospedagem e domínios',
        'Domínios da Wix',
        'Domínios da Shopify',
        'Domínios do Canva',
        'Serviço de registro de domínios',
        'Hospedagem e domínios',
        'Domínios do Squarespace',
        'Serviço de hospedagem',
        'Hospedagem e domínios',
        'Registro de domínios',
        'Framework para sites estáticos'
    ]
    
    data['title'].extend(domains_titles)
    data['url'].extend(domains_urls)
    data['icon'].extend(domains_icons)
    data['category'].extend(['Domínios & Hosting'] * len(domains_titles))
    data['description'].extend(domains_descriptions)

    # Desenvolvimento
    dev_titles = ['VSCode Web', 'CodePen', 'NestJS Docs', 'NPM', 'StackBlitz', 'Google Colab', 
                 'Replit', 'Gitpod', 'CodeSandbox', 'Codeanywhere', 'React Icons', 'Amplication', 
                 'Can I Use', 'Ambassador', 'Hashnode', 'InkDrop', 'CoderByte', 'Codility', 
                 'CircleCI', 'P5.js Editor']
    
    dev_urls = [
        'https://vscode.dev',
        'https://codepen.io/estevam5s',
        'https://docs.nestjs.com',
        'https://www.npmjs.com/',
        'https://stackblitz.com/',
        'https://colab.research.google.com/',
        'https://replit.com/~',
        'https://gitpod.io/',
        'https://codesandbox.io/',
        'https://codeanywhere.com/solutions/collaborate',
        'https://react-icons.github.io/react-icons/search/#q=bitcoin',
        'https://app.amplication.com/login',
        'https://caniuse.com/',
        'https://app.getambassador.io/auth/realms/production/protocol/openid-connect/auth?client_id=ambassador&redirect_uri=https%3A%2F%2Fapp.getambassador.io%2F.ambassador%2Foauth2%2Fredirection-endpoint&response_type=code&scope=profile+openid+email&state=b970c0287c15582429be641470baa869b4b35579da00fcc88fc82822acb1005c',
        'https://hashnode.com/products/blogs?source=blog-footer',
        'https://www.inkdrop.app/',
        'https://coderbyte.com/',
        'https://www.codility.com/',
        'https://circleci.com/',
        'https://editor.p5js.org/gustavomaga97/sketches/JThwT9SsM'
    ]
    
    dev_icons = ['fas fa-code', 'fab fa-codepen', 'fas fa-book', 'fab fa-npm', 'fas fa-bolt', 
                'fab fa-google', 'fas fa-terminal', 'fab fa-git', 'fas fa-cube', 'fas fa-code', 
                'fab fa-react', 'fas fa-database', 'fas fa-browser', 'fas fa-users', 
                'fas fa-blog', 'fas fa-sticky-note', 'fas fa-code', 'fas fa-tasks', 
                'fas fa-circle', 'fas fa-paint-brush']
    
    dev_descriptions = [
        'Editor de código online',
        'Editor de HTML/CSS/JS',
        'Documentação do NestJS',
        'Gerenciador de pacotes Node',
        'IDE online',
        'Notebooks de Python',
        'Ambiente de desenvolvimento',
        'IDE baseada no VS Code',
        'IDE para React',
        'Plataforma de codificação colaborativa',
        'Biblioteca de ícones para React',
        'Plataforma para criação de aplicações',
        'Compatibilidade de recursos em navegadores',
        'Plataforma de marketing para desenvolvedores',
        'Plataforma de blogs para desenvolvedores',
        'App para anotações para desenvolvedores',
        'Desafios de programação',
        'Testes técnicos para desenvolvedores',
        'CI/CD para desenvolvimento',
        'Editor para p5.js (Processing)'
    ]
    
    data['title'].extend(dev_titles)
    data['url'].extend(dev_urls)
    data['icon'].extend(dev_icons)
    data['category'].extend(['Desenvolvimento'] * len(dev_titles))
    data['description'].extend(dev_descriptions)

    # IoT & Desenvolvimento
    iot_titles = ['Alexa Skills Development', 'Arduino', 'AWS Free Tier']
    
    iot_urls = [
        'https://www.amazon.com/ap/signin',
        'https://app.arduino.cc/',
        'https://aws.amazon.com/pt/free/'
    ]
    
    iot_icons = ['fab fa-amazon', 'fas fa-microchip', 'fab fa-aws']
    
    iot_descriptions = [
        'Desenvolvimento de skills para Alexa',
        'Plataforma de prototipagem eletrônica',
        'Nível gratuito da AWS'
    ]
    
    data['title'].extend(iot_titles)
    data['url'].extend(iot_urls)
    data['icon'].extend(iot_icons)
    data['category'].extend(['IoT & Desenvolvimento'] * len(iot_titles))
    data['description'].extend(iot_descriptions)

    # Cyber Segurança
    security_titles = ['TryHackMe', 'Hispy', 'Exploit-DB', 'Kali Forums', 'Google Hacking DB', 
                       'OffSec', 'Shodan', 'WiFi Pumpkin', 'Ngrok']
    
    security_urls = [
        'https://tryhackme.com/r/hacktivities',
        'https://www.hispy.io',
        'https://www.exploit-db.com',
        'https://forums.kali.org',
        'https://www.exploit-db.com/google-hacking-database',
        'https://www.offsec.com',
        'https://www.shodan.io',
        'https://wifipumpkin3.github.io/docs/getting-started',
        'https://dashboard.ngrok.com/login'
    ]
    
    security_icons = ['fas fa-shield-alt', 'fas fa-user-secret', 'fas fa-bug', 'fas fa-dragon', 
                      'fab fa-google', 'fas fa-graduation-cap', 'fas fa-search', 'fas fa-wifi', 
                      'fas fa-tunnel']
    
    security_descriptions = [
        'Plataforma de aprendizado em segurança',
        'Ferramenta de OSINT',
        'Banco de dados de exploits',
        'Fórum da distribuição Kali Linux',
        'Técnicas de busca avançada',
        'Treinamentos em segurança',
        'Motor de busca de dispositivos',
        'Framework para redes WiFi',
        'Túneis para expor serviços locais'
    ]
    
    data['title'].extend(security_titles)
    data['url'].extend(security_urls)
    data['icon'].extend(security_icons)
    data['category'].extend(['Cyber Segurança'] * len(security_titles))
    data['description'].extend(security_descriptions)

    # Inteligência Artificial
    ai_titles = ['Claude AI', 'ChatGPT', 'Perplexity AI', 'Google Gemini', 'Blackbox AI', 
                'Microsoft Copilot', 'Mapify', 'Devin AI', 'OpenAI Playground', 'CrewAI', 
                'DeepSeek', 'Grok', 'V0', 'Lovable', 'Bolt']
    
    ai_urls = [
        'https://claude.ai',
        'https://chatgpt.com/auth/login',
        'https://www.perplexity.ai',
        'https://gemini.google.com',
        'https://www.blackbox.ai',
        'https://copilot.microsoft.com',
        'https://mapify.so/pt/editor',
        'https://www.cognition.ai/blog/introducing-devin',
        'https://platform.openai.com/playground',
        'https://www.crewai.com/',
        'https://chat.deepseek.com/',
        'https://grok.com/',
        'https://v0.dev/',
        'https://lovable.dev/',
        'https://bolt.new/'
    ]
    
    ai_icons = ['fas fa-brain', 'fas fa-robot', 'fas fa-lightbulb', 'fab fa-google', 
                'fas fa-cube', 'fab fa-microsoft', 'fas fa-map', 'fas fa-microchip', 
                'fas fa-flask', 'fas fa-users', 'fas fa-search-plus', 'fas fa-comment-dots', 
                'fas fa-code', 'fas fa-heart', 'fas fa-bolt']
    
    ai_descriptions = [
        'Assistente IA da Anthropic',
        'Assistente IA da OpenAI',
        'Busca com IA',
        'Assistente IA do Google',
        'IDE com IA',
        'Assistente IA da Microsoft',
        'Criação de mapas mentais',
        'Engenheiro de software autônomo',
        'Ambiente de testes OpenAI',
        'Framework para agentes IA',
        'Modelo LLM de código aberto',
        'Assistente IA da X',
        'Gerador de UI com IA',
        'Gerador de UI com IA',
        'Framework de desenvolvimento'
    ]
    
    data['title'].extend(ai_titles)
    data['url'].extend(ai_urls)
    data['icon'].extend(ai_icons)
    data['category'].extend(['Inteligência Artificial'] * len(ai_titles))
    data['description'].extend(ai_descriptions)

    # Cloud & DevOps
    cloud_titles = ['DigitalOcean', 'Termius', 'Easypanel', 'Proxmox', 'Proxmox Scripts', 'Umbrel', 'Hasura Cloud']
    
    cloud_urls = [
        'https://www.digitalocean.com',
        'https://account.termius.com/login',
        'http://147.93.66.4:3000/projects/services/create',
        'https://192.168.1.109:8006/#nodes/proxmox',
        'https://tteck.github.io/Proxmox/#n8n-lxc',
        'http://192.168.1.111/login?redirect=/',
        'https://cloud.hasura.io/signup?redirect_url=/projects'
    ]
    
    cloud_icons = ['fab fa-digital-ocean', 'fas fa-terminal', 'fas fa-layer-group', 
                  'fas fa-server', 'fas fa-book', 'fas fa-umbrella', 'fas fa-database']
    
    cloud_descriptions = [
        'Provedor de infraestrutura cloud',
        'Cliente SSH avançado',
        'Painel de administração para Docker',
        'Gerenciador de virtualização',
        'Scripts para Proxmox',
        'Servidor pessoal auto-hospedado',
        'Plataforma GraphQL como serviço'
    ]
    
    data['title'].extend(cloud_titles)
    data['url'].extend(cloud_urls)
    data['icon'].extend(cloud_icons)
    data['category'].extend(['Cloud & DevOps'] * len(cloud_titles))
    data['description'].extend(cloud_descriptions)

    # Segurança & Senhas
    password_titles = ['Bitwarden', 'Bitwarden Pessoal', 'LastPass Generator', 'Yubico Authenticator']
    
    password_urls = [
        'https://bitwarden.com',
        'https://bitwarden.estevamsouza.com.br/#/login',
        'https://www.lastpass.com/pt/features/password-generator',
        'https://www.yubico.com/products/yubico-authenticator/#h-download-yubico-authenticator'
    ]
    
    password_icons = ['fas fa-key', 'fas fa-lock', 'fas fa-key', 'fas fa-shield-alt']
    
    password_descriptions = [
        'Gerenciador de senhas',
        'Gerenciador de senhas hospedado',
        'Gerador de senhas seguras',
        'Autenticação em dois fatores'
    ]
    
    data['title'].extend(password_titles)
    data['url'].extend(password_urls)
    data['icon'].extend(password_icons)
    data['category'].extend(['Segurança & Senhas'] * len(password_titles))
    data['description'].extend(password_descriptions)

    # Monetização
    money_titles = ['GitHub Sponsors', 'Patreon', 'Buy Me a Coffee', 'Stripe']
    
    money_urls = [
        'https://github.com/sponsors/estevam5s/dashboard',
        'https://www.patreon.com/profile?u=148884361',
        'https://buymeacoffee.com/estevamsl/extras',
        'https://dashboard.stripe.com/login?redirect=/settings/user'
    ]
    
    money_icons = ['fab fa-github', 'fab fa-patreon', 'fas fa-coffee', 'fab fa-stripe']
    
    money_descriptions = [
        'Patrocínios no GitHub',
        'Plataforma de patrocínio',
        'Plataforma de doações',
        'Processamento de pagamentos'
    ]
    
    data['title'].extend(money_titles)
    data['url'].extend(money_urls)
    data['icon'].extend(money_icons)
    data['category'].extend(['Monetização'] * len(money_titles))
    data['description'].extend(money_descriptions)

    # Treino de Código
    training_titles = ['LeetCode', 'CodeWars', 'HackerRank']
    
    training_urls = [
        'https://leetcode.com/',
        'https://www.codewars.com/',
        'https://www.hackerrank.com/'
    ]
    
    training_icons = ['fas fa-code', 'fas fa-laptop-code', 'fab fa-hackerrank']
    
    training_descriptions = [
        'Plataforma de desafios de código',
        'Desafios de programação',
        'Desafios técnicos e entrevistas'
    ]
    
    data['title'].extend(training_titles)
    data['url'].extend(training_urls)
    data['icon'].extend(training_icons)
    data['category'].extend(['Treino de Código'] * len(training_titles))
    data['description'].extend(training_descriptions)

    # Treino de Digitação
    typing_titles = ['MonkeyType', '10FastFingers']
    
    typing_urls = [
        'https://monkeytype.com/',
        'https://10fastfingers.com/typing-test/portuguese'
    ]
    
    typing_icons = ['fas fa-keyboard', 'fas fa-keyboard']
    
    typing_descriptions = [
        'Treino de digitação minimalista',
        'Teste de velocidade de digitação'
    ]
    
    data['title'].extend(typing_titles)
    data['url'].extend(typing_urls)
    data['icon'].extend(typing_icons)
    data['category'].extend(['Treino de Digitação'] * len(typing_titles))
    data['description'].extend(typing_descriptions)

    # Carteira de Cripto
    crypto_titles = ['Binance', 'Bity Preço', 'Bity', 'SafePal']
    
    crypto_urls = [
        'https://accounts.binance.com/pt-BR/login',
        'https://market.bitypreco.com/profile/account',
        'https://www.bity.com.br/',
        'https://safepal.com/'
    ]
    
    crypto_icons = ['fab fa-bitcoin', 'fas fa-chart-line', 'fab fa-ethereum', 'fas fa-wallet']
    
    crypto_descriptions = [
        'Exchange de criptomoedas',
        'Monitor de preços de criptomoedas',
        'Serviço de câmbio de criptomoedas',
        'Carteira de hardware para criptomoedas'
    ]
    
    data['title'].extend(crypto_titles)
    data['url'].extend(crypto_urls)
    data['icon'].extend(crypto_icons)
    data['category'].extend(['Carteira de Cripto'] * len(crypto_titles))
    data['description'].extend(crypto_descriptions)

    # Armazenamento em Nuvem
    storage_titles = ['Dropbox']
    
    storage_urls = [
        'https://www.dropbox.com/home'
    ]
    
    storage_icons = ['fab fa-dropbox']
    
    storage_descriptions = [
        'Armazenamento em nuvem'
    ]
    
    data['title'].extend(storage_titles)
    data['url'].extend(storage_urls)
    data['icon'].extend(storage_icons)
    data['category'].extend(['Armazenamento em Nuvem'] * len(storage_titles))
    data['description'].extend(storage_descriptions)

    # VPN
    vpn_titles = ['NordVPN', 'Tailscale']
    
    vpn_urls = [
        'https://nordaccount.com/login',
        'https://login.tailscale.com/admin/machines'
    ]
    
    vpn_icons = ['fas fa-shield-alt', 'fas fa-network-wired']
    
    vpn_descriptions = [
        'Serviço de VPN',
        'Rede mesh VPN'
    ]
    
    data['title'].extend(vpn_titles)
    data['url'].extend(vpn_urls)
    data['icon'].extend(vpn_icons)
    data['category'].extend(['VPN'] * len(vpn_titles))
    data['description'].extend(vpn_descriptions)

    # Educação
    education_titles = ['Udemy', 'Danki Code', 'Origamid', 'Ignite', 'StudoCu', 'Passei Direto', 
                       'Codecademy', 'W3Schools', 'freeCodeCamp', 'GitHub Learning Lab']
    
    education_urls = [
        'https://www.udemy.com/',
        'https://cursos.dankicode.com/login',
        'https://www.origamid.com/conta/',
        'https://hotmart.com/pt-br/marketplace/produtos/ignite-6eb3n/K83217735E',
        'https://www.studocu.com/pt-br/home',
        'https://www.passeidireto.com/',
        'https://www.codecademy.com/',
        'https://www.w3schools.com/',
        'https://www.freecodecamp.org/',
        'https://github.com/apps/github-learning-lab'
    ]
    
    education_icons = ['fas fa-graduation-cap', 'fas fa-laptop-code', 'fas fa-fox-alt', 
                      'fas fa-fire', 'fas fa-book', 'fas fa-book-open', 'fas fa-code', 
                      'fas fa-globe', 'fab fa-free-code-camp', 'fab fa-github']
    
    education_descriptions = [
        'Plataforma de cursos online',
        'Cursos de programação',
        'Cursos de design e front-end',
        'Bootcamp da Rocketseat',
        'Compartilhamento de materiais de estudo',
        'Plataforma de materiais acadêmicos',
        'Plataforma de aprendizado interativo',
        'Tutoriais de desenvolvimento web',
        'Cursos gratuitos de programação',
        'Aprendizado no GitHub'
    ]
    
    data['title'].extend(education_titles)
    data['url'].extend(education_urls)
    data['icon'].extend(education_icons)
    data['category'].extend(['Educação'] * len(education_titles))
    data['description'].extend(education_descriptions)

    # Documentação de Código
    docs_titles = ['NestJS', 'Node.js', 'Prisma', 'Sequelize', 'NPM Docs', 'DevDocs', 'Express.js', 
                  'C++ Reference', 'CoffeeScript', 'Gulp.js', 'Husky', 'Knex.js', 'Julia Docs', 
                  'Scilab Docs', 'GeeksForGeeks', 'TypeORM', 'GraphQL', 'Apollo', 'TypeScript', 
                  'MongoDB', 'PostgreSQL', 'Docker', 'Git', 'Railway Docs', 'Roadmap.sh', 
                  'Deno', 'ESLint', 'Learn X in Y Minutes', 'Babel', 'CircleCI Docs', 
                  'PlanetScale', 'Mongoose', 'Jest', 'Prettier', 'Yarn']
    
    docs_urls = [
        'https://nestjs.com/',
        'https://nodejs.org/docs/latest/api/',
        'https://www.prisma.io/docs',
        'https://sequelize.org/docs/v7/getting-started/',
        'https://docs.npmjs.com/',
        'https://devdocs.io/',
        'https://expressjs.com/',
        'https://cplusplus.com/reference/clibrary/',
        'https://coffeescript.org/#strings',
        'https://gulpjs.com/',
        'https://typicode.github.io/husky/get-started.html',
        'https://knexjs.org/',
        'https://docs.julialang.org/en/v1/',
        'https://scilab.gitlab.io/legacy_wiki/Documentation',
        'https://www.geeksforgeeks.org/',
        'https://typeorm.io/',
        'https://graphql.org/learn/',
        'https://www.apollographql.com/docs/',
        'https://www.typescriptlang.org/docs/',
        'https://www.mongodb.com/pt-br/docs/drivers/node/current/',
        'https://www.postgresql.org/docs/',
        'https://docs.docker.com/',
        'https://git-scm.com/docs',
        'https://docs.railway.com/',
        'https://roadmap.sh/',
        'https://docs.deno.com/runtime/',
        'https://eslint.org/docs/latest/use/migrating-to-7.0.0',
        'https://learnxinyminutes.com/',
        'https://babeljs.io/docs/',
        'https://circleci.com/docs/getting-started/',
        'https://planetscale.com/docs',
        'https://mongoosejs.com/docs/guide.html',
        'https://jestjs.io/docs/getting-started',
        'https://prettier.io/docs/index.html',
        'https://classic.yarnpkg.com/lang/en/docs/'
    ]
    
    # Icons para documentação
    docs_icons = ['fas fa-cog', 'fab fa-node-js', 'fas fa-database', 'fas fa-table', 
                 'fab fa-npm', 'fas fa-book-reader', 'fas fa-server', 'fas fa-code', 
                 'fas fa-coffee', 'fas fa-stream', 'fas fa-dog', 'fas fa-database', 
                 'fas fa-code', 'fas fa-flask', 'fas fa-code', 'fas fa-database', 
                 'fas fa-project-diagram', 'fas fa-rocket', 'fab fa-js', 'fas fa-database', 
                 'fas fa-database', 'fab fa-docker', 'fab fa-git-alt', 'fas fa-train', 
                 'fas fa-road', 'fas fa-globe', 'fas fa-code', 'fas fa-language', 
                 'fas fa-scroll', 'fas fa-circle', 'fas fa-planet-ringed', 'fas fa-database', 
                 'fas fa-vial', 'fas fa-magic', 'fas fa-yarn']
    
    # Descrições para documentação
    docs_descriptions = [
        'Framework Node.js',
        'Documentação do Node.js',
        'ORM para Node.js',
        'ORM para Node.js',
        'Documentação do NPM',
        'Biblioteca de documentações centralizada',
        'Framework web para Node.js',
        'Referência da biblioteca C',
        'Linguagem que compila para JavaScript',
        'Automatizador de tarefas para JavaScript',
        'Git hooks simplificados',
        'Query builder para SQL',
        'Linguagem de programação científica',
        'Ambiente de computação numérica',
        'Recursos para desenvolvimento e algoritmos',
        'ORM para TypeScript',
        'Linguagem de consulta para APIs',
        'Cliente GraphQL',
        'JavaScript com tipagem',
        'Driver para MongoDB',
        'Documentação do PostgreSQL',
        'Plataforma de contêineres',
        'Sistema de controle de versão',
        'Documentação da Railway',
        'Guias de aprendizado para desenvolvedores',
        'Runtime JavaScript moderno',
        'Linter para JavaScript',
        'Aprendizado rápido de linguagens',
        'Compilador JavaScript',
        'Documentação do CircleCI',
        'Banco de dados serverless',
        'ODM para MongoDB',
        'Framework de testes para JavaScript',
        'Formatador de código',
        'Gerenciador de pacotes'
    ]
    
    data['title'].extend(docs_titles)
    data['url'].extend(docs_urls)
    data['icon'].extend(docs_icons)
    data['category'].extend(['Doc de Código'] * len(docs_titles))
    data['description'].extend(docs_descriptions)

    # GitHub e Ferramentas
    github_titles = ['GitHub Developer Program', 'Source Karma', 'Sourcegraph', 'DeepSource', 
                    'Gitea', 'Shields.io', 'GitHub Repositórios', 'Awesome GitHub Stats', 
                    'GitHut', 'GitHub Readme Stats', 'Devicon', 'Easystats']
    
    github_urls = [
        'https://developer.github.com/program/',
        'https://sourcekarma.vercel.app/',
        'https://sourcegraph.com/search',
        'https://app.deepsource.com/',
        'https://about.gitea.com/',
        'https://shields.io/',
        'https://thiagosalome.github.io/github-repositorios/dist/internal.html',
        'https://awesome-github-stats.azurewebsites.net/',
        'https://madnight.github.io/githut/#/pull_requests/2022/1',
        'https://www.jasongaylord.com/blog/2020/10/28/implementing-github-readme-statistics',
        'https://devicon.dev/',
        'https://easystats.github.io/easystats/'
    ]
    
    github_icons = ['fab fa-github', 'fas fa-code-branch', 'fas fa-search', 'fas fa-microscope', 
                   'fab fa-git-alt', 'fas fa-shield-alt', 'fas fa-folder-open', 'fas fa-chart-bar', 
                   'fas fa-chart-pie', 'fas fa-star', 'fas fa-icons', 'fas fa-chart-line']
    
    github_descriptions = [
        'Programa para desenvolvedores GitHub',
        'Estatísticas sobre contribuições',
        'Mecanismo de busca de código',
        'Análise automática de código',
        'Git auto-hospedado',
        'Distintivos para README',
        'Visualizador de repositórios',
        'Estatísticas para GitHub',
        'Visualização de dados do GitHub',
        'Estatísticas para README',
        'Ícones de tecnologias para desenvolvedores',
        'Framework de estatísticas para R'
    ]
    
    data['title'].extend(github_titles)
    data['url'].extend(github_urls)
    data['icon'].extend(github_icons)
    data['category'].extend(['GitHub & Ferramentas'] * len(github_titles))
    data['description'].extend(github_descriptions)

    # Serviços de Pagamento
    payment_titles = ['PayPal']
    
    payment_urls = [
        'https://www.paypal.com/signin'
    ]
    
    payment_icons = ['fab fa-paypal']
    
    payment_descriptions = [
        'Serviço de pagamentos online'
    ]
    
    data['title'].extend(payment_titles)
    data['url'].extend(payment_urls)
    data['icon'].extend(payment_icons)
    data['category'].extend(['Serviços de Pagamento'] * len(payment_titles))
    data['description'].extend(payment_descriptions)

    # Fontes e Design
    fonts_titles = ['Nerd Fonts']
    
    fonts_urls = [
        'https://www.nerdfonts.com/#home'
    ]
    
    fonts_icons = ['fas fa-font']
    
    fonts_descriptions = [
        'Fontes para desenvolvedores com ícones'
    ]
    
    data['title'].extend(fonts_titles)
    data['url'].extend(fonts_urls)
    data['icon'].extend(fonts_icons)
    data['category'].extend(['Fontes & Design'] * len(fonts_titles))
    data['description'].extend(fonts_descriptions)

    # Outros
    others_titles = ['LinkedIn Skill Assessments']
    
    others_urls = [
        'https://github.com/Ebazhanov/linkedin-skill-assessments-quizzes'
    ]
    
    others_icons = ['fab fa-linkedin']
    
    others_descriptions = [
        'Quizzes para avaliações do LinkedIn'
    ]
    
    data['title'].extend(others_titles)
    data['url'].extend(others_urls)
    data['icon'].extend(others_icons)
    data['category'].extend(['Outros'] * len(others_titles))
    data['description'].extend(others_descriptions)

    # Criar o DataFrame
    df = pd.DataFrame(data)
    return df

# Aplicação principal - Inicialização e configuração
def main():
    # Aplicar CSS personalizado
    local_css()
    
    # Carregamento inicial de dados
    links_df = load_links_data()
    
    # Sidebar
    with st.sidebar:
        try:
            profile_image = load_image_from_url("https://media.licdn.com/dms/image/v2/D4D03AQG1LthzngDNMQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1729293996215?e=1740614400&v=beta&t=fWNRhpyHopeBTOQF3H-KWLVvEh4TZeQRTY-_42RtzB4")
            st.image(profile_image, width=150)
        except:
            st.image("https://via.placeholder.com/150", width=150)
        
        st.markdown("<h2>Estevam Souza</h2>", unsafe_allow_html=True)
        st.markdown("<p>Desenvolvedor Full Stack & Especialista em IA</p>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Links", "Categorias", "Análise", "Sobre"],
            icons=["speedometer2", "link", "folder", "graph-up", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )

    # Dashboard principal
    if selected == "Dashboard":
        st.markdown("<h1 class='dashboard-title'>Hub de Serviços - Dashboard</h1>", unsafe_allow_html=True)
        
        # Stats em cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Total de links
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-link"></i></div>
                <div class="stat-value">{len(links_df)}</div>
                <div class="stat-label">Total de Links</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Total de categorias
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-folder"></i></div>
                <div class="stat-value">{links_df['category'].nunique()}</div>
                <div class="stat-label">Categorias</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Categoria com mais links
        top_category = links_df['category'].value_counts().index[0]
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-star"></i></div>
                <div class="stat-value">{links_df['category'].value_counts().max()}</div>
                <div class="stat-label">Links na maior categoria</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Categoria principal
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-trophy"></i></div>
                <div class="stat-value">{top_category}</div>
                <div class="stat-label">Categoria principal</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Links por Categoria")
            category_counts = links_df['category'].value_counts().reset_index()
            category_counts.columns = ['Categoria', 'Quantidade']
            
            # Ordena e pega top 10 para melhor visualização
            category_counts = category_counts.sort_values('Quantidade', ascending=False).head(10)
            
            fig = px.bar(category_counts, x='Categoria', y='Quantidade', 
                        color='Quantidade', 
                        color_continuous_scale='Blues',
                        labels={'Quantidade': 'Número de Links'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Distribuição de Links")
            top_categories = category_counts.head(8)
            fig = px.pie(top_categories, values='Quantidade', names='Categoria', hole=0.4)
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        # Links recentes ou destaques
        st.markdown("<h3>Links em Destaque</h3>", unsafe_allow_html=True)
        
        # Filtrando algumas categorias importantes para destacar
        important_categories = ['Desenvolvimento', 'Inteligência Artificial', 'Serviços']
        featured_links = pd.concat([
            links_df[links_df['category'] == cat].sample(min(2, len(links_df[links_df['category'] == cat]))) 
            for cat in important_categories
        ]).reset_index(drop=True)
        
        # Organizando em colunas
        cols = st.columns(3)
        
        for i, (_, link) in enumerate(featured_links.iterrows()):
            with cols[i % 3]:
                st.markdown(create_link_card(
                    link['icon'],
                    link['title'],
                    link['url'],
                    link['description']
                ), unsafe_allow_html=True)

    # Página de Links
    elif selected == "Links":
        st.markdown("<h1 class='dashboard-title'>Todos os Links</h1>", unsafe_allow_html=True)
        
        # Barra de pesquisa
        search_query = st.text_input("Pesquisar links...", key="search_links")
        
        # Filtros de categoria
        all_categories = sorted(links_df['category'].unique())
        selected_categories = st.multiselect(
            "Filtrar por categoria",
            all_categories,
            default=[]
        )
        
        # Aplicar filtros
        if search_query or selected_categories:
            filtered_df = links_df.copy()
            
            # Filtro de busca textual
            if search_query:
                filtered_df = filtered_df[
                    filtered_df['title'].str.contains(search_query, case=False) | 
                    filtered_df['category'].str.contains(search_query, case=False) |
                    filtered_df['description'].str.contains(search_query, case=False)
                ]
                st.write(f"Mostrando {len(filtered_df)} resultados para '{search_query}'")
            
            # Filtro de categorias
            if selected_categories:
                filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
                
            if len(filtered_df) == 0:
                st.warning("Nenhum resultado encontrado. Tente outros termos de busca.")
        else:
            filtered_df = links_df
        
        # Exibir links por categoria
        categories = filtered_df['category'].unique()
        
        for category in categories:
            cat_links = filtered_df[filtered_df['category'] == category]
            
            st.markdown(f"<h2 class='category-title'>{category} <span class='category-count'>{len(cat_links)} links</span></h2>", unsafe_allow_html=True)
            
            # Criando colunas para os cards
            cols = st.columns(3)
            
            # Distribuindo os links nas colunas
            for i, (_, link) in enumerate(cat_links.iterrows()):
                with cols[i % 3]:
                    st.markdown(create_link_card(
                        link['icon'],
                        link['title'],
                        link['url'],
                        link['description']
                    ), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

    # Página de Categorias
    elif selected == "Categorias":
        st.markdown("<h1 class='dashboard-title'>Gerenciar Categorias</h1>", unsafe_allow_html=True)
        
        # Obter categorias e contagem
        category_counts = links_df['category'].value_counts().reset_index()
        category_counts.columns = ['Categoria', 'Total de Links']
        
        # Visualização das categorias
        st.subheader("Categorias de Links")
        
        # Métrica para total de categorias
        st.metric("Total de Categorias", category_counts.shape[0])
        
        # Tabela de categorias
        st.dataframe(category_counts, use_container_width=True, hide_index=True)
        
        # Visualização em gráfico
        st.subheader("Distribuição de Links por Categoria")
        fig = px.bar(category_counts, 
                    x='Categoria', 
                    y='Total de Links',
                    color='Total de Links',
                    color_continuous_scale='blues',
                    labels={'Total de Links': 'Quantidade'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Funcionalidade simulada para adicionar categoria
        st.subheader("Adicionar Nova Categoria")
        with st.form("add_category_form"):
            category_name = st.text_input("Nome da Categoria")
            category_icon = st.text_input("Ícone FontAwesome (ex: fas fa-folder)")
            category_description = st.text_area("Descrição da Categoria")
            submitted = st.form_submit_button("Adicionar Categoria")
            
            if submitted:
                if category_name:
                    st.success(f"Categoria '{category_name}' adicionada com sucesso! (simulação)")
                    st.info("Em um sistema real, esta categoria seria salva no banco de dados.")
                else:
                    st.error("O nome da categoria é obrigatório.")

        # Remover categoria (simulado)
        st.subheader("Remover Categoria")
        with st.form("remove_category_form"):
            categories = links_df['category'].unique().tolist()
            category_to_remove = st.selectbox("Selecione a categoria para remover", categories)
            confirm_removal = st.checkbox("Confirmo que desejo remover esta categoria")
            submitted = st.form_submit_button("Remover Categoria")
            
            if submitted:
                if confirm_removal:
                    st.warning(f"Categoria '{category_to_remove}' removida com sucesso! (simulação)")
                    st.info("Em um sistema real, esta categoria seria removida do banco de dados.")
                else:
                    st.error("Você precisa confirmar a remoção da categoria.")

    # Página de Análise
    elif selected == "Análise":
        st.markdown("<h1 class='dashboard-title'>Análise de Links</h1>", unsafe_allow_html=True)
        
        # Estatísticas gerais
        st.subheader("Estatísticas Gerais")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Links", len(links_df))
        
        with col2:
            st.metric("Total de Categorias", links_df['category'].nunique())
        
        with col3:
            st.metric("Média de Links por Categoria", round(len(links_df) / links_df['category'].nunique(), 1))
        
        # Análise de categorias
        st.subheader("Distribuição de Links")
        
        # Criando dados para visualização
        category_data = links_df['category'].value_counts().reset_index()
        category_data.columns = ['Categoria', 'Quantidade']
        
        # Gráfico de barras horizontal
        fig = px.bar(category_data, 
                    x='Quantidade', 
                    y='Categoria',
                    orientation='h',
                    color='Quantidade',
                    color_continuous_scale='blues',
                    title='Links por Categoria')
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de uso (simulado)
        st.subheader("Análise de Uso (Simulado)")
        
        # Simulando dados de uso
        import numpy as np
        np.random.seed(42)
        
        # Criar um dataframe de uso simulado
        usage_data = {
            'categoria': [],
            'cliques': [],
            'data': []
        }
        
        # Simular dados de uso para os últimos 30 dias
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=30)
        dates = [start_date + datetime.timedelta(days=x) for x in range(31)]
        
        for date in dates:
            for category in links_df['category'].unique():
                usage_data['categoria'].append(category)
                usage_data['cliques'].append(np.random.randint(1, 30))
                usage_data['data'].append(date.strftime('%Y-%m-%d'))
        
        usage_df = pd.DataFrame(usage_data)
        
        # Agregando por data
        daily_usage = usage_df.groupby('data')['cliques'].sum().reset_index()
        daily_usage.columns = ['Data', 'Cliques']
        
        # Gráfico de linha para uso diário
        fig = px.line(daily_usage, 
                    x='Data', 
                    y='Cliques',
                    title='Uso Diário (Cliques)',
                    markers=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Agregando por categoria
        category_usage = usage_df.groupby('categoria')['cliques'].sum().reset_index()
        category_usage.columns = ['Categoria', 'Cliques']
        category_usage = category_usage.sort_values('Cliques', ascending=False)
        
        # Top categorias mais acessadas
        st.subheader("Top Categorias Mais Acessadas")
        
        # Gráfico de pizza
        fig = px.pie(category_usage.head(5), 
                    values='Cliques', 
                    names='Categoria',
                    title='Top 5 Categorias por Uso',
                    hole=0.4)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(category_usage.head(5), hide_index=True, use_container_width=True)
            
        # Mapa de calor dos cliques por dia da semana e categoria (simulado)
        st.subheader("Padrões de Uso por Dia da Semana (Simulado)")
        
        # Criar dados simulados
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        top_categories = links_df['category'].value_counts().head(5).index.tolist()
        
        heatmap_data = []
        for day in days:
            for category in top_categories:
                heatmap_data.append({
                    'Dia': day,
                    'Categoria': category,
                    'Cliques': np.random.randint(10, 100)
                })
        
        heatmap_df = pd.DataFrame(heatmap_data)
        
        # Criar mapa de calor
        heatmap_pivot = heatmap_df.pivot(index='Dia', columns='Categoria', values='Cliques')
        
        fig = px.imshow(
            heatmap_pivot,
            labels=dict(x="Categoria", y="Dia da Semana", color="Cliques"),
            x=heatmap_pivot.columns,
            y=days,
            color_continuous_scale='blues',
            aspect="auto"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise de tendências (simulado)
        st.subheader("Tendências de Uso (Simulado)")
        
        # Simular dados de tendência para 3 categorias
        trend_categories = ['Desenvolvimento', 'Inteligência Artificial', 'Cloud & DevOps']
        dates = pd.date_range(end=datetime.datetime.now(), periods=90, freq='D')
        
        trend_data = []
        for category in trend_categories:
            # Criar tendência com aumento gradual para IA, estável para Dev e variável para Cloud
            base = 30 if category == 'Desenvolvimento' else (
                np.linspace(10, 50, 90) if category == 'Inteligência Artificial' else np.sin(np.linspace(0, 6, 90)) * 10 + 25
            )
            
            for i, date in enumerate(dates):
                trend_data.append({
                    'Data': date,
                    'Categoria': category,
                    'Cliques': int(base[i] if isinstance(base, np.ndarray) else base + np.random.normal(0, 5))
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        # Gráfico de linha
        fig = px.line(trend_df, 
                     x='Data', 
                     y='Cliques', 
                     color='Categoria',
                     title='Tendências de Uso por Categoria')
        
        st.plotly_chart(fig, use_container_width=True)

    # Página Sobre
    elif selected == "Sobre":
        st.markdown("<h1 class='dashboard-title'>Sobre o Hub de Serviços</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                profile_image = load_image_from_url("https://media.licdn.com/dms/image/v2/D4D03AQG1LthzngDNMQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1729293996215?e=1740614400&v=beta&t=fWNRhpyHopeBTOQF3H-KWLVvEh4TZeQRTY-_42RtzB4")
                st.image(profile_image, width=200)
            except:
                st.image("https://via.placeholder.com/200", width=200)
        
        with col2:
            st.markdown("""
            ## Estevam Souza
            ### Desenvolvedor Full Stack & Especialista em IA
            
            Profissional com experiência em desenvolvimento web, inteligência artificial e arquitetura de sistemas.
            
            - **LinkedIn**: [linkedin.com/in/estevam-souza](https://www.linkedin.com/in/estevam-souza)
            - **Website**: [estevamsouza.com.br](https://www.estevamsouza.com.br)
            - **Email**: contato@estevamsouza.com.br
            """)
        
        st.markdown("---")
        
        st.markdown("""
        ## Sobre este Dashboard
        
        Este Hub de Serviços é uma plataforma desenvolvida com Python e Streamlit para organizar e gerenciar links profissionais de forma eficiente.
        
        ### Funcionalidades:
        
        - Organização de links em categorias
        - Busca rápida por links e categorias
        - Visualizações e estatísticas de uso
        - Interface responsiva e profissional
        
        ### Tecnologias Utilizadas:
        
        - **Python**: Linguagem de programação principal
        - **Streamlit**: Framework para criação de dashboards interativos
        - **Pandas**: Manipulação e análise de dados
        - **Plotly**: Visualizações e gráficos interativos
        - **FontAwesome**: Ícones para interface
        
        ### Como Instalar:
        
        ```bash
        # Clone o repositório
        git clone https://github.com/estevam5s/hub-servicos.git
        
        # Entre no diretório
        cd hub-servicos
        
        # Instale as dependências
        pip install -r requirements.txt
        
        # Execute a aplicação
        streamlit run app.py
        ```
        """)
        
        # Versão do sistema
        st.markdown("---")
        st.markdown("**Hub de Serviços v1.0.0** | Desenvolvido por Estevam Souza | &copy; 2025")
        
        # Contato
        st.subheader("Entre em Contato")
        
        with st.form("contact_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nome")
            
            with col2:
                email = st.text_input("Email")
            
            message = st.text_area("Mensagem")
            submitted = st.form_submit_button("Enviar")
            
            if submitted:
                if name and email and message:
                    st.success("Mensagem enviada com sucesso! (simulação)")
                    st.info("Em um sistema real, esta mensagem seria enviada para o email de contato.")
                else:
                    st.error("Por favor, preencha todos os campos.")

# Executar o aplicativo
if __name__ == "__main__":
    main()