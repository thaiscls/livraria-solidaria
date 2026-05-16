import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Livraria Solidária",
    page_icon="📚",
    layout="centered",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
}

.titulo-app {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: #3b2a1a;
    text-align: center;
    margin-bottom: 0.2rem;
}

.subtitulo-app {
    text-align: center;
    color: #7a5c3e;
    font-size: 1rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

.card-livro {
    background: #fdf6ee;
    border-left: 5px solid #c9863a;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
}

.disponivel {
    color: #2e7d32;
    font-weight: 700;
    font-size: 1.1rem;
}

.emprestado {
    color: #c62828;
    font-weight: 700;
    font-size: 1.1rem;
}

.info-label {
    color: #7a5c3e;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.info-valor {
    color: #3b2a1a;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

div[data-testid="stButton"] > button {
    background-color: #c9863a;
    color: white;
    border: none;
    border-radius: 6px;
    font-family: 'Lato', sans-serif;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.5rem 1.5rem;
    width: 100%;
}

div[data-testid="stButton"] > button:hover {
    background-color: #a86c25;
    color: white;
}

.aviso-sucesso {
    background: #e8f5e9;
    border-left: 4px solid #2e7d32;
    padding: 1rem;
    border-radius: 6px;
    color: #1b5e20;
    margin: 1rem 0;
}

.aviso-erro {
    background: #ffebee;
    border-left: 4px solid #c62828;
    padding: 1rem;
    border-radius: 6px;
    color: #b71c1c;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Constantes ──────────────────────────────────────────────────────────────
ARQUIVO_LIVROS = "livros.xlsx"
PRAZO_DIAS = 30  # 1 mês de prazo

# ── Funções utilitárias ─────────────────────────────────────────────────────
def carregar_dados():
    """Lê o arquivo Excel e retorna um DataFrame."""
    if not os.path.exists(ARQUIVO_LIVROS):
        df = pd.DataFrame({
            "id":           [1, 2, 3],
            "titulo":       ["O Pequeno Príncipe", "Dom Casmurro", "A Moreninha"],
            "autor":        ["Antoine de Saint-Exupéry", "Machado de Assis", "Joaquim Manuel de Macedo"],
            "genero":       ["Ficção", "Romance", "Romance"],
            "disponivel":   [True, True, True],
            "nome_usuario": ["", "", ""],
            "data_emprestimo": ["", "", ""],
            "data_devolucao":  ["", "", ""],
        })
        df.to_excel(ARQUIVO_LIVROS, index=False)
    df = pd.read_excel(ARQUIVO_LIVROS)
    # Garante que colunas de texto nunca virem numéricas
    for col in ["nome_usuario", "data_emprestimo", "data_devolucao", "titulo", "autor", "genero"]:
        df[col] = df[col].fillna("").astype(str)
    return df


def salvar_dados(df: pd.DataFrame):
    """Salva o DataFrame de volta no Excel."""
    df.to_excel(ARQUIVO_LIVROS, index=False)


def buscar_livro(df: pd.DataFrame, termo: str):
    """Busca livros por título ou autor (case-insensitive)."""
    termo = termo.strip().lower()
    mask = (
        df["titulo"].str.lower().str.contains(termo, na=False) |
        df["autor"].str.lower().str.contains(termo, na=False)
    )
    return df[mask]


def registrar_emprestimo(df: pd.DataFrame, livro_id: int, nome: str):
    """Marca o livro como emprestado e registra dados."""
    hoje = datetime.today()
    devolucao = hoje + timedelta(days=PRAZO_DIAS)
    idx = df.index[df["id"] == livro_id][0]
    df.at[idx, "disponivel"] = False
    df.at[idx, "nome_usuario"] = nome
    df.at[idx, "data_emprestimo"] = hoje.strftime("%d/%m/%Y")
    df.at[idx, "data_devolucao"] = devolucao.strftime("%d/%m/%Y")
    salvar_dados(df)
    return devolucao.strftime("%d/%m/%Y")


def registrar_devolucao(df: pd.DataFrame, livro_id: int):
    """Marca o livro como disponível e limpa os dados de empréstimo."""
    idx = df.index[df["id"] == livro_id][0]
    df.at[idx, "disponivel"] = True
    df.at[idx, "nome_usuario"] = ""
    df.at[idx, "data_emprestimo"] = ""
    df.at[idx, "data_devolucao"] = ""
    salvar_dados(df)


# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-app">📚 Livraria Solidária</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo-app">Condomínio · Leia, compartilhe, inspire.</div>', unsafe_allow_html=True)
st.divider()

# ── Menu de navegação ───────────────────────────────────────────────────────
aba = st.radio(
    "O que você quer fazer?",
    ["🔍 Buscar livro", "📋 Ver todos os livros", "↩️ Devolver livro", "🛠️ Área do administrador"],
    horizontal=True,
    label_visibility="collapsed",
)

df = carregar_dados()

# ════════════════════════════════════════════════════════════════════════════
# ABA 1 – BUSCAR LIVRO
# ════════════════════════════════════════════════════════════════════════════
if aba == "🔍 Buscar livro":
    st.subheader("Buscar livro")

    # Verifica se veio um parâmetro ?busca=... na URL (vindo do QR code)
    params = st.query_params
    termo_url = params.get("busca", "")

    termo = st.text_input("Digite o título ou o nome do autor:", value=termo_url)

    if termo:
        resultados = buscar_livro(df, termo)

        if resultados.empty:
            st.markdown('<div class="aviso-erro">❌ Nenhum livro encontrado. Tente outro termo.</div>', unsafe_allow_html=True)
        else:
            for _, livro in resultados.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="card-livro">
                        <div style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#3b2a1a;">
                            {livro['titulo']}
                        </div>
                        <div class="info-label">Autor</div>
                        <div class="info-valor">{livro['autor']}</div>
                        <div class="info-label">Gênero</div>
                        <div class="info-valor">{livro['genero']}</div>
                    """, unsafe_allow_html=True)

                    if livro["disponivel"]:
                        st.markdown('<div class="disponivel">✅ Disponível para empréstimo</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="emprestado">📕 Emprestado</div>
                        <div class="info-label">Emprestado para</div>
                        <div class="info-valor">{livro['nome_usuario']}</div>
                        <div class="info-label">Devolução prevista</div>
                        <div class="info-valor">{livro['data_devolucao']}</div>
                        """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

                    # Formulário de empréstimo
                    if livro["disponivel"]:
                        with st.expander("📖 Pegar este livro emprestado"):
                            nome = st.text_input("Seu nome completo:", key=f"nome_{livro['id']}")
                            if st.button("Confirmar empréstimo", key=f"btn_{livro['id']}"):
                                if nome.strip() == "":
                                    st.warning("Por favor, preencha seu nome.")
                                else:
                                    data_dev = registrar_emprestimo(df, livro["id"], nome.strip())
                                    st.markdown(f"""
                                    <div class="aviso-sucesso">
                                        ✅ <strong>Empréstimo registrado!</strong><br>
                                        Devolva até <strong>{data_dev}</strong>. Boa leitura! 📖
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.balloons()
                    st.write("")

# ════════════════════════════════════════════════════════════════════════════
# ABA 2 – TODOS OS LIVROS
# ════════════════════════════════════════════════════════════════════════════
elif aba == "📋 Ver todos os livros":
    st.subheader("Acervo completo")

    col1, col2 = st.columns(2)
    total = len(df)
    disponiveis = df["disponivel"].sum()
    col1.metric("Total de livros", total)
    col2.metric("Disponíveis agora", int(disponiveis))

    st.write("")
    filtro = st.selectbox("Filtrar por:", ["Todos", "Disponíveis", "Emprestados"])

    if filtro == "Disponíveis":
        exibir = df[df["disponivel"] == True]
    elif filtro == "Emprestados":
        exibir = df[df["disponivel"] == False]
    else:
        exibir = df

    for _, livro in exibir.iterrows():
        status = "✅ Disponível" if livro["disponivel"] else f"📕 Emprestado até {livro['data_devolucao']}"
        cor_status = "disponivel" if livro["disponivel"] else "emprestado"
        st.markdown(f"""
        <div class="card-livro">
            <div style="font-family:'Playfair Display',serif; font-size:1.2rem; color:#3b2a1a;">{livro['titulo']}</div>
            <div class="info-label">Autor</div>
            <div class="info-valor">{livro['autor']}</div>
            <div class="{cor_status}">{status}</div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# ABA 3 – DEVOLVER LIVRO
# ════════════════════════════════════════════════════════════════════════════
elif aba == "↩️ Devolver livro":
    st.subheader("Registrar devolução")

    emprestados = df[df["disponivel"] == False]

    if emprestados.empty:
        st.info("Nenhum livro emprestado no momento.")
    else:
        opcoes = {
            f"{row['titulo']} — {row['nome_usuario']}": row["id"]
            for _, row in emprestados.iterrows()
        }
        escolha = st.selectbox("Qual livro está sendo devolvido?", list(opcoes.keys()))

        livro_id = opcoes[escolha]
        livro_info = df[df["id"] == livro_id].iloc[0]

        st.markdown(f"""
        <div class="card-livro">
            <div class="info-label">Livro</div>
            <div class="info-valor">{livro_info['titulo']}</div>
            <div class="info-label">Emprestado para</div>
            <div class="info-valor">{livro_info['nome_usuario']}</div>
            <div class="info-label">Data de empréstimo</div>
            <div class="info-valor">{livro_info['data_emprestimo']}</div>
            <div class="info-label">Devolução prevista</div>
            <div class="info-valor">{livro_info['data_devolucao']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✅ Confirmar devolução"):
            registrar_devolucao(df, livro_id)
            st.markdown('<div class="aviso-sucesso">📚 Livro devolvido com sucesso! Obrigado!</div>', unsafe_allow_html=True)
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# ABA 4 – ADMINISTRADOR
# ════════════════════════════════════════════════════════════════════════════
elif aba == "🛠️ Área do administrador":
    st.subheader("Administrar acervo")

    senha = st.text_input("Senha do administrador:", type="password")

    # Troque 'livraria123' pela senha que você quiser
    if senha == "livraria123":
        st.success("Acesso liberado! 🔓")

        st.write("### ➕ Adicionar novo livro")
        with st.form("form_novo_livro"):
            novo_titulo  = st.text_input("Título")
            novo_autor   = st.text_input("Autor")
            novo_genero  = st.text_input("Gênero (ex: Romance, Ficção, Autoajuda…)")
            salvar = st.form_submit_button("Salvar livro")

        if salvar:
            if novo_titulo.strip() and novo_autor.strip():
                novo_id = int(df["id"].max()) + 1 if not df.empty else 1
                nova_linha = pd.DataFrame([{
                    "id": novo_id,
                    "titulo": novo_titulo.strip(),
                    "autor": novo_autor.strip(),
                    "genero": novo_genero.strip(),
                    "disponivel": True,
                    "nome_usuario": "",
                    "data_emprestimo": "",
                    "data_devolucao": "",
                }])
                df = pd.concat([df, nova_linha], ignore_index=True)
                salvar_dados(df)
                st.success(f"✅ Livro '{novo_titulo}' adicionado! ID: {novo_id}")
            else:
                st.warning("Preencha pelo menos o título e o autor.")

        st.write("### 📊 Tabela completa do acervo")
        st.dataframe(df, use_container_width=True)

        st.write("### 📥 Baixar planilha atualizada")
        with open(ARQUIVO_LIVROS, "rb") as f:
            st.download_button(
                "Baixar livros.xlsx",
                data=f,
                file_name="livros.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    elif senha != "":
        st.markdown('<div class="aviso-erro">❌ Senha incorreta.</div>', unsafe_allow_html=True)
