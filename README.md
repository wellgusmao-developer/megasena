🎰 Mega-Sena Analyst PRO
https://img.shields.io/badge/Python-3.11-blue
https://img.shields.io/badge/Streamlit-1.28-red
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Status-Ativo-brightgreen

Uma ferramenta completa para análise estatística da Mega-Sena com dados oficiais da Caixa Econômica Federal

<p align="center"> <img src="https://raw.githubusercontent.com/wellgusmao/megasena/main/screenshot.png" alt="Mega-Sena Analyst PRO" width="800"> </p>
📌 Sobre o Projeto
O Mega-Sena Analyst PRO é uma aplicação web desenvolvida em Python com Streamlit que permite analisar todos os resultados oficiais da Mega-Sena e gerar jogos baseados em estatísticas reais. A ferramenta consome diretamente a API oficial da Caixa Econômica Federal, garantindo dados 100% confiáveis e atualizados.

🎯 Objetivo
Democratizar o acesso às estatísticas da Mega-Sena, permitindo que qualquer pessoa possa tomar decisões mais informadas na hora de fazer suas apostas, com base em dados reais e análises aprofundadas.

✨ Funcionalidades
📥 Download Automático
Busca todos os resultados diretamente da API oficial da Caixa

Mais de 3.000 concursos analisados

Atualização automática quando novos concursos são sorteados

🎯 Último Resultado
Visualização imediata do concurso mais recente

Informações detalhadas: data, local, prêmio, ganhadores

Destaque visual quando o concurso acumula

📊 Análise Estatística Completa
Frequência individual de cada número (1 a 60)

Top 15 números mais sorteados (🔥 Números Quentes)

Top 15 números menos sorteados (❄️ Números Frios)

Pares de números mais frequentes (🤝 Top 20)

Gráficos interativos com Plotly

Linha da média para referência visual

🎰 Gerador Inteligente de Jogos
Estratégias disponíveis:

Aleatório: Números puramente aleatórios

Números Quentes: Apenas os mais frequentes

Números Frios: Apenas os menos frequentes

Mistura Quente/Frio (3/3): Equilíbrio entre frequentes e raros

Par/Ímpar Balanceado (3/3): Distribuição equilibrada

📱 Design Responsivo
Funciona perfeitamente em celulares, tablets e computadores

Interface moderna com gradientes e animações

Cards interativos com efeitos hover

🚀 Tecnologias Utilizadas
Tecnologia	Versão	Função
Python	3.11	Linguagem principal
Streamlit	1.28	Framework web
Pandas	2.1	Manipulação de dados
Plotly	5.18	Gráficos interativos
Requests	2.31	Consumo da API
API Caixa	-	Fonte oficial dos dados
📦 Instalação Local
Pré-requisitos
Python 3.11 ou superior

pip (gerenciador de pacotes)

Passo a Passo
Clone o repositório

bash
git clone https://github.com/wellgusmao/megasena.git
cd megasena
Crie um ambiente virtual (recomendado)

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
Instale as dependências

bash
pip install -r requirements.txt
Execute a aplicação

bash
streamlit run app.py
Acesse no navegador

text
http://localhost:8501
☁️ Deploy no Streamlit Cloud
O projeto já está disponível online! Acesse:

🔗 https://megasenaanalyzer.streamlit.app/

Para fazer seu próprio deploy:
Faça um fork deste repositório

Acesse share.streamlit.io

Conecte sua conta do GitHub

Selecione o repositório e o branch main

Clique em "Deploy"

📁 Estrutura do Projeto
text
megasena/
│
├── app.py                    # Aplicação principal
├── megasena_analyzer.py      # Módulo de análise
├── requirements.txt          # Dependências
├── runtime.txt               # Versão do Python
├── packages.txt              # Dependências do sistema
├── .gitignore                # Arquivos ignorados
│
├── megasena_completo.json    # Cache dos resultados
└── README.md                 # Documentação
📊 Como Usar
1. Download dos Dados
Ao abrir o app, clique em "📥 Download Resultados"

Aguarde o download dos mais de 3.000 concursos

Após o download, os dados ficam em cache para acesso rápido

2. Análise Estatística
Navegue até "📊 Análise Estatística"

Visualize as métricas principais

Explore os gráficos interativos

Confira os tops de números quentes e frios

Veja os pares mais frequentes

3. Gerador de Jogos
Acesse "🎰 Gerador de Jogos"

Escolha uma estratégia

Defina quantidade de conjuntos e jogos

Clique em "Gerar Jogos"

Faça download dos resultados em CSV

💚 Apoie o Projeto
Se você gostou da ferramenta e quer ajudar a mantê-la no ar com melhorias constantes, considere fazer uma doação via PIX:

📧 Chave PIX (E-mail): wellingtongsmao34@gmail.com

Qualquer valor é bem-vindo e será revertido em:

☁️ Manutenção do servidor

🚀 Novas funcionalidades

📱 Versão mobile nativa

🤖 Mais estratégias de jogo

📊 Gráficos e estatísticas avançadas

🤝 Contribuições
Contribuições são sempre bem-vindas! Para contribuir:

Faça um fork do projeto

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📝 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

📬 Contato
Wellington Gusmão

📧 E-mail: wellingtongsmao34@gmail.com

💚 PIX: wellingtongsmao34@gmail.com

🔗 LinkedIn: Seu LinkedIn

🐙 GitHub: wellgusmao

🙏 Agradecimentos
Caixa Econômica Federal pela disponibilização dos dados

Streamlit pela plataforma incrível

Comunidade Open Source pelas bibliotecas utilizadas

Todos os apoiadores que contribuíram via PIX

<p align="center"> Feito com 💚 por <a href="https://github.com/wellgusmao">Wellington Gusmão</a> </p><p align="center"> <a href="https://megasenaanalyzer.streamlit.app/">🌐 Acesse o App</a> • <a href="https://www.youtube.com/watch?v=KRWRkiisxh8">📺 Assista ao Vídeo</a> </p>
