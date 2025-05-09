import streamlit as st
import backend as db

st.markdown("# 💰 Vendas", unsafe_allow_html=True)
st.markdown("### Registro de Venda", unsafe_allow_html=True)

# CARRINHO
if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

# --- SELEÇÃO DE CLIENTE E PET ---
with st.container():
    col1, col2 = st.columns(2)
    clientes = db.listar_clientes()
    cliente_opcoes = {cliente[1]: cliente[0] for cliente in clientes}
    with col1:
        cliente_nome = st.selectbox("👤 Cliente", list(cliente_opcoes.keys()))
    cliente_id = cliente_opcoes[cliente_nome]

    pets = db.listar_pets_por_cliente(cliente_id)
    if pets:
        pet_opcoes = {pet[1]: pet[0] for pet in pets}
        with col2:
            pet_nome = st.selectbox("🐾 Pet", list(pet_opcoes.keys()))
        pet_id = pet_opcoes[pet_nome]
    else:
        st.warning("Este cliente ainda não tem pets cadastrados.")
        st.stop()

# --- ADICIONAR PRODUTO AO CARRINHO ---
st.markdown("### 🛍️ Adicionar Produto")
col1, col2 = st.columns([3, 1])
produtos = db.listar_produtos()
produto_nomes = [f"{p[1]} - R${p[5]:.2f}" for p in produtos]

with col1:
    produto_selecionado = st.selectbox("Produto", produto_nomes)
with col2:
    quantidade = st.number_input("Qtd", min_value=1, value=1)

if st.button("➕ Adicionar ao Carrinho"):
    idx = produto_nomes.index(produto_selecionado)
    p = produtos[idx]
    st.session_state.carrinho.append({
        "id": p[0],
        "nome": p[1],
        "preco": p[5],
        "quantidade": quantidade
    })
    st.success(f"{p[1]} adicionado ao carrinho!")

# --- EXIBIR CARRINHO ---
if st.session_state.carrinho:
    st.markdown("### 🛒 Carrinho")
    total = 0.0
    for item in st.session_state.carrinho:
        st.markdown(f"- **{item['nome']}**: {item['quantidade']}x — R${item['preco']:.2f}")
        total += item['quantidade'] * item['preco']
    st.markdown(f"**💵 Total: R${total:.2f}**")

    col1, col2 = st.columns(2)
    with col1:
        forma_pagamento = st.selectbox("💳 Forma de Pagamento", ["Dinheiro", "PIX", "Cartão"])
    with col2:
        status_pagamento = st.selectbox("📌 Status do Pagamento", ["Pago", "Aguardando", "Não Pago"])

    if st.button("✅ Finalizar Venda"):
        venda_id = db.registrar_venda(pet_id, st.session_state.carrinho, forma_pagamento, status_pagamento)
        st.success(f"✅ Venda registrada com ID #{venda_id}")
        st.session_state.carrinho.clear()


# --- HISTÓRICO DE VENDAS ---
st.markdown("## 📜 Histórico de Vendas")

vendas = db.listar_vendas()
if vendas:
    for venda in vendas:
        venda_id, pet_nome, cliente_nome, data, forma_pagamento, status_pagamento, produtos_str, total = venda
        with st.expander(f"🧾 Venda #{venda_id} — R${float(total):.2f}"):
            st.markdown(f"**Pet:** {pet_nome}")
            st.markdown(f"**Cliente:** {cliente_nome}")
            st.markdown(f"**Data:** {data}")
            st.markdown(f"**Forma de Pagamento:** {forma_pagamento}")
            st.markdown(f"**Status do Pagamento:** {status_pagamento}")
            st.markdown("**Produtos Vendidos:**")

            # Produtos formatados: "Produto xQTD (R$ VALOR)", separados por vírgula
            produtos_list = produtos_str.split(", ")
            nomes, quantidades, valores = [], [], []

            for prod in produtos_list:
                try:
                    nome_qtd, preco = prod.split(" (R$ ")
                    nome, qtd = nome_qtd.rsplit(" x", 1)
                    preco = preco.replace(")", "")
                    nomes.append(nome)
                    quantidades.append(qtd)
                    valores.append(preco)
                except:
                    nomes.append(prod)
                    quantidades.append("-")
                    valores.append("-")

            col1, col2, col3 = st.columns([4, 1, 2])
            with col1:
                st.markdown("**Produto**")
                for nome in nomes:
                    st.markdown(f"- {nome}")
            with col2:
                st.markdown("**Qtd**")
                for qtd in quantidades:
                    st.markdown(f"- {qtd}")
            with col3:
                st.markdown("**Valor (R$)**")
                for preco in valores:
                    st.markdown(f"- R${preco}")
else:
    st.info("Nenhuma venda registrada ainda.")

