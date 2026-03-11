import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
from datetime import datetime
from megasena_analyzer import MegaSenaDeepAnalyzer

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Mega-Sena Analyst PRO",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': '### Mega-Sena Analyst PRO\nVersão 2.0\n\nDados oficiais da Caixa Econômica Federal'
    }
)

# -------- CSS MODERNO --------
st.markdown("""
<style>
    /* Remover elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo global */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Cards modernos */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card h3 {
        font-size: 1rem;
        margin-bottom: 10px;
        opacity: 0.9;
    }
    
    .metric-card .value {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    /* Números em quadrados */
    .number-square {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        display: inline-block;
        text-align: center;
        line-height: 60px;
    }
    
    .number-hot {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .number-cold {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Container para números */
    .numbers-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
        justify-content: center;
    }
    
    /* Títulos */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(102,126,234,0.4);
    }
    
    /* Sidebar corrigida */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Texto da sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Título da sidebar */
    .sidebar-title {
        text-align: center;
        font-size: 1.5rem;
        color: white;
        padding: 20px 0;
    }
    
    /* Card de resultado */
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .info-tag {
        background: #f0f2f6;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        color: #666;
        display: inline-block;
        margin: 5px;
    }
            
    /* RESPONSIVO MOBILE */
    @media (max-width: 600px) {

        .donation-banner {
            padding: 8px 10px;
        }

        .banner-content {
            gap: 8px;
            flex-direction: column;
        }

        .pix-card {
            font-size: 0.9rem;
            padding: 6px 12px;
            gap: 8px;
        }

        .copy-button {
            padding: 4px 10px;
            font-size: 0.8rem;
        }

    }
</style>
""", unsafe_allow_html=True)

# -------- SESSION --------
if "analyzer" not in st.session_state:
    st.session_state.analyzer = MegaSenaDeepAnalyzer()

if "stats" not in st.session_state:
    st.session_state.stats = None

if "last_update" not in st.session_state:
    st.session_state.last_update = None

if "last_result" not in st.session_state:
    st.session_state.last_result = None

analyzer = st.session_state.analyzer

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>🎰 Mega-Sena<br>Analyst PRO</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "📌 Menu",
        [
            "📥 Download Resultados",
            "📊 Análise Estatística",
            "🎰 Gerador de Jogos"
        ],
        label_visibility="collapsed",
        key="menu_principal"
    )
    
    if st.session_state.stats:
        st.markdown("---")
        st.metric("📊 Concursos", st.session_state.stats['total_games'])
        
        if st.session_state.last_update:
            st.caption(f"🕐 Atualizado: {st.session_state.last_update}")
    
    st.markdown("---")
    st.caption("v2.0 - Dados Oficiais Caixa")

# -------- CONTEÚDO PRINCIPAL --------
st.markdown("<h1 class='section-title'>🎰 Mega-Sena Analyst PRO</h1>", unsafe_allow_html=True)

