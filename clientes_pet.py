import streamlit as st
from backend import (
    criar_tabelas, adicionar_cliente, listar_clientes,
    buscar_clientes_por_nome, editar_cliente, excluir_cliente,
    adicionar_pet, listar_pets_por_cliente, excluir_pet
)

# Cria tabelas
criar_tabelas()

st.set_page_config(page_title="Clientes e Pets", layout="centered")

st.title("👤 Cadastro de Clientes e Pets")
st.markdown("Registre tutores e associe seus pets para controle completo de atendimento.")

# --- CADASTRO DE CLIENTE ---
st.subheader("➕ Cadastrar Novo Cliente")
with st.form("form_cliente"):
    nome_tutor = st.text_input("Nome do Tutor")
    whatsapp = st.text_input("WhatsApp")
    endereco = st.text_input("Endereço")
    sexo = st.selectbox("Sexo", ["Homem", "Mulher", "Outro"])
    botao_cliente = st.form_submit_button("Salvar Cliente")
    if botao_cliente:
        if nome_tutor:
            adicionar_cliente(nome_tutor, whatsapp, endereco, sexo)
            st.success("✅ Cliente cadastrado com sucesso.")
            st.rerun()
        else:
            st.warning("⚠️ Informe pelo menos o nome.")


st.markdown("---")

# --- LISTA DE CLIENTES ---
st.subheader("📋 Lista de Clientes")
busca_nome = st.text_input("🔍 Buscar por nome")

clientes = buscar_clientes_por_nome(busca_nome) if busca_nome else listar_clientes()

for cliente in clientes:
    with st.expander(f"{cliente[1]} | {cliente[2]}"):
        st.markdown(f"**Endereço:** {cliente[3]}")
        st.markdown(f"**Sexo:** {cliente[4]}")

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Excluir", key=f"excluir_cliente_{cliente[0]}"):
                excluir_cliente(cliente[0])
                st.warning("🗑️ Cliente excluído.")
                st.rerun()
        with col2:
            if st.button("➕ Pet", key=f"adicionar_pet_{cliente[0]}"):
                st.session_state["cliente_pet_id"] = cliente[0]
                st.session_state["cliente_nome"] = cliente[1]
                st.session_state["mostrar_pet_form"] = True
                st.rerun()

        # --- LISTA DE PETS DO CLIENTE ---
        pets = listar_pets_por_cliente(cliente[0])
        if pets:
            st.markdown("🐶 **Pets cadastrados:**")
            for pet in pets:
                with st.container():
                    st.markdown(
                        f"""
                        <div style='background-color:#444; padding:15px; border-radius:10px; margin-bottom:10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.3); color: white;'>
                            <p><strong>Nome:</strong> {pet[2]}</p>
                            <p><strong>Idade:</strong> {pet[3]} anos</p>
                            <p><strong>Peso:</strong> {pet[4]} kg</p>
                            <p><strong>Raça:</strong> {pet[5]}</p>
                            <p><strong>Espécie:</strong> {pet[6]}</p>
                            <p><strong>Castrado:</strong> {pet[7]}</p>
                            <p><strong>Cor:</strong> {pet[8]}</p>
                            <p><strong>Sexo Pet:</strong> {pet[9]}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button("❌ Excluir Pet", key=f"excluir_pet_{pet[0]}"):
                        excluir_pet(pet[0])
                        st.warning("Pet excluído.")
                        st.rerun()
        else:
            st.info("Nenhum pet cadastrado para este cliente.")

        # --- FORMULÁRIO DE PET ---
        if st.session_state.get("mostrar_pet_form") and st.session_state.get("cliente_pet_id") == cliente[0]:
            st.subheader(f"🐾 Cadastrar Pet para {cliente[1]}")
            with st.form(f"form_pet_{cliente[0]}"):
                nome_pet = st.text_input("Nome do Pet")
                idade = st.number_input("Idade", min_value=0)
                peso = st.number_input("Peso", min_value=0.0)
                raca = st.text_input("Raça")
                especie = st.text_input("Espécie")
                castrado = st.selectbox("Castrado?", ["Sim", "Não"])
                cor = st.text_input("Cor")
                sexo_pet = st.selectbox("Sexo PET", ["MACHO", "FÊMEA"])
                botao_pet = st.form_submit_button("Salvar Pet")
                if botao_pet:
                    adicionar_pet(cliente[0], nome_pet, idade, peso, raca, especie, castrado, cor, sexo_pet)
                    st.success("✅ Pet cadastrado com sucesso.")
                    st.session_state["mostrar_pet_form"] = False
                    st.rerun()
