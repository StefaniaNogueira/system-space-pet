import streamlit as st
import backend as db
from datetime import datetime

st.set_page_config(page_title="Estoque - Espaço Pet", layout="wide")

st.markdown("## 🧾 Controle de Estoque")
st.markdown("Gerencie os produtos disponíveis no sistema.")

# --- Adicionar Produto ---
with st.expander("➕ Adicionar Produto ao Estoque"):
    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Nome do Produto")
        categoria = st.text_input("Categoria")
    with col2:
        validade = st.date_input("Validade")
        data_entrada = st.date_input("Data de Entrada", value=datetime.today())
    with col3:
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        preco = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.01)

    if st.button("Salvar Produto"):
        if nome and quantidade > 0:
            if validade < data_entrada:
                st.warning("A data de validade não pode ser anterior à data de entrada.")
            else:
                db.adicionar_produto(nome, categoria, validade.strftime("%Y-%m-%d"), quantidade, preco, data_entrada.strftime("%Y-%m-%d"))
                st.success("Produto adicionado com sucesso!")
                st.rerun()
        else:
            st.warning("Preencha todos os campos obrigatórios.")

st.markdown("---")

# --- Buscar Produto ---
busca_nome = st.text_input("🔍 Buscar Produto por Nome")
produtos = db.buscar_produtos_por_nome(busca_nome) if busca_nome else db.listar_produtos_estoque()

# --- Produtos em Baixo Estoque ---
st.markdown("#### 🚨 Produtos com Estoque Baixo")
produtos_baixo_estoque = [p for p in produtos if p[4] <= 2]

if produtos_baixo_estoque:
    for p in produtos_baixo_estoque:
        st.warning(f"⚠️ {p[1]} - Apenas {p[4]} unidades em estoque.")
else:
    st.success("Nenhum produto com estoque baixo.")

# --- Produtos Vencidos ou Próximos do Vencimento ---
st.markdown("#### 🧪 Produtos Vencidos ou Próximos do Vencimento")
hoje = datetime.today().date()
produtos_vencidos = []
produtos_proximos_vencimento = []

for p in produtos:
    validade = p[3]
    if isinstance(validade, str):
        try:
            validade = datetime.strptime(validade, "%Y-%m-%d").date()
        except ValueError:
            validade = None
    elif isinstance(validade, datetime):
        validade = validade.date()

    if validade:
        dias_para_vencer = (validade - hoje).days
        if validade < hoje:
            produtos_vencidos.append(p)
        elif dias_para_vencer <= 7:
            produtos_proximos_vencimento.append((p, dias_para_vencer))

# Exibe produtos vencidos
if produtos_vencidos:
    for p in produtos_vencidos:
        st.error(f"❌ {p[1]} - Vencido em {p[3]}")
else:
    st.success("Nenhum produto vencido.")

# Exibe produtos próximos do vencimento
if produtos_proximos_vencimento:
    for p, dias in produtos_proximos_vencimento:
        st.warning(f"⏳ {p[1]} - Vence em {dias} dia(s) ({p[3]})")
else:
    st.success("Nenhum produto próximo do vencimento.")

# --- Listar Produtos ---
st.markdown("### 📦 Produtos no Estoque")

if produtos:
    for produto in produtos:
        id_, nome, categoria, validade, quantidade, preco, data_entrada = produto
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.markdown(f"**{nome}**  \nCategoria: {categoria}")
            col2.markdown(f"Validade: `{validade}`  \nEntrada: `{data_entrada}`")
            col3.markdown(f"Quantidade: **{quantidade}**  \nPreço: R$ {preco:.2f}")
            col4.markdown("")

            if f"editar_{id_}" not in st.session_state:
                st.session_state[f"editar_{id_}"] = False

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("✏️ Editar", key=f"edit_{id_}"):
                    st.session_state[f"editar_{id_}"] = not st.session_state[f"editar_{id_}"]

            with col_b2:
                if st.button("🗑️ Excluir", key=f"delete_{id_}"):
                    st.session_state["confirmar_exclusao"] = id_

            if st.session_state.get("confirmar_exclusao") == id_:
                st.error("⚠️ Confirmar exclusão?")
                if st.button("✅ Sim, excluir", key=f"confirm_{id_}"):
                    db.excluir_produto(id_)
                    st.success("Produto excluído com sucesso.")
                    st.session_state.pop("confirmar_exclusao")
                    st.rerun()
                if st.button("❌ Cancelar", key=f"cancel_{id_}"):
                    st.session_state.pop("confirmar_exclusao")

            if st.session_state[f"editar_{id_}"]:
                with st.form(f"form_editar_{id_}"):
                    novo_nome = st.text_input("Nome", value=nome, key=f"nome_{id_}")
                    nova_categoria = st.text_input("Categoria", value=categoria, key=f"categoria_{id_}")
                    nova_validade = st.date_input("Validade", value=datetime.strptime(str(validade), "%Y-%m-%d"), key=f"validade_{id_}")
                    nova_data_entrada = st.date_input("Data Entrada", value=datetime.strptime(str(data_entrada), "%Y-%m-%d"), key=f"entrada_{id_}")
                    nova_quantidade = st.number_input("Quantidade", value=quantidade, step=1, key=f"quantidade_{id_}")
                    novo_preco = st.number_input("Preço", value=preco, step=0.01, key=f"preco_{id_}")
                    submitted = st.form_submit_button("Salvar Alterações")
                    if submitted:
                        db.editar_produto(id_, novo_nome, nova_categoria, nova_validade.strftime("%Y-%m-%d"),
                                          nova_quantidade, novo_preco, nova_data_entrada.strftime("%Y-%m-%d"))
                        st.success("Produto atualizado com sucesso!")
                        st.session_state[f"editar_{id_}"] = False
                        st.rerun()
else:
    st.info("Nenhum produto encontrado.")
