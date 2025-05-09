import streamlit as st
from backend import criar_tabelas

# Criação das tabelas do banco
criar_tabelas()

# Configuração da página principal
st.set_page_config(page_title="Espaço Pet System", layout="centered")

# Logo e título
with st.container():
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.image("logopet.png", width=200)
    st.markdown('<h2 style="color: #a48563;">🐾 Espaço Pet System Guajiru</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Layout com 3 colunas para os botões
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📦 Estoque"):
        st.switch_page("pages/estoque.py")

    if st.button("📝 Prontuário"):
        st.switch_page("pages/prontuario.py")

with col2:
    if st.button("👤 Cliente e Pet"):
        st.switch_page("pages/clientes_pet.py")

    if st.button("📚 Histórico Prontuário"):
        st.switch_page("pages/historico_prontuario.py")

with col3:
    if st.button("💰 Vendas"):
        st.switch_page("pages/vendas.py")