# ----------------------------------------------------
# DOWNLOAD RESULTADOS
# ----------------------------------------------------
if menu == "📥 Download Resultados":
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📥 Download de Resultados")
        st.info("Clique no botão abaixo para baixar TODOS os resultados da Mega-Sena direto da API oficial da Caixa")
        
        if st.button("🚀 Baixar TODOS os Resultados", use_container_width=True, key="btn_download"):
            with st.spinner("📥 Baixando dados históricos (isso pode levar alguns minutos)..."):
                ok = analyzer.fetch_all_results(force_download=True)
                
                if ok:
                    st.session_state.stats = analyzer.comprehensive_analysis()
                    st.session_state.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")
                    
                    # Buscar último resultado formatado
                    latest = analyzer.get_latest_result()
                    if latest:
                        st.session_state.last_result = latest
                    
                    st.success(f"""
                    ✅ Download concluído!
                    - 📊 {analyzer.stats['total_games']} concursos analisados
                    - 📅 Atualizado em: {st.session_state.last_update}
                    """)
                else:
                    st.error("❌ Erro ao baixar dados. Verifique sua conexão.")
    
    with col2:
        # Mostrar último resultado se disponível
        if st.session_state.last_result:
            st.markdown("### 🎯 Último Resultado")
            
            # Extrair dados
            concurso = st.session_state.last_result.get('concurso', '')
            data = st.session_state.last_result.get('data', '')
            numeros = st.session_state.last_result.get('numeros', [])
            acumulado = st.session_state.last_result.get('acumulado', False)
            premio = st.session_state.last_result.get('estimativa', 0)
            
            # Card do resultado
            st.markdown(f"""
            <div class="result-card">
                <h3>Concurso {concurso}</h3>
                <p>{data}</p>
                <div class="numbers-container">
            """, unsafe_allow_html=True)
            
            # Mostrar números
            cols = st.columns(6)
            for i, num in enumerate(numeros):
                with cols[i]:
                    st.markdown(f"<div class='number-square'>{num:02d}</div>", unsafe_allow_html=True)
            
            # Informações adicionais
            st.markdown("</div>", unsafe_allow_html=True)
            
            if acumulado:
                st.markdown("""
                <p style='color: #ff6b6b; font-weight: bold; margin-top: 10px;'>
                    ⚠️ ACUMULOU!
                </p>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <p style='margin-top: 10px;'>
                    <span class='info-tag'>💰 Prêmio: R$ {premio:,.2f}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Detalhes dos ganhadores
            with st.expander("📊 Detalhes do concurso"):
                st.markdown(f"""
                - **Ganhadores (6 acertos):** {st.session_state.last_result.get('ganhadores_6', 0)}
                - **Ganhadores (5 acertos):** {st.session_state.last_result.get('ganhadores_5', 0)}
                - **Ganhadores (4 acertos):** {st.session_state.last_result.get('ganhadores_4', 0)}
                - **Local:** {st.session_state.last_result.get('local', '')}
                - **Próximo concurso:** {st.session_state.last_result.get('data_proximo', '')}
                """)
        else:
            st.info("📅 Faça o download para ver o último resultado")

# ----------------------------------------------------
# ANÁLISE ESTATÍSTICA
# ----------------------------------------------------
elif menu == "📊 Análise Estatística":
    
    if not st.session_state.stats:
        st.warning("⚠️ Faça o download dos resultados primeiro no menu 'Download Resultados'")
    else:
        stats = st.session_state.stats
        freq = stats["frequencies"]
        
        df_freq = pd.DataFrame(
            [(n, freq[n]) for n in range(1, 61)],
            columns=["Número", "Frequência"]
        )
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total de Concursos</h3>
                <div class="value">{stats['total_games']}</div>
                <div>histórico completo</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            most_common = freq.most_common(1)[0]
            st.markdown(f"""
            <div class="metric-card">
                <h3>Nº Mais Sorteado</h3>
                <div class="value">{most_common[0]:02d}</div>
                <div>{most_common[1]} vezes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            least_common = freq.most_common()[-1]
            st.markdown(f"""
            <div class="metric-card">
                <h3>Nº Menos Sorteado</h3>
                <div class="value">{least_common[0]:02d}</div>
                <div>{least_common[1]} vezes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            media = sum(freq.values()) / 60
            st.markdown(f"""
            <div class="metric-card">
                <h3>Média por Nº</h3>
                <div class="value">{media:.1f}</div>
                <div>aparições</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráfico de frequência
        st.markdown("### 📈 Distribuição de Frequência")
        
        fig = px.bar(
            df_freq,
            x="Número",
            y="Frequência",
            color="Frequência",
            color_continuous_scale=['#667eea', '#764ba2'],
            text="Frequência"
        )
        
        fig.add_hline(
            y=media,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Média: {media:.1f}"
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top e Flop
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔥 Top 15 Números Mais Sorteados")
            top15 = df_freq.nlargest(15, 'Frequência').reset_index(drop=True)
            top15.index = range(1, 16)
            st.dataframe(
                top15,
                use_container_width=True,
                hide_index=False,
                column_config={
                    "Número": "Nº",
                    "Frequência": "Vezes"
                }
            )
        
        with col2:
            st.markdown("### ❄️ Top 15 Números Menos Sorteados")
            bottom15 = df_freq.nsmallest(15, 'Frequência').reset_index(drop=True)
            bottom15.index = range(1, 16)
            st.dataframe(
                bottom15,
                use_container_width=True,
                hide_index=False,
                column_config={
                    "Número": "Nº",
                    "Frequência": "Vezes"
                }
            )
        
        st.markdown("---")
        
        # Pares mais frequentes
        st.markdown("### 🤝 Top 20 Pares Mais Frequentes")
        
        pairs = stats["pairs"].most_common(20)
        df_pairs = pd.DataFrame(
            [(f"{p[0]:02d} - {p[1]:02d}", c) for p, c in pairs],
            columns=["Par", "Frequência"]
        )
        df_pairs.index = range(1, 21)
        
        st.dataframe(
            df_pairs,
            use_container_width=True,
            hide_index=False,
            column_config={
                "Par": "Combinação",
                "Frequência": "Ocorrências"
            }
        )

# ----------------------------------------------------
# GERADOR DE JOGOS
# ----------------------------------------------------
elif menu == "🎰 Gerador de Jogos":
    
    if not st.session_state.stats:
        st.warning("⚠️ Faça o download dos resultados primeiro no menu 'Download Resultados'")
    else:
        stats = st.session_state.stats
        freq = stats["frequencies"]
        
        all_freq = freq.most_common()
        hot = [n for n, _ in all_freq[:20]]
        cold = [n for n, _ in all_freq[-20:]]
        
        st.markdown("### ⚙️ Configuração do Gerador")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            estrategia = st.selectbox(
                "🎯 Estratégia",
                [
                    "Aleatório",
                    "Números Quentes",
                    "Números Frios",
                    "Mistura Quente/Frio (3/3)",
                    "Par/Ímpar Balanceado"
                ],
                key="select_estrategia"
            )
        
        with col2:
            conjuntos = st.number_input(
                "📦 Conjuntos", 
                1, 10, 2,
                key="num_conjuntos"
            )
        
        with col3:
            jogos = st.number_input(
                "🎲 Jogos por conjunto", 
                1, 20, 6,
                key="num_jogos"
            )
        
        # Mostrar números em destaque
        st.markdown("### 🔥 Números em Destaque")
        
        col_hot, col_cold = st.columns(2)
        
        with col_hot:
            st.markdown("**Números Quentes (mais frequentes):**")
            hot_html = ""
            for n in sorted(hot[:15]):
                hot_html += f"<span class='number-square number-hot'>{n:02d}</span>"
            st.markdown(f"<div class='numbers-container'>{hot_html}</div>", unsafe_allow_html=True)
        
        with col_cold:
            st.markdown("**Números Frios (menos frequentes):**")
            cold_html = ""
            for n in sorted(cold[:15]):
                cold_html += f"<span class='number-square number-cold'>{n:02d}</span>"
            st.markdown(f"<div class='numbers-container'>{cold_html}</div>", unsafe_allow_html=True)
        
        if st.button("🎰 Gerar Jogos", use_container_width=True, key="btn_gerar"):
            
            resultados = []
            
            for c in range(conjuntos):
                grupo = []
                
                for _ in range(jogos):
                    if estrategia == "Aleatório":
                        game = sorted(random.sample(range(1,61), 6))
                    
                    elif estrategia == "Números Quentes":
                        game = sorted(random.sample(hot, 6))
                    
                    elif estrategia == "Números Frios":
                        game = sorted(random.sample(cold, 6))
                    
                    elif estrategia == "Mistura Quente/Frio (3/3)":
                        game = sorted(random.sample(hot, 3) + random.sample(cold, 3))
                    
                    elif estrategia == "Par/Ímpar Balanceado":
                        pares = [n for n in range(1,61) if n%2==0]
                        impares = [n for n in range(1,61) if n%2==1]
                        game = sorted(random.sample(pares, 3) + random.sample(impares, 3))
                    
                    grupo.append(game)
                
                resultados.append(grupo)
            
            st.markdown("---")
            
            for i, grupo in enumerate(resultados):
                st.markdown(f"### 📦 Conjunto {i+1}")
                
                cols = st.columns(3)
                
                for idx, jogo in enumerate(grupo):
                    with cols[idx % 3]:
                        st.markdown(f"**Jogo {idx+1}**")
                        
                        num_html = ""
                        for num in jogo:
                            if num in hot:
                                num_html += f"<span class='number-square number-hot'>{num:02d}</span>"
                            elif num in cold:
                                num_html += f"<span class='number-square number-cold'>{num:02d}</span>"
                            else:
                                num_html += f"<span class='number-square'>{num:02d}</span>"
                        
                        st.markdown(f"<div class='numbers-container'>{num_html}</div>", unsafe_allow_html=True)
                
                st.markdown("---")
                
                df = pd.DataFrame(grupo, columns=[f"N{i+1}" for i in range(6)])
                csv = df.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download Conjunto {i+1} (CSV)",
                    data=csv,
                    file_name=f"megasena_conjunto_{i+1}.csv",
                    mime="text/csv",
                    key=f"download_conjunto_{i}"
                )

# ----------------------------------------------------
# BANNER DE DOAÇÃO
# ----------------------------------------------------
st.markdown("""
<style>
    .donation-banner {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        text-align: center;
        color: white;
        box-shadow: 0 -10px 30px rgba(102, 126, 234, 0.5);
        z-index: 999;
        border-top: 3px solid rgba(255, 255, 255, 0.3);
        animation: slideUp 0.5s ease;
        font-family: 'Arial', sans-serif;
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .banner-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .pix-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 50px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        display: flex;
        align-items: center;
        gap: 15px;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .pix-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.3);
    }
    
    .copy-button {
        background: white;
        color: #667eea;
        border: none;
        padding: 5px 15px;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .copy-button:hover {
        transform: scale(1.1);
        background: #f0f0f0;
    }
    
    .main {
        padding-bottom: 80px !important;
    }
</style>

<div class="donation-banner">
    <div class="banner-content">
        <span style="font-size: 1.5rem;">💚</span>
        <span style="font-weight: bold;">APOIE O PROJETO</span>
        <div class="pix-card">
            <span>💚 PIX:</span>
            <span style="font-family: monospace;">wellingtongusmao34@gmail.com</span>
            <button class="copy-button" onclick="copyPIX()">
                📋 Copiar
            </button>
        </div>
        <span style="font-size: 0.9rem;">🙏 Dados oficiais da CAIXA</span>
    </div>
</div>

<script>
function copyPIX() {
    const pixKey = 'wellingtongusmao34@gmail.com';
    navigator.clipboard.writeText(pixKey).then(function() {
        alert('✅ PIX copiado! Obrigado por apoiar o projeto!');
    });
}
</script>
""", unsafe_allow_html=True)

# RODAPÉ
st.markdown("""
<div style='text-align: center; color: #666; padding: 10px; margin-bottom: 60px;'>
    <p style='font-size: 0.8rem;'>© 2024 Mega-Sena Analyst PRO - v2.0 | Dados oficiais da Caixa Econômica Federal</p>
</div>
""", unsafe_allow_html=True)