import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import base64

st.set_page_config(
    page_title="Livraria Solidária Real Park",
    page_icon="🌿",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.header-box {
    background: #4AB095;
    border-radius: 16px;
    padding: 1.4rem 1.5rem 1.2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.header-titulo {
    font-size: 1.45rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0.6rem 0 0.15rem;
    letter-spacing: 0.01em;
}
.header-subtitulo {
    font-size: 0.88rem;
    color: #d4f0e8;
    font-weight: 400;
    margin: 0;
}
.header-slogan {
    display: inline-block;
    background: #E8608A;
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    border-radius: 20px;
    padding: 0.25rem 1rem;
    margin-top: 0.75rem;
}
.card-livro {
    background: #ffffff;
    border: 1.5px solid #b2e0d2;
    border-left: 6px solid #4DB99A;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 0.8rem 0;
}
.titulo-livro {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0F6E56;
    margin-bottom: 0.4rem;
}
.disponivel {
    color: #0F6E56;
    font-weight: 700;
    font-size: 0.95rem;
    background: #e1f5ee;
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    margin-top: 0.4rem;
}
.emprestado {
    color: #993556;
    font-weight: 700;
    font-size: 0.95rem;
    background: #fce8f0;
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    margin-top: 0.4rem;
}
.info-label {
    color: #4DB99A;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.5rem;
}
.info-valor { color: #1a3d30; font-size: 0.96rem; margin-bottom: 0.15rem; }
div[data-testid="stButton"] > button {
    background-color: #4DB99A; color: white; border: none;
    border-radius: 8px; font-family: Nunito, sans-serif; font-weight: 700;
    letter-spacing: 0.04em; padding: 0.5rem 1.5rem; width: 100%;
}
div[data-testid="stButton"] > button:hover { background-color: #3aa085; color: white; }
.aviso-sucesso {
    background: #e1f5ee; border-left: 5px solid #4DB99A;
    padding: 1rem 1.2rem; border-radius: 8px; color: #0F6E56;
    margin: 1rem 0; font-weight: 600;
}
.aviso-erro {
    background: #fce8f0; border-left: 5px solid #E8608A;
    padding: 1rem 1.2rem; border-radius: 8px; color: #993556;
    margin: 1rem 0; font-weight: 600;
}
div[data-testid="stMetric"] {
    background: #f0faf6; border: 1.5px solid #b2e0d2;
    border-radius: 10px; padding: 0.7rem 1rem;
}
</style>
""", unsafe_allow_html=True)

LOGO_B64 = "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"

logo_html = (
    '<div class="header-box">'
    '<img src="data:image/png;base64,' + LOGO_B64 + '" style="height:90px; width:auto; border-radius:8px;" />'
    '<div class="header-titulo">Livraria Solid&#225;ria Real Park</div>'
    '<div class="header-subtitulo">Condom&#237;nio Real Park Sumar&#233;</div>'
    '<div class="header-slogan">Traga &middot; Pegue &middot; Leia &middot; Devolva</div>'
    '</div>'
)
st.markdown(logo_html, unsafe_allow_html=True)

aba = st.radio(
    "Navegacao",
    ["🔍 Buscar livro", "📋 Ver todos os livros", "↩️ Devolver livro", "🛠️ Área do administrador"],
    horizontal=True,
    label_visibility="collapsed",
)

ARQUIVO_LIVROS = "livros.xlsx"
PRAZO_DIAS = 30

def carregar_dados():
    if not os.path.exists(ARQUIVO_LIVROS):
        df = pd.DataFrame({
            "id":              [1, 2, 3],
            "titulo":          ["O Pequeno Príncipe", "Dom Casmurro", "A Moreninha"],
            "autor":           ["Antoine de Saint-Exupéry", "Machado de Assis", "Joaquim Manuel de Macedo"],
            "genero":          ["Ficção", "Romance", "Romance"],
            "disponivel":      [True, True, True],
            "nome_usuario":    ["", "", ""],
            "data_emprestimo": ["", "", ""],
            "data_devolucao":  ["", "", ""],
        })
        df.to_excel(ARQUIVO_LIVROS, index=False)
    df = pd.read_excel(ARQUIVO_LIVROS)
    for col in ["nome_usuario", "data_emprestimo", "data_devolucao", "titulo", "autor", "genero"]:
        df[col] = df[col].fillna("").astype(str)
    return df

def salvar_dados(df):
    df.to_excel(ARQUIVO_LIVROS, index=False)

def buscar_livro(df, termo):
    termo = termo.strip().lower()
    mask = (
        df["titulo"].str.lower().str.contains(termo, na=False) |
        df["autor"].str.lower().str.contains(termo, na=False)
    )
    return df[mask]

def registrar_emprestimo(df, livro_id, nome):
    hoje = datetime.today()
    devolucao = hoje + timedelta(days=PRAZO_DIAS)
    idx = df.index[df["id"] == livro_id][0]
    df.at[idx, "disponivel"] = False
    df.at[idx, "nome_usuario"] = nome
    df.at[idx, "data_emprestimo"] = hoje.strftime("%d/%m/%Y")
    df.at[idx, "data_devolucao"] = devolucao.strftime("%d/%m/%Y")
    salvar_dados(df)
    return devolucao.strftime("%d/%m/%Y")

def registrar_devolucao(df, livro_id):
    idx = df.index[df["id"] == livro_id][0]
    df.at[idx, "disponivel"] = True
    df.at[idx, "nome_usuario"] = ""
    df.at[idx, "data_emprestimo"] = ""
    df.at[idx, "data_devolucao"] = ""
    salvar_dados(df)

df = carregar_dados()

if aba == "🔍 Buscar livro":
    st.subheader("Buscar livro")
    params = st.query_params
    termo_url = params.get("busca", "")
    termo = st.text_input("Digite o título ou o nome do autor:", value=termo_url)
    if termo:
        resultados = buscar_livro(df, termo)
        if resultados.empty:
            st.markdown('<div class="aviso-erro">❌ Nenhum livro encontrado. Tente outro termo.</div>', unsafe_allow_html=True)
        else:
            for _, livro in resultados.iterrows():
                badge = '<span class="disponivel">✅ Disponível</span>' if livro["disponivel"] else '<span class="emprestado">📕 Emprestado</span>'
                card = (
                    '<div class="card-livro">' +
                    '<div class="titulo-livro">' + str(livro["titulo"]) + '</div>' +
                    '<div class="info-label">Autor</div>' +
                    '<div class="info-valor">' + str(livro["autor"]) + '</div>' +
                    '<div class="info-label">Gênero</div>' +
                    '<div class="info-valor">' + str(livro["genero"]) + '</div>' +
                    badge + '</div>'
                )
                st.markdown(card, unsafe_allow_html=True)
                if not livro["disponivel"]:
                    st.markdown(
                        '<div class="info-label" style="margin-top:.6rem">Devolução prevista</div>' +
                        '<div class="info-valor">' + str(livro["data_devolucao"]) + '</div>',
                        unsafe_allow_html=True
                    )
                if livro["disponivel"]:
                    with st.expander("📖 Pegar este livro emprestado"):
                        nome = st.text_input("Seu nome completo:", key=f"nome_{livro['id']}")
                        if st.button("Confirmar empréstimo", key=f"btn_{livro['id']}"):
                            if nome.strip() == "":
                                st.warning("Por favor, preencha seu nome.")
                            else:
                                data_dev = registrar_emprestimo(df, livro["id"], nome.strip())
                                st.markdown(
                                    '<div class="aviso-sucesso">🌿 Empréstimo registrado!<br>Devolva até <strong>' + data_dev + '</strong>. Boa leitura! 📚</div>',
                                    unsafe_allow_html=True
                                )
                                st.balloons()
                st.write("")

elif aba == "📋 Ver todos os livros":
    st.subheader("Acervo completo")
    col1, col2 = st.columns(2)
    col1.metric("Total de livros", len(df))
    col2.metric("Disponíveis agora", int(df["disponivel"].sum()))
    st.write("")
    filtro = st.selectbox("Filtrar por:", ["Todos", "Disponíveis", "Emprestados"])
    if filtro == "Disponíveis":
        exibir = df[df["disponivel"] == True]
    elif filtro == "Emprestados":
        exibir = df[df["disponivel"] == False]
    else:
        exibir = df
    for _, livro in exibir.iterrows():
        if livro["disponivel"]:
            status_html = '<span class="disponivel">✅ Disponível</span>'
        else:
            status_html = '<span class="emprestado">📕 Emprestado até ' + str(livro["data_devolucao"]) + '</span>'
        card = (
            '<div class="card-livro">' +
            '<div class="titulo-livro">' + str(livro["titulo"]) + '</div>' +
            '<div class="info-label">Autor</div>' +
            '<div class="info-valor">' + str(livro["autor"]) + '</div>' +
            status_html + '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)

elif aba == "↩️ Devolver livro":
    st.subheader("Registrar devolução")
    emprestados = df[df["disponivel"] == False]
    if emprestados.empty:
        st.info("Nenhum livro emprestado no momento.")
    else:
        opcoes = {f"{row['titulo']} — {row['nome_usuario']}": row["id"] for _, row in emprestados.iterrows()}
        escolha = st.selectbox("Qual livro está sendo devolvido?", list(opcoes.keys()))
        livro_id = opcoes[escolha]
        livro_info = df[df["id"] == livro_id].iloc[0]
        card = (
            '<div class="card-livro">' +
            '<div class="titulo-livro">' + str(livro_info["titulo"]) + '</div>' +
            '<div class="info-label">Emprestado para</div>' +
            '<div class="info-valor">' + str(livro_info["nome_usuario"]) + '</div>' +
            '<div class="info-label">Data do empréstimo</div>' +
            '<div class="info-valor">' + str(livro_info["data_emprestimo"]) + '</div>' +
            '<div class="info-label">Devolução prevista</div>' +
            '<div class="info-valor">' + str(livro_info["data_devolucao"]) + '</div>' +
            '</div>'
        )
        st.markdown(card, unsafe_allow_html=True)
        if st.button("✅ Confirmar devolução"):
            registrar_devolucao(df, livro_id)
            st.markdown('<div class="aviso-sucesso">🌿 Livro devolvido com sucesso! Obrigado por participar!</div>', unsafe_allow_html=True)
            st.rerun()

elif aba == "🛠️ Área do administrador":
    st.subheader("Administrar acervo")
    senha = st.text_input("Senha do administrador:", type="password")
    if senha == "livraria123":
        st.success("Acesso liberado! 🌿")
        st.write("### ➕ Adicionar novo livro")
        with st.form("form_novo_livro"):
            novo_titulo = st.text_input("Título")
            novo_autor  = st.text_input("Autor")
            novo_genero = st.text_input("Gênero (ex: Romance, Ficção, Autoajuda…)")
            salvar = st.form_submit_button("Salvar livro")
        if salvar:
            if novo_titulo.strip() and novo_autor.strip():
                novo_id = int(df["id"].max()) + 1 if not df.empty else 1
                nova_linha = pd.DataFrame([{
                    "id": novo_id, "titulo": novo_titulo.strip(), "autor": novo_autor.strip(),
                    "genero": novo_genero.strip(), "disponivel": True,
                    "nome_usuario": "", "data_emprestimo": "", "data_devolucao": "",
                }])
                df = pd.concat([df, nova_linha], ignore_index=True)
                salvar_dados(df)
                st.success(f"✅ '{novo_titulo}' adicionado com sucesso!")
            else:
                st.warning("Preencha pelo menos o título e o autor.")
        st.write("### 📊 Tabela completa do acervo")
        st.dataframe(df, use_container_width=True)
        st.write("### 📥 Baixar planilha atualizada")
        with open(ARQUIVO_LIVROS, "rb") as f:
            st.download_button("Baixar livros.xlsx", data=f, file_name="livros.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif senha != "":
        st.markdown('<div class="aviso-erro">❌ Senha incorreta.</div>', unsafe_allow_html=True)

st.divider()
st.markdown(
    '<div style="text-align:center;color:#4DB99A;font-size:.8rem;font-weight:700;letter-spacing:.05em;padding-bottom:.5rem;">' +
    '🌿 REAL PARK SUMARÉ · Todo bom livro deve ser compartilhado</div>',
    unsafe_allow_html=True
)
