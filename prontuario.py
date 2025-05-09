import streamlit as st
from datetime import datetime
import backend as db

st.title("🩺 Registrar Atendimento")

# --- Seleção de Cliente ---
clientes = db.listar_clientes()
cliente_dict = {cliente[1]: cliente[0] for cliente in clientes}
cliente_nome = st.selectbox("Selecione o Cliente", [""] + list(cliente_dict.keys()))

if cliente_nome:
    cliente_id = cliente_dict[cliente_nome]

    # --- Seleção de Pet associado ---
    pets = db.listar_pets_por_cliente(cliente_id)
    if pets:
        pet_dict = {pet[2]: pet[0] for pet in pets}
        pet_nome = st.selectbox("Selecione o Pet", list(pet_dict.keys()))
        pet_id = pet_dict[pet_nome]

        # --- Formulário de Atendimento ---
        st.subheader("📋 Dados do Atendimento")
        data = st.date_input("Data do Atendimento", value=datetime.today())
        anamnese = st.text_area("Anamnese")
        tratamento = st.text_area("Tratamento")
        exames = st.text_area("Exames")

        if st.button("💾 Salvar Registro"):
            if not anamnese and not tratamento and not exames:
                st.warning("Preencha pelo menos um dos campos: Anamnese, Tratamento ou Exames.")
            else:
                prontuario_id = db.inserir_prontuario(
                    pet_id,
                    str(data),
                    anamnese,
                    tratamento,
                    exames
                )
                st.session_state["prontuario_id_atual"] = prontuario_id
                st.success("✅ Registro salvo com sucesso.")
    else:
        st.info("Nenhum pet cadastrado para este cliente.")
